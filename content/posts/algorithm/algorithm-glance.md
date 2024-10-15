---
title: "算法学习笔记"
subtitle: "持续更新中"

init_date: "2022-08-27T12:20:21+08:00"

date: 2021-06-03

lastmod: 2022-08-27

draft: true

author: "xiaobinqt"
description: "xiaobinqt,"

featuredImage: ""

featuredImagePreview: ""

reproduce: false

translate: false

tags: ["算法"]
categories: ["算法与数学"]
lightgallery: true

toc: true

math:
enable: true
---

<!-- author： xiaobinqt -->
<!-- email： xiaobinqt@163.com -->
<!-- https://xiaobinqt.github.io -->
<!-- https://www.xiaobinqt.cn -->

## 主定理

![Master Theorem](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220827/b48dd98212ff40719bc4cc0eafad27a2.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'Master Theorem')

+ 思考
    + 二叉树前中后序遍历，时间复杂度是多少 ?

      O(n)，n 是节点总数，每个节点会访问一次且仅会访问一次。
    + 图的遍历，时间复杂度是多少 ?

      O(n)，n 是图的节点总数，每个节点会访问一次且仅会访问一次。
    + DFS(深度优先)，BFS(广度优先)算法的时间复杂度是多少 ?

      O(n)，n 是搜索空间的节点总数，每个节点会访问一次且仅会访问一次。
    + 二分查找时间复杂度 ?

      O(logn)

    + 跳表的时间复杂度

      O(logn)

## 参考

+ [Clean Code: Book Review](https://www.markhneedham.com/blog/2008/09/15/clean-code-book-review/)
+ [Master theorem (analysis of algorithms)](https://en.wikipedia.org/wiki/Master_theorem_(analysis_of_algorithms))



