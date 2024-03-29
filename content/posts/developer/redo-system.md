---
title: "windows 重做系统"

date: 2018-10-07

lastmod: 2022-03-16

draft: false

author: "xiaobinqt"
description: "Windows,系统,重做系统,win,win10,U盘安装系统"
resources:

- name: ""
  src: ""

tags: ["windows"]
categories: ["开发者手册"]
lightgallery: true

toc: true

math: true
---

## 下载系统

首先我们需要一个最小 4G 大的 U 盘

![image](https://cdn.xiaobinqt.cn/%E5%BE%AE%E4%BF%A1%E5%9B%BE%E7%89%87_20181007201814.jpg  " ")

进入[大白菜网站](http://www.bigbaicai.com/)下载大白菜装机版安装到电脑，好吧，之前一直叫大白菜，不知道什么时候改成叫老白菜了:cry:。

![image](https://cdn.xiaobinqt.cn/TIM%E6%88%AA%E5%9B%BE20181007195445.png " ")

![image](https://cdn.xiaobinqt.cn/TIM%E6%88%AA%E5%9B%BE20181007195654.png " ")

将 U 盘插到电脑上,双击打开大白菜装机版,它会自动读到我们插入的 U 盘，自动匹配默认模式,不需要手动选择。

![image](https://cdn.xiaobinqt.cn/TIM%E6%88%AA%E5%9B%BE20181007203320.png " ")

点击开始制作 --> 确认

![image](https://cdn.xiaobinqt.cn/TIM%E6%88%AA%E5%9B%BE20181007203544.png " ")

等待写入数据包完成和格式化完成后关掉大白菜软件

![image](https://cdn.xiaobinqt.cn/TIM%E6%88%AA%E5%9B%BE20181007203843.png " ")

![image](https://cdn.xiaobinqt.cn/TIM%E6%88%AA%E5%9B%BE20181007204132.png " ")

![image](https://cdn.xiaobinqt.cn/TIM%E6%88%AA%E5%9B%BE20181007204222.png " ")

制作完 U 盘启动盘后我们的 U 盘会变成这样说明启动盘已经制作成功 !

[image](https://cdn.xiaobinqt.cn/TIM%E6%88%AA%E5%9B%BE20181007204825.png)![image](https://cdn.xiaobinqt.cn/TIM%E6%88%AA%E5%9B%BE20181007204842.png)

去[itellyou](https://msdn.itellyou.cn/)下载需要安装的操作系统 !

![image](https://cdn.xiaobinqt.cn/TIM%E6%88%AA%E5%9B%BE20181007205139.png " ")

比如我们要安装这个版本的 win10

![image](https://cdn.xiaobinqt.cn/TIM%E6%88%AA%E5%9B%BE20181007205619.png " ")

通过百度网盘下载 ed2k 文件资源,然后再通过百度网盘下载到电脑本地,可以放在除 C 盘外的其他盘中

![image](https://cdn.xiaobinqt.cn/TIM%E6%88%AA%E5%9B%BE2018100720594sd0.png " ")

下载到本地的文件是这样的光盘映像文件 !

![image](https://cdn.xiaobinqt.cn/TIM%E6%88%AA%E5%9B%BE20181007211023.png " ")

将我们下载到电脑本地的光盘映像文件复制到刚制作完成的 U 盘启动盘中,复制完成后我们 U 盘启动盘就全部制作完成了

![image](https://cdn.xiaobinqt.cn/TIM%E6%88%AA%E5%9B%BE20181007211227.png " ")

## 重做系统

将我们制作好的 U 盘启动盘插到需要重做系统的电脑上,重启电脑一直按 F12 进入 bios 界面(不同的电脑可能按键不同,可以百度)

![image](https://cdn.xiaobinqt.cn/%E5%BE%AE%E4%BF%A1%E5%9B%BE%E7%89%87_20181007214346.jpg " ")

选择 usb 方式,回车进入大白菜启动方式,选择 02 方式进入

![image](https://cdn.xiaobinqt.cn/TIM%E6%88%AA%E5%9B%BE20181007214548.png " ")

进入 u 盘驱动界面,系统默认会选择 C 盘为系统盘,直接点击确定

![image](https://cdn.xiaobinqt.cn/%E5%BE%AE%E4%BF%A1%E5%9B%BE%E7%89%87_20181007214933.jpg " ")

确定后进入格式化 C 盘阶段,所有配置为默认配置,直接确定,等待格式化完成!

![image](https://cdn.xiaobinqt.cn/%E5%BE%AE%E4%BF%A1%E5%9B%BE%E7%89%87_20181007215302.jpg " ")

格式化完成后选择 是 重启电脑,**拔出 u 盘** 等待电脑重启

## 安装系统完成

![image](https://cdn.xiaobinqt.cn/%E5%BE%AE%E4%BF%A1%E5%9B%BE%E7%89%87_20181007215500.jpg " ")

![image](https://cdn.xiaobinqt.cn/%E5%BE%AE%E4%BF%A1%E5%9B%BE%E7%89%87_20181007215505.jpg " ")

## WinNTSetup 使用

最新的大白菜桌面是这样:point_down:

<div align="center"><img src="https://cdn.xiaobinqt.cn/xiaobinqt.io/20230320/533790d147e3404fa9e457357d5aab5f.jpg?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15" width=400  /></div>

可以使用 WinNTSetup 安装纯净版系统。双击 WinNTSetup 进入，选择 windows 安装源为下载的 ISO 镜像，选择引导驱动器和安装驱动器盘符。

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230320/1a6fa186dda6407f86f4a16dcc531484.jpg?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '使用 WinNTSetup')

## 系统激活

1. 进入系统后按 Win+X 键，选择命令提示符（管理员）
2. 复制以下内容并运行

```shell
# 第一步
slmgr.vbs /skms  222.184.9.98

## 第二步
slmgr.vbs /ato 
```



