---
title: "Jetbrains 家族 ide 破解方法，支持最新版"
subtitle: ""

init_date: "2022-05-14T16:23:30+08:00"

date: 2021-12-28

lastmod: 2022-05-14

draft: false

author: "xiaobinqt"
description: "xiaobinqt"

featuredImage: ""

featuredImagePreview: "https://cdn.xiaobinqt.cn/xiaobinqt.io/20220514/7e6b991559614e7da550543bcbc18e66.png"

reproduce: false

translate: false

tags: ["jetbrains","ide"]
categories: ["开发者手册"]
lightgallery: true

toc: true

math:
enable: true
---

<!-- author： xiaobinqt -->
<!-- email： xiaobinqt@163.com -->
<!-- https://xiaobinqt.github.io -->
<!-- https://www.xiaobinqt.cn -->


Jetbrains 家族的 ide 对开发者友好，基本支持所有的开发语言，可以去下载页面下载对应的
ide [https://www.jetbrains.com/products/](https://www.jetbrains.com/products/)。

![下载界面](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220514/c0a16a951c564d6491babdcb55f7cc3d.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '下载界面')

## ja-netfilter-all

ide 下载完成后，去 [https://jetbra.in/s](https://jetbra.in/s) 页面下载 ja-netfilter-all 包，

![下载 ja-netfilter-all](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220514/e0477d633ba144c0833db3d63791925a.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '下载 ja-netfilter-all')

将下载的 ja-netfilter-all.zip 解压到不带中文的任意目录，

## 配置 vmoptions

在 ide 的安装目录中找打 `idea64.exe.vmoptions` 文件，比如我的路径是 `D:\mySoft\GoLand\GoLand 2021.1\bin`：

![XXX.vmoptions 路径](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220514/98a21e1f84c743e48c17c19759f23e4b.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'XXX.vmoptions 路径')

使用文本编辑打开，在最后添加一行配置，指向上一步解压出来的 ja-netfilter.jar 文件：

```shell
-javaagent:路径\ja-netfilter.jar=jetbrains
```

![编辑 vmoptions](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220514/9adab854b2344ca0815f28ddd3f552bd.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '编辑 vmoptions')

## 激活码

以上配置完后，重启 ide，复制激活码到 ide 激活即可：

![复制激活码](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220514/e1101a3f6aa14d99a2f10a71dd37b333.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '复制激活码')

![激活](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220514/16ccd8c33c24495aaabf521cdcc39e4c.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '激活')

[//]: # (## 参考)

[//]: # ()
[//]: # (+ [https://springboot.io/t/topic/4592]&#40;https://springboot.io/t/topic/4592&#41;)





