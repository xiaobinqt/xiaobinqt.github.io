---
title: "JavaScript heap out of memory"

date: 2022-03-16

lastmod: 2022-03-16

draft: false

author: "xiaobinqt"
description: "node,nodejs, heap out of memory"
resources:

- name: ""
  src: ""

tags: ["web","node"]
categories: ["web"]
lightgallery: true

toc:
  enable: false
  auto: false

math:
  enable: true
---


刚在打包项目时执行 `yarn run build ` 时出现了 oom 的情况，具体报错信息如下：

![JavaScript heap out of memory](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220314/90ed6000706b48e39d4da241245dd9f0.png?imageView2/0/interlace/1/q/50|imageslim " ")

我的环境是 win10 专业版 WSL。

解决办法，设置 `export NODE_OPTIONS=--max_old_space_size=4096`，设置完之后重新执行 `yarn run build ` 即可。

## 参考

+ [Node.js heap out of memory](https://stackoverflow.com/questions/38558989/node-js-heap-out-of-memory)