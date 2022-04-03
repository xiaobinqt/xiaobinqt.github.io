---
title: "go GMP 模型"

date: 2022-03-16

lastmod: 2022-03-16

draft: false

author: "xiaobinqt"
description: "golang GMP 模型,go 数学模型,GMP,进程,线程,协程,goroutine,go 调度器,golang调度器"
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

## 进程、线程、协程的区别

## 协程的上下文切换比线程的上下文切换代价小

## go 调度器机制

### 知识点

Go程序中没有语言级的关键字让你去创建一个内核线程，你只能创建 goroutine，内核线程只能由 runtime 根据实际情况去创建。

Go运行时系统并没有内核调度器的中断能力，内核调度器会发起抢占式调度将长期运行的线程中断并让出CPU资源，让其他线程获得执行机会。

## 参考

+ [Go 为什么这么“快”](https://zhuanlan.zhihu.com/p/111346689)
+ [让你很快就能理解-go的协程调度原理](https://blog.csdn.net/weixin_38054045/article/details/104098072)
+ [Golang goroutine与调度器](https://studygolang.com/articles/9211)
+ [Go语言的并发模型](https://www.golangroadmap.com/class/goadvanced/3-4.html#_1-2-%E7%94%A8%E6%88%B7%E7%BA%A7%E7%BA%BF%E7%A8%8B%E6%A8%A1%E5%9E%8B)


