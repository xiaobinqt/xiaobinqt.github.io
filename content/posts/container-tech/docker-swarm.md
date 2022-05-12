---
title: "Docker Swarm 笔记"
subtitle: ""

init_date: "2022-04-28T16:11:59+08:00"

date: 2020-06-14

lastmod: 2022-04-28

draft: false

author: "xiaobinqt"
description: "xiaobinqt,docker swarm"

featuredImage: ""

reproduce: false

tags: ["docker"]
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


[//]: # (![Overlay network]&#40;https://cdn.xiaobinqt.cn/xiaobinqt.io/20220428/982405a94bc347559812099a15aabeb2.png 'Overlay network'&#41;)

作为容器集群管理器，Swarm 最大的优势之一就是原生支持 Docker API。各种基于标准 API 的工具比如 Compose、Docker
SDK、各种管理软件，甚至 Docker 本身等都可以很容易的与 Swarm
进行集成，这大大方便了用户将原先基于单节点的系统移植到 Swarm 上。同时 Swarm 内置了对 Docker 网络插件的支持，这样就可以很容易地**部署跨主机的容器集群服务**。

![主从结构](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220512/a2c6cdd8918444218b889fa03a9a9605.png '主从结构')

Swarm 采用了典型的主从结构，通过 Raft 协议来在多个[管理节点]^(Manager)中实现共识。[工作节点]^(Worker)
上运行 agent 接受管理节点的统一管理和任务分配。用户提交服务请求只需要发给管理节点即可，管理节点会按照调度策略在集群中分配节点来运行服务相关的任务。

## 基本概念

### Swarm集群

Swarm[集群]^(Cluster)为一组被统一管理起来的 Docker 主机。集群是 Swarm 所管理的对象。这些主机通过 Docker 引擎的 Swarm
模式相互沟通，其中部分主机可能作为[管理节点]^(manager)响应外部的管理请求，其他主机作为[工作节点]^(worker)
来实际运行 Docker 容器。同一个主机也可以既作为管理节点，同时作为工作节点。

当使用 Swarm 集群时，首先定义一个服务（指定状态、复制个数、网络、存储、暴露端口等），然后通过管理节点发出启动服务的指令，管理节点随后会按照指定的服务规则进行调度，在集群中启动起来整个服务，并确保它正常运行。

### 节点

[节点]^(Node)是 Swarm 集群的最小资源单位。每个节点实际上都是一台 Docker 主机。Swarm 集群中节点分为两种：

+ [管理节点]^(manager node)：负责响应外部对集群的操作请求，并维持集群中资源，分发任务给工作节点。同时，多个管理节点之间通过Raft协议构成共识。一般推荐每个集群设置5个或7个管理节点。
+ [工作节点]^(worker node)：负责执行管理节点安排的具体任务。默认情况下，管理节点自身也同时是工作节点。每个工作节点上运行代理（agent）来汇报任务完成情况。

可以通过`docker node promote`命令来提升一个工作节点为管理节点；或者通过`docker node demote`命令来将一个管理节点降级为工作节点。

### 服务

一个[服务]^(Service)可以由若干个任务组成，每个任务为某个具体的应用。服务还包括对应的存储、网络、端口映射、副本个数、访问配置、升级配置等附加参数。

一般来说，服务需要面向特定的场景，例如一个典型的 Web 服务可能包括前端应用、后端应用，以及数据库等。这些应用都属于该服务的管理范畴。

Swarm 集群中服务类型也分为两种（可以通过`-mode`指定）：

+ [复制服务]^(replicated services)模式：默认模式，每个任务在集群中会存在若干副本，这些副本会被管理节点按照调度策略分发到集群中的工作节点上。此模式下可以使用`-replicas`参数设置副本数量。

+ [全局服务]^(global services)模式：调度器将在每个可用节点都执行一个相同的任务。该模式适合运行节点的检查，如监控应用等

### 任务

任务是 Swarm 集群中最小的调度单位，即一个指定的应用容器。例如仅仅运行前端业务的前端容器。任务从生命周期上将可能处于[创建]^(NEW)、[等待]^(PENDING)
、[分配]^(ASSIGNED)、[接受]^(ACCEPTED)、[准备]^(PREPARING)、[开始]^(STARTING)、[运行]^(RUNNING)、[完成]^(COMPLETE)、[失败]^(FAILED)
、[关闭]^(SHUTDOWN)、[拒绝]^(REJECTED)、[孤立]^(ORPHANED)等不同状态。

Swarm 集群中的管理节点会按照调度要求将任务分配到工作节点上。例如指定副本为 2 时，可能会被分配到两个不同的工作节点上。一旦当某个任务被分配到一个工作节点，将无法被转移到另外的工作节点，即 Swarm 中的任务不支持迁移。

### 外部访问

Swarm 集群中的服务要被集群外部访问，必须要能允许任务的响应端口映射出来。Swarm 中支持[入口负载均衡]^(ingress load balancing)的映射模式。该模式下，每个服务都会被分配一个[公开端口]^(
PublishedPort)，该端口在集群中任意节点上都可以访问到，并被保留给该服务。

当有请求发送到任意节点的公开端口时，该节点若并没有实际执行服务相关的容器，则会通过路由机制将请求转发给实际执行了服务容器的工作节点。

## 搭建集群

我用 VMWare 搭建了 2 台主机，IP 分别为 `192.168.48.125` 和 `192.168.48.8`，现在将`192.168.48.128`作为管理节点，将`192.168.48.8`作为工作节点。

在集群中，时间同步是很重要，可以使用`ntp`先同步时间。

```shell
yum -y install ntp
systemctl enable ntpd
systemctl start ntpd
```

### 创建集群

```shell
docker swarm init --advertise-addr 192.168.48.125
```

![swarm init](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220512/4dad63ec41c74aa7bb34fc3eb36c2f67.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'swarm init')

**注意**返回的 token 串，这是集群的唯一 id，加入集群的各个节点将需要这个信息。

默认的管理服务端口为 2377，需要能被工作节点访问到；另外，为了支持集群的成员发现和外部服务映射，还需要再所有节点上开启 7946 TCP/UDP 端口和 4789 UDP 端口。

![开发端口](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220512/ae34164603074161b0bd725a3eca796f.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '开发端口')

关于 Centos7.x
开放端口可以参考[https://blog.csdn.net/qq_39007083/article/details/106875997](https://blog.csdn.net/qq_39007083/article/details/106875997)
。

### 加入集群

在所有要加入集群的普通节点上面执行`swarm join`命令，表示把这台机器加入指定集群当中。例如，在`192.168.48.8`工作节点上，将其加入刚创建的集群，则可以通过：

```shell
docker swarm join --token SWMTKN-1-15692f3ho3t3oi68ljnv0fi5nxerox2jsuplmhv0qzerzqpfh1-er9ufvvh4bym5o3iifummtvnf 192.168.48.125:2377
```

![加入集群](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220512/04a42d532f814048aa2b5036d7165e5a.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '加入集群')

此时在管理节点可以看到刚加进来的`192.168.48.8`工作节点：

![工作节点加入成功](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220512/f883196e32e04000a22eebf0297910a9.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '工作节点加入成功')

### 使用集群服务

搭建成功的集群，可以使用使用`docker service`命令使用 Swarm 提供的服务。

可以在管理节点上执行如下命令来快速创建一个应用服务，并制定服务的复制份数为 2。如下命令所示，默认会自动检查确认服务状态都正常：

```shell
docker service create --replicas 2 --name ping_app debian:jessie ping docker.com
```

![docker service create](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220512/7815a5ff32724a86b3933c8a13bef9ba.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'docker service create')

在管理节点上使用 `docker service ls` 可以查看集群中服务情况：

![service ls](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220512/56517c7b0d994d4594268d3ff04bd894.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'service ls')

可以看到，管理节点和工作节点上都运行了一个容器，镜像为`debian:jessie`：

![service ps](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220512/890b1178de3840c0bca1cad2b219bab8.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'service ps')

### 扩展服务

可以通过

```shell
docker service scale <SERVICE-ID>=<NUMBER-OF-TASKS>
```

命令来对服务进行伸缩，例如将服务复制个数从 2 改为 1。

![扩展服务](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220512/8b65b07f8ce74086925f7b81317aad93.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '扩展服务')

### 离开集群

节点可以在任何时候通过`swarm leave`命令离开一个集群。命令格式为`dockerswarm leave [OPTIONS]`，支持`-f`, `--force`意味着强制离开集群。

### 常用命令

Docker 通过 service 命令来管理应用服务，主要包括`create`、`inspect`、`logs`、`ls`、`ps`、`rm`、`rollback`、`scale`、`update`等若干子命令：

![常用命令](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220512/bb88c53985fe4641801deed194fbd823.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '常用命令')

## 参考

+ [Docker Swarm 深入浅出](https://www.wenjiangs.com/docs/docker-swarm-guides)
+ [docker-swarm 节点增加、删除、权限提升、降低、服务部署、配置可视化界面、stack等一系列操作](https://blog.csdn.net/qq_36573407/article/details/121351589)
+ [https://docs.docker.com/engine/swarm/](https://docs.docker.com/engine/swarm/)









