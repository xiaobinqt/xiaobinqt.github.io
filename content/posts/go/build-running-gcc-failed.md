---
title: "running gcc failed: exit status 1"

date: 2022-02-10

lastmod: 2022-03-16

draft: false

author: "xiaobinqt"
description: "running gcc failed: exit status 1"
resources:

- name: ""
  src: ""

tags: ["golang","build"]
categories: ["golang"]
lightgallery: true

toc: false

math:
  enable: true
---



今天在编译 go 项目时出现了如下错误：

```shell
/usr/local/go/pkg/tool/linux_amd64/link: running gcc failed: exit status 1
/usr/bin/ld: cannot find -lpthread
/usr/bin/ld: cannot find -lc
collect2: error: ld returned 1 exit status
```

解决办法：

```shell
yum install glibc-static.x86_64 -y
```

