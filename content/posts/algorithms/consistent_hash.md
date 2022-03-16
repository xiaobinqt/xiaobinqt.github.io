---
title: "一致性 hash"

date: 2022-01-15T22:01:59+08:00

lastmod: 2022-03-16T22:01:59+08:00

draft: false

author: "xiaobinqt"
description: ""
resources:

- name: ""
  src: ""

tags: ["算法"]
categories: ["algorithms"]
lightgallery: true

toc:
auto: false

math:
enable: true
---

## 存在的意义

一致性哈希算法解决了普通余数 Hash 算法伸缩性差的问题，可以保证在上线、下线服务器的情况下尽量有多的请求命中原来路由到的服务器。

## 优化

一致性哈希算法在服务节点太少时，容易因为节点分部不均匀而造成数据倾斜问题。可以通过通过增加虚拟节点来解决数据倾斜问题。

如果存在大量的虚拟节点，节点的查找性能就成为必须考虑的因数。可以使用[红黑树](https://xiaozhuanlan.com/topic/1248367905) 来加快查找速度，

## 参考

+ [一致性Hash(Consistent Hashing)原理剖析及Java实现](https://blog.csdn.net/suifeng629/article/details/81567777)
+ [图解一致性哈希算法](https://segmentfault.com/a/1190000021199728)
+ [golang实现一致性hash环及优化方法](http://jintang.zone/2018/08/20/golang%E5%AE%9E%E7%8E%B0%E4%B8%80%E8%87%B4%E6%80%A7hash%E7%8E%AF%E5%8F%8A%E4%BC%98%E5%8C%96%E6%96%B9%E6%B3%95.html)
+ [一致性哈希](https://geektutu.com/post/geecache-day4.html)
