---
title: "Linux 环境下安装 Go"
subtitle: "Linux Platform Install Go"

init_date: "2022-04-06T11:27:04+08:00"

date: 2020-08-12

lastmod: 2022-04-06

draft: false

author: "xiaobinqt"
description: "Linux 环境下安装 Go,Linux Platform Install Go,如何在 Linux 环境下安装 Go,go,golang"

featuredImage: ""

reproduce: false

tags: ["golang"]
categories: ["golang"]
lightgallery: true

toc:
  auto: false

math:
  enable: true
---

## 安装

在[官网 https://go.dev/dl/](https://go.dev/dl/)，根据自己的环境下载对应的安装包：

![官网安装包列表](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220406/d9f09be56c424e4aac52bf334c302133.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '官网安装包列表')

可以直接用 `wget` 下载

![下载安装包](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220406/17343a1a875d4908bf27bcc49591422b.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '下载安装包')

执行 `tar` 解压到 `/usr/loacl`目录下（官方推荐），得到 go 文件夹等。

```shell
tar -C /usr/local -zxvf go1.17.7.linux-amd64.tar.gz
```

`go1.17.7.linux-amd64.tar.gz` 换成你自己的 go 版本。

添加 `/usr/loacl/go/bin` 目录到 `PATH` 变量中。添加到 `/etc/profile` 或 `$HOME/.profile` 都可以。

```shell
vim /etc/profile
# 在最后一行添加
export GOROOT=/usr/local/go
export PATH=$PATH:$GOROOT/bin
```

![添加环境变量](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220406/5b5467edf57b4810911289caadf9c4cd.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '添加环境变量')

保存退出后source一下

```shell
source /etc/profile
```

![go env](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220406/092b8e8add3045ac92793290c839afe9.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'go env')

## Go环境变量

+ `$GOROOT` 表示 Go 在你的电脑上的安装位置，值一般都是 `$HOME/go`，当然，也可以安装在别的地方。
+ `$GOARCH` 表示目标机器的处理器架构，它的值可以是 386、amd64 或 arm。
+ `$GOOS` 表示目标机器的操作系统，它的值可以是 darwin、freebsd、linux 或 windows。
+ `$GOBIN` 表示编译器和链接器的安装位置，默认是 `$GOROOT/bin`，如果使用的是 Go 1.0.3 及以后的版本，一般情况下你可以将它的值设置为空，Go 将会使用默认值。
+ `$GOPATH` 默认采用和 `$GOROOT` 一样的值，但从 Go 1.1 版本开始，你必须修改为其它路径。它可以包含多个包含 Go 语言源码文件、包文件和可执行文件的路径，而这些路径下又必须分别包含三个规定的目录：src、pkg
  和 bin，这三个目录分别用于存放源码文件、包文件和可执行文件。
+ `$GOARM` 专门针对基于 arm 架构的处理器，它的值可以是 5~7，默认为 6。
+ `$GOMAXPROCS` 用于设置应用程序可使用的处理器个数与核数。