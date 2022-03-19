---
title: "将google浏览器插件下载到本地"

date: 2022-03-16T20:21:27+08:00

lastmod: 2022-03-16T20:21:27+08:00

draft: false

author: "xiaobinqt"
description: "将google浏览器插件下载到本地"
resources:

- name: ""
  src: ""

tags: ["开发者工具"]
categories: ["developer"]
lightgallery: true

toc:
auto: false

math:
enable: true
---



国内的网络太复杂了，在不能访问 google 的情况下，甚至都不能打开[网上应用商店]()，所以我们需要一个方便的方式来下载google浏览器插件并分享 给需要的小伙伴。

我们打开任意一个浏览器插件，如：

![浏览器插件](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220310/44011f7633904acfb7ba4d6aaf8721a5.png?imageView2/0/interlace/1/q/50|imageslim " ")

URL 地址栏中有一串字符串，这是唯一的，通过这个字符串可以获取到插件的下载地址，如：

![插件UUID](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220310/cc9222ca1f174fd08017f2b54342ff02.png?imageView2/0/interlace/1/q/50|imageslim " ")

下载地址为：

```shell
https://clients2.google.com/service/update2/crx?response=redirect&os=win&arch=x64&os_arch=x86_64&nacl_arch=x86-64&prod=chromecrx&prodchannel=&prodversion=77.0.3865.90&lang=zh-CN&acceptformat=crx2,crx3&x=id%3D{XXXX}%26installsource%3Dondemand%26uc
```

将以上的 `{XXXX}` 替换为插件的 ID，就可以下载到本地了。

以下这个地址是`Mote：语音笔记和反馈`插件的下载地址，成功下载的插件是 .crx 结尾的文件。直接拖到浏览器中就会自动安装。

```shell
https://clients2.google.com/service/update2/crx?response=redirect&os=win&arch=x64&os_arch=x86_64&nacl_arch=x86-64&prod=chromecrx&prodchannel=&prodversion=77.0.3865.90&lang=zh-CN&acceptformat=crx2,crx3&x=id%3Dajphlblkfpppdpkgokiejbjfohfohhmk%26installsource%3Dondemand%26uc
```


