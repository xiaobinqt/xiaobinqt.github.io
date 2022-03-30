---
title: "golang make 和 new 的区别"

date: 2021-06-21

lastmod: 2022-03-16

draft: false

author: "xiaobinqt"
description: ""
resources:

- name: ""
  src: ""

tags: ["golang"]
categories: ["golang"]
lightgallery: true

toc:
auto: false

math:
enable: true
---

## 总结

+ make用于内建类型（map、slice 和channel）的内存分配。new用于各种类型的内存分配。
+ new返回指针，指向新分配的类型 T 的零值。
+ make返回初始化后的（非零）值。

## 参考

+ [make、new操作](https://github.com/astaxie/build-web-application-with-golang/blob/master/zh/02.2.md#makenew%E6%93%8D%E4%BD%9C)
+ [Go make 和 new的区别](https://www.cnblogs.com/vincenshen/p/9356974.html)








