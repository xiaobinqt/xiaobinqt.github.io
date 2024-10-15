---
title: "curl: (60) Peer's Certificate has expired 问题解决"
subtitle: ""

init_date: "2023-01-17T17:28:16+08:00"

date: 2023-01-17

lastmod: 2023-01-17

draft: false

author: "xiaobinqt"
description: "xiaobinqt,Peer's Certificate has expired"

featuredImage: ""

featuredImagePreview: ""

reproduce: false

translate: false

tags: ["linux"]
categories: ["开发者手册"]
lightgallery: true

series: []

series_weight:

toc: false

math: true
---

<!-- author： xiaobinqt -->
<!-- email： xiaobinqt@163.com -->
<!-- https://xiaobinqt.github.io -->
<!-- https://www.xiaobinqt.cn -->


刚执行 curl 命令时发现一个问题 curl: (60) Peer's Certificate has expired

<!--more-->

刚执行 curl 命令时发现一个问题

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230117/51b67e1e9f9847d096a86fe7f7ff27e3.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'Certificate has expired')

可以先更新证书试试

```shell
update-ca-trust
```

更新证书后如果问题没有解决，继续看是不是由于时间过期引起的问题

```shell
date
```

如果发现机器时间不对就需要同步时间

```shell
ntpdate pool.ntp.org

```

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230117/b4ce330953b840b4a1d63c1380beb688.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '问题解决')





