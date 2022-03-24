---
title: "go 常用命令"

date: 2022-03-16T21:01:50+08:00

lastmod: 2022-03-16T21:01:50+08:00

draft: false

author: "xiaobinqt"
description: "go build 常用命令"
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

## 常用编译参数

| 参数               | 说明                                                                                                                                                  |
|------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| -o               | 指定输出可执行文件名                                                                                                                                          |
| -v               | 编译时显示包名，可以理解成输出详细编译信息                                                                                                                               |
| -race            | 开启竞态检测                                                                                                                                              |
| *.go             | 编译当前目录下的所有go文件，也可以写成 f2.go f2.go ...                                                                                                                |
| -a               | 强制重新构建                                                                                                                                              |
| -w               | 去掉DWARF调试信息，得到的程序就不能用gdb调试了                                                                                                                         |
| -s               | 去掉符号表,panic时候的stack trace就没有任何文件名/行号信息了，这个等价于普通C/C++程序被strip的效果                                                                                     |
| -X               | 设置包中的变量值                                                                                                                                            |
| `-gcflags "-N -l"` | 编译目标程序的时候会嵌入运行时(runtime)的二进制，禁止优化和内联可以让运行时(runtime)中的函数变得更容易调试。gcflags 其实是给go编译器传入参数，也就是传给go tool compile的参数，因此可以用`go tool compile --help`查看所有可用的参数 |
| -ldflags         | 给go链接器传入参数，实际是给go tool link的参数，可以用`go tool link --help`查看可用的参数。                                                                                     |
| `-ldflags '-extldflags "-static"' `       | 静态编译                                                                                                                                                |

## 交叉编译

| 参数      | 说明                |                                                                   
|---------|-------------------|
| GOOS    | GOARCH            |
| linux   | 386 / amd64 / arm |
| darwin  | 386 / amd64       |
| feedbsd | 386 / amd64       |
| windows | 386 / amd64       |

对于编译给ARM使用的Go程序，需要根据实际情况配置$GOARM，这是用来控制CPU的浮点协处理器的参数。

$GOARM默认是6，对于不支持VFP使用软件运算的老版本ARM平台要设置成5，支持VFPv1的设置成6，支持VFPv3的设置成7。

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