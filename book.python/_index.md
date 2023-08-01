---
title: 简介

type: docs
---

# Python 学习笔记

<div align="center"><img src="https://cdn.xiaobinqt.cn/xiaobinqt.io/20230726/9dea00d3781b4d79b785eec21c13475f.png" width=  /></div>

## 简介

Python 是一种解释型语言，它的代码不会直接被计算机硬件执行，而是由 Python 解释器在运行时逐行解释并执行。

Python 虚拟机负责将 Python 代码转换成可执行的机器码，以便计算机可以理解和执行它们。虚拟机是一个中间层，它充当 Python 代码与底层硬件之间的桥梁。

Python 虚拟机和 Python 解释器在许多文献中可能会被用来描述相同的概念，但它们实际上可以指代不同的层次或不同的角度来理解 Python 的执行方式。

通常情况下，它们可以归纳为以下关系：

1. Python 解释器：Python 解释器是负责执行 Python 代码的软件程序。它读取并解释源代码，并将其转换为可以在计算机上运行的机器码或字节码。解释器可以分为标准 CPython 解释器和其他实现，如 Jython、IronPython 等。CPython 是官方的 Python 解释器，它用 C 语言实现，并且是最常用的实现。

2. Python 虚拟机：Python 虚拟机是一种执行 Python 字节码的虚拟机。当 Python 源代码被解释器解析后，它会生成字节码，这是一种类似于汇编语言的中间形式，不是直接在硬件上运行的机器码。然后，Python 虚拟机会逐行执行这些字节码，并将其翻译成底层硬件指令，以实际执行代码。

Python 解释器是将源代码解析并生成字节码的执行引擎，而 Python 虚拟机是负责运行这些字节码并将其转换为机器码的**运行时环境**。实际上，它们通常被一起提到，因为它们在 Python 代码的执行过程中密切相关。解释器将源代码转换为字节码，并将字节码传递给虚拟机执行。

+ Python 是一种高级编程语言
+ Python 是强类型。比如 `"123" + 5` 这种写法是不被允许的。
+ Python 是解释型语言
+ Python 语法和自然语言很像
+ 足够流行，应用的行业广泛
+ 有着丰富的库（标准库和第三方库）

### 不适用场景

+ 抢购、电商类计算密集型场景
+ 涉及到内存等底层硬件操作
+ 网页、小程序等前端开发
+ App 开发

## 学习资料

+ [Python 官方文档](https://docs.python.org/)
+ [极客时间-零基础学 Python（2023 版）](https://time.geekbang.org/course/intro/100310001)
+ [Youtube-尹会生-零基础学Python（2023版）](https://www.youtube.com/watch?v=Cp8COc1b1z8&list=PLtlSrYhs_2fQJo7gIZH55_EOWIewimzUe&ab_channel=%E5%BF%AB%E8%B6%A3%E5%AD%B8%E7%BF%92)


