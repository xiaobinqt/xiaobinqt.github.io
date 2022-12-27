---
title: "Go 常用命令"

date: 2022-03-16

lastmod: 2022-03-16

draft: false

author: "xiaobinqt"
description: "go build 常用命令,golang,编译,go 编译"
resources:

- name: ""
  src: ""

tags: ["golang"]
categories: ["golang"]
lightgallery: true

toc: true

math: true
---

## 常用编译参数

| 参数                                  | 说明                                                                                                                                                |
|-------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------|
| -o                                  | 指定输出可执行文件名                                                                                                                                        |
| -v                                  | 编译时显示包名，可以理解成输出详细编译信息                                                                                                                             |
| -u                                  | 不加`-u`标记，执行 go get 一个已有的代码包，会发现命令什么都不执行。加了`-u`才会去拉取最新的代码包的最新版本                                                               |
| -race                               | 开启竞态检测                                                                                                                                            |
| *.go                                | 编译当前目录下的所有go文件，也可以写成 f2.go f2.go ...                                                                                                              |
| -a                                  | 强制重新构建                                                                                                                                            |
| -w                                  | 去掉DWARF调试信息，得到的程序就不能用gdb调试了                                                                                                                       |
| -s                                  | 去掉符号表,panic时候的stack trace就没有任何文件名/行号信息了，这个等价于普通C/C++程序被strip的效果                                                                                   |
| -X                                  | 设置包中的变量值                                                                                                                                          |
| `-gcflags "-N -l"`                  | 编译目标程序的时候会嵌入运行时(runtime)的二进制，禁止优化和内联可以让运行时(runtime)中的函数变得更容易调试。gcflags 其实是给go编译器传入参数，也就是传给go tool compile的参数，因此可以用`go tool compile --help`查看所有可用的参数 |
| -ldflags                            | 给go链接器传入参数，实际是给go tool link的参数，可以用`go tool link --help`查看可用的参数。                                                                                   |
| `-ldflags '-extldflags "-static"' ` | 静态编译                                                                                                                                              |

## 交叉编译

| 参数      | 说明                |                                                                   
|---------|-------------------|
| GOOS    | GOARCH            |
| linux   | 386 / amd64 / arm |
| darwin  | 386 / amd64       |
| feedbsd | 386 / amd64       |
| windows | 386 / amd64       |

对于编译给 ARM 使用的 Go 程序，需要根据实际情况配置`$GOARM`，这是用来控制 CPU 的浮点协处理器的参数。

`$GOARM`默认是 6，对于不支持 VFP 使用软件运算的老版本 ARM 平台要设置成 5，支持 VFPv1 的设置成 6，支持 VFPv3 的设置成 7。

示例

```shell
GOARM=7 GOARCH=arm GOOS=linux go build -v -o fca
```

## go mod

// TODO

## 参考

+ [golang编译时的参数传递（gcflags, ldflags）](https://studygolang.com/articles/23900)
+ [Golang交叉编译（跨平台编译）简述](https://blog.csdn.net/hx7013/article/details/91489642)
+ [交叉编译Go程序](https://holmesian.org/golang-cross-compile)
+ [ARM flags GOARM](https://github.com/goreleaser/goreleaser/issues/36)
+ [go mod使用](https://www.jianshu.com/p/760c97ff644c)