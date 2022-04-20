---
title: "mysql workbench 查看触发器"
subtitle: "How SHOW Triggers in Mysql Workbench"

init_date: "2022-04-20T14:53:14+08:00"

date: 2022-04-20

lastmod: 2022-04-20

draft: false

author: "xiaobinqt"
description: "xiaobinqt,mysql workbench 查看 Triggers 触发器"

featuredImage: ""

reproduce: false

tags: ["mysql"]
categories: ["mysql"]
lightgallery: true

toc: false

math:
enable: true
---

<!-- author： xiaobinqt -->
<!-- email： xiaobinqt@163.com -->
<!-- https://xiaobinqt.github.io -->
<!-- https://www.xiaobinqt.cn -->


mysql [workbench](https://dev.mysql.com/downloads/workbench/) 是官方推荐的数据库工具，用了很长时间却一直不知道触发器在哪儿:cry:。

触发器是对单个表的操作，而不是整个数据库的操作，所以 `Alter Table `就可以看到触发器：

![图1](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220420/795d688e27b34d9d8f7b512a99721148.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '图1')

![图2](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220420/f3c5261baeba4b99abf32e5ad9411cc3.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '图2')

点这个扳手图标也可以看到触发器，跟 `Alter Table `效果一样：

![图3](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220420/ac8c3ed5178346a59c61a187b398ef0b.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '图3')

## 参考

+ [MySQL Workbench : How to Configure Triggers in MySQL](https://www.youtube.com/watch?v=X8o0gETy-OQ)
