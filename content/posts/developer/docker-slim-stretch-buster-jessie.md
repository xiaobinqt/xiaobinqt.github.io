---
title: "Docker slim、stretch、buster、jessie"
subtitle: ""

init_date: "2022-04-24T12:46:42+08:00"

date: 2018-05-10

lastmod: 2022-04-24

draft: false

author: "xiaobinqt"
description: "xiaobinqt,Docker slim、stretch、buster、jessie"

featuredImage: ""

reproduce: false

tags: ["docker"]
categories: ["开发者手册"]
lightgallery: true

toc: false

math:
enable: true
---

<!-- author： xiaobinqt -->
<!-- email： xiaobinqt@163.com -->
<!-- https://xiaobinqt.github.io -->
<!-- https://www.xiaobinqt.cn -->


在写 Dockerfile 时，在引用基础镜像时经常会看到这样的写法：

```dockerfile
FROM debian:buster
```

或是

```dockerfile
FROM node:14.16.1-stretch-slim
```

那这里的 `buster` 和 `stretch` 具体是什么呢？其实 `buster`、`stretch`还有`jessie`针对的是不同 Debian 代号：

| tag     | debian 版本 |
|---------|-----------|
| `buster`  | Debian 10 |
| `stretch` | Debian 9  |
| `jessie`  | Debian 8  |

`slim` 可以理解为精简版，跟 `Minimal`是一样的。

所以`FROM debian:buster` 就是把 debian 10 作为基础镜像，`FROM node:14.16.1-stretch-slim` 就是把 debian 9 的精简版作为基础镜像。

