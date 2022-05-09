# slim、stretch、buster、jessie、alpine、debian、ubuntu、centOS、fedora、buildpack-deps


<!-- author： xiaobinqt -->
<!-- email： xiaobinqt@163.com -->
<!-- https://xiaobinqt.github.io -->
<!-- https://www.xiaobinqt.cn -->

## 版本代号

我太难了，搞这么多代号干啥:cry:

在写 Dockerfile 引用基础镜像时经常会看到这样的写法：

```dockerfile
FROM debian:buster
```

或是

```dockerfile
FROM node:14.16.1-stretch-slim
```

那这里的 `buster` 和 `stretch` 具体是什么呢？其实 `buster`、`stretch`还有`jessie`针对的是不同 Debian [代号]^(codename)，除了 Debian 之外，还有
Ubuntu、CentOS、Fedora，他们每次在更新版本时都会更新代号。

### ubuntu 版本代号

![ubuntu版本代号](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220507/e902306343af4eb78a8b04396d2338e8.png 'ubuntu版本代号')

### debian 版本代号

![debian版本代号](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220507/1d34964dde2344738f39c32182e35297.png 'debian版本代号')

## slim

`slim` 可以理解为精简版，跟 `Minimal`是一样的，仅安装运行特定工具所需的最少软件包。

所以`FROM debian:buster` 就是把 debian 10 作为基础镜像，`FROM node:14.16.1-stretch-slim` 就是把 debian 9 的精简版作为基础镜像。

## buildpack-deps

[buildpack-deps](https://hub.docker.com/_/buildpack-deps)  是 docker hub 官方提供的一个镜像工具包，很多 docker
官方的基础镜像都基于此基础镜像进行构建的，buildpack-deps 已经提供了很多内置好的依赖库，可以简化镜像部署，官方也提供了 debian 以及 ubuntu 等的镜像，如 debian
10 `buildpack-deps:buster`，ubuntu 16 `buildpack-deps:xenial` 等。

## 操作系统

`alpine`、`debian`、`ubuntu`、`centOS`、`fedora` 这些都是操作系统，是 Linux 的发行版。

![Linux发行版](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220507/f18e321c61d749359df40c04029e8e5a.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'Linux发行版')

### Alpine

BusyBox 是一个集成了一百多个最常用 Linux 命令和工具（如cat、echo、grep、mount、telnet等）的**精简工具箱**，它只有几MB的大小，被誉为“Linux系统的瑞士军刀”。

Alpine 操作系统是一个面向安全的轻型 Linux 发行版。它不同于通常的 Linux 发行版，Alpine 采用了 musl libc 和 BusyBox 以减小系统的体积和运行时资源消耗，但功能上比 BusyBox
又完善得多。在保持瘦身的同时，Alpine 还提供了自己的包管理工具`apk`
，可以通过 [https://pkgs.alpinelinux.org/packages](https://pkgs.alpinelinux.org/packages) 查询包信息，也可以通过`apk`命令直接查询和安装各种软件。

相比于其他 Docker 镜像，Alpine Docker 的容量非常小，仅仅只有 5MB 左右，而 Ubuntu 系列镜像接近 200MB，且拥有非常友好的包管理机制。

`Alpine` 镜像的缺点就在于它实在**过于精简**，以至于麻雀虽小，也无法做到五脏俱全了。在 `Alpine` 中缺少很多常见的工具和类库，以至于如果想基于 `Alpine`
标签的镜像进行二次构建，那搭建的过程会相当烦琐。所以如果想要对软件镜像进行改造，并基于其构建新的镜像，那么 `Alpine` 镜像不是一个很好的选择。

### Debian

Debian 是由 GPL 和其他自由软件许可协议授权的自由软件组成的操作系统，由 Debian Project 组织维护。Debian 以其坚守 Unix 和自由软件的精神，以及给予用户的众多选择而闻名。

作为一个大的系统组织框架，Debian下面有多种不同操作系统核心的**分支计划**，主要为采用 Linux 核心的 Debian GNU/Linux 系统，其他还有采用 GNU Hurd 核心的 Debian GNU/Hurd 系统、采用
FreeBSD 核心的 Debian GNU/kFreeBSD 系统，以及采用 NetBSD 核心的 Debian GNU/NetBSD 系统，甚至还有利用 Debian 的系统架构和工具，采用 OpenSolaris 核心构建而成的
Nexenta OS 系统。在这些 Debian 系统中，以采用 Linux 核心的 Debian GNU/Linux 最为著名。

众多的 Linux 发行版，例如 Ubuntu、Knoppix 和 Linspire 及 Xandros 等，都基于 Debian GNU/Linux。

### Ubuntu

Ubuntu 是一个以桌面应用为主的 GNU/Linux 操作系统。Ubuntu 基于 Debian 发行版和 GNOME/Unity 桌面环境，与 Debian 的不同在于它每6个月会发布一个新版本，每2年会推出一个长期支持（Long
Term Support，LTS）版本，一般支持3年。

### CentOS

CentOS 是基于 Redhat 的常见 Linux 分支。CentOS 是目前企业级服务器的常用操作系统。

CentOS（Community Enterprise Operating System，社区企业操作系统）是基于 Red Hat Enterprise Linux 源代码编译而成的。由于 CentOS 与 Redhat Linux
源于相同的代码基础，所以很多成本敏感且需要高稳定性的公司就使用 CentOS 来替代商业版 Red Hat Enterprise Linux。CentOS 自身不包含闭源软件。

### Fedora

Fedora 也是基于 Redhat 的常见 Linux分支。Fedora 则主要面向个人桌面用户。

Fedora 是由 Fedora Project 社区开发，红帽公司赞助的 Linux
发行版。它的目标是创建一套新颖、多功能并且自由和开源的操作系统。对用户而言，Fedora是一套功能完备的、可以更新的免费操作系统，而对赞助商 RedHat 而言，它是许多新技术的测试平台，被认为可用的技术最终会加入到 RedHat
Enterprise Linux 中。

## 参考

+ [趣谈形形色色的 Linux 发行版的代号](https://linux.cn/article-7893-1.html)
+ [Docker运行操作系统环境(BusyBox&Alpine&Debian/Ubuntu&CentOS/Fedora)](https://www.cnblogs.com/lovezbs/p/14058250.html)
