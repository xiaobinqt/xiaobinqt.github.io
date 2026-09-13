(function () {
  "use strict";

  const SVG_NS = "http://www.w3.org/2000/svg";
  const VIEWBOX = { width: 1000, height: 720, padding: 38 };
  const WHO_LABELS = {
    together: "我们俩",
    me: "我",
    partner: "TA",
  };

  function normalizeProvince(name) {
    return String(name || "")
      .replace(/特别行政区$/, "")
      .replace(/壮族自治区$|回族自治区$|维吾尔自治区$|自治区$/, "")
      .replace(/省$|市$/, "");
  }

  function placeCountryCode(place) {
    if (place.countryCode) return String(place.countryCode).toUpperCase();
    return !place.country || place.country === "中国" || place.country === "中华人民共和国" ? "CHN" : "";
  }

  function createElement(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  function createSvgElement(tag, attributes) {
    const node = document.createElementNS(SVG_NS, tag);
    Object.keys(attributes || {}).forEach((key) => node.setAttribute(key, attributes[key]));
    return node;
  }

  function collectCoordinates(geometry, callback) {
    if (!geometry || !geometry.coordinates) return;
    const walk = (value) => {
      if (typeof value[0] === "number" && typeof value[1] === "number") {
        callback(value);
        return;
      }
      value.forEach(walk);
    };
    walk(geometry.coordinates);
  }

  function chinaRawProjection([longitude, latitude]) {
    return [(longitude - 105) * Math.cos((35 * Math.PI) / 180), latitude];
  }

  function worldRawProjection([longitude, latitude]) {
    return [longitude, latitude];
  }

  function getBounds(features, rawProject) {
    const bounds = { minX: Infinity, maxX: -Infinity, minY: Infinity, maxY: -Infinity };
    features.forEach((feature) => {
      collectCoordinates(feature.geometry, (coordinate) => {
        const [x, y] = rawProject(coordinate);
        bounds.minX = Math.min(bounds.minX, x);
        bounds.maxX = Math.max(bounds.maxX, x);
        bounds.minY = Math.min(bounds.minY, y);
        bounds.maxY = Math.max(bounds.maxY, y);
      });
    });
    return bounds;
  }

  function createProjection(bounds, rawProject) {
    const innerWidth = VIEWBOX.width - VIEWBOX.padding * 2;
    const innerHeight = VIEWBOX.height - VIEWBOX.padding * 2;
    const scale = Math.min(
      innerWidth / (bounds.maxX - bounds.minX),
      innerHeight / (bounds.maxY - bounds.minY)
    );
    const contentWidth = (bounds.maxX - bounds.minX) * scale;
    const contentHeight = (bounds.maxY - bounds.minY) * scale;
    const offsetX = (VIEWBOX.width - contentWidth) / 2;
    const offsetY = (VIEWBOX.height - contentHeight) / 2;

    return (coordinate) => {
      const [rawX, rawY] = rawProject(coordinate);
      return [
        offsetX + (rawX - bounds.minX) * scale,
        offsetY + (bounds.maxY - rawY) * scale,
      ];
    };
  }

  function ringToPath(ring, project) {
    return (
      ring
        .map((point, index) => {
          const [x, y] = project(point);
          return `${index === 0 ? "M" : "L"}${x.toFixed(1)},${y.toFixed(1)}`;
        })
        .join("") + "Z"
    );
  }

  function geometryToPath(geometry, project) {
    if (geometry.type === "Polygon") {
      return geometry.coordinates.map((ring) => ringToPath(ring, project)).join("");
    }
    if (geometry.type === "MultiPolygon") {
      return geometry.coordinates
        .map((polygon) => polygon.map((ring) => ringToPath(ring, project)).join(""))
        .join("");
    }
    return "";
  }

  function initTravelMap(root) {
    if (root.dataset.initialized === "true") return;
    root.dataset.initialized = "true";

    const dataNode = root.querySelector(".travel-map__data");
    const config = JSON.parse(dataNode.textContent || "{}");
    const places = Array.isArray(config.places) ? config.places : [];
    const svg = root.querySelector("[data-map-svg]");
    const loading = root.querySelector("[data-map-loading]");
    const error = root.querySelector("[data-map-error]");
    const tooltip = root.querySelector("[data-map-tooltip]");
    const detail = root.querySelector("[data-place-detail]");
    const list = root.querySelector("[data-place-list]");
    const emptyState = root.querySelector("[data-empty-state]");
    const resultCount = root.querySelector("[data-result-count]");
    const listHeading = root.querySelector("[data-list-heading]");
    const clearRegion = root.querySelector("[data-clear-province]");
    const mapHint = root.querySelector("[data-map-hint]");
    const filterButtons = Array.from(root.querySelectorAll("[data-travel-filter]"));
    const modeButtons = Array.from(root.querySelectorAll("[data-map-mode]"));
    const viewButtons = Array.from(root.querySelectorAll("[data-travel-view]"));
    const viewPanels = Array.from(root.querySelectorAll("[data-travel-panel]"));
    const yearbookContent = root.querySelector("[data-yearbook-content]");
    const yearbookEmpty = root.querySelector("[data-yearbook-empty]");
    const yearTabs = root.querySelector("[data-year-tabs]");
    const yearTitle = root.querySelector("[data-year-title]");
    const yearLabel = root.querySelector("[data-year-label]");
    const yearNarrative = root.querySelector("[data-year-narrative]");
    const yearRoute = root.querySelector("[data-year-route]");
    const yearTimeline = root.querySelector("[data-year-timeline]");
    const yearJourneys = root.querySelector("[data-year-journeys]");
    const state = {
      filter: "all",
      mapMode: "china",
      regionCode: "",
      regionName: "",
      selectedId: "",
      year: "",
      view: window.location.hash === "#yearbook" ? "yearbook" : "map",
      maps: {},
      project: null,
    };

    const domesticPlaces = places.filter((place) => placeCountryCode(place) === "CHN");
    const provinceCount = new Set(domesticPlaces.map((place) => normalizeProvince(place.province)).filter(Boolean)).size;
    const countryCount = new Set(places.map((place) => placeCountryCode(place) || place.country).filter(Boolean)).size;
    root.querySelector('[data-stat="places"]').textContent = places.length;
    root.querySelector('[data-stat="provinces"]').textContent = provinceCount;
    root.querySelector('[data-stat="countries"]').textContent = countryCount;
    root.querySelector('[data-stat="stories"]').textContent = places.filter((place) => place.article).length;

    function setTravelView(view, updateHash) {
      const nextView = view === "yearbook" ? "yearbook" : "map";
      state.view = nextView;
      viewButtons.forEach((button) => {
        const active = button.dataset.travelView === nextView;
        button.classList.toggle("is-active", active);
        button.setAttribute("aria-selected", active ? "true" : "false");
        button.tabIndex = active ? 0 : -1;
      });
      viewPanels.forEach((panel) => {
        panel.hidden = panel.dataset.travelPanel !== nextView;
      });
      if (updateHash) {
        window.history.replaceState(null, "", nextView === "yearbook" ? "#yearbook" : "#map");
      }
    }

    function dateParts(place) {
      const match = String(place.date || "").match(/^(\d{4})-(0[1-9]|1[0-2])/);
      return match ? { year: match[1], month: Number(match[2]) } : null;
    }

    function visitsForPlace(place) {
      const name = place.name || place.city || place.country;
      return places
        .filter((item) => (item.name || item.city || item.country) === name)
        .sort((left, right) => {
          const byDate = String(left.date || "").localeCompare(String(right.date || ""));
          return byDate || places.indexOf(left) - places.indexOf(right);
        });
    }

    function visitLabel(place) {
      const samePlaceVisits = visitsForPlace(place);
      if (samePlaceVisits.length < 2) return "";
      return `第 ${samePlaceVisits.indexOf(place) + 1} 次到访`;
    }

    function visitDateText(place) {
      return [place.date || "日期待补", visitLabel(place)].filter(Boolean).join(" · ");
    }

    const datedPlaces = places.filter(dateParts);
    const years = Array.from(new Set(datedPlaces.map((place) => dateParts(place).year))).sort(
      (left, right) => Number(right) - Number(left)
    );
    state.year = years[0] || "";

    function focusYearPlace(place) {
      setTravelView("map", true);
      const targetMode = placeCountryCode(place) === "CHN" ? "china" : "world";
      state.filter = "all";
      state.regionCode = "";
      state.regionName = "";
      if (state.mapMode !== targetMode) {
        state.mapMode = targetMode;
        if (state.maps[targetMode]) renderMap();
      } else {
        applyState();
      }
      selectPlace(place, false);
      root.querySelector(".travel-map__workspace").scrollIntoView({ behavior: "smooth", block: "center" });
    }

    function annualNarrative(yearPlaces) {
      const togetherCount = yearPlaces.filter((place) => place.who === "together").length;
      if (togetherCount === yearPlaces.length) {
        return "这一年的每一次抵达，都有彼此在身边。山河很远，但并肩走过以后，都成了共同记忆。";
      }
      if (togetherCount > 0) {
        return `有 ${togetherCount} 次并肩出发，也有各自带回来的风景。不同方向的路，最后汇进同一本旅行簿。`;
      }
      return "这一年，你们从不同方向看见世界，再把沿途的光和风带回来，放进共同的旅行簿。";
    }

    function renderYearbook() {
      yearTabs.replaceChildren();
      if (!years.length) {
        yearbookContent.hidden = true;
        yearbookEmpty.hidden = false;
        return;
      }

      yearbookContent.hidden = false;
      yearbookEmpty.hidden = true;
      years.forEach((year) => {
        const button = createElement("button", state.year === year ? "is-active" : "", year);
        button.type = "button";
        button.setAttribute("aria-pressed", state.year === year ? "true" : "false");
        button.addEventListener("click", () => {
          state.year = year;
          renderYearbook();
        });
        yearTabs.append(button);
      });

      const yearPlaces = datedPlaces
        .filter((place) => dateParts(place).year === state.year)
        .sort((left, right) => String(left.date).localeCompare(String(right.date)));
      const togetherCount = yearPlaces.filter((place) => place.who === "together").length;
      const destinationCount = new Set(
        yearPlaces.map((place) => place.name || place.city || place.country).filter(Boolean)
      ).size;
      const storyCount = yearPlaces.filter((place) => place.article).length;
      const countrySet = new Set(yearPlaces.map((place) => placeCountryCode(place)).filter(Boolean));
      const provinceSet = new Set(
        yearPlaces
          .filter((place) => placeCountryCode(place) === "CHN")
          .map((place) => normalizeProvince(place.province))
          .filter(Boolean)
      );
      const firstPlace = yearPlaces[0];
      const lastPlace = yearPlaces[yearPlaces.length - 1];
      const firstName = firstPlace.name || firstPlace.city || firstPlace.country;
      const lastName = lastPlace.name || lastPlace.city || lastPlace.country;
      const coverage = countrySet.size > 1
        ? `${countrySet.size} 个国家`
        : `${provinceSet.size || countrySet.size} 个${provinceSet.size ? "省份" : "国家"}`;

      yearLabel.textContent = `${state.year} · 年度旅行记录`;
      yearTitle.textContent = `${state.year}，我们把 ${yearPlaces.length} 次出发写进地图`;
      yearNarrative.textContent = annualNarrative(yearPlaces);
      yearRoute.textContent = yearPlaces.length > 1
        ? `从 ${firstName} 到 ${lastName}，足迹覆盖 ${coverage}。`
        : `这一年的坐标停在 ${firstName}，一段旅程也足以让时间有了刻度。`;
      root.querySelector('[data-year-stat="visits"]').textContent = yearPlaces.length;
      root.querySelector('[data-year-stat="destinations"]').textContent = destinationCount;
      root.querySelector('[data-year-stat="together"]').textContent = togetherCount;
      root.querySelector('[data-year-stat="stories"]').textContent = storyCount;

      const months = Array.from({ length: 12 }, (_, index) =>
        yearPlaces.filter((place) => dateParts(place).month === index + 1)
      );
      const maxMonthCount = Math.max(1, ...months.map((monthPlaces) => monthPlaces.length));
      yearTimeline.replaceChildren();
      months.forEach((monthPlaces, index) => {
        const month = String(index + 1).padStart(2, "0");
        const button = createElement(
          "button",
          `travel-map__year-month${monthPlaces.length ? " has-journey" : ""}`
        );
        button.type = "button";
        button.disabled = monthPlaces.length === 0;
        button.setAttribute(
          "aria-label",
          monthPlaces.length ? `${state.year} 年 ${index + 1} 月有 ${monthPlaces.length} 次旅行` : `${index + 1} 月没有旅行`
        );
        const pulse = createElement("i", "");
        pulse.style.setProperty("--month-strength", monthPlaces.length / maxMonthCount);
        button.append(
          createElement("span", "travel-map__year-month-label", month),
          createElement("span", "travel-map__year-month-track")
        );
        button.lastElementChild.append(pulse);
        button.append(createElement("small", "", monthPlaces.length ? String(monthPlaces.length) : "·"));
        if (monthPlaces.length) {
          button.addEventListener("click", () => focusYearPlace(monthPlaces[0]));
        }
        yearTimeline.append(button);
      });

      yearJourneys.replaceChildren();
      yearPlaces.forEach((place, index) => {
        const button = createElement("button", "travel-map__year-journey");
        button.type = "button";
        button.setAttribute("aria-label", `查看 ${visitDateText(place)} 的${place.name || place.city || place.country}足迹`);
        const order = createElement("span", "travel-map__year-journey-order", String(index + 1).padStart(2, "0"));
        const copy = createElement("span", "travel-map__year-journey-copy");
        copy.append(
          createElement("small", "", visitDateText(place)),
          createElement("strong", "", place.name || place.city || place.country)
        );
        const who = createElement(
          "span",
          `travel-map__year-journey-who is-${place.who || "together"}`,
          WHO_LABELS[place.who] || "我们俩"
        );
        button.append(order, copy, who);
        button.addEventListener("click", () => focusYearPlace(place));
        yearJourneys.append(button);
      });
    }

    function regionCodeForPlace(place) {
      return state.mapMode === "china" ? normalizeProvince(place.province) : placeCountryCode(place);
    }

    function visiblePlaces() {
      return places.filter((place) => {
        const matchesScope = state.mapMode === "world" || placeCountryCode(place) === "CHN";
        const matchesPerson = state.filter === "all" || place.who === state.filter;
        const matchesRegion = !state.regionCode || regionCodeForPlace(place) === state.regionCode;
        return matchesScope && matchesPerson && matchesRegion;
      });
    }

    function locationText(place) {
      const values = [];
      if (place.country && placeCountryCode(place) !== "CHN") values.push(place.country);
      [place.province, place.city, place.district].filter(Boolean).forEach((value) => {
        if (!values.includes(value)) values.push(value);
      });
      return values.join(" · ") || place.country || "地点待补";
    }

    function coordinateText(place) {
      if (!Array.isArray(place.coordinates) || place.coordinates.length < 2) return "坐标待补";
      const longitude = Number(place.coordinates[0]);
      const latitude = Number(place.coordinates[1]);
      if (!Number.isFinite(longitude) || !Number.isFinite(latitude)) return "坐标待补";
      return `${Math.abs(latitude).toFixed(4)}° ${latitude >= 0 ? "N" : "S"}  ·  ${Math.abs(longitude).toFixed(4)}° ${longitude >= 0 ? "E" : "W"}`;
    }

    function setDetail(place) {
      detail.replaceChildren();
      delete detail.dataset.entryIndex;
      if (!place) {
        const empty = createElement("div", "travel-map__empty-detail");
        const compass = createElement("span", "travel-map__compass", "⌖");
        compass.setAttribute("aria-hidden", "true");
        empty.append(
          compass,
          createElement("p", "travel-map__detail-kicker", "从一个坐标开始"),
          createElement("h3", "", "选择地图上的足迹"),
          createElement("p", "", "这里会展示日期、具体地点和游记入口。")
        );
        detail.append(empty);
        return;
      }

      const entryIndex = places.indexOf(place) + 1;
      detail.dataset.entryIndex = String(entryIndex).padStart(2, "0");

      const header = createElement("div", "travel-map__detail-top");
      const badge = createElement(
        "span",
        `travel-map__who is-${place.who || "together"}`,
        WHO_LABELS[place.who] || "我们俩"
      );
      const date = createElement("time", "", visitDateText(place));
      if (place.date) date.dateTime = place.date;
      header.append(badge, date);

      const kicker = createElement(
        "p",
        "travel-map__detail-kicker",
        `TRAVEL ENTRY · ${String(entryIndex).padStart(2, "0")}`
      );
      const title = createElement("h3", "", place.name || place.city || place.country || "未命名足迹");
      const location = createElement("p", "travel-map__location", locationText(place));
      detail.append(header, kicker, title, location);

      const spotNames = Array.isArray(place.spots) && place.spots.length
        ? place.spots
        : [place.name || place.city || place.country || "地点待补"];

      const spotLog = createElement("section", "travel-map__spot-log");
      spotLog.append(createElement("p", "travel-map__section-label", "这次走过"));
      const spots = createElement("ol", "travel-map__spots");
      spotNames.forEach((spot) => {
        const item = createElement("li", "");
        item.append(createElement("span", "", spot));
        spots.append(item);
      });
      spotLog.append(spots);
      detail.append(spotLog);

      const footer = createElement("div", "travel-map__detail-footer");
      const signal = createElement("div", "travel-map__coordinate");
      signal.append(
        createElement("small", "", "LOCATION SIGNAL"),
        createElement("code", "", coordinateText(place))
      );
      footer.append(signal);

      if (place.article) {
        const link = createElement("a", "travel-map__article-link", "阅读这篇游记");
        link.href = place.article;
        link.append(createElement("span", "", "→"));
        footer.append(link);
      } else {
        footer.append(
          createElement("span", "travel-map__article-link is-disabled", "游记待补 · 添加 article 后自动开启")
        );
      }
      detail.append(footer);
    }

    function selectPlace(place, shouldScroll) {
      state.selectedId = place ? String(place.id || place.name) : "";
      setDetail(place);
      root.querySelectorAll("[data-place-id]").forEach((node) => {
        const selected = node.dataset.placeId === state.selectedId;
        node.classList.toggle("is-selected", selected);
        node.setAttribute("aria-pressed", selected ? "true" : "false");
      });
      if (shouldScroll && window.matchMedia("(max-width: 760px)").matches) {
        detail.scrollIntoView({ behavior: "smooth", block: "nearest" });
      }
    }

    function createListCard(place) {
      const card = createElement("article", "travel-map__place-card");
      const button = createElement("button", "travel-map__place-button");
      button.type = "button";
      button.dataset.placeId = String(place.id || place.name);
      button.setAttribute("aria-pressed", "false");
      button.setAttribute("aria-label", `查看${place.name || place.city || place.country}的旅行记录`);

      const top = createElement("div", "travel-map__place-card-top");
      top.append(
        createElement(
          "span",
          `travel-map__who is-${place.who || "together"}`,
          WHO_LABELS[place.who] || "我们俩"
        ),
        createElement("time", "", visitDateText(place))
      );
      button.append(
        top,
        createElement("h4", "", place.name || place.city || place.country || "未命名足迹"),
        createElement("p", "", locationText(place)),
        createElement("span", "travel-map__card-action", place.article ? "查看足迹与游记 →" : "查看足迹 →")
      );
      button.addEventListener("click", () => selectPlace(place, true));
      card.append(button);
      return card;
    }

    function renderList() {
      const filtered = visiblePlaces();
      list.replaceChildren();
      filtered.forEach((place) => list.append(createListCard(place)));
      emptyState.hidden = filtered.length !== 0;
      resultCount.textContent = `${filtered.length} 个坐标`;
      const scopeLabel = state.mapMode === "china" ? "中国足迹" : "世界足迹";
      listHeading.textContent = state.regionName
        ? `${state.regionName}的足迹`
        : state.filter === "all"
          ? scopeLabel
          : `${WHO_LABELS[state.filter]}的${scopeLabel}`;

      if (state.selectedId) {
        const selected = filtered.find((place) => String(place.id || place.name) === state.selectedId);
        if (!selected) {
          selectPlace(null, false);
        } else {
          root.querySelectorAll("[data-place-id]").forEach((node) => {
            const isSelected = node.dataset.placeId === state.selectedId;
            node.classList.toggle("is-selected", isSelected);
            node.setAttribute("aria-pressed", isSelected ? "true" : "false");
          });
        }
      }
    }

    function updateMapState() {
      const filtered = visiblePlaces();
      const visibleIds = new Set(filtered.map((place) => String(place.id || place.name)));
      const visitedRegions = new Set(filtered.map(regionCodeForPlace).filter(Boolean));

      svg.querySelectorAll(".travel-map__province").forEach((path) => {
        const code = path.dataset.regionCode;
        const isVisited = visitedRegions.has(code);
        path.classList.toggle("is-visited", isVisited);
        path.classList.toggle("is-selected", state.regionCode === code);
        path.setAttribute("tabindex", isVisited ? "0" : "-1");
        path.setAttribute("aria-pressed", state.regionCode === code ? "true" : "false");
      });
      svg.querySelectorAll(".travel-map__marker").forEach((marker) => {
        const visible = visibleIds.has(marker.dataset.placeId);
        marker.classList.toggle("is-hidden", !visible);
        marker.setAttribute("tabindex", visible ? "0" : "-1");
      });
    }

    function applyState() {
      clearRegion.hidden = !state.regionCode;
      clearRegion.textContent = state.regionName ? `× ${state.regionName}` : "查看全部";
      mapHint.textContent =
        state.mapMode === "china"
          ? "点击省份筛选 · 点击坐标查看故事"
          : "点击国家筛选 · 点击坐标查看故事";
      filterButtons.forEach((button) => {
        const active = button.dataset.travelFilter === state.filter;
        button.classList.toggle("is-active", active);
        button.setAttribute("aria-pressed", active ? "true" : "false");
      });
      modeButtons.forEach((button) => {
        const active = button.dataset.mapMode === state.mapMode;
        button.classList.toggle("is-active", active);
        button.setAttribute("aria-pressed", active ? "true" : "false");
      });
      renderList();
      updateMapState();
    }

    function showTooltip(event, text) {
      tooltip.textContent = text;
      tooltip.classList.add("is-visible");
      const rect = root.querySelector("[data-map-canvas]").getBoundingClientRect();
      tooltip.style.left = `${event.clientX - rect.left}px`;
      tooltip.style.top = `${event.clientY - rect.top}px`;
    }

    function hideTooltip() {
      tooltip.classList.remove("is-visible");
    }

    function renderMap() {
      const isWorld = state.mapMode === "world";
      const geojson = state.maps[state.mapMode];
      if (!geojson) return;
      const rawProject = isWorld ? worldRawProjection : chinaRawProjection;
      const features = isWorld
        ? geojson.features.filter((feature) => feature.properties.ADM0_A3 !== "ATA")
        : geojson.features;
      state.project = createProjection(getBounds(features, rawProject), rawProject);
      svg.replaceChildren();
      svg.setAttribute("aria-label", isWorld ? "世界旅行足迹地图" : "中国旅行足迹地图");

      const regionLayer = createSvgElement("g", { class: "travel-map__province-layer" });
      features.forEach((feature) => {
        const properties = feature.properties || {};
        const regionCode = isWorld
          ? String(properties.ADM0_A3 || properties.NAME_EN || "")
          : normalizeProvince(properties.name);
        const regionName = isWorld
          ? String(properties.NAME_ZH || properties.NAME_EN || regionCode)
          : regionCode;
        const path = createSvgElement("path", {
          class: "travel-map__province",
          d: geometryToPath(feature.geometry, state.project),
          role: "button",
          tabindex: "-1",
          "aria-label": regionName,
          "aria-pressed": "false",
        });
        path.dataset.regionCode = regionCode;
        path.dataset.regionName = regionName;
        path.addEventListener("pointerenter", (event) => showTooltip(event, regionName));
        path.addEventListener("pointermove", (event) => showTooltip(event, regionName));
        path.addEventListener("pointerleave", hideTooltip);
        const toggleRegion = () => {
          if (state.regionCode === regionCode) {
            state.regionCode = "";
            state.regionName = "";
          } else {
            state.regionCode = regionCode;
            state.regionName = regionName;
          }
          applyState();
        };
        path.addEventListener("click", toggleRegion);
        path.addEventListener("keydown", (event) => {
          if (event.key === "Enter" || event.key === " ") {
            event.preventDefault();
            toggleRegion();
          }
        });
        regionLayer.append(path);
      });
      svg.append(regionLayer);

      const markerLayer = createSvgElement("g", { class: "travel-map__marker-layer" });
      const scopedPlaces = places.filter((place) => {
        const matchesScope = isWorld || placeCountryCode(place) === "CHN";
        return matchesScope && Array.isArray(place.coordinates) && place.coordinates.length >= 2;
      });
      const coordinateGroups = new Map();
      scopedPlaces.forEach((place) => {
        const key = place.coordinates.map((value) => Number(value).toFixed(5)).join(",");
        if (!coordinateGroups.has(key)) coordinateGroups.set(key, []);
        coordinateGroups.get(key).push(place);
      });
      scopedPlaces.forEach((place) => {
        const key = place.coordinates.map((value) => Number(value).toFixed(5)).join(",");
        const group = coordinateGroups.get(key);
        const visitIndex = group.indexOf(place);
        const radius = group.length > 1 ? Math.min(20, 11 + group.length * 2) : 0;
        const angle = -Math.PI / 2 + (visitIndex * Math.PI * 2) / group.length;
        const offsetX = radius ? Math.cos(angle) * radius : 0;
        const offsetY = radius ? Math.sin(angle) * radius : 0;
        const [projectedX, projectedY] = state.project(place.coordinates);
        const x = projectedX + offsetX;
        const y = projectedY + offsetY;
        const marker = createSvgElement("g", {
          class: `travel-map__marker is-${place.who || "together"}`,
          transform: `translate(${x.toFixed(1)} ${y.toFixed(1)})`,
          role: "button",
          tabindex: "0",
          "aria-label": `${place.name || place.city || place.country}，${visitDateText(place)}，${WHO_LABELS[place.who] || "我们俩"}的足迹`,
          "aria-pressed": "false",
        });
        marker.dataset.placeId = String(place.id || place.name);
        marker.append(
          createSvgElement("circle", { class: "travel-map__marker-pulse", r: "18" }),
          createSvgElement("circle", { class: "travel-map__marker-ring", r: "10" }),
          createSvgElement("circle", { class: "travel-map__marker-core", r: "5" })
        );
        marker.addEventListener("pointerenter", (event) =>
          showTooltip(event, `${place.name || place.city || place.country} · ${visitDateText(place)}`)
        );
        marker.addEventListener("pointermove", (event) =>
          showTooltip(event, `${place.name || place.city || place.country} · ${visitDateText(place)}`)
        );
        marker.addEventListener("pointerleave", hideTooltip);
        marker.addEventListener("click", (event) => {
          event.stopPropagation();
          selectPlace(place, true);
        });
        marker.addEventListener("keydown", (event) => {
          if (event.key === "Enter" || event.key === " ") {
            event.preventDefault();
            selectPlace(place, true);
          }
        });
        markerLayer.append(marker);
      });
      svg.append(markerLayer);
      loading.hidden = true;
      applyState();
    }

    viewButtons.forEach((button, index) => {
      button.addEventListener("click", () => setTravelView(button.dataset.travelView, true));
      button.addEventListener("keydown", (event) => {
        let nextIndex = null;
        if (event.key === "ArrowRight") nextIndex = (index + 1) % viewButtons.length;
        if (event.key === "ArrowLeft") nextIndex = (index - 1 + viewButtons.length) % viewButtons.length;
        if (event.key === "Home") nextIndex = 0;
        if (event.key === "End") nextIndex = viewButtons.length - 1;
        if (nextIndex === null) return;
        event.preventDefault();
        const nextButton = viewButtons[nextIndex];
        setTravelView(nextButton.dataset.travelView, true);
        nextButton.focus();
      });
    });
    window.addEventListener("hashchange", () => {
      if (window.location.hash === "#map" || window.location.hash === "#yearbook") {
        setTravelView(window.location.hash.slice(1), false);
      }
    });

    filterButtons.forEach((button) => {
      button.addEventListener("click", () => {
        state.filter = button.dataset.travelFilter;
        applyState();
      });
    });
    modeButtons.forEach((button) => {
      button.addEventListener("click", () => {
        const mode = button.dataset.mapMode;
        if (mode === state.mapMode || !state.maps[mode]) return;
        state.mapMode = mode;
        state.regionCode = "";
        state.regionName = "";
        selectPlace(null, false);
        renderMap();
      });
    });
    clearRegion.addEventListener("click", () => {
      state.regionCode = "";
      state.regionName = "";
      applyState();
    });

    setTravelView(state.view, false);
    renderYearbook();
    renderList();
    Promise.all([
      fetch(config.chinaMapUrl).then((response) => {
        if (!response.ok) throw new Error(`China map request failed: ${response.status}`);
        return response.json();
      }),
      fetch(config.worldMapUrl).then((response) => {
        if (!response.ok) throw new Error(`World map request failed: ${response.status}`);
        return response.json();
      }),
    ])
      .then(([china, world]) => {
        state.maps = { china, world };
        renderMap();
      })
      .catch(() => {
        loading.hidden = true;
        error.hidden = false;
      });
  }

  function boot() {
    document.querySelectorAll("[data-travel-map]").forEach(initTravelMap);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot, { once: true });
  } else {
    boot();
  }
})();
