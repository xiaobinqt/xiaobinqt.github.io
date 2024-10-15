---
title: "Goland 远程调试"
subtitle: ""

init_date: "2022-05-10T15:52:27+08:00"

date: 2022-05-10

lastmod: 2022-05-10

draft: true

author: "xiaobinqt"
description: "xiaobinqt"

featuredImage: ""

featuredImagePreview: ""

reproduce: false

translate: false

tags: [ "golang" ]
categories: [ "golang" ]
lightgallery: true

toc: true

math:
  enable: true
---

<!-- author： xiaobinqt -->
<!-- email： xiaobinqt@163.com -->
<!-- https://xiaobinqt.github.io -->
<!-- https://www.xiaobinqt.cn -->


远程调试就是使用使用本地 IDE 来调试远程服务器上的服务。本地打断点，调用远程服务的接口。本地会停在断点。相当于 debug 远程服务。

```go
package main

import (
	"fmt"
	"os/exec"
)

func main() {
	cmdOutput, err := exec.Command("/bin/sh", "-c", "mktemp").CombinedOutput()
	if err != nil {
		fmt.Println("command err", string(cmdOutput))
		return
	}
	fmt.Println("success........", string(cmdOutput))
}

```

上面的这段代码在 windows 中是无法执行的，如果我的电脑是 windows 的，这时我就需要远程调试这段代码是否正常。

在 Goland 中点击 Edit Configurations：

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20231010/068b0ff17fe44604b4baaf82a43b0713.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'Edit Configurations')

添加一个 Go build：

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20231010/2e448961aa5348f6a601311c9ef6e903.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'Go build')

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20231010/d04fc4c83993467080c4f651fe19e04e.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15)

选择 ssh：

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20231010/8a35483740ac4c469a53c05f986e56aa.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15)

添加服务器地址和密码等：

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20231010/9c9dfabc74774b148e49c6b589d8627c.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15)



-------------------------------

## 安装 dlv

我的服务器上的 Go 环境是 go1.18.5，这的 dlv 使用 1.8.2 版本：

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20231010/b8cd0fdb765f4c09b5c08ebaf9ee732d.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'Go 版本')

```
go install github.com/go-delve/delve/cmd/dlv@v1.8.2
```

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20231010/4e9cdcfaf20848b8946a44b0bce96ada.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'install dlv')

安装完成之后可以使用 `dlv version` 命令验证。

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20231010/db3bd309f65a43fe843726714ea20da5.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'dlv version')

## 使用

比如有如下 Go 代码：

```go
package main

import (
	"fmt"
	"os/exec"
)

func main() {
	cmdOutput, err := exec.Command("/bin/sh", "-c", "mktemp").CombinedOutput()
	if err != nil {
		fmt.Println("command err", string(cmdOutput))
		return
	}
	fmt.Println("success........", string(cmdOutput))
}

```

将代码上传到服务器之后，编译：

```
go build -gcflags "all=-N -l"  -v -o mytest main.go
```

运行如下命令

```
dlv --listen=:2345 --headless=true --api-version=2 --accept-multiclient exec ./mytest
```

带命令行参数,在可执行程序后面带上 `--`，再后面就是命令行参数：

```
dlv --listen=:2345 --headless=true --api-version=2 --accept-multiclient exec ./mytest -- -s 123
```

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20231010/cc929e7c32cc4f679a7458a65d03c645.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'dlv exec')


> 注：dlv 运行的服务只能使用 **kill** 将进程杀死的方式来终止服务

1. 本地Goland配置 其中 Host 设置我对应服务器 IP, Port 为对应端口

![](https://pic1.zhimg.com/v2-6044b19b83b330a1862b824686045904_b.jpg)

![](https://pic3.zhimg.com/v2-9796483762a44516c26fdc16bf6a9a06_b.jpg)

![](https://pic2.zhimg.com/v2-73658923151ee839d1d89cfd23061711_b.jpg)

## 参考

+ [使用goland调试远程代码的操作步骤](http://www.17bigdata.com/study/programming/it-go/it-go-214318.html)

