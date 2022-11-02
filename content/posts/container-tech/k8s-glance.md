---
title: "kubernetes 笔记"
subtitle: "Kubernetes Core Concepts"

init_date: "2022-04-14T14:40:02+08:00"

date: 2021-10-02

lastmod: 2022-04-14

draft: true

author: "xiaobinqt"
description: "xiaobinqt,Kubernetes 核心概念，什么是 k8s,k8s 自动化容器平台"

featuredImage: ""

reproduce: true

tags: ["k8s"]
categories: ["开发者手册"]
lightgallery: true

toc: true

math: true
---

<!-- author： xiaobinqt -->
<!-- email： xiaobinqt@163.com -->
<!-- https://xiaobinqt.github.io -->
<!-- https://www.xiaobinqt.cn -->


[Kubernetes]^(K8S) 可以为基于容器的应用部署和生产管理打造一套强大并且易用的操作平台。

Kubernetes 为了更好地管理应用的生命周期，将不同资源对象进行了进一步的操作抽象。

Kubernetes中每种对象都拥有一个对应的声明式API。对象包括三大属性：[元数据]^(metadata)、[规范]^(spec)和[状态]^(status)。

当使用 Kubernetes 管理这些对象时，每个对象可以使用一个外部的 json 或 yaml 模板文件来定义，通过参数传递给命令或 API。每个模板文件中定义
apiVersion（如v1）、kind（如Deployment、Service）、metadata（包括名称、标签信息等）、spec（具体的定义）等信息。例如：

```yaml
apiVersion: v1
  kind: Service
  metadata:
    name: nginxsvc
    labels:
      app: nginx
  spec:
    type: NodePort
    ports:
      - port: 80
        protocol: TCP
        name: http
      - port: 443
        protocol: TCP
        name: https
    selector:
      app: nginx
```

![概念](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220512/d87b25b5d51e4e5db0c6ecb1b12d112f.png '概念')

## 资源抽象

基础的操作对象主要是指资源抽象对象，主要包括：

### 容器组

[容器组]^(Pod) 是 Kubernetes 中最小的资源单位。由位于同一节点上**若干容器**组成，彼此共享网络命名空间和[存储卷]^(Volume)。Pod 是 Kubernetes
中进行管理的最小资源单位，是最为基础的概念。

在 Kubernetes中，并不直接操作容器，最小的管理单位是容器组（Pod）。容器组由一个或多个容器组成，Kubernetes围绕容器组进行创建、调度、停止等生命周期管理。

同一个容器组中，各个容器共享命名空间（包括网络、IPC、文件系统等容器支持的命名空间）、cgroups
限制和存储卷。这意味着同一个容器组中，各个应用可以很方便地相互进行访问，比如通过localhost地址进行网络访问，通过信号量和共享内存进行进程间通信等，类似经典场景中运行在同一个操作系统中的一组进程。可以简单地将一个Pod当作是一个抽象的“虚拟机”，里面运行若干个不同的进程（每个进程实际上就是一个容器）。

实现上，是先创建一个`gcr.io/google_containers/pause`容器，创建相关命名空间，然后创建Pod中的其他应用容器，并共享 pause 容器的命名空间。

组成容器组的若干容器往往是存在共同的应用目的，彼此关联十分紧密，例如一个Web应用与对应的日志采集应用、状态监控应用。如果单纯把这些相关的应用放一个容器里面，又会造成过度耦合，管理、升级都不方便。

容器组既保持了容器轻量解耦的特性，又提供了调度操作的便利性，在实践中提供了比单个容器更为灵活和更有意义的抽象。

容器组生命周期包括五种状态值：`待定`、`运行`、`成功`、`失败`、`未知`。

| 状态                               | 说明                         |
|----------------------------------|----------------------------|
| [待定]^(Pending)                   | 已经被系统接受，但容器镜像还未就绪          |
| [运行]^(Running)                   | 分配到节点，所有容器都被创建，至少一个容器在运行中  |
| [成功]^(Succeeded)                 | 所有容器都正常退出，不需要重启，任务完成       |
| [失败]^(Failed)                    | 所有容器都退出，至少一个容器是非正常退出       |
| [未知]^(Unknown)                   | 未知状态，例如所在节点无法汇报状态          |

### 服务

[服务]^(Service)是对外提供某个特定功能的一组 Pod（可通过标签来选择）和所关联的访问配置。由于 Pod 的地址是不同的，而且可能改变，直接访问 Pod 将无法获得稳定的业务。Kubernetes
通过服务提供唯一固定的访问地址（如IP地址或者域名），不随后面 Pod 改变而变化，用户无须关心具体的 Pod 信息。

### 存储卷

[存储卷]^(Volume)类似 Docker 中的概念，提供数据的持久化存储（如 Pod 重启后），并支持更高级的生命周期管理和参数指定功能，支持多种本地和云存储类型。

### 命名空间

[命名空间]^(Namespace)是 Kubernetes 通过命名空间来实现虚拟化，将同一组物理资源虚拟为不同的抽象集群，避免不同租户的资源发生命名冲突，另外可以进行资源限额。

## 控制器抽象

为了方便操作基础对象，Kubernetes 引入了[控制器]^(Controller)的高级抽象概念。这些控制器面向特定场景提供了自动管理 Pod 功能，用户使用控制器而无须关心具体的 Pod 相关细节。控制器抽象对象主要包括：

### 副本集

[副本集]^(ReplicaSet) 在旧版本中叫做[复制控制器]^(ReplicationController)。副本集是一个基于 Pod 的抽象。使用它可以让集群中始终维持某个 Pod 的指定副本数的健康实例。副本集中的 Pod
相互并无差异，可以彼此替换。由于操作相对底层，一般不推荐直接使用。

### 部署

[部署]^(Deployment) 自 1.2.0 版本开始引入。比副本集更高级的抽象，可以管理 Pod 或副本集，并且支持升级操作。部署控制器可以提供提供比副本集更方便的操作，推荐使用。

### 状态集

[状态集]^(StatefulSet) 管理带有状态的应用。相比部署控制器，状态集可以为 Pod 分配独一无二的身份，确保在重新调配等操作时也不会相互替换。自 1.9 版本开始正式支持。

### Daemon集

[Daemon集]^(DaemonSet) 确保节点上肯定运行某个 Pod，一般用来采集日志（如logstash）、监控节点（如collectd）或提供存储（如glusterd）使用。

### 任务

[任务]^(Job) 适用于短期处理场景。任务将创建若干 Pod，并确保给定数目的 Pod 最终正常退出（完成指定的处理）。

### 横向Pod扩展器

[横向Pod扩展器]^(Horizontal Pod Autoscaler, HPA) 类似云里面的自动扩展组，根据 Pod 的使用率（典型如CPU）自动调整一个部署里面 Pod 的个数，保障服务可用性。

### 入口控制器

[入口控制器]^(Ingress Controller) 定义外部访问集群中资源的一组规则，用来提供七层代理和负载均衡服务。

## 其他抽象

| 名称                                  | 说明                                               |
|-------------------------------------|--------------------------------------------------|
| [标签]^(Label)                        | 键值对，可以标记到资源对象上，用来对资源进行分类和筛选                      |
| [选择器]^(Selector)                    | 基于标签概念的一个正则表达式，可通过标签来筛选出一组资源                     |
| [注解]^(Annotation)                   | 键值对，可以存放大量任意数据，一般用来添加对资源对象的详细说明，可供其他工具处理         |
| [秘密数据]^(Secret)                     | 存放敏感数据，例如用户认证的口令等                                |
| [名字]^(Name)                         | 用户提供给资源的别名，同类资源不能重名                              |
| [持久化存储]^(PersistentVolume)          | 确保数据不会丢失                                         |
| [资源限额]^(Resource Quotas)            | 用来限制某个命名空间下对资源的使用，开始逐渐提供多租户支持                    |
| [安全上下文]^(Security Context)          | 应用到容器上的系统安全配置，包括 uid、gid、capabilities、SELinux角色等 |
| [服务账号]^(Service Accounts)           | 操作资源的用户账号                                        |

## 参考

+ [十分钟带你理解Kubernetes核心概念](http://www.dockone.io/article/932)





















