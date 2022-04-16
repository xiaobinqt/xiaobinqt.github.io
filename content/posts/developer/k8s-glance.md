---
title: "k8s 核心概念"
subtitle: "Kubernetes Core Concepts"

init_date: "2022-04-14T14:40:02+08:00"

date: 2022-04-02

lastmod: 2022-04-14

draft: false

author: "xiaobinqt"
description: "xiaobinqt,Kubernetes 核心概念，什么是 k8s,k8s 自动化容器平台"

featuredImage: ""

reproduce: true

tags: ["k8s"]
categories: ["开发者手册"]
lightgallery: true

toc:
auto: false

math:
enable: true
---

[//]: # (author： xiaobinqt)

[//]: # (email： xiaobinqt@163.com)

[//]: # (https://xiaobinqt.github.io)

[//]: # (https://www.xiaobinqt.cn)

## 什么是 Kubernetes

Kubernetes（k8s）是自动化容器操作的开源平台，这些操作包括部署，调度和节点集群间扩展。

如果你曾经用过 Docker 容器技术部署容器，那么可以将 Docker 看成 Kubernetes 内部使用的低级别组件。Kubernetes 不仅仅支持 Docker，还支持 Rocket，这是另一种容器技术。 使用
Kubernetes 可以：

+ 自动化容器的部署和复制
+ 随时扩展或收缩容器规模
+ 将容器组织成组，并且提供容器间的负载均衡
+ 很容易地升级应用程序容器的新版本
+ 提供容器弹性，如果容器失效就替换它，等等...

实际上，使用 Kubernetes 只需一个部署文件，使用一条命令就可以部署多层容器（前端，后台等）的完整集群：

```shell
kubectl create -f single-config-file.yaml
```

kubectl 是和 Kubernetes API 交互的命令行程序。

## 集群

集群是一组节点，这些节点可以是物理服务器或者虚拟机，之上安装了 Kubernetes 平台。下图展示这样的集群。注意该图为了强调核心概念有所简化。这里可以看到一个典型的 Kubernetes 架构图。

![集群架构](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220414/0ce2d13e9dd3467782c89d74b3c5d9d2.png '集群架构')

上图可以看到如下组件，使用特别的图标表示Service和Label：

+ Pod
+ Container（容器）
+ Label ![label](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220414/3edd10f36368462890623a79905b9f45.png)（标签）
+ Replication Controller（复制控制器）
+ Service ![Service](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220414/2de24a183c174deca2bd5163fcd02588.png)（服务）
+ Node（节点）
+ Kubernetes Master（Kubernetes主节点）

## Pod

Pod（上图绿色方框）安排在节点上，包含一组容器和卷。同一个Pod里的容器共享同一个网络命名空间，可以使用localhost互相通信。Pod是短暂的，不是持续性实体。你可能会有这些问题：

+ 如果Pod是短暂的，那么我怎么才能持久化容器数据使其能够跨重启而存在呢？ 是的，Kubernetes支持卷的概念，因此可以使用持久化的卷类型。
+ 是否手动创建Pod，如果想要创建同一个容器的多份拷贝，需要一个个分别创建出来么？可以手动创建单个Pod，但是也可以使用Replication Controller使用Pod模板创建出多份拷贝，下文会详细介绍。
+ 如果Pod是短暂的，那么重启时IP地址可能会改变，那么怎么才能从前端容器正确可靠地指向后台容器呢？这时可以使用Service，下文会详细介绍。

## Lable

正如图所示，一些Pod有Label（![label](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220414/3edd10f36368462890623a79905b9f45.png)）。一个
Label 是 attach 到 Pod 的一对键/值对，用来传递用户定义的属性。比如，你可能创建了一个“tier”和“app”标签，通过 Label（**tier=frontend , app=myapp**
）来标记前端 Pod 容器，使用 Label（**tier=backend, app=myapp**）标记后台 Pod 。然后可以使用 Selectors 选择带有特定 Label 的 Pod，并且将 Service 或者
Replication Controller 应用到上面。

## Replication Controller

是否手动创建 Pod ，如果想要创建同一个容器的多份拷贝，需要一个个分别创建出来么，能否将 Pods 划到逻辑组里？

Replication Controller 确保任意时间都有指定数量的 Pod “副本”在运行。如果为某个 Pod 创建了 Replication Controller 并且指定3个副本，它会创建 3 个
Pod，并且持续监控它们。如果某个 Pod 不响应，那么 Replication Controller 会替换它，保持总数为3.如下面的动画所示：

![Replication Controller](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220414/03d07039d9fc80c0f692d6176f65936e.gif 'Replication Controller')

如果之前不响应的Pod恢复了，现在就有4个Pod了，那么Replication Controller会将其中一个终止保持总数为3。如果在运行中将副本总数改为5，Replication
Controller会立刻启动2个新Pod，保证总数为5。还可以按照这样的方式缩小Pod，这个特性在执行滚动升级时很有用。

当创建Replication Controller时，需要指定两个东西：

1. Pod模板：用来创建Pod副本的模板

2. Label：Replication Controller需要监控的Pod的标签。

现在已经创建了Pod的一些副本，那么在这些副本上如何均衡负载呢？我们需要的是Service。

## Service

如果Pods是短暂的，那么重启时IP地址可能会改变，怎么才能从前端容器正确可靠地指向后台容器呢？

Service 是定义一系列 Pod 以及访问这些 Pod 的策略的一层抽象。Service 通过 Label 找到 Pod 组。因为 Service 是抽象的，所以在图表里通常看不到它们的存在，这也就让这一概念更难以理解。

现在，假定有 2 个后台 Pod，并且定义后台 Service 的名称为 ‘backend-service’ ，lable 选择器为（**tier=backend, app=myapp**）。backend-service 的
Service 会完成如下两件重要的事情：

+ 会为 Service 创建一个本地集群的DNS入口，因此前端Pod只需要DNS查找主机名为 ‘backend-service’，就能够解析出前端应用程序可用的IP地址。
+ 现在前端已经得到了后台服务的 IP 地址，但是它应该访问 2 个后台Pod的哪一个呢？Service 在这 2 个后台 Pod 之间提供透明的负载均衡，会将请求分发给其中的任意一个（如下面的动画所示）。通过每个 Node
  上运行的代理（kube-proxy）完成。

下述动画展示了 Service 的功能。注意该图作了很多简化。如果不进入网络配置，那么达到透明的负载均衡目标所涉及的底层网络和路由相对先进。

![service](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220414/e7a273fcdc03d2417b354b60c253552f.gif 'service')

有一个特别类型的Kubernetes Service，称为 'LoadBalancer' ，作为外部负载均衡器使用，在一定数量的 Pod 之间均衡流量。比如，对于负载均衡Web流量很有用。

## Node

节点（上图橘色方框）是物理或者虚拟机器，作为Kubernetes worker，通常称为 Minion。每个节点都运行如下 Kubernetes 关键组件：

+ Kubelet：是主节点代理。
+ Kube-proxy：Service 使用其将链接路由到 Pod，如上文所述。
+ Docker 或 Rocket：Kubernetes 使用的容器技术来创建容器。

## Kubernetes Master

集群拥有一个Kubernetes Master（紫色方框）。Kubernetes Master提供集群的独特视角，并且拥有一系列组件，比如Kubernetes API Server。API
Server提供可以用来和集群交互的REST端点。master节点包括用来创建和复制Pod的Replication Controller。

## 参考

+ [十分钟带你理解Kubernetes核心概念](http://www.dockone.io/article/932)





















