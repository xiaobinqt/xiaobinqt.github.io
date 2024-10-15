---
title: "插画版 k8s 概念"
subtitle: ""

init_date: "2022-04-29T17:06:08+08:00"

date: 2022-04-29

lastmod: 2022-04-29

draft: true

author: "xiaobinqt"
description: "xiaobinqt"

featuredImage: ""

featuredImagePreview: "https://cdn.xiaobinqt.cn/xiaobinqt.io/20220430/15df17b2917a4554ade3acdf9a36f693.jpg"

reproduce: false

translate: true

tags: ["k8s"]
categories: ["开发者手册"]
lightgallery: true

toc: false

math:
enable: true
---

<!-- author： xiaobinqt -->
<!-- email： xiaobinqt@163.com -->
<!-- https://xiaobinqt.github.io -->
<!-- https://www.xiaobinqt.cn -->


![图01](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220429/f7ee10bd67824f8b906460bb165b6ba1.jpg "图01")

["I’m bored Aunt Phippy," Zee slouched further down on the couch. "What are we going to do today?"]^(Phippy 阿姨，我好无聊啊。Zee 懒懒的躺在沙发上问，今天我们要做什么?)

[“Why not go see the animals?” said Phippy with a smile. “We’ll go to the zoo!”]^(“为什不去看动物呢? 我们去动物园吧! ”，Phippy 笑着说。)

[“Yeah!” Zee let out a whoop and ran to find some shoes.]^(好的，Zee 边叫着边去找鞋子。)

![图02](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220429/36b0deef329e499cbc304763fdd43f14.jpg '图02')

[The first animals they came upon were the size of squirrels. Furry and blue, each little animal carried a tiny box as they unceasingly zipped back and forth.]^(他们遇到的第一种动物只有松鼠那么大，蓝色的，毛茸茸的，每只小动物都搬运着一只小箱子不停的来回移动。)

[“Those,” said Phippy, “are Pods. All day and all night, they run back and forth carrying their little containers.”]^(Phippy 说，那些就是`Pod`，它们整日整夜，来来回回的搬运这他们的小容器。)

[“Is that all they do, Aunt Phippy?”]^(Phippy，它们就一直做这个吗? )

[“Yup, Zee. For their entire lives, that’s all the Pods do. They run.”]^(是的，Zee，`Pods` 的整个生命周期都是这样的运行。)

![图03](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220429/44fda6bf920c4cae8a0554451c979364.jpg '图03')

[In Kubernetes, Pods are responsible for running your containers.]^(在 Kubernetes 中，`Pods` 的职责就是运行你的容器。) 

[Every Pod holds at least one container, and controls the execution of that container. When the containers exit, the Pod dies too.]^(每个`Pod`至少运行一个容器，并且控制和执行这个容器。当容器退出时，这个`Pod`也销毁了。)

![图04](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220429/638781951dfd4e178a246522e6fc986e.jpg '图04')

[As Phippy and Zee walked on, they saw a large glass enclosure.]^(Phippy 和 Zee 继续在公园里散步，他们看到了一个很大的玻璃围墙。)

[Pressed against the window was a line of happy little meerkat faces. “Those are the ReplicaSets,” said Phippy.]^(一排开心的小猫鼬把脸贴在窗户上。Phippy 说，“那些就是`ReplicaSets`”)

[As Zee watched, the face on the right grinned widely, and tipped itself off the ledge. In unison, the others hopped over to fill the space, and then an identical meerkat scurried up on the left side.]^(当 Zee 在一旁看着的时候，右边的那只猫鼬笑的特别开心，以至于让自己从窗台上摔了下去。于此同时，其他的猫鼬跳过来填补了摔下去的那只猫鼬的位置，左边的位置也跑上了一只一模一样的猫鼬。)

[“Every time one little replica falls, another one hops right up,” explained Phippy.]^(Phippy 解释道：“每次一个`replica`掉下去，另一个就会立刻调上来。”)


![图05](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220429/4bc26c18830245028b463d414581c5f8.jpg '图05')

[A ReplicaSet ensures that a set of identically configured Pods are running at the desired replica count. If a Pod drops off, the ReplicaSet brings a new one online as a replacement.]^(`ReplicaSet`)

![图06](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220429/200b652d782447199dc73651b5ab0789.jpg '图06')

![图07](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220429/889bc11e5c5a4e588ad08f0e8737dfcb.jpg?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15)

![图08](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220429/1345a06a5b4d444c8663b1dfeef3cc88.jpg?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15)

![图09](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220429/998c0a99223a466493aecf04128def70.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15)

![图10](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220429/47c1b2a9315a40d28a585ee5ec667710.jpg?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15)

![图11](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220429/74634b048fb34610829f0e5671174bdb.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15)

![图12](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220429/54517d42c2724ca2acdb7e11e40a43e6.jpg?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15)

![图13](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220429/3f3a2bfdb773407facab918b89eedf27.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15)

![图14](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220429/ddaf8050df8e420e917f72d12d9b6be8.jpg?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15)

![图15](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220429/98b2a7b2f3ea4427972309094277c634.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15)

![图16](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220429/5c3c05ddb23e492eb749d8f863af816a.jpg?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15)

![图17](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220429/5d7f1fa91e3f403e85bdf6b5194cb470.jpg?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15)

![图18](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220429/d2c324b48e954fbc9f2c584cfa6a0c6b.jpg?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15)

![图19](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220429/733d2f6bece641cf889f69fff7840aa8.jpg?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15)

## 原文地址

+ [https://azure.microsoft.com/mediahandler/files/resourcefiles/phippy-goes-to-the-zoo/Phippy%20Goes%20To%20The%20Zoo_MSFTonline.pdf](https://azure.microsoft.com/mediahandler/files/resourcefiles/phippy-goes-to-the-zoo/Phippy%20Goes%20To%20The%20Zoo_MSFTonline.pdf)




