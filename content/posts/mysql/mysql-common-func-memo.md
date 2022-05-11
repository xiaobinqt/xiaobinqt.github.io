---
title: "Mysql 常用函数备忘"
subtitle: ""

init_date: "2022-05-11T12:55:44+08:00"

date: 2018-11-08

lastmod: 2022-05-11

draft: false

author: "xiaobinqt"
description: "xiaobinqt,mysql 时间函数,mysql 时间戳转时间类型"

featuredImage: ""

featuredImagePreview: ""

reproduce: false

translate: false

tags: ["mysql"]
categories: ["mysql"]
lightgallery: true

toc: true

math:
enable: true
---

<!-- author： xiaobinqt -->
<!-- email： xiaobinqt@163.com -->
<!-- https://xiaobinqt.github.io -->
<!-- https://www.xiaobinqt.cn -->

## 时间戳与日期格式转换

UNIX时间戳转换为日期用函数： `FROM_UNIXTIME()`

```mysql
select FROM_UNIXTIME(1156219870);
```

![FROM_UNIXTIME](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220511/16f68bfe754148f1bd995b6aa0b2e74c.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'FROM_UNIXTIME')

日期转换为UNIX时间戳用函数： `UNIX_TIMESTAMP()`

![UNIX_TIMESTAMP](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220511/d1182fbf011d43bf95af2b195956f88b.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'UNIX_TIMESTAMP')


