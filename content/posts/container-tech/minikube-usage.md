---
title: "minikube 安装使用"
subtitle: ""

init_date: "2022-12-31T22:06:08+08:00"

date: 2022-12-31

lastmod: 2022-12-31

draft: false

author: "xiaobinqt"
description: "xiaobinqt,minikube 安装使用，如何使用 minikube 安装 k8s 环境,debian11 安装 Docker"

featuredImage: ""

featuredImagePreview: "https://cdn.xiaobinqt.cn/xiaobinqt.io/20230128/3cce82b4c8ec479aa27d81f4d0388055.png"

reproduce: false

translate: false

tags: ["k8s"]
categories: ["开发者手册"]
lightgallery: true

series: []

series_weight:

toc: true

math: true
---

<!-- author： xiaobinqt -->
<!-- email： xiaobinqt@163.com -->
<!-- https://xiaobinqt.github.io -->
<!-- https://www.xiaobinqt.cn -->

## 简介

Kubernetes 是一个生产级别的容器编排平台和集群管理系统，不仅能够创建、调度容器，还能够监控、管理服务器，它凝聚了 Google 等大公司和开源社区的集体智慧，从而让中小型公司也可以具备轻松运维海量计算节点，也就是 “云计算” 的能力。

minikube 是一个 “迷你” 版本的 Kubernetes，自从 2016 年发布以来一直在积极地开发维护，紧跟 Kubernetes 的版本更新，同时也兼容较旧的版本（最多可以到之前的 6 个小版本）。

minikube 最大特点就是 “小而美”，可执行文件仅有不到 100MB，运行镜像也不过 1GB。minikube 集成了 Kubernetes 的绝大多数功能特性，不仅有核心的容器编排功能，还有丰富的插件，例如 Dashboard、GPU、Ingress、Istio、Kong、Registry 等。

## 安装 Docker

我的系统是 debian 11，**本文所有的操作都是在 debian 11 的环境下进行**。

![系统版本](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230117/1ce3091edf2d4b63933d4d5d7938fd5c.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '系统版本')

Docker 的安装可以参考官网 [Install Docker Engine on Debian](https://docs.docker.com/engine/install/debian/)，其他系统的安装方式都可以在官网找到。debian 11 的安装步骤大致如下。

```shell
apt-get remove docker docker-engine docker.io containerd runc # 卸载旧版本

apt-get update

apt-get install \
  ca-certificates \
  curl \
  gnupg \
  lsb-release

mkdir -p /etc/apt/keyrings

curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list >/dev/null

apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin

```

## 安装 minikube

可以去官网 [https://minikube.sigs.k8s.io/docs/start/](https://minikube.sigs.k8s.io/docs/start/) 下载对应的版本。

![下载](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230117/a7572d5e517e45758a4822e28602502b.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '下载地址')

```shell
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64

install minikube-linux-amd64 /usr/local/bin/minikube
```

![下载并安装](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230117/e285a6927b944c0296c175a192f143d7.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '下载并安装 minikube')

## 安装 kubectl

minikube 只能够搭建 Kubernetes 环境，要操作 Kubernetes，还需要另一个专门的客户端工具 kubectl。

kubectl 是一个命令行工具，通过它可以与 Kubernetes 后台服务通信，把我们的命令转发给 Kubernetes，实现容器和集群的管理功能。

kubectl 是一个与 Kubernetes、minikube 彼此独立的项目，不包含在 minikube 里，但 minikube 提供了安装它的简化方式，只需执行下面的这条命令：

```shell
minikube kubectl
```

![下载 kubectl](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230117/ae06b019feba415092522d5887a34c0b.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '下载 kubectl')

以上这条命令会把与当前 Kubernetes 版本匹配的 kubectl 下载下来，存放在内部目录（例如`.minikube/cache/linux/amd64/v1.23.3`），然后就可以使用它来操作 Kubernetes 了。

在 minikube 环境里会用到两个客户端，minikube 管理 Kubernetes 集群环境，kubectl 操作实际的 Kubernetes 功能。

## 启动环境

安装了 minikube 和 kubectl 就可以在本机上运行 minikube，创建 Kubernetes 实验环境了。

最好先关闭 swap 分区，不然会 WARNING 提示：

> swap is enabled; production deployments should disable swap unless testing the NodeSwap feature gate of the kubelet

```shell
# 关闭 swap分区
swapoff -a
```

使用命令 minikube start 会从 Docker Hub 上拉取镜像，以当前最新版本的 Kubernetes 启动集群，也可以在后面再加上一个参数`--kubernetes-version` 明确指定要使用 Kubernetes 版本。这里使用 “1.23.3”，启动命令是：

```shell
minikube start --kubernetes-version=v1.23.3

```

如果出现类似以下的问题：

```shell
* minikube v1.28.0 on Centos 7.9.2009 (lxc/amd64)
* Automatically selected the docker driver. Other choices: none, ssh
* The "docker" driver should not be used with root privileges. If you wish to continue as root, use --force.
* If you are running minikube within a VM, consider using --driver=none:
*   https://minikube.sigs.k8s.io/docs/reference/drivers/none/

X Exiting due to DRV_AS_ROOT: The "docker" driver should not be used with root privileges.
```

可以使用加上 `--force`

```shell
minikube start --kubernetes-version=v1.23.3 --force
```

国内网络环境复杂，一般访问外网比较慢，也可以使用加上`--image-mirror-country='cn'`参数：

```shell
minikube start --image-mirror-country='cn' --kubernetes-version=v1.23.3 --force

```

![minikube start](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230117/756c1c2c48154d44aedd334ad6d5fe41.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'minikube start')

## 简单使用

minikube 自带的 kubectl 有一点限制，必须要在前面加上 minikube 的前缀，后面再加上 `--` 才能使用，像这样：

```shell
minikube kubectl -- version
```

![kubectl version](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230117/6d9652c6330c4cd888416362c9087f12.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'kubectl version')

我们在 Kubernetes 里运行一个 Nginx 应用，命令与 Docker 类似，也是 run，但是需要用`--image`指定镜像，然后 Kubernetes 会自动拉取镜像并运行：

```shell
minikube kubectl -- run ngx --image=nginx:alpine
```

![运行应用](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230117/caec80f930f94095832101c5bd351122.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '运行应用')

命令执行之后可以看到，在 Kubernetes 集群里就有了一个名字叫 ngx 的 Pod 正在运行，表示这个单节点 minikube 环境已经搭建成功。

## 什么是容器编排

容器，是现代程序的运行方式。编排就是部署、管理应用程序的系统，能动态地响应变化，如：回滚、滚动升级、故障自愈、自动扩缩容。自动完成这些所有任务，需要人工最初进行一些配置，就可以一劳永逸。所以，运行容器形式的应用程序，这些应用程序的构建方式，使它们能够实现回滚、滚动升级、故障自愈、自动扩缩容等就是容器编排。

## K8s 和 Docker 的区别

Docker 应用打包、测试、交付，Kubernetes 是基于 Docker 的产物，进行编排、运行。例如有 1 个集群，3 个节点。这些节点，都以 Docker 作为容器运行时，Docker 是更偏向底层的技术。Kubernetes 更偏向上层的技术 ，它实现了对容器运行时的抽象，抽象的目的是兼容底层容器运行时（容器进行时技术不仅有 Docker，还有 containerd、kata 等，无论哪种容器运行时，Kubernetes 层面的操作都是一样的）以及解耦，同时还提供了一套容器运行时的标准。抽象的产物是容器运行时接口 CRI（Container Runtime Interface）。

## 参考

+ [minikube start](https://minikube.sigs.k8s.io/docs/start/)
+ [docker docs](https://docs.docker.com/engine/install/debian/)
