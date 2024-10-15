---
title: "如何进行小程序抓包"
subtitle: ""

init_date: "2022-09-19T22:49:07+08:00"

date: 2022-09-19

lastmod: 2022-09-23

draft: true

author: "xiaobinqt"
description: "xiaobinqt,"

featuredImage: ""

featuredImagePreview: ""

reproduce: false

translate: false

tags: ["抓包","httpDebugger"]
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


抓包是第一步，推荐使用 HTTPDebugger 抓包软件，因为小白上手快，当然也可以使用 Fiddler 或是 Charles，具体使用教程可以去网上搜...

<!--more-->

## 说明

本文只是为了抓包和哄女朋友开心，不做任何商业用途。

## 如何抓包

抓包是第一步，推荐使用 HTTPDebugger 抓包软件，因为小白上手快，当然也可以使用 Fiddler 或是 Charles，具体使用教程可以去网上搜， 这里推荐一个 HTTPDebugger 的 B 站教程 [使用HTTPDebuggerPro抓包工具获取认证码教程](https://www.bilibili.com/video/BV15i4y1U7Yh/?vd_source=1230278c476e4b633e6d1d0aa5433749)
，
[HTTP Debugger Pro破解版 v9.12 附破解补丁](https://www.downbank.cn/soft/141795.htm)。

## 通过小程序抓取用户信息

羊了个羊的 domain 是 `cat-match.easygame2021.com`，通过 httpDebugger 设置只显示这个 domain

![设置显示 domain](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220923/1c23375f42574b398c4394bf8f52d86d.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15)

通过用户信息的接口获取我们需要的信息

![用户信息](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220924/135dc2c5d4ab4227bbc23ba07bcd242c.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15)

## 开始通关

## FAQ

```shell
The accepted certificate will be saved in truststore xxxx\ssl\cacerts with the default password changeit
```

在使用 httpDebugger 的时候，发现 goland 的图片上传功能不用用了，并且有时还提示:point_up:
上面这个错误，解决方式可以参考 [如何解决服务器证书不受信任,pycharm 如何跳出服务器证书不受信任的提示](https://blog.csdn.net/weixin_33805938/article/details/119307550)
。

