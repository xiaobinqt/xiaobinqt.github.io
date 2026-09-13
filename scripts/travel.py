#!/usr/bin/env python3
"""旅行地图与游记维护工具。

最常用的新增命令：
    ./scripts/travel.py add 北京 太庙

这条命令表示“记录一次发生在北京太庙的旅行”。北京是直辖市，因此只需
“城市 + 地点”两个参数；普通省市使用“省 + 市 + 地点”，例如：
    ./scripts/travel.py add 浙江省 杭州市 西湖

不增加其他参数时，脚本默认：
    - 日期为执行命令的当天；
    - 同行人为 together（我们俩）；
    - 地点名称同时作为本次 spots；
    - 创建并直接发布旅行文章，不保存为草稿。

新增时会使用高德 Web 服务地理编码补全省、市、区县和 [经度, 纬度]，在
终端显示查询结果并等待确认。确认后生成唯一地点 id，原子写入
content/travel/index.md，并在 content/posts/travel/ 创建旅行文章，最后把
文章路径自动关联回地图。原子写入表示执行失败时不会留下只写了一半的 YAML。

高德 Key 只读取环境变量 AMAP_WEB_KEY；传入 --coordinates 时不调用高德。
如果设置了 OPENAI_API_KEY，脚本还会生成带资料来源的地点介绍初稿。所有
API Key 都不会写入数据、文章或 Git 仓库。

同一地点在不同日期可以直接再次新增；同一天确实需要两条记录时使用
--repeat。删除默认只移除地图足迹；同时删除 travel_id 对应的文章时使用：
    ./scripts/travel.py del 地点ID --with-post

更多命令运行 ./scripts/travel.py --help，完整说明见 content/travel/README.md。
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

try:
    from pypinyin import lazy_pinyin
except ImportError:  # macOS 可使用系统转写，其他系统会给出明确安装提示。
    lazy_pinyin = None


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTENT_FILE = PROJECT_ROOT / "content" / "travel" / "index.md"
DEFAULT_POSTS_DIR = PROJECT_ROOT / "content" / "posts" / "travel"
WORLD_MAP_FILE = PROJECT_ROOT / "static" / "data" / "world-countries.geojson"
AMAP_GEOCODE_URL = "https://restapi.amap.com/v3/geocode/geo"
OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"
DEFAULT_OPENAI_MODEL = "gpt-5.4-mini"
MACOS_PINYIN_SCRIPT = """
function run(argv) {
  ObjC.import('Foundation');
  const value = $.NSMutableString.alloc.initWithString(argv[0]);
  $.CFStringTransform(value, null, $.kCFStringTransformToLatin, false);
  $.CFStringTransform(value, null, $.kCFStringTransformStripCombiningMarks, false);
  return ObjC.unwrap(value);
}
"""
WHO_LABELS = {"together": "我们俩", "me": "我", "partner": "TA"}
COUNTRY_CODES = {
    "中国": "CHN",
    "日本": "JPN",
    "韩国": "KOR",
    "朝鲜": "PRK",
    "泰国": "THA",
    "新加坡": "SGP",
    "马来西亚": "MYS",
    "印度尼西亚": "IDN",
    "菲律宾": "PHL",
    "越南": "VNM",
    "柬埔寨": "KHM",
    "印度": "IND",
    "美国": "USA",
    "加拿大": "CAN",
    "英国": "GBR",
    "法国": "FRA",
    "德国": "DEU",
    "意大利": "ITA",
    "西班牙": "ESP",
    "葡萄牙": "PRT",
    "荷兰": "NLD",
    "比利时": "BEL",
    "瑞士": "CHE",
    "奥地利": "AUT",
    "希腊": "GRC",
    "土耳其": "TUR",
    "俄罗斯": "RUS",
    "阿联酋": "ARE",
    "澳大利亚": "AUS",
    "新西兰": "NZL",
}
MUNICIPALITY_NAMES = {
    "北京": "北京市",
    "北京市": "北京市",
    "上海": "上海市",
    "上海市": "上海市",
    "天津": "天津市",
    "天津市": "天津市",
    "重庆": "重庆市",
    "重庆市": "重庆市",
    "香港": "香港特别行政区",
    "香港特别行政区": "香港特别行政区",
    "澳门": "澳门特别行政区",
    "澳门特别行政区": "澳门特别行政区",
}
ID_PATTERN = re.compile(r"^  - id:\s*(?:\"([^\"]+)\"|'([^']+)'|([^\s#]+))\s*$")
FIELD_PATTERN = re.compile(r"^    ([a-zA-Z_][a-zA-Z0-9_]*):\s*(.*)$")


class TravelError(RuntimeError):
    """可直接展示给使用者的错误。"""


@dataclass(frozen=True)
class FrontMatter:
    lines: list[str]
    closing_index: int


@dataclass(frozen=True)
class PlaceBlock:
    place_id: str
    start: int
    end: int
    fields: dict[str, str]


@dataclass(frozen=True)
class GeocodeResult:
    longitude: float
    latitude: float
    province: str
    city: str
    district: str
    adcode: str
    formatted_address: str
    level: str


@dataclass(frozen=True)
class TravelIntro:
    summary: str
    founded: str
    history: str
    anecdote: str
    highlights: tuple[str, ...]
    sources: tuple[tuple[str, str], ...]


def parse_front_matter(text: str) -> FrontMatter:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        raise TravelError("旅行页面缺少 YAML Front Matter 起始标记。")

    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return FrontMatter(lines=lines, closing_index=index)
    raise TravelError("旅行页面缺少 YAML Front Matter 结束标记。")


def unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        if value[0] == '"':
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                pass
        return value[1:-1]
    return value


def parse_place_blocks(front_matter: FrontMatter) -> list[PlaceBlock]:
    starts: list[tuple[int, str]] = []
    for index in range(1, front_matter.closing_index):
        match = ID_PATTERN.match(front_matter.lines[index].rstrip("\r\n"))
        if match:
            starts.append((index, next(group for group in match.groups() if group is not None)))

    blocks: list[PlaceBlock] = []
    for position, (start, place_id) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else front_matter.closing_index
        fields: dict[str, str] = {"id": place_id}
        for line in front_matter.lines[start + 1 : end]:
            match = FIELD_PATTERN.match(line.rstrip("\r\n"))
            if match:
                fields[match.group(1)] = unquote(match.group(2))
        blocks.append(PlaceBlock(place_id=place_id, start=start, end=end, fields=fields))
    return blocks


def scalar(value: object, fallback: str = "") -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list) and value:
        return str(value[0])
    return fallback


def geocode(province: str, city: str, place: str, api_key: str) -> GeocodeResult:
    query = urllib.parse.urlencode(
        {
            "key": api_key,
            "address": f"{province}{city}{place}",
            "city": city,
            "output": "JSON",
        }
    )
    request = urllib.request.Request(
        f"{AMAP_GEOCODE_URL}?{query}",
        headers={"User-Agent": "xiaobinqt-travel-map-maintainer/1.0"},
    )

    try:
        with urllib.request.urlopen(request, timeout=12) as response:
            payload = json.load(response)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise TravelError(f"无法连接高德地理编码服务：{exc}") from exc

    if payload.get("status") != "1":
        message = payload.get("info") or "未知错误"
        code = payload.get("infocode") or "unknown"
        raise TravelError(f"高德地理编码失败：{message}（{code}）")

    results = payload.get("geocodes") or []
    if not results:
        raise TravelError("没有找到这个地点。请补充更具体的区县或景点名称后重试。")

    item = results[0]
    location = str(item.get("location") or "").split(",")
    if len(location) != 2:
        raise TravelError("高德返回了无法识别的坐标。")
    try:
        longitude, latitude = (float(location[0]), float(location[1]))
    except ValueError as exc:
        raise TravelError("高德返回了无法识别的坐标。") from exc

    return GeocodeResult(
        longitude=longitude,
        latitude=latitude,
        province=scalar(item.get("province"), province),
        city=scalar(item.get("city"), city),
        district=scalar(item.get("district")),
        adcode=scalar(item.get("adcode")),
        formatted_address=scalar(item.get("formatted_address"), f"{province}{city}{place}"),
        level=scalar(item.get("level")),
    )


def manual_geocode(
    province: str,
    city: str,
    coordinates: str,
    district: str,
    scope: str,
) -> GeocodeResult:
    try:
        longitude_text, latitude_text = coordinates.split(",", maxsplit=1)
        longitude = float(longitude_text.strip())
        latitude = float(latitude_text.strip())
    except (TypeError, ValueError) as exc:
        raise TravelError("--coordinates 格式应为“经度,纬度”，例如 116.397,39.916。") from exc

    if not (-180 <= longitude <= 180 and -90 <= latitude <= 90):
        raise TravelError("坐标超出有效范围，请确认顺序是“经度,纬度”。")
    if scope == "china" and not (70 <= longitude <= 140 and 0 <= latitude <= 60):
        raise TravelError("坐标看起来不在中国附近，请确认顺序是“经度,纬度”。")
    return GeocodeResult(
        longitude=longitude,
        latitude=latitude,
        province=province,
        city=city,
        district=district,
        adcode="",
        formatted_address=f"{province}{city}{district}",
        level="手动坐标",
    )


def plain_text(value: object) -> str:
    """把模型返回值收敛成适合写入 Markdown 单行字段的纯文本。"""
    return re.sub(r"\s+", " ", str(value or "")).strip()


def valid_http_url(value: object) -> str:
    url = plain_text(value)
    parsed = urllib.parse.urlparse(url)
    return url if parsed.scheme in {"http", "https"} and bool(parsed.netloc) else ""


def extract_response_text(payload: dict[str, object]) -> str:
    for item in payload.get("output", []):
        if not isinstance(item, dict) or item.get("type") != "message":
            continue
        for content in item.get("content", []):
            if isinstance(content, dict) and content.get("type") == "output_text":
                text = content.get("text")
                if isinstance(text, str) and text.strip():
                    return text
    error = payload.get("error")
    if isinstance(error, dict) and error.get("message"):
        raise TravelError(f"AI 生成失败：{plain_text(error['message'])}")
    raise TravelError("AI 没有返回可用的地点介绍。")


def generate_travel_intro(
    *,
    api_key: str,
    model: str,
    display_name: str,
    country: str,
    province: str,
    city: str,
    district: str,
    spots: Sequence[str],
    reference: str,
) -> TravelIntro:
    location = " · ".join(
        dict.fromkeys(value for value in (country, province, city, district) if value)
    )
    schema = {
        "type": "object",
        "properties": {
            "summary": {"type": "string"},
            "founded": {"type": "string"},
            "history": {"type": "string"},
            "anecdote": {"type": "string"},
            "highlights": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 2,
                "maxItems": 4,
            },
            "sources": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "url": {"type": "string"},
                    },
                    "required": ["title", "url"],
                    "additionalProperties": False,
                },
                "minItems": 1,
                "maxItems": 3,
            },
        },
        "required": ["summary", "founded", "history", "anecdote", "highlights", "sources"],
        "additionalProperties": False,
    }
    supplied_reference = reference or "未提供"
    prompt = (
        f"为中文旅行游记编写一份简洁、可核验的地点小档案。\n"
        f"地点：{display_name}\n行政区：{location or '未提供'}\n"
        f"本次景点：{'、'.join(spots) or display_name}\n"
        f"用户提供的参考链接：{supplied_reference}\n\n"
        "请先用网页搜索核对事实，再输出结果。summary 用 80～150 个中文字符说明它是什么、"
        "为何值得来及其历史文化位置；founded 写始建年代、形成时期或首次可靠记载；"
        "history 用 1～2 句话概括关键沿革；anecdote 写一个有可靠来源的典故，没有可靠典故时"
        "明确写暂无可核验典故；highlights 给出 2～4 个现场可观察的细节。"
        "sources 只使用景区/博物馆官网、政府文旅或文保部门、国际组织等权威页面的真实完整 URL。"
        "不要把传说写成史实，不要使用 Markdown，不要虚构日期、人物或链接。"
    )
    body = {
        "model": model,
        "store": False,
        "reasoning": {"effort": "low"},
        "tools": [{"type": "web_search"}],
        "input": prompt,
        "text": {
            "format": {
                "type": "json_schema",
                "name": "travel_place_intro",
                "strict": True,
                "schema": schema,
            }
        },
        "max_output_tokens": 1800,
    }
    request = urllib.request.Request(
        OPENAI_RESPONSES_URL,
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "xiaobinqt-travel-map-maintainer/1.0",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            response_payload = json.load(response)
    except urllib.error.HTTPError as exc:
        try:
            error_payload = json.loads(exc.read().decode("utf-8"))
            message = plain_text((error_payload.get("error") or {}).get("message"))
        except (UnicodeDecodeError, json.JSONDecodeError, AttributeError):
            message = ""
        detail = f"：{message}" if message else ""
        raise TravelError(f"OpenAI API 请求失败（HTTP {exc.code}）{detail}") from exc
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise TravelError(f"无法连接 OpenAI API：{exc}") from exc

    try:
        result = json.loads(extract_response_text(response_payload))
    except json.JSONDecodeError as exc:
        raise TravelError("AI 返回的地点介绍不是有效 JSON。") from exc
    if not isinstance(result, dict):
        raise TravelError("AI 返回的地点介绍结构不正确。")

    highlights = tuple(
        text for text in (plain_text(item) for item in result.get("highlights", [])) if text
    )
    sources: list[tuple[str, str]] = []
    for item in result.get("sources", []):
        if not isinstance(item, dict):
            continue
        title = plain_text(item.get("title"))
        url = valid_http_url(item.get("url"))
        if title and url and url not in {source_url for _, source_url in sources}:
            sources.append((title, url))
    if not highlights or not sources:
        raise TravelError("AI 介绍缺少现场看点或有效的权威资料链接。")
    return TravelIntro(
        summary=plain_text(result.get("summary")),
        founded=plain_text(result.get("founded")),
        history=plain_text(result.get("history")),
        anecdote=plain_text(result.get("anecdote")),
        highlights=highlights,
        sources=tuple(sources),
    )


def compact_region_name(name: str) -> str:
    suffixes = (
        "特别行政区",
        "壮族自治区",
        "回族自治区",
        "维吾尔自治区",
        "蒙古族藏族自治州",
        "藏族自治州",
        "自治州",
        "自治区",
        "地区",
        "盟",
        "省",
        "市",
    )
    for suffix in suffixes:
        if name.endswith(suffix) and len(name) > len(suffix):
            return name[: -len(suffix)]
    return name


def create_id(
    result: GeocodeResult,
    country: str,
    country_code: str,
    province: str,
    city: str,
    place: str,
    date: str,
) -> str:
    digest = hashlib.sha256(
        f"{country}|{province}|{city}|{place}|{date}".encode("utf-8")
    ).hexdigest()[:8]
    prefix = result.adcode if result.adcode.isdigit() else country_code.lower()
    return f"{prefix}-{digest}"


def country_center(country_code: str) -> tuple[float, float]:
    if not WORLD_MAP_FILE.exists():
        raise TravelError("找不到世界地图数据，请使用 --coordinates 手动提供坐标。")
    payload = json.loads(WORLD_MAP_FILE.read_text(encoding="utf-8"))
    feature = next(
        (
            item
            for item in payload.get("features", [])
            if str(item.get("properties", {}).get("ADM0_A3", "")).upper() == country_code
        ),
        None,
    )
    if not feature:
        raise TravelError(f"世界地图里找不到国家代码 {country_code}，请检查代码或使用 --coordinates。")

    geometry = feature.get("geometry", {})
    coordinates = geometry.get("coordinates", [])
    polygons = [coordinates] if geometry.get("type") == "Polygon" else coordinates
    if not polygons:
        raise TravelError("无法计算国家中心，请使用 --coordinates 手动提供坐标。")
    largest_polygon = max(polygons, key=lambda polygon: len(polygon[0]) if polygon else 0)
    outer_ring = largest_polygon[0] if largest_polygon else []
    if not outer_ring:
        raise TravelError("无法计算国家中心，请使用 --coordinates 手动提供坐标。")
    longitudes = [float(point[0]) for point in outer_ring]
    latitudes = [float(point[1]) for point in outer_ring]
    return ((min(longitudes) + max(longitudes)) / 2, (min(latitudes) + max(latitudes)) / 2)


def yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def yaml_string_list(values: Sequence[str]) -> str:
    return "[" + ", ".join(yaml_string(value) for value in values) + "]"


def validate_travel_date(value: str) -> str:
    for date_format in ("%Y-%m", "%Y-%m-%d"):
        try:
            dt.datetime.strptime(value, date_format)
            return value
        except ValueError:
            continue
    raise TravelError("--date 只支持 YYYY-MM 或 YYYY-MM-DD，例如 2025-04。")


def post_date(value: str) -> str:
    return f"{value}-01" if re.fullmatch(r"\d{4}-\d{2}", value) else value


def normalize_slug(value: str) -> str:
    slug = value.strip().lower().replace("_", "-")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        raise TravelError("--slug 只能包含小写英文字母、数字和短横线。")
    return slug


def pinyin_filename_part(value: str) -> str:
    source = value.strip()
    if not source.isascii():
        if lazy_pinyin is not None:
            source = "".join(lazy_pinyin(source))
        elif sys.platform == "darwin":
            try:
                completed = subprocess.run(
                    ["osascript", "-l", "JavaScript", "-e", MACOS_PINYIN_SCRIPT, source],
                    check=True,
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                source = re.sub(r"\s+", "", completed.stdout.strip())
            except (OSError, subprocess.SubprocessError) as exc:
                raise TravelError(
                    "无法自动生成拼音文件名，请增加 --slug，例如 --slug beijing-taimiao。"
                ) from exc
        else:
            raise TravelError(
                "自动生成拼音文件名需要 pypinyin。请执行 `python3 -m pip install pypinyin==0.55.0`，"
                "或增加 --slug，例如 --slug beijing-taimiao。"
            )
    return re.sub(r"[^a-z0-9]+", "-", source.lower()).strip("-")


def default_post_slug(
    *,
    date: str,
    country: str,
    city: str,
    place: str,
    country_level: bool,
) -> str:
    labels = [country] if country_level else [compact_region_name(city), place]
    readable_labels = list(dict.fromkeys(pinyin_filename_part(label) for label in labels if label))
    readable_labels = [label for label in readable_labels if label]
    return "-".join([date, *(readable_labels or ["travel"])])


def render_post(
    *,
    place_id: str,
    display_name: str,
    country: str,
    province: str,
    city: str,
    district: str,
    date: str,
    spots: Sequence[str],
    note: str,
    reference: str,
    intro: TravelIntro | None,
    draft: bool,
) -> str:
    regions = [value for value in (country, province, city, district) if value]
    tags = list(dict.fromkeys([*regions, *spots]))
    spot_list = "\n".join(f"- {spot}" for spot in spots) or "- 待补充"
    if intro:
        sources = list(intro.sources)
        if reference and reference not in {url for _, url in sources}:
            sources.append(("补充资料", reference))
        source_links = "；".join(
            f"[{title.replace('[', '〔').replace(']', '〕')}]({url})" for title, url in sources
        )
        intro_lines = [
            f"> {intro.summary}\n\n",
            f"- **始建 / 形成**：{intro.founded}\n",
            f"- **历史沿革**：{intro.history}\n",
            f"- **经典典故**：{intro.anecdote}\n",
            f"- **别错过**：{'；'.join(intro.highlights)}\n",
            f"- **资料来源**：{source_links}\n\n",
            "<!-- AI 已生成初稿，请在发布前打开来源链接并人工复核年代、人物和专有名称。 -->\n\n",
        ]
    else:
        reference_line = (
            f"- **资料来源**：[查看官方或权威资料]({reference})\n"
            if reference
            else "- **资料来源**：待补充\n"
        )
        intro_lines = [
            "> 用 80～150 字介绍这里：它是什么、为什么值得来，以及它在当地历史或文化中的位置。\n\n",
            "- **始建 / 形成**：待补充\n",
            "- **历史沿革**：待补充\n",
            "- **经典典故**：待补充\n",
            "- **别错过**：待补充\n",
            reference_line,
            "\n",
            "<!--\n",
            "填写规则：\n",
            "1. 简介保持客观，旅行感受留到文末。\n",
            "2. 年代写清朝代/年份；存在争议时写“相传”或列出不同说法。\n",
            "3. 典故只写与地点直接相关且可以查证的内容，不复制大段原文。\n",
            "4. “别错过”写 2～4 个现场可观察的建筑、展品、景观或仪式细节。\n",
            "5. 至少保留一个来源链接，优先级：景区/博物馆官网 > 政府文旅或文保资料 > 权威百科。\n",
            "-->\n\n",
        ]
    generated_note = (
        "<!-- 这篇游记由 scripts/travel.py 自动创建。完成后运行 publish 命令发布。 -->"
        if draft
        else "<!-- 这篇游记由 scripts/travel.py 自动创建。 -->"
    )
    return "".join(
        [
            "---\n",
            f"title: {yaml_string(f'{display_name}｜{date}')}\n",
            f"date: {post_date(date)}\n",
            f"draft: {'true' if draft else 'false'}\n",
            f"description: {yaml_string(note)}\n",
            f"categories: {yaml_string_list(['旅行'])}\n",
            f"tags: {yaml_string_list(tags)}\n",
            f"travel_id: {yaml_string(place_id)}\n",
            "lightgallery: true\n",
            "toc: true\n",
            "---\n\n",
            f"{generated_note}\n\n",
            "## 此行所感\n\n",
            f"{note}\n\n",
            "## 行程与照片\n\n",
            f"{spot_list}\n\n",
            "<!-- TODO：在这里补充行程和沿途故事；多张照片使用 travel-gallery 短代码，写法见 content/travel/README.md。 -->\n\n",
            "## 认识这里\n\n",
            *intro_lines,
        ]
    )


def render_place_block(
    *,
    place_id: str,
    display_name: str,
    country: str,
    country_code: str,
    result: GeocodeResult,
    date: str,
    who: str,
    spots: Sequence[str],
    note: str,
    article: str,
) -> list[str]:
    return [
        f"  - id: {place_id}\n",
        f"    name: {yaml_string(display_name)}\n",
        f"    country: {yaml_string(country)}\n",
        f"    countryCode: {yaml_string(country_code)}\n",
        f"    province: {yaml_string(result.province)}\n",
        f"    city: {yaml_string(result.city)}\n",
        f"    district: {yaml_string(result.district)}\n",
        f"    coordinates: [{result.longitude:.6f}, {result.latitude:.6f}]\n",
        f"    date: {yaml_string(date)}\n",
        f"    who: {who}\n",
        f"    spots: {yaml_string_list(spots)}\n",
        f"    note: {yaml_string(note)}\n",
        f"    article: {yaml_string(article)}\n",
    ]


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        newline="",
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        delete=False,
    ) as handle:
        temporary_path = Path(handle.name)
        handle.write(text)
    try:
        os.replace(temporary_path, path)
    except Exception:
        temporary_path.unlink(missing_ok=True)
        raise


def confirm(prompt: str, assume_yes: bool) -> bool:
    if assume_yes:
        return True
    if not sys.stdin.isatty():
        raise TravelError("当前终端无法确认写入；确认信息无误后增加 --yes。")
    answer = input(f"{prompt} [Y/n] ").strip().lower()
    return answer in {"", "y", "yes"}


def get_content_path(args: argparse.Namespace) -> Path:
    return Path(args.file).expanduser().resolve()


def get_posts_dir(args: argparse.Namespace) -> Path:
    return Path(args.posts_dir).expanduser().resolve()


def command_add(args: argparse.Namespace) -> int:
    content_path = get_content_path(args)
    if not content_path.exists():
        raise TravelError(f"找不到旅行页面：{content_path}")

    country = args.country
    country_code = (args.country_code or COUNTRY_CODES.get(country, "")).upper()
    province = args.province
    city = args.city or ""
    place = args.place or country
    if args.scope == "china":
        if args.place is None:
            municipality = MUNICIPALITY_NAMES.get(province)
            if not municipality:
                raise TravelError(
                    "两参数简写只适用于直辖市和特别行政区，例如 `add 北京 太庙`。\n"
                    "普通省市请使用三个参数，例如 `add 浙江省 杭州市 西湖`。"
                )
            place = city
            province = municipality
            city = municipality
        else:
            province = MUNICIPALITY_NAMES.get(province, province)
            city = MUNICIPALITY_NAMES.get(city, city)
    country_level = args.scope == "world" and not city and not args.place
    if not country_code:
        raise TravelError("无法识别国家代码，请增加 --country-code，例如日本使用 JPN。")

    if args.coordinates:
        result = manual_geocode(
            province,
            city,
            args.coordinates,
            args.district or "",
            args.scope,
        )
    elif args.scope == "world":
        if not country_level:
            raise TravelError(
                "海外城市或景点需要精确坐标。请增加 --coordinates '经度,纬度'；"
                f"如果只记录去过{country}，使用 `./scripts/travel.py add-world {country}`。"
            )
        longitude, latitude = country_center(country_code)
        result = GeocodeResult(
            longitude=longitude,
            latitude=latitude,
            province=args.province,
            city=city,
            district=args.district or "",
            adcode="",
            formatted_address=country,
            level="国家概览坐标",
        )
    else:
        api_key = os.environ.get("AMAP_WEB_KEY") or os.environ.get("AMAP_KEY")
        if not api_key:
            raise TravelError(
                "缺少高德 Web 服务 Key。请先执行：\n"
                "  export AMAP_WEB_KEY='你的Key'\n"
                "如果不想使用接口，也可以增加 --coordinates '经度,纬度'。"
            )
        result = geocode(province, city, place, api_key)

    if args.district:
        result = GeocodeResult(
            longitude=result.longitude,
            latitude=result.latitude,
            province=result.province,
            city=result.city,
            district=args.district,
            adcode=result.adcode,
            formatted_address=result.formatted_address,
            level=result.level,
        )

    city_label = compact_region_name(result.city or city)
    default_name = country if country_level else (f"{city_label} · {place}" if city_label else f"{country} · {place}")
    display_name = args.name or default_name
    date = validate_travel_date(args.date or dt.date.today().isoformat())
    base_place_id = args.id or create_id(
        result, country, country_code, province, city, place, date
    )
    spots = args.spot or ([] if country_level else [place])
    note = args.note or "这段旅程的故事，等待慢慢补上。"
    if args.draft and args.publish:
        raise TravelError("--draft 和 --publish 不能同时使用；现在默认就是直接发布。")
    if args.draft and (args.no_post or args.article):
        raise TravelError("--draft 只用于脚本自动创建的旅行文章。")
    if args.publish and (args.no_post or args.article):
        raise TravelError("--publish 需要由脚本创建文章，不能与 --no-post 或 --article 一起使用。")
    if args.slug and (args.no_post or args.article):
        raise TravelError("--slug 只用于脚本自动创建的旅行文章。")
    if args.reference and (args.no_post or args.article):
        raise TravelError("--reference 只用于脚本自动创建的旅行文章。")
    if args.reference and not re.match(r"^https?://", args.reference):
        raise TravelError("--reference 必须是以 http:// 或 https:// 开头的完整链接。")
    if args.ai and (args.no_post or args.article):
        raise TravelError("--ai 只用于脚本自动创建的旅行文章。")

    original_text = content_path.read_text(encoding="utf-8")
    front_matter = parse_front_matter(original_text)
    blocks = parse_place_blocks(front_matter)
    same_day_blocks = [
        block
        for block in blocks
        if block.fields.get("name") == display_name and block.fields.get("date") == date
    ]
    repeat_number = 1
    if same_day_blocks:
        if not args.repeat:
            raise TravelError(
                f"{date} 已经存在“{display_name}”的到访记录。\n"
                "如果是同一天的另一段独立行程，请增加 --repeat；否则请修改已有记录。"
            )
        repeat_number = len(same_day_blocks) + 1
    elif args.repeat:
        raise TravelError("--repeat 只在同一地点、同一日期已经存在记录时使用。")

    place_id = base_place_id
    if repeat_number > 1 and not args.id:
        place_id = f"{base_place_id}-{repeat_number}"
    if any(block.place_id == place_id for block in blocks):
        raise TravelError(f"地点 ID 已存在：{place_id}")

    publish_now = not args.draft
    article = normalize_article_path(args.article or "")
    post_path: Path | None = None
    post_text = ""
    ai_intro: TravelIntro | None = None
    if not args.article and not args.no_post:
        if args.slug:
            slug = normalize_slug(args.slug)
        else:
            slug = default_post_slug(
                date=date,
                country=country,
                city=result.city or city,
                place=place,
                country_level=country_level,
            )
            if repeat_number > 1:
                slug = f"{slug}-{repeat_number}"
        post_path = get_posts_dir(args) / f"{slug}.md"
        if post_path.exists():
            raise TravelError(f"旅行文章已存在：{post_path}")
        openai_key = os.environ.get("OPENAI_API_KEY", "").strip()
        use_ai = not args.no_ai and bool(openai_key)
        if args.ai and not openai_key:
            raise TravelError(
                "--ai 需要 OPENAI_API_KEY。请先执行：\n"
                "  export OPENAI_API_KEY='你的 OpenAI API Key'"
            )
        if use_ai:
            model = os.environ.get("OPENAI_MODEL", DEFAULT_OPENAI_MODEL).strip() or DEFAULT_OPENAI_MODEL
            print(f"正在用 AI 查询并整理“{display_name}”的地点介绍（{model}）……")
            try:
                ai_intro = generate_travel_intro(
                    api_key=openai_key,
                    model=model,
                    display_name=display_name,
                    country=country,
                    province=result.province,
                    city=result.city or city,
                    district=result.district,
                    spots=spots,
                    reference=args.reference or "",
                )
            except TravelError as exc:
                if args.ai:
                    raise
                print(f"提示：{exc} 已改用待补充模板。", file=sys.stderr)
        if publish_now:
            article = f"/{slug}/"
        post_text = render_post(
            place_id=place_id,
            display_name=display_name,
            country=country,
            province=result.province,
            city=result.city,
            district=result.district,
            date=date,
            spots=spots,
            note=note,
            reference=args.reference or "",
            intro=ai_intro,
            draft=not publish_now,
        )

    print("\n识别到的地点")
    print(f"  名称：{display_name}")
    print(f"  国家：{country}（{country_code}）")
    print(f"  地址：{result.formatted_address}")
    print(f"  区县：{result.district or '未识别'}")
    print(f"  坐标：{result.longitude:.6f}, {result.latitude:.6f}")
    print(f"  同行：{WHO_LABELS[args.who]}")
    print(f"  日期：{date}")
    if repeat_number > 1:
        print(f"  到访：同日第 {repeat_number} 条独立记录")
    if post_path:
        status = "直接发布" if publish_now else "草稿"
        print(f"  文章：{post_path.relative_to(PROJECT_ROOT) if post_path.is_relative_to(PROJECT_ROOT) else post_path}（{status}）")
        print(f"  介绍：{'AI 初稿，发布前请复核' if ai_intro else '待手动补充'}")
    elif article:
        print(f"  文章：关联已有路径 {article}")
    else:
        print("  文章：不创建")
    if result.level:
        print(f"  匹配：{result.level}")

    new_block = render_place_block(
        place_id=place_id,
        display_name=display_name,
        country=country,
        country_code=country_code,
        result=result,
        date=date,
        who=args.who,
        spots=spots,
        note=note,
        article=article,
    )
    if args.dry_run:
        print("\n将要写入的内容（dry-run，文件未修改）\n")
        print("".join(new_block), end="")
        if post_path:
            print(f"\n将要创建的文章：{post_path}\n")
            print(post_text, end="")
        return 0
    if not confirm("确认把这个地点加入旅行地图吗？", args.yes):
        print("已取消，文件没有修改。")
        return 0

    if post_path:
        atomic_write(post_path, post_text)
    insertion = front_matter.closing_index
    updated_lines = front_matter.lines[:insertion] + new_block + front_matter.lines[insertion:]
    atomic_write(content_path, "".join(updated_lines))
    print(f"\n已添加：{display_name}（ID: {place_id}）")
    if post_path:
        if publish_now:
            print(f"文章已发布并关联：{article}")
        else:
            print(f"游记草稿已创建：{post_path}")
            print(f"写完后运行：./scripts/travel.py publish {place_id}")
    print("运行 `hugo server --configDir config.io` 即可预览。")
    return 0


def command_list(args: argparse.Namespace) -> int:
    content_path = get_content_path(args)
    if not content_path.exists():
        raise TravelError(f"找不到旅行页面：{content_path}")
    front_matter = parse_front_matter(content_path.read_text(encoding="utf-8"))
    blocks = parse_place_blocks(front_matter)
    if not blocks:
        print("旅行地图里还没有地点。")
        return 0

    columns = [("ID", 22), ("名称", 22), ("日期", 10), ("同行", 8), ("文章", 18)]
    print("  ".join(label.ljust(width) for label, width in columns))
    print("  ".join("-" * width for _, width in columns))
    for block in blocks:
        values = [
            block.place_id,
            block.fields.get("name", ""),
            block.fields.get("date", ""),
            WHO_LABELS.get(block.fields.get("who", ""), block.fields.get("who", "")),
            block.fields.get("article", "") or "待补",
        ]
        print("  ".join(value[:width].ljust(width) for value, (_, width) in zip(values, columns)))
    return 0


def find_block_or_fail(front_matter: FrontMatter, place_id: str) -> PlaceBlock:
    for block in parse_place_blocks(front_matter):
        if block.place_id == place_id:
            return block
    raise TravelError(f"找不到地点 ID：{place_id}。可先运行 list 查看。")


def command_remove(args: argparse.Namespace) -> int:
    content_path = get_content_path(args)
    original_text = content_path.read_text(encoding="utf-8")
    front_matter = parse_front_matter(original_text)
    block = find_block_or_fail(front_matter, args.id)
    place_name = block.fields.get("name", args.id)
    post_path = None
    if args.with_post:
        post_path, _ = find_travel_post(get_posts_dir(args), args.id)

    target_description = f"“{place_name}”的地图足迹"
    if post_path:
        target_description += f"及旅行文章 {post_path}"
    if not confirm(f"确认删除{target_description}吗？", args.yes):
        print("已取消，文件没有修改。")
        return 0

    updated_lines = front_matter.lines[: block.start] + front_matter.lines[block.end :]
    atomic_write(content_path, "".join(updated_lines))
    print(f"已删除地图足迹：{place_name}")
    if post_path:
        post_path.unlink()
        print(f"已删除旅行文章：{post_path}")
    else:
        print("旅行文章已保留；如需一并删除，请增加 --with-post。")
    return 0


def normalize_article_path(article: str) -> str:
    article = article.strip()
    if not article:
        return ""
    if re.match(r"^https?://", article):
        return article
    return f"/{article.strip('/')}/"


def update_place_article(
    front_matter: FrontMatter,
    block: PlaceBlock,
    article: str,
) -> list[str]:
    updated_lines = list(front_matter.lines)
    article_index = None
    for index in range(block.start + 1, block.end):
        if updated_lines[index].startswith("    article:"):
            article_index = index
            break
    if article_index is None:
        updated_lines.insert(block.end, f"    article: {yaml_string(article)}\n")
    else:
        updated_lines[article_index] = f"    article: {yaml_string(article)}\n"
    return updated_lines


def command_article(args: argparse.Namespace) -> int:
    content_path = get_content_path(args)
    original_text = content_path.read_text(encoding="utf-8")
    front_matter = parse_front_matter(original_text)
    block = find_block_or_fail(front_matter, args.id)
    article = normalize_article_path(args.path)

    updated_lines = update_place_article(front_matter, block, article)
    atomic_write(content_path, "".join(updated_lines))
    if article:
        print(f"已关联文章：{block.fields.get('name', args.id)} → {article}")
    else:
        print(f"已清空文章链接：{block.fields.get('name', args.id)}")
    return 0


def find_travel_post(posts_dir: Path, place_id: str) -> tuple[Path, FrontMatter]:
    matches: list[tuple[Path, FrontMatter]] = []
    if posts_dir.exists():
        for path in posts_dir.rglob("*.md"):
            if path.name == "_index.md":
                continue
            try:
                post_front_matter = parse_front_matter(path.read_text(encoding="utf-8"))
            except TravelError:
                continue
            for line in post_front_matter.lines[1 : post_front_matter.closing_index]:
                match = re.match(r"^travel_id:\s*(.*)$", line.rstrip("\r\n"))
                if match and unquote(match.group(1)) == place_id:
                    matches.append((path, post_front_matter))
                    break
    if not matches:
        raise TravelError(f"找不到 travel_id 为 {place_id} 的旅行文章。")
    if len(matches) > 1:
        paths = "\n  ".join(str(path) for path, _ in matches)
        raise TravelError(f"发现多篇文章使用同一个 travel_id：\n  {paths}")
    return matches[0]


def set_post_draft_false(front_matter: FrontMatter) -> list[str]:
    updated_lines = list(front_matter.lines)
    draft_index = None
    for index in range(1, front_matter.closing_index):
        if re.match(r"^draft:\s*", updated_lines[index]):
            draft_index = index
            break
    if draft_index is None:
        updated_lines.insert(front_matter.closing_index, "draft: false\n")
    else:
        updated_lines[draft_index] = "draft: false\n"
    return updated_lines


def command_publish(args: argparse.Namespace) -> int:
    content_path = get_content_path(args)
    original_text = content_path.read_text(encoding="utf-8")
    front_matter = parse_front_matter(original_text)
    block = find_block_or_fail(front_matter, args.id)
    post_path, post_front_matter = find_travel_post(get_posts_dir(args), args.id)
    article = f"/{post_path.stem}/"

    if not confirm(
        f"确认发布“{block.fields.get('name', args.id)}”并关联 {article} 吗？",
        args.yes,
    ):
        print("已取消，文件没有修改。")
        return 0

    atomic_write(post_path, "".join(set_post_draft_false(post_front_matter)))
    updated_map_lines = update_place_article(front_matter, block, article)
    atomic_write(content_path, "".join(updated_map_lines))
    print(f"已发布文章：{post_path}")
    print(f"已关联地图：{block.fields.get('name', args.id)} → {article}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="用简单命令维护 content/travel/index.md 中的旅行地点。",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "示例：\n"
            "  ./scripts/travel.py add 北京 太庙\n"
            "  ./scripts/travel.py add 浙江省 杭州市 西湖 --date 2026-03\n"
            "  ./scripts/travel.py add-world 日本\n"
            "  ./scripts/travel.py add-world 日本 东京 浅草寺 --coordinates 139.7967,35.7148\n"
            "  ./scripts/travel.py list\n"
            "  ./scripts/travel.py publish 110101-ab12cd34\n"
            "  ./scripts/travel.py article 110101-ab12cd34 /beijing-trip/\n"
            "  ./scripts/travel.py del 110101-ab12cd34\n"
            "  ./scripts/travel.py del 110101-ab12cd34 --with-post"
        ),
    )
    parser.add_argument(
        "--file",
        default=str(DEFAULT_CONTENT_FILE),
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--posts-dir",
        default=str(DEFAULT_POSTS_DIR),
        help=argparse.SUPPRESS,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="查询坐标并新增地点")
    add_parser.add_argument("province", help="省、自治区、直辖市或特别行政区")
    add_parser.add_argument("city", help="城市")
    add_parser.add_argument("place", nargs="?", help="景点或具体地点；直辖市可省略重复的城市参数")
    add_parser.add_argument("--who", choices=WHO_LABELS, default="together", help="同行人，默认 together")
    add_parser.add_argument("--date", help="旅行日期，支持 YYYY-MM 或 YYYY-MM-DD，默认今天")
    add_parser.add_argument("--district", help="手动指定区县")
    add_parser.add_argument("--spot", action="append", help="景点，可重复使用；默认使用地点名称")
    add_parser.add_argument("--note", help="旅行摘要")
    add_parser.add_argument("--reference", help="景区官网或其他权威介绍的完整链接")
    add_ai_group = add_parser.add_mutually_exclusive_group()
    add_ai_group.add_argument("--ai", action="store_true", help="强制使用 AI 生成地点介绍；缺少 Key 时报错")
    add_ai_group.add_argument("--no-ai", action="store_true", help="即使配置了 OpenAI Key 也不使用 AI")
    add_parser.add_argument("--article", help="对应文章的站内路径")
    add_parser.add_argument("--slug", help="自动创建文章的英文文件名，不含 .md")
    add_parser.add_argument("--no-post", action="store_true", help="只新增地图足迹，不创建游记")
    add_parser.add_argument("--draft", action="store_true", help="把自动创建的游记保存为草稿，不关联地图")
    add_parser.add_argument("--publish", action="store_true", help="兼容旧命令；现在默认直接发布")
    add_parser.add_argument("--repeat", action="store_true", help="同一地点同一天再次新增为独立记录")
    add_parser.add_argument("--name", help="自定义显示名称")
    add_parser.add_argument("--id", help="自定义唯一 ID")
    add_parser.add_argument("--coordinates", help="跳过接口，直接使用“经度,纬度”")
    add_parser.add_argument("--dry-run", action="store_true", help="只展示结果，不修改文件")
    add_parser.add_argument("--yes", action="store_true", help="跳过写入确认")
    add_parser.set_defaults(
        handler=command_add,
        country="中国",
        country_code="CHN",
        scope="china",
    )

    world_parser = subparsers.add_parser("add-world", help="新增海外国家、城市或地点")
    world_parser.add_argument("country", help="国家中文名称，例如日本")
    world_parser.add_argument("city", nargs="?", default="", help="可选城市；填写后需要提供精确坐标")
    world_parser.add_argument("place", nargs="?", default="", help="可选景点；填写后需要提供精确坐标")
    world_parser.add_argument("--country-code", help="ISO 3166-1 三位国家代码；常见国家可自动识别")
    world_parser.add_argument("--who", choices=WHO_LABELS, default="together", help="同行人，默认 together")
    world_parser.add_argument("--date", help="旅行日期，支持 YYYY-MM 或 YYYY-MM-DD，默认今天")
    world_parser.add_argument("--district", help="区县或地区")
    world_parser.add_argument("--spot", action="append", help="景点，可重复使用；默认使用地点名称")
    world_parser.add_argument("--note", help="旅行摘要")
    world_parser.add_argument("--reference", help="景区官网或其他权威介绍的完整链接")
    world_ai_group = world_parser.add_mutually_exclusive_group()
    world_ai_group.add_argument("--ai", action="store_true", help="强制使用 AI 生成地点介绍；缺少 Key 时报错")
    world_ai_group.add_argument("--no-ai", action="store_true", help="即使配置了 OpenAI Key 也不使用 AI")
    world_parser.add_argument("--article", help="对应文章的站内路径")
    world_parser.add_argument("--slug", help="自动创建文章的英文文件名，不含 .md")
    world_parser.add_argument("--no-post", action="store_true", help="只新增地图足迹，不创建游记")
    world_parser.add_argument("--draft", action="store_true", help="把自动创建的游记保存为草稿，不关联地图")
    world_parser.add_argument("--publish", action="store_true", help="兼容旧命令；现在默认直接发布")
    world_parser.add_argument("--repeat", action="store_true", help="同一地点同一天再次新增为独立记录")
    world_parser.add_argument("--name", help="自定义显示名称")
    world_parser.add_argument("--id", help="自定义唯一 ID")
    world_parser.add_argument("--coordinates", help="精确坐标，格式为“经度,纬度”")
    world_parser.add_argument("--dry-run", action="store_true", help="只展示结果，不修改文件")
    world_parser.add_argument("--yes", action="store_true", help="跳过写入确认")
    world_parser.set_defaults(handler=command_add, province="", scope="world")

    list_parser = subparsers.add_parser("list", help="查看已有地点及 ID")
    list_parser.set_defaults(handler=command_list)

    article_parser = subparsers.add_parser("article", help="关联或清空地点的文章链接")
    article_parser.add_argument("id", help="地点 ID")
    article_parser.add_argument("path", help="文章路径；传入空字符串可清空")
    article_parser.set_defaults(handler=command_article)

    publish_parser = subparsers.add_parser("publish", help="发布脚本生成的游记并关联地图")
    publish_parser.add_argument("id", help="地点 ID")
    publish_parser.add_argument("--yes", action="store_true", help="跳过发布确认")
    publish_parser.set_defaults(handler=command_publish)

    remove_parser = subparsers.add_parser(
        "remove",
        aliases=["del"],
        help="按 ID 删除地点（del 为快捷写法）",
    )
    remove_parser.add_argument("id", help="地点 ID")
    remove_parser.add_argument(
        "--with-post",
        action="store_true",
        help="同时删除 travel_id 匹配的旅行文章",
    )
    remove_parser.add_argument("--yes", action="store_true", help="跳过删除确认")
    remove_parser.set_defaults(handler=command_remove)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.handler(args))
    except TravelError as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 2
    except FileNotFoundError as exc:
        print(f"错误：找不到文件：{exc.filename}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("\n已取消。", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
