---
title: "IPv4 forwarding is disabled. Networking will not work"
subtitle: ""

init_date: "2022-05-08T23:19:32+08:00"

date: 2020-11-08

lastmod: 2022-05-08

draft: false

author: "xiaobinqt"
description: "xiaobinqt,docker IPv4 forwarding is disabled. Networking will not work"

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

今天在操作 docker 时遇到了一个问题`IPv4 forwarding is disabled. Networking will not work`:point_down:

![报错信息](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220508/e1bf06fd0d134476833680c7c412da4a.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '报错信息')

我的系统是 CentOS7.9

![系统信息](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220508/bd163e7f159544fb82224f0e6e37fbf6.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '系统信息')

## 解决方案

在宿主机执行

```shell
echo "net.ipv4.ip_forward=1" >>/usr/lib/sysctl.d/00-system.conf
```

然后重启网络和 docker

```shell
systemctl restart network
systemctl restart docker
```

![问题解决](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220508/a8321d29039d48be9106c0ad5ba07f35.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '问题解决')




