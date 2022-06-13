---
title: "Go build 添加版本等信息"
subtitle: ""

init_date: "2022-06-13T13:56:06+08:00"

date: 2021-05-24

lastmod: 2022-06-13

draft: false

author: "xiaobinqt"
description: "xiaobinqt,go,go build,go build 添加版本等信息,golang 构建添加额外的参数"

featuredImage: ""

featuredImagePreview: ""

reproduce: false

translate: false

tags: ["golang"]
categories: ["golang"]
lightgallery: true

toc: false

math:
enable: true
---

<!-- author： xiaobinqt -->
<!-- email： xiaobinqt@163.com -->
<!-- https://xiaobinqt.github.io -->
<!-- https://www.xiaobinqt.cn -->


Go 在编译时可以添加一些额外的参数，这些参数可以用来添加版本信息。

比如有以下的 t.go 文件源码:point_down:

```go
package main

import (
	"flag"
	"fmt"
	"runtime"
)

var (
	version   string
	buildTime string
	commitID  string
)

func init() {
	flag.StringVar(&version, "version", "", "版本信息")
}
func main() {
	flag.Parse()
	if version == "version" || version == "v" {
		fmt.Printf("Git commit:   %s\nGo version:   %s\nBuilt:        %s\nOS/Arch:      %s/%s\n ",
			commitID, runtime.Version(), buildTime, runtime.GOOS, runtime.GOARCH)
		return
	}
	fmt.Println("hello world")
}


```

用以下命令编译:point_down:

**注意**：`-X` 后面要写完整的包路径，示例中是 main 包。

```shell
go build -ldflags "-X 'main.version=1.0.0' -X 'main.buildTime=$(date +"%Y-%m-%d %H:%M:%S")' -X 'main.commitID=1234567890'" -o t t.go
```

![示例结果](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220613/4d68fd3e1a534653a83c099a30079ea9.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '示例结果')

可以看到，编译后的文件中包含了版本信息，比如版本号、编译时间、提交ID等。


