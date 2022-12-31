# Docker 学习笔记


<!-- author： xiaobinqt -->
<!-- email： xiaobinqt@163.com -->
<!-- https://xiaobinqt.github.io -->
<!-- https://www.xiaobinqt.cn -->

## 虚拟化

### 硬件虚拟化

硬件虚拟化，指物理硬件本身就提供虚拟化的支持。

比如，A 平台的 CPU，能够将 B 平台的指令集转换为自身的指令集执行，并给程序完全运行在 B 平台上的感觉。又或者，CPU 能够自身模拟裂变，让程序或者操作系统认为存在多个 CPU，进而能够同时运行多个程序或者操作系统。这些都是硬件虚拟化的体现。

### 软件虚拟化

软件虚拟化指的是通过软件的方式来实现虚拟化中关键的**指令转换部分**。

比如，在软件虚拟化实现中，通过一层夹杂在应用程序和硬件平台上的虚拟化实现软件来进行指令的转换。也就是说，虽然应用程序向操作系统或者物理硬件发出的指令不是当前硬件平台所支持的指令，这个实现虚拟化的软件也会将之转换为当前硬件平台所能识别的。

### 浅析 Docker

可以把容器看作一个简易版的 Linux 系统环境（包括 root 用户权限、进程空间、用户空间和网络空间等）以及运行在其中的应用程序打包而成的[沙盒]^(sandbox)。

每个容器内运行着一个应用，不同的容器相互隔离，容器之间也可以通过网络互相通信。容器的创建和停止十分快速，几乎跟创建和终止原生应用一致；另外，容器自身对系统资源的额外需求也十分有限，远远低于传统虚拟机。很多时候，甚至直接把容器当作应用本身也没有任何问题。

Docker 并没有和虚拟机一样利用一个独立的 OS 执行环境的隔离，它利用的是目前 Linux 内核本身支持的容器方式，实现了资源和环境的隔离。

支撑 docker 的核心技术有三个：`Namespace`，`Cgroup`，`UnionFS`。

`Namespace` 是 2002 年从 Linux 2.4.19 开始出现的，提供了虚拟层面的隔离，比如文件隔离，网络隔离等等。每个命名空间中的应用看到的，都是不同的IP地址，用户空间，进程 ID 等。

`Cgroup`是 2008 年从 Linux 2.6.24 开始出现的，它的全称是 Linux Control Group。提供了物理资源的隔离，比如 CPU，内存，磁盘等等。

`UnionFS` 给 docker 镜像提供了技术支撑。在 Docker 中，提供了一种对 UnionFS 的改进实现，也就是 [AUFS]^(Advanced Union File System)。 AUFS 将文件的更新挂载到老的文件之上，而不去修改那些不更新的内容，这意味着即使虚拟的文件系统被反复修改，也能保证对真实文件系统的空间占用保持一个较低水平。就像在 Git 中每进行一次提交，Git 并不是将我们所有的内容打包成一个版本，而只是将修改的部分进行记录，这样即使我们提交很多次后，代码库的空间占用也不会倍数增加。 通过 AUFS，Docker
**大幅减少了虚拟文件系统对物理存储空间的占用**。

### 虚拟机和 Docker

[虚拟机]^(Virtual Machine)，通常来说就是通过一个[虚拟机监视器]^(Virtual Machine Monitor)
的设施来隔离操作系统与硬件或者应用程序和操作系统，以此达到虚拟化的目的。这个夹在其中的虚拟机监视器，常常被称为
**Hypervisor**。:point_down:是虚拟机和 Docker 的对比：

![虚拟机和容器](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220506/c869ee3cf8d94b20ae793d98e6022afd.png '虚拟机和容器')


[//]: # (![虚拟机和容器]&#40;https://cdn.xiaobinqt.cn/xiaobinqt.io/20220428/2763785408b64bfa92d0263dfd6c6e77.png '虚拟机和容器'&#41;)

传统方式是在硬件层面实现虚拟化，需要有额外的虚拟机管理应用和虚拟机操作系统层。Docker容器是在操作系统层面上实现虚拟化，直接
**复用本地主机的操作系统**，因此更加轻量级。

虚拟机更擅长彻底隔离整个运行环境。例如，云服务提供商通常采用虚拟机技术隔离不同的用户。而 Docker 通常用于隔离不同的应用，例如前端，后端以及数据库。

## 常用命令

![官方架构图](https://cdn.xiaobinqt.cn/xiaobinqt.io/20221231/e5053d518f254d20ac99dc5324bdb51f.png '官方架构图')

| CMD                                    | 说明                                                   |
|----------------------------------------|------------------------------------------------------|
| `sudo docker create --name 容器名称 镜像名称`  | 创建容器                                                 |
| `docker start 名称`                      | 启动容器                                                 |
| `sudo docker run --name 容器名称 -d 镜像名称`  | 创建并启动容器且在后台运行,`-d=--detach`                          |
| `docker ps `                           | 列出**运行中**容器                                          |
| `docker ps -a`                         | 列出所有容器, `-a=--all`                                   |
| `docker stop 容器名称/ID`                  | 停止容器                                                 |
| `docker rm 容器名称/ID`                    | 删除容器                                                 |
| `docker exec -it 容器名称 bash/sh`         | 进入容器                                                 |
| `docker attach --sig-proxy=false 容器名称` | 将容器转为了前台运行，如果不加`--sig-proxy=false` `Ctrl + C` 后会停止容器 |
| `docker logs 容器名称`                     | 查看容器日志                                               |
| `docker network ls/list`               | 查看已经存在的网络                                            |
| `docker network create -d 网络驱动 网络名`    | 创建新网络                                                |
| `docker volume ls`                     | 列出当前已创建的数据卷                                          |
| `docker volume create 名称`              | 创建数据卷                                                |
| `docker volume rm 名称`                  | 删除数据卷                                                |
| `docker volume prune`                  | 删除没有被容器引用的数据卷                                        |
| `docker build`                         | 构建镜像                                                 |
| `docker inspect 容器名/ID`                | 查看容器详情                                               |
| `docker run --privileged`              | 容器获取宿主机root权限                                        |

`docker exec` 命令能帮助我们在正在运行的容器中运行指定的命令。

```shell
docker exec [-i] 容器名 命令

```

![docker exec](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220426/0b8a159e61264e45ae982fcfd8418016.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'docker exec')

`--rm` 选项参数，可以让容器在停止后自动删除，不需要再使用容器删除命令来删除，对临时容器友好:point_down:。

```shell
docker run --rm --name mysql2 -e MYSQL_RANDOM_ROOT_PASSWORD=yes  mysql:5.7
```

```shell
 docker build -t webapp:latest -f ./webapp/a.Dockerfile ./webapp
```

:point_up:`-t` 选项，指定新生成镜像的名称。`-f` 指定 Dockerfile 文件所在目录，如果不写的话会从 `./webapp`
目录中去找，`./webapp` 可以直接写成`.`
理解成当前目录，也是镜像构建的上下文，比如 `COPY`指令执行时就是从这个上下文中去找的。

如果需要禁止缓存可以加上`--no-cache`参数。

```shell
docker build --no-cache  .....
```

### images 子命令

更多子命令选项还可以通过`man docker-images`
来查看，或者查看官方文档 [docker images](https://docs.docker.com/engine/reference/commandline/images/)
。

| 选项                                                        | 说明                                                 |
|-----------------------------------------------------------|----------------------------------------------------|
| <code>-a, &hyphen;&hyphen;all=true &#124; false</code>    | 列出所有（包括临时文件）镜像文件，默认为否                              |
| <code>&hyphen;&hyphen;digests=true &#124; false </code>   | 列出镜像的数字摘要值，默认为否                                    |
| `-f, --filter=[]`                                         | 过滤列出的镜像，如`dangling=true`只显示没有被使用的镜像；也可指定带有特定标注的镜像等 |
| `--format="TEMPLATE"`                                     | 控制输出格式，如`.ID`代表ID信息，`.Repository`代表仓库信息等           |
| <code>&hyphen;&hyphen;no-trunc=true &#124; false </code>  | 对输出结果中太长的部分是否进行截断，如镜像的ID信息，默认为是                    |
| <code>-q, &hyphen;&hyphen;quiet=true &#124; false </code> | 仅输出ID信息，默认为否                                       |

![--format](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220507/68e1884199cf428a981afd09c0b2a2dd.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '--format')

![--filter](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220508/039153bec0674bfea7169d2c4f1325d5.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '--filter')

### create 子命令

create 命令支持的选项都十分复杂，选项主要包括如下几大类：与容器运行模式相关、与容器环境配置相关、与容器资源限制和安全保护相关。

+ :warning:容器运行模式相关的选项

![容器运行模式相关的选项](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220507/33cd51368fe748cfa3537c318f148f0a.png '容器运行模式相关的选项')

+ :warning:容器环境和配置相关的选项

![容器环境和配置相关的选项](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220507/fea604964abd42a3a3c26aa84e320b6d.png '容器环境和配置相关的选项')

+ :warning:容器资源限制和安全保护相关的选项

![容器资源限制和安全保护相关的选项](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220507/e6eb7947b0c44d0cb039e4118a3e03b9.png '容器资源限制和安全保护相关的选项')

### build 子命令

![build 子命令](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220509/92e3455beeb546f6b046fb34936f8020.png 'build 子命令')

## 容器网络

在 Docker 网络中，有三个比较核心的概念，就是：[沙盒]^(Sandbox) 、[网络]^(Network)、[端点]^(Endpoint)。

+ 沙盒提供了容器的虚拟网络栈，也就是端口套接字、IP 路由表、防火墙等内容。实现隔离容器网络与宿主机网络，形成了完全独立的容器网络环境。
+ 网络可以理解为 Docker 内部的虚拟子网，网络内的参与者相互可见并能够进行通讯。Docker 的这种虚拟网络也是于宿主机网络存在隔离关系的，其目的主要是形成容器间的安全通讯环境。
+ 端点是位于容器或网络隔离墙之上的洞，其主要目的是形成一个可以控制的突破封闭的网络环境的出入口。当容器的端点与网络的端点形成配对后，就如同在这两者之间搭建了桥梁，便能够进行数据传输了。

这三者形成了 Docker 网络的核心模型，也就是[容器网络模型]^(Container Network Model)。

![容器网络](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220426/de6fe8d93f6144869b7df7e89bfc88b6.png '容器网络')

Docker 官方提供了五种 Docker 网络驱动：`Bridge Driver`、`Host Driver`、`Overlay Driver`、`MacLan Driver`、`None Driver`。

![网络驱动](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220426/2e40239883264b8fa413bcd39eaf701a.png '网络驱动')

`Bridge` 网络是 Docker 容器的默认网络驱动，通过网桥来实现网络通讯。为容器创建独立的网络命名空间，分配网卡、IP 地址等网络配置，并通过 veth 接口对将容器挂载到一个虚拟网桥（默认为docker0）上。bridge 模式多了虚拟网桥和网卡，通信效率会低一些，但是可以灵活配置应用端口。

<div align="center"> <img src="https://cdn.xiaobinqt.cn/xiaobinqt.io/20221231/92f31a89783a4f8c95abe007d7633f45.png" width="600"/> </div>

`none`为容器创建独立的网络命名空间，但不进行网络配置，即容器内没有创建网卡、IP地址等。允许其他的网络插件来自定义网络连接。

`host`不为容器创建独立的网络命名空间，容器内看到的网络配置（网卡信息、路由表、Iptables 规则等）均与主机上的保持一致。注意其他资源还是与主机隔离的。这种模式没有中间层，相当于去掉了容器的网络隔离，自然通信效率高，但缺少了隔离，运行太多的容器也容易
**导致端口冲突**，比如宿主机和容器不能运行端口相同的应用。

`Overlay` 驱动默认采用 VXLAN 协议，在 **IP 地址可以互相访问**的多个主机之间搭建隧道，让容器可以互相访问，并且让这些容器感觉这个网络与其他类型的网络没有区别。

![Overlay network](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220428/982405a94bc347559812099a15aabeb2.png 'Overlay network')

### 创建网络

在 Docker 中，能够创建自定义网络，形成自己定义虚拟子网的目的。创建网络的命令是 `docker network create`。

```shell
docker network create -d bridge individual
```

通过 `-d` 选项我们可以为新的网络**指定驱动的类型**，其值可以默认的 `bridge`、`host`、`overlay`、`maclan`、`none`
，也可以是其他网络驱动插件所定义的类型。 当不指定网络驱动时，Docker 也会默认采用 `Bridge Driver` 作为网络驱动。

通过 `docker network ls` 或是 `docker network list` 可以查看 Docker 中已经存在的网络。

在创建容器时，可以通过 `--network` 来指定容器所加入的网络，一旦这个参数被指定，容器便不会默认加入到 `bridge`
这个网络中，但是仍然可以通过 `--network bridge` 让其加入。

```shell
docker run -d --name mysql -e MYSQL_RANDOM_ROOT_PASSWORD=yes --network individual mysql:5.7
```

可以通过 `docker inspect 容器名/ID` 观察此时的容器网络。

Docker 中如果两个容器处于不同的网络，之间是不能相互连接引用的。

### 容器互联

要让一个容器连接到另外一个容器，可以在容器通过 `docker create` 或 `docker run` 创建时通过 `--link` 选项进行配置。

例如，创建一个 MySQL 容器，将运行 Web 应用的容器连接到这个 MySQL 容器上，打通两个容器间的网络，实现它们之间的网络互通。

```shell
 docker run -d --name mysql -e MYSQL_RANDOM_ROOT_PASSWORD=yes mysql
 docker run -d --name webapp --link mysql webapp:latest
```

容器间的网络已经打通，如何在 Web 应用中连接到 MySQL 数据库:question:

Docker 为容器间连接提供了一种非常友好的方式，只需要将容器的网络命名（容器名）填入到连接地址中，就可以访问需要连接的容器了。

```shell
mysql:3306
```

在这里，连接地址中的 mysql（容器名） 好比常见的域名解析，Docker 会将其指向 MySQL 容器的 IP 地址。

Docker 在容器互通中带来的一项便利就是，不再需要真实的知道另外一个容器的 IP 地址就能进行连接。在以往的开发中，每切换一个环境（例如将程序从开发环境提交到测试环境），都需要重新配置程序中的各项连接地址等参数，而在 Docker 里，并不需要关心这个，只需要程序中配置被连接容器的名称，映射 IP 的工作就可以交给 Docker。

在 Docker 里还支持连接时使用**别名**来摆脱容器名的限制。

```shell
sudo docker run -d --name webapp --link mysql:database webapp:latest
```

在这里，使用 `--link <name>:<alias>` 的形式，连接到 MySQL 容器，并设置它的别名为 `database`。当我们要在 Web 应用中使用 MySQL 连接时，我们就可以使用 `database`
来代替连接地址了。

```shell
database:3306
```

### 端口映射

容器直接通过 Docker 网络进行的互相访问，在实际使用中，我们需要在容器外通过网络访问容器中的应用。最简单的一个例子，我们提供了 Web 服务，那么我们就需要提供一种方式访问运行在容器中的 Web 应用。

![端口映射](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220428/4b474ffc3f9c468abe6086eb13d43428.png '端口映射')

通过 Docker 端口映射功能，可以把容器的端口映射到宿主操作系统的端口上，当我们从外部访问宿主操作系统的端口时，数据请求就会自动发送给与之关联的容器端口。

要映射端口，可以在创建容器时使用 -p 或者是 --publish 选项。

```shell
docker run -d --name nginx -p 80:80 -p 443:443 nginx:1.12 
```

使用端口映射选项的格式是 `-p <ip>:<host-port>:<container-port>`，其中 ip 是宿主操作系统的监听 ip，可以用来控制监听的网卡，默认为 `0.0.0.0`，即是监听所有网卡。`host-port` 和
`container-port` 分别表示映射到宿主操作系统的端口和容器的端口，这两者是可以不一样的，比如，可以将容器的 80 端口映射到宿主操作系统的 8080 端口，传入 `-p 8080:80` 即可。

## 文件挂载

### Bind Mount

`Bind Mount`能够直接将宿主操作系统中的目录和文件挂载到容器内的文件系统中，通过指定容器外的路径和容器内的路径，就可以形成挂载映射关系，在容器内外对文件的读写，都是相互可见的。

```shell
docker run -d --name nginx -v /webapp/html:/usr/share/nginx/html nginx:1.12
```

使用 `-v` 或 `--volume` 来挂载宿主操作系统目录的形式是 `-v <host-path>:<container-path>`
或 `--volume <host-path>:<container-path>`，其中`host-path` 和 `container-path` 分别代表宿主操作系统中的目录和容器中的目录。这里需要注意的是，Docker 这里强制定义目录时
**必须使用绝对路径，不能使用相对路径**。

Docker 还支持以只读的方式挂载，通过只读方式挂载的目录和文件，只能被容器中的程序读取，但不接受容器中程序修改它们的请求。在挂载选项 `-v`
后再接上 `:ro` 就可以只读挂载了。

```shell
docker run -d --name nginx -v /webapp/html:/usr/share/nginx/html:ro nginx:1.12
```

### Volume

[数据卷]^(Volume)是从宿主操作系统中挂载目录到容器内，只不过这个挂载的目录由 Docker 进行管理，**只需要指定容器内的目录**
，不需要关心具体挂载到了宿主操作系统中的哪里。

可以使用 `-v` 或 `--volume` 选项来定义数据卷的挂载。

```shell
docker run -d --name webapp -v /webapp/storage webapp:latest
```

数据卷挂载到容器后，可以通过 `docker inspect 容器名/ID` 看到容器中数据卷挂载的信息:point_down:。

```json
[
  {
    // ......
    "Mounts": [
      {
        "Type": "volume",
        "Name": "2bbd2719b81fbe030e6f446243386d763ef25879ec82bb60c9be7ef7f3a25336",
        "Source": "/var/lib/docker/volumes/2bbd2719b81fbe030e6f446243386d763ef25879ec82bb60c9be7ef7f3a25336/_data",
        "Destination": "/webapp/storage",
        "Driver": "local",
        "Mode": "",
        "RW": true,
        "Propagation": ""
      }
    ]
    // ......
  }
]
```

`Source` 是 Docker 为我们分配用于挂载的宿主机目录，其位于 Docker 的资源区域，一般默认为 `/var/lib/docker`
。一般并不需要关心这个目录，一切对它的管理都已经在 Docker 内实现了。

为了方便识别数据卷，可以像命名容器一样为数据卷命名，这里的 `Name` 是数据卷的命名，在未给出数据卷命名的时候，Docker 会采用数据卷的 ID 命名数据卷。可以通过 `-v <name>:<container-path>`
这种形式来命名数据卷。

````shell
docker run -d --name webapp -v appdata:/webapp/storage webapp:latest
````

> `-v` 在定义`Bind Mount`时必须使用绝对路径，当不是绝对路径是就是`Volume` 的定义。

### Tmpfs Mount

`Tmpfs Mount`支持挂载系统**内存中**的一部分到容器的文件系统里，不过由于内存和容器的特征，它的存储并不是持久的，其中的内容会随着容器的停止而消失。

挂载临时文件目录要通过 `--tmpfs` 这个选项来完成。由于内存的具体位置不需要指定，在这个选项里只需要传递挂载到容器内的目录即可。

```shell
docker run -d --name webapp --tmpfs /webapp/cache webapp:latest
```

## 镜像版本管理

工作中，当某个镜像不能满足我们的需求时，我们能够将容器内的修改记录下来，保存为一个新的镜像。

### 提交修改生成新镜像

以下以官方的 [nginx:1.12](https://hub.docker.com/layers/nginx/library/nginx/1.12/images/sha256-4037a5562b030fd80ec889bb885405587a52cfef898ffb7402649005dfda75ff?context=explore)
镜像示例，修改后生成一个 nginx-v2 镜像。

先下载镜像:point_down:

```docker
# 下载镜像
docker pull nginx:1.12

# 运行容器

docker run --name mynginx -d nginx:1.12
```

![下载镜像并启动容器](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220428/39577e6404624bfeba82a985652b7103.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '下载镜像并启动容器')

通过 `docker exec` 进入容器，并在 /root 目录下新增 hw.txt 文件，文件内容为 `hello world`：

![添加新文件](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220428/17f756252ad3482480613efb90087efd.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '添加新文件')

将这个改动后的容器保存为新的镜像，`docker commit`提交这次修改，提交容器更新后产生的镜像并没 `REPOSITORY` 和 `TAG`
的内容，也就是说，这个新的镜像还没有名字。可以使用 `docker tag`
给新镜像命名。

![提交修改生成新镜像](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220428/ff0c45e23ed1400487138fcc6c290a78.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '提交修改生成新镜像')

### 存出载入镜像

对于某个镜像我们可以导出成一个 tar 包，也可以将一个 tar 镜像导入到系统中。

`docker save -o` 命令可以将一个镜像导出为 tar 包:point_down:

![导出镜像](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220428/a28fbe578b704a16b618a051838c19e1.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '导出镜像')

可以通过`docker load` 导入一个 tar 包为镜像，以下删除了原有的 nginx-v2 镜像，通过 nginx-v2.tar 成功导入了 nginx-v2 镜像。

![导入镜像](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220428/6843de674516449f85ab8186120c96f4.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '导入镜像')

利用导入的 nginx-v2 镜像启动一个新容器 mynginxv2，在新容器中的 /root 就会有一个 hw.txt 新文件，内容为 `hello world`：

![新镜像](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220428/29efb46165124cbf9eb9fbb668dad3c8.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '新镜像')

## Dockerfile

利用 Dockerfile 文件可以生成镜像，这对于自定义镜像非常优雅，也利于镜像分享，直接分享 Dockerfile 文件就可以了。

### 常用指令

![常用指令](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220509/02c21142855e479a8826db7fcfbd438d.png '常用指令')

> Only the instructions `RUN`, `COPY`, `ADD` create layers. Other instructions create temporary intermediate images, and do not increase the size of the build.

只有 RUN, COPY, ADD 会生成新的镜像层，其它指令只会产生临时层，不影响构建大小。

+ :trophy:`FROM`

通过 `FROM` 指令指定一个基础镜像，接下来所有的指令都是基于这个镜像所展开的。
**为了保证镜像精简，可以选用体积较小的镜像如`Alpine`或`Debian`作为基础镜像**。

`FROM` 指令支持三种形式：

```shell
FROM <image> [AS <name>]
FROM <image>[:<tag>] [AS <name>]
FROM <image>[@<digest>] [AS <name>]
```

Dockerfile 中的第一条指令必须是 `FROM` 指令，因为没有了基础镜像，一切构建过程都无法开展。

+ :trophy:`RUN`

`RUN` 指令用于向控制台发送命令的指令，在 `RUN` 指令之后，我们直接拼接上需要执行的命令，在构建时，Docker 就会执行这些命令，并将它们对文件系统的修改记录下来，形成镜像的变化。

```shell
RUN <command>
RUN ["executable", "param1", "param2"]
```

`RUN` 指令是支持 `\`换行的，如果单行的长度过长，建议对内容进行切割，方便阅读。

+ :trophy:`ENTRYPOINT` 和 `CMD`

在容器启动时会根据镜像所定义的一条命令来启动容器中进程号为 1 的进程。而这个命令的定义，就是通过 Dockerfile 中的 `ENTRYPOINT` 和 `CMD` 实现的。

```shell
ENTRYPOINT ["executable", "param1", "param2"]
ENTRYPOINT command param1 param2

CMD ["executable","param1","param2"]
CMD ["param1","param2"]
CMD command param1 param2
```

当 `ENTRYPOINT` 与 `CMD` 同时给出时，`CMD` 中的内容会作为 `ENTRYPOINT` 定义命令的参数，最终执行容器启动的还是 `ENTRYPOINT`
中给出的命令。

+ :trophy:`EXPOSE`

通过 EXPOSE 指令就可以为镜像指定要暴露的端口。

```shell
EXPOSE <port>
```

+ :trophy:VOLUME

```shell
VOLUME ["/data"]
```

在 `VOLUME` 指令中定义的目录，在基于新镜像创建容器时，会自动建立为数据卷，不需要再单独使用 `-v` 选项来配置。

+ :trophy:`LABEL`

`LABEL`指令可以为生成的镜像添加元数据标签信息。这些信息可以用来辅助过滤出特定镜像。格式为：

```shell
LABEL <key>=<value> 

LABEL version=1.2
```

+ :trophy: COPY 和 ADD

在制作新的镜像的时候，可能需要将一些软件配置、程序代码、执行脚本等直接导入到镜像内的文件系统里，使用 `COPY` 或 `ADD`
指令能够帮助我们直接从宿主机的文件系统里拷贝内容到镜像里的文件系统中。

```shell
COPY [--chown=<user>:<group>] <src>... <dest>
ADD [--chown=<user>:<group>] <src>... <dest>

COPY [--chown=<user>:<group>] ["<src>",... "<dest>"]
ADD [--chown=<user>:<group>] ["<src>",... "<dest>"]
```

`COPY` 与 `ADD` 指令的定义方式完全一样，需要注意的仅是当我们的目录中存在空格时，可以使用后两种格式避免空格产生歧义。

### ARG 参数

在 Dockerfile 里，可以用 `ARG` 指令来建立一个参数变量，可以在构建时通过构建指令传入这个参数变量，并且在 Dockerfile 里使用它。

```shell
FROM debian:stretch-slim

## ......

ARG TOMCAT_MAJOR
ARG TOMCAT_VERSION

## ......

RUN wget -O tomcat.tar.gz "https://www.apache.org/dyn/closer.cgi?action=download&filename=tomcat/tomcat-$TOMCAT_MAJOR/v$TOMCAT_VERSION/bin/apache-tomcat-$TOMCAT_VERSION.tar.gz"

## ......

```

在:point_up:这个例子里，我们将 Tomcat 的版本号通过 `ARG` 指令定义为参数变量，在调用下载 Tomcat 包时，使用变量替换掉下载地址中的版本号。通过这样的定义，就可以让我们在不对 Dockerfile 进行大幅修改的前提下，轻松实现对 Tomcat 版本的切换并重新构建镜像了。

如果我们需要通过这个 Dockerfile 文件构建 Tomcat 镜像，我们可以在构建时通过 docker build 的 `--build-arg` 选项来设置参数变量。

Docker**内置**了一些镜像创建变量，用户可以直接使用而无须声明，包括（不区分大小写）`HTTP_PROXY`、`HTTPS_PROXY`、`FTP_PROXY`
、`NO_PROXY`。

```shell
docker build --build-arg TOMCAT_MAJOR=8 --build-arg TOMCAT_VERSION=8.0.53 -t tomcat:8.0 ./tomcat
```

### ENV 参数

ENV 环境变量设置的实质，其实就是定义操作系统环境变量，所以在运行的容器里，一样拥有这些变量，而容器中运行的程序也能够得到这些变量的值。

```shell
FROM debian:stretch-slim

## ......

ENV TOMCAT_MAJOR 8
ENV TOMCAT_VERSION 8.0.53

## ......

```

环境变量的值不是在构建指令中传入的，而是在 Dockerfile 中编写。由于环境变量在容器运行时依然有效，所以运行容器时我们也可以对其进行覆盖，在创建容器时使用 `-e` 或是 `--env`
选项，可以对环境变量的值进行修改或定义新的环境变量。

```shell
docker run -e MYSQL_ROOT_PASSWORD=my-secret-pw -d mysql:5.7
```

**ENV 指令所定义的变量，永远会覆盖 ARG 所定义的变量**。

## FAQ

### CMD 指令

CMD指令用来指定启动容器时默认执行的命令。支持三种格式：

+ `CMD ["executable", "param1", "param2"]`：相当于执行 `executable param1 param2`，推荐方式。

+ `CMD command param1 param2`：在默认的 Shell 中执行，提供给需要交互的应用。

+ `CMD ["param1", "param2"]`：提供给 ENTRYPOINT 的默认参数。

每个 Dockerfile 只能有一条 CMD 命令。如果指定了多条命令，只有最后一条会被执行。

### ENTRYPOINT 和 CMD 的区别

这 2 个命令都是用来指定基于此镜像所创建容器里主进程的启动命令。

`ENTRYPOINT` 指令的**优先级高于** `CMD` 指令。当 `ENTRYPOINT` 和 `CMD` 同时在镜像中被指定时，`CMD`
里的内容会作为 `ENTRYPOINT` 的参数，两者拼接之后，才是最终执行的命令。

| ENTRYPOINT                       | CMD                         | 实际执行                                                |
|----------------------------------|-----------------------------|-----------------------------------------------------|
| `ENTRYPOINT ["/bin/ep", "arge"]` | 	                           | `/bin/ep arge`                                      |
| `ENTRYPOINT /bin/ep arge`        | 	                           | `/bin/sh -c /bin/ep arge`                           |
| `CMD ["/bin/exec", "args"]`      | `/bin/exec args`            |                                                     |
| `CMD /bin/exec args`             | `/bin/sh -c /bin/exec args` |                                                     |
| `ENTRYPOINT ["/bin/ep", "arge"]` | `CMD ["/bin/exec", "argc"]` | `/bin/ep arge /bin/exec argc`                       |
| `ENTRYPOINT ["/bin/ep", "arge"]` | `CMD /bin/exec args`        | `/bin/ep arge /bin/sh -c /bin/exec args`            |
| `ENTRYPOINT /bin/ep arge`        | `CMD ["/bin/exec", "argc"]` | `/bin/sh -c /bin/ep arge /bin/exec argc`            |
| `ENTRYPOINT /bin/ep arge`        | `CMD /bin/exec args`        | `/bin/sh -c /bin/ep arge /bin/sh -c /bin/exec args` |

`ENTRYPOINT` 指令主要用于对容器进行一些初始化，而 `CMD` 指令则用于真正定义容器中主程序的启动命令。

创建容器时可以改写容器主程序的启动命令，而这个覆盖只会覆盖 `CMD` 中定义的内容，不会影响 `ENTRYPOINT` 中的内容。

每个 Dockerfile 中只能有一个`ENTRYPOINT`，当指定多个时，只有最后一个起效。在运行时，可以被`--entrypoint`
参数覆盖掉，如`docker run --entrypoint`。

> 使用脚本文件来作为 `ENTRYPOINT` 的内容是常见的做法，因为对容器运行初始化的命令相对较多，全部直接放置在 `ENTRYPOINT`
> 后会特别复杂。

### COPY 和 ADD 的区别

```shell
COPY [--chown=<user>:<group>] <src>... <dest>
ADD [--chown=<user>:<group>] <src>... <dest>

COPY [--chown=<user>:<group>] ["<src>",... "<dest>"]
ADD [--chown=<user>:<group>] ["<src>",... "<dest>"]
```

两者的区别主要在于 `ADD` 能够支持使用网络端的 URL 地址作为 src 源，并且在源文件被识别为压缩包时，自动进行解压，而 `COPY`
没有这两个能力。

当使用本地目录为源目录时，推荐使用 `COPY`。

### 写时复制

在编程里，[写时复制]^(Copy on Write)
常常用于对象或数组的拷贝中，当拷贝对象或数组时，复制的过程并不是马上发生在内存中，而只是先让两个变量同时指向同一个内存空间，并进行一些标记，当要对对象或数组进行修改时，才真正进行内存的拷贝。

Docker 的写时复制与编程中的相类似，在通过镜像运行容器时，并不是马上就把镜像里的所有内容拷贝到容器所运行的沙盒文件系统中，而是利用 UnionFS 将镜像以只读的方式挂载到沙盒文件系统中。只有在容器中发生对文件的修改时，修改才会体现到沙盒环境上。 也就是说，容器在创建和启动的过程中，不需要进行任何的文件系统复制操作，也不需要为容器单独开辟大量的硬盘空间，与其他虚拟化方式对这个过程的操作进行对比，Docker 启动的速度可见一斑。

采用写时复制机制来设计的 Docker，既保证了镜像在生成为容器时，以及容器在运行过程中，不会对自身造成修改。又借助剔除常见虚拟化在初始化时需要从镜像中拷贝整个文件系统的过程，大幅提高了容器的创建和启动速度。可以说，Docker 容器能够实现秒级启动速度，写时复制机制在其中发挥了举足轻重的作用。

### docker save、export 区别

`docker save` 和 `docker load` 是对镜像的操作，导入导出的是镜像文件。

`docker export` 和 `docker import`是对容器的操作，是导出导入容器，导出一个已经创建的容器到一个文件，不管此时这个容器是否处于运行状态，可以理解为容器快照。

容器快照文件将丢弃所有的历史记录和元数据信息（即仅保存容器当时的快照状态，如标签信息会被丢弃），而镜像存储文件将保存完整记录，体积更大。从容器快照文件导入时可以重新指定标签等元数据信息。

### -v 和 --mount 的区别

使用`-v`时，如果宿主机上没有这个文件，也会自动创建，如果使用`--mount`时，宿主机中没有这个文件会报错找不到这个文件，并创建失败。

`--mount`由多个键-值对组成，以逗号分隔，每个键-值对由一个`<key>=<value>`元组组成。`--mount`语法比`-v`或`--volume`更冗长，但是键的顺序并不重要，标记的值也更容易理解。 挂载的类型`type`，可以是`bind`、`volume`或者`tmpfs`。

### 镜像里的层都是只读不可修改的，但容器运行的时候经常会写入数据，这个冲突应该怎么解决

<div align="center"> <img src="https://cdn.xiaobinqt.cn/xiaobinqt.io/20221231/1f2e25d662f84aefa3599f6f4d20b843.png" width="600"/> </div>

Docker 采用 UNION FS 文件系统，将文件系统分为上层和下层。即上层为容器层，下层为镜像层。如果下层有修改，运行容器时，上层会同步修改。如果上层有数据修改（即容器层数据修改），不会影响到下层（即镜像层）。

## 参考

+ [Docker技术入门与实战(第三版)](https://book.douban.com/subject/30329430/)
+ [对比Docker和虚拟机 ](https://www.cnblogs.com/zhangcz/p/15089684.html)
+ [开发者必备的 Docker 实践指南](https://juejin.cn/book/6844733746462064654)
+ [Docker 基础知识 - 使用绑定挂载(bind mounts)管理应用程序数据](https://www.cnblogs.com/ittranslator/p/13352727.html)
+ [php 中文网 docker](https://www.php.cn/docker/)
+ [Dockerfile reference](https://docs.docker.com/engine/reference/builder/)
