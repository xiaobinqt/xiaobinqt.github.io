---
title: "golang make 和 new 的区别"

date: 2021-06-21

lastmod: 2022-03-16

draft: false

author: "xiaobinqt"
description: "go make 和 new 的区别,golang make,golang new,defference with golang make and new"
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

+ make 的作用是初始化内置的数据结构，也就是 `slice`、`map`和 `channel`。
+ new 的作用是根据传入的类型分配一片内存空间并返回指向这片内存空间的指针。

## make

内置函数 `make` 仅支持 `slice`、`map`、`channel` 三种数据类型的内存创建，**其返回值是所创建类型的本身，而不是新的指针引用**。

```
func make(t Type, size ...IntegerType) Type
```

```
func main() {
 v1 := make([]int, 1, 5)
 v2 := make(map[int]bool, 5)
 v3 := make(chan int, 1)
    
 fmt.Println(v1, v2, v3)
}
```

在:point_up:代码中，我们分别对三种类型调用了 `make` 函数进行了初始化。会发现有的入参是有多个长度指定，有的没有。 这里的区别主要
是长度（len）和容量（cap）的指定，**有的类型是没有容量这一说法**。

输出结果：

```
[0] map[] 0xc000044070
```

调用 `make`函数去初始化切片（slice）的类型时，会带有零值。

## new

内置函数 `new` 可以对任意类型进行内存创建和初始化。**其返回值是所创建类型的指针引用**。

```
func new(Type) *Type
```

`new(T)` 和 `&T{}` 效果是一样的。

## 区别

`make` 函数在初始化时，会初始化 `slice`、`chan`、`map` 类型的内部数据结构，`new` 函数并不会。

例如，在 `map` 类型中，合理的长度（len）和容量（cap）可以提高效率和减少开销。

+ `make` 函数：
    + 能够分配并初始化类型所需的内存空间和结构，返回引用类型的本身。
    + 具有使用范围的局限性，仅支持 `channel`、`map`、`slice` 三种类型。
    + 具有独特的优势，`make` 函数会对三种类型的内部数据结构（长度、容量等）赋值。

+ `new` 函数：
    + 能够分配类型所需的内存空间，返回指针引用（指向内存的指针），同时把分配的内存置为零，也就是类型的零值。
    + 可被替代，其实不常用，我们通常都是采用短语句声明以及结构体的字面量达到我们的目的，比如：
      ```
       i := 0
       u := user{}
      ```

## 零值

+ array、struct 每个元素或字段都是对应该类型的零值
+ slice、map 对于零值 nil

## 参考

+ [make、new操作](https://github.com/astaxie/build-web-application-with-golang/blob/master/zh/02.2.md#makenew%E6%93%8D%E4%BD%9C)
+ [Go make 和 new的区别](https://www.cnblogs.com/vincenshen/p/9356974.html)
+ [Go - var & make & new 在复杂类型上的使用区别](https://dryyun.com/2019/05/30/go-new-make-use/)
+ [面试官：Golang 的 new 与make 区别是什么？](https://juejin.cn/post/7085915779006201870)





