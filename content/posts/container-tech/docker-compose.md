---
title: "Docker Compose 笔记"
subtitle: ""

init_date: "2022-04-28T16:11:22+08:00"

date: 2019-05-21

lastmod: 2022-04-28

draft: false

author: "xiaobinqt"
description: "xiaobinqt,docker compose 使用方法,docker compose 如何映射端口,docker compose 常用命令,dokcer compose 指定镜像,文件挂载,使用数据卷"

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


在日常工作中，经常会碰到需要多个容器相互配合来完成某项任务的情况。例如要实现一个 Web 项目，除了 Web 服务容器本身，往往还需要再加上后端的数据库服务容器，甚至还包括前端的负载均衡容器等。Compose
恰好满足了这样的需求。Compose 定位是**定义和运行多个Docker容器的应用**。

Compose 允许用户通过一个单独的 docker-compose.yml 模板文件（YAML格式）来定义一组相关联的应用容器为一个[服务栈]^(stack)。

Compose中有几个重要的概念：

+ [任务]^(task)：一个容器被称为一个任务。任务拥有独一无二的ID，在同一个服务中的多个任务序号依次递增。
+ [服务]^(service)：某个相同应用镜像的容器副本集合，一个服务可以横向扩展为多个容器实例。
+ [服务栈]^(stack)：由多个服务组成，相互配合完成特定业务，如Web应用服务、数据库服务共同构成Web服务栈，一般由一个docker-compose.yml文件定义。

Compose 的默认管理对象是服务栈，通过子命令对栈中的多个服务进行便捷的生命周期管理。

## 常用命令

| CMD                         | 说明                                                               |
|-----------------------------|------------------------------------------------------------------|
| `docker-compose up`         | 根据 docker-compose.yml 中配置的内容，创建所有的容器、网络、数据卷等等内容，并将它们启动。          |
| `docker-compose down`       | 停止所有的容器，并将它们删除，同时消除网络等配置内容。                                      |
| `docker-compose logs 服务名` | 查看服务日志                                                           |

![常用 compose 命令](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220511/364fd570c3c34f73a782ea8e47b09c82.png '常用 compose 命令')

具体可以参考

+ [https://yeasy.gitbook.io/docker_practice/compose/commands](https://yeasy.gitbook.io/docker_practice/compose/commands)
+ [https://weread.qq.com/web/reader/57f327107162732157facd6kbd432fb02a1bd4c9ab736c3](https://weread.qq.com/web/reader/57f327107162732157facd6kbd432fb02a1bd4c9ab736c3)

`docker-compose` 命令默认会识别当前控制台所在目录内的 docker-compose.yml 文件，会以这个目录的名字作为组装的应用项目的名称。如果需要改变它们，可以通过选项 `-f` 来修改识别的 Docker
Compose 配置文件，通过 `-p` 选项来定义项目名:point_down:。

```shell
docker-compose -f ./compose/docker-compose.yml -p myapp up -d
```

## 配置项

![常见配置项](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220511/fe7bc1c181984359a0212a117b30e28f.png '常见配置项')

具体可以参看

+ [https://yeasy.gitbook.io/docker_practice/compose/compose_file](https://yeasy.gitbook.io/docker_practice/compose/compose_file)

+ [https://weread.qq.com/web/reader/57f327107162732157facd6kb73329202a0b73ce398cadd](https://weread.qq.com/web/reader/57f327107162732157facd6kb73329202a0b73ce398cadd)

## 示例说明

```yaml
version: "3"

services:

  redis:
    image: redis:3.2
    networks:
      - backend
    volumes:
      - ./redis/redis.conf:/etc/redis.conf:ro
    ports:
      - "6379:6379"
    command: [ "redis-server", "/etc/redis.conf" ]

  database:
    image: mysql:5.7
    networks:
      - backend
    volumes:
      - ./mysql/my.cnf:/etc/mysql/my.cnf:ro
      - mysql-data:/var/lib/mysql
    environment:
      - MYSQL_ROOT_PASSWORD=my-secret-pw
    ports:
      - "3306:3306"

  webapp:
    build: ./webapp
    networks:
      - frontend
      - backend
    volumes:
      - ./webapp:/webapp
    depends_on:
      - redis
      - database

  nginx:
    image: nginx:1.12
    networks:
      - frontend
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/conf.d:/etc/nginx/conf.d:ro
      - ./webapp/html:/webapp/html
    depends_on:
      - webapp
    ports:
      - "80:80"
      - "443:443"

networks:
  frontend:
  backend:

volumes:
  mysql-data:
```

:point_up:如上：

+ `version`，这个配置是可选的，代表定义的 docker-compose.yml 文件内容所采用的版本，目前 Docker Compose 的配置文件已经迭代至了第三版。

+ `services` ，是整个 docker-compose.yml 的核心，`services`定义了容器的各项细节。 在 Docker Compose 里不直接体现容器这个概念，而是把 `service`
  作为配置的最小单元。虽然看上去每个 `service` 里的配置内容就像是在配置容器，但其实 `service` 代表的是一个应用集群的配置。

### 定义服务

在使用 docker compose 时，可以为为每个服务定义一个名称，用以区别不同的服务。在这个例子里，`redis`、`database`、`webapp`、`nginx`就是服务的名称。

### 指定镜像

容器最基础的就是镜像，而每个服务必须指定镜像。在 Docker Compose 里，可以通过两种方式为服务指定所采用的镜像。

一种是通过 image 这个配置，给出能在镜像仓库中找到镜像的名称即可。

另外一种指定镜像的方式就是直接采用 Dockerfile 来构建镜像，通过 `build` 这个配置能够定义构建的环境目录，可以通过这种方式指定镜像，Docker Compose 先会帮助我们执行镜像的构建，之后再通过这个镜像启动容器。

在`docker build`里还能通过选项定义许多内容，这些在 Docker Compose 里依然可以:point_down:，我们能够指定更多的镜像构建参数，例如 Dockerfile 的文件名，构建参数等等。

```
  webapp:
    build:
      context: ./webapp
      dockerfile: webapp-dockerfile
      args:
        - JAVA_VERSION=1.6
```

### 依赖声明

如果服务间有非常强的依赖关系，就必须告知 Docker Compose 容器的**先后启动顺序**。只有当被依赖的容器完全启动后，Docker Compose 才会创建和启动这个容器。

定义依赖的方式很简单，在上面的[例子](#配置项)里可以看到，就是 `depends_on` 这个配置项，只需要通过它列出这个服务所有依赖的其他服务即可。在 Docker Compose
为我们启动项目的时候，会检查所有依赖，形成正确的启动顺序并按这个顺序来依次启动容器。

### 文件挂载

Docker Compose 里定义文件挂载的方式与 Docker Engine 里也并没有太多的区别，使用 `volumes` 配置可以像 docker CLI 里的 `-v` 选项一样来指定外部挂载和数据卷挂载。

在上面的[例子](#配置项)里，可以看到几种常用挂载的方式。我们能够直接挂载宿主机文件系统中的目录，也可以通过数据卷的形式挂载内容。

可以直接指定相对目录进行挂载，这里的相对目录是指相对于 docker-compose.yml 文件的目录。

### 使用数据卷

**独立于** `services` 的 `volumes` 配置就是用来声明数据卷的。定义数据卷最简单的方式仅需要提供数据卷的名称。

如果想把属于 Docker Compose 项目以外的数据卷引入进来直接使用，可以将数据卷定义为外部引入，通过 `external` 这个配置就能完成这个定义。

```
volumes:
  mysql-data:
    external: true
```

在加入 `external` 定义后，Docker Compose 在创建项目时不会直接创建数据卷，而是优先从 Docker Engine 中已有的数据卷里寻找并直接采用。

### 端口映射

`ports` 这个配置项，它是用来定义端口映射的。可以利用它进行宿主机与容器端口的映射，这个配置与 docker CLI 中 `-p` 选项的使用方法是近似的。

由于 YAML 格式对 `xx:yy` 这种格式的解析有特殊性，在设置小于 60 的值时，会被当成时间而不是字符串来处理，所以最好**使用引号**将端口映射的定义包裹起来，避免歧义。

## 参考

+ [https://docs.docker.com/compose/](https://docs.docker.com/compose/)
+ [Docker-入门到实践](https://yeasy.gitbook.io/docker_practice/)










