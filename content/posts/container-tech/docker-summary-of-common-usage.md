---
title: "Docker 常用命令备忘"
subtitle: "Docker Summary of common Usage"

init_date: "2022-05-06T16:49:05+08:00"

date: 2020-05-06

lastmod: 2022-05-06

draft: false

author: "xiaobinqt"
description: "xiaobinqt,docker root用户执行"

featuredImage: "https://cdn.xiaobinqt.cn/xiaobinqt.io/20220517/ede3bf33a6994294a1d88e7a073a5e9c.png"

featuredImagePreview: "https://cdn.xiaobinqt.cn/xiaobinqt.io/20220506/3305e58fbade4acc862591389ce7cd0f.png"

reproduce: false

translate: false

tags: ["docker","备忘"]
categories: ["开发者手册"]
lightgallery: true

toc: true

math:
    enable: true
---

<!-- author： xiaobinqt -->
<!-- email： xiaobinqt@163.com -->
<!-- https://xiaobinqt.github.io -->
<!-- https://www.xiaobinqt.cn -->

[//]: # (+ :interrobang: root 用户执行)

## root 用户执行

有时进入容器后，用户就是变成非 root 用户，这种时候又没有密码，在执行一些操作的时候就会非常不方便，这是可以用 `-u root` 来指定用户。

![非root用户](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220506/4c15cdd08fc44144ba76364b04a5daed.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '非root用户')

执行简单命令可以这样:point_down:

![图01](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220506/0cb85b06bf314f989212dea7af42535e.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '图01')

如果需要进入容器，可以这样:point_down:

```shell
docker exec  -u root -it 容器名  bash
#或者
docker exec  -u root -it 容器名  sh
```

![图02](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220506/fbee690400664f6d88aea131abc00465.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '图02')














