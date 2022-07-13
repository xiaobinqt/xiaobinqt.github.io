---
title: "Centos 7.9 安装 Redis 6.0.16"
subtitle: "how centos 7.9 install redis 6.0.16"

init_date: "2022-07-13T17:22:29+08:00"

date: 2021-07-13

lastmod: 2020-07-13

draft: false

author: "xiaobinqt"
description: "xiaobinqt,centos 7.9 安装 Redis 6.0.16,centos 安装 redis"

featuredImage: ""

featuredImagePreview: ""

reproduce: false

translate: false

tags: ["redis","linux"]
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

## 服务器版本

![linux version](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220713/366f5d82de6e4da6af53042bc19237b3.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'linux version')

## 下载

可以直接去官网[下载](https://redis.io/download/)需要的版本即可，这里已 6.0.16 版本为准。

![redis download](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220713/049679c099254e5997410c5b3ac3320c.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'redis download')

## 安装

我把下载的 tar 包放在了 `/root` 目录下，这里可以自行修改。

````shell
tar -xzf redis-6.0.16.tar.gz 
cd redis-6.0.16
make && make install
````

安装成功启动服务：

![install success](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220713/60ee0e9fb15347e7bb24fd512296201c.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'install success')

![redis start](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220713/610f7cb66b1144fa831debe76fe97613.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'redis start')

## 常见问题

### cc: command not found

需要安装 gcc:point_down:

```shell
yum -y install gcc gcc-c++ libstdc++-devel
```

### struct redisServer server_xxx

需要升级 gcc 到 9 版本:point_down:

```shell
yum -y install centos-release-scl
yum -y install devtoolset-9-gcc devtoolset-9-gcc-c++ devtoolset-9-binutils
scl enable devtoolset-9 bash
```

设置永久升级

```shell
echo "source /opt/rh/devtoolset-9/enable" >>/etc/profile
```








