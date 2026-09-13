# 中国省级地图数据

`china-provinces.geojson` 用于 `/travel/` 旅行足迹页面的省级轮廓和坐标投影。

- 数据来源：阿里云 DataV GeoAtlas（数据来自高德开放平台）
- 原始地址：`https://geo.datav.aliyun.com/areas_v3/bound/100000_full.json`
- 处理方式：保留全部 35 个 Feature，使用 Mapshaper 做 8% 拓扑简化并保留形状，坐标精度保留到 0.001 度
- 获取及处理日期：2026-09-12

这份数据只承担旅行足迹的概览展示，不用于测绘、导航或行政边界认定。

## 世界国家地图

`world-countries.geojson` 用于 `/travel/` 的世界地图视图。

- 数据来源：Natural Earth `ne_110m_admin_0_countries.geojson`
- 原始地址：`https://github.com/nvkelso/natural-earth-vector`
- 数据许可：Public Domain
- 处理方式：保留 177 个国家或地区 Feature，保留中英文名称与三位国家代码，使用 Mapshaper 做 35% 拓扑简化
- 获取及处理日期：2026-09-12

世界地图用于个人旅行足迹概览，不用于导航或政治、行政边界认定。
