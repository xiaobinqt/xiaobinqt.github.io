---
title: "WARNING: bridge-nf-call-iptables is disabled"
subtitle: ""

init_date: "2022-05-12T10:12:04+08:00"

date: 2020-08-06

lastmod: 2022-05-12

draft: false

author: "xiaobinqt"
description: "xiaobinqt,WARNING: bridge-nf-call-iptables is disabled"

featuredImage: ""

featuredImagePreview: ""

reproduce: false

translate: false

tags: ["docker"]
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

## 问题

今天在使用 docker 时出现如下问题：

```shell
WARNING: bridge-nf-call-iptables is disabled
```

![warning](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220512/5851b966f1d243718279d4e31dd229e6.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'warning')

我的系统版本是`CentOS 7.9`，

![系统版本](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220512/1265baf476d6436a87f9d0f04eeb2125.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '系统版本')

## 解决办法

```shell
vim /etc/sysctl.conf
```

在 `/etc/sysctl.conf` 中添加如下内容：

```shell
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
```

执行 `sysctl -p` 即可。


