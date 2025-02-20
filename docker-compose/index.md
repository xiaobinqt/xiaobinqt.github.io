# Docker Compose 笔记


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

| 命令                                        | 描述                    | 示例                                          |
|-------------------------------------------|-----------------------|---------------------------------------------|
| `docker-compose up`                       | 启动所有服务（在前台运行）         | `docker-compose up`                         |
| `docker-compose up -d`                    | 启动所有服务（在后台运行）         | `docker-compose up -d`                      |
| `docker-compose down`                     | 停止并删除所有容器、网络和挂载卷      | `docker-compose down`                       |
| `docker-compose down -v`                  | 停止并删除所有容器、网络、挂载卷以及数据卷 | `docker-compose down -v`                    |
| `docker-compose start`                    | 启动已存在的容器              | `docker-compose start`                      |
| `docker-compose stop`                     | 停止正在运行的容器             | `docker-compose stop`                       |
| `docker-compose restart`                  | 重启所有服务                | `docker-compose restart`                    |
| `docker-compose ps`                       | 列出所有容器的状态             | `docker-compose ps`                         |
| `docker-compose logs`                     | 查看所有容器的日志             | `docker-compose logs`                       |
| `docker-compose logs <service>`           | 查看指定服务的日志             | `docker-compose logs web`                   |
| `docker-compose build`                    | 构建或重新构建服务的镜像          | `docker-compose build`                      |
| `docker-compose exec <service> <command>` | 在指定服务中执行命令            | `docker-compose exec web bash`              |
| `docker-compose pull`                     | 拉取服务所需的镜像             | `docker-compose pull`                       |
| `docker-compose config`                   | 验证和查看 Compose 文件的配置   | `docker-compose config`                     |
| `docker-compose scale <service>=<num>`    | 扩展指定服务的容器数量           | `docker-compose scale web=3`                |
| `docker-compose top`                      | 显示正在运行的进程             | `docker-compose top`                        |
| `docker-compose pause`                    | 暂停所有服务                | `docker-compose pause`                      |
| `docker-compose unpause`                  | 恢复所有服务                | `docker-compose unpause`                    |
| `docker-compose rm`                       | 删除已停止的容器              | `docker-compose rm`                         |
| `docker-compose run <service> <command>`  | 在指定服务上运行一次性命令         | `docker-compose run web echo "Hello World"` |
| `docker-compose port <service> <port>`    | 查看指定服务绑定的公共端口         | `docker-compose port web 80`                |
| `docker-compose images`                   | 列出所有服务使用的镜像           | `docker-compose images`                     |
| `docker-compose kill`                     | 强制停止容器                | `docker-compose kill`                       |
| `docker-compose events`                   | 实时查看容器事件              | `docker-compose events`                     |

这些命令涵盖了大多数常见的 Docker Compose 操作，可以帮助你有效地管理和调试你的容器化服务。

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

## 数据卷和文件挂载的区别

在 Docker 中，**数据卷（Volumes）和文件挂载（Bind Mounts）** 都用于将容器中的数据持久化或与主机系统共享，但是它们有一些关键的区别：

| 特性        | 数据卷（Volumes）                                      | 文件挂载（Bind Mounts）                         |
|-----------|---------------------------------------------------|-------------------------------------------|
| **定义**    | 数据卷是由 Docker 管理的数据存储位置，通常存储在 Docker 主机的特定目录中。     | 文件挂载是将主机文件系统中的某个文件或目录直接挂载到容器内部。           |
| **位置**    | 存储在 Docker 管理的目录（通常是 `/var/lib/docker/volumes/`）。 | 存储在主机文件系统的任何路径上，可以是任何主机目录。                |
| **管理**    | 由 Docker 管理，Docker 会自动处理数据的存储和权限。                 | 由操作系统和用户管理，Docker 不管理主机文件系统的挂载。           |
| **性能**    | 适用于需要高性能的场景，因为它是经过 Docker 优化的。                    | 可能会受到主机文件系统性能的影响，尤其是当挂载的文件或目录较多时。         |
| **生命周期**  | 数据卷的生命周期与容器的生命周期无关，可以在多个容器之间共享数据。                 | 文件挂载的生命周期与主机文件系统和挂载的容器有关，可以随容器的启动和停止进行管理。 |
| **访问权限**  | 数据卷权限由 Docker 控制，并且通常比文件挂载更安全。                    | 文件挂载依赖于主机文件系统的权限，可能会涉及到不必要的权限问题。          |
| **适用场景**  | 用于容器内的持久化数据存储，尤其是数据库等应用程序的数据。                     | 用于开发、调试或在容器与主机文件系统之间共享文件。                 |
| **备份和迁移** | 数据卷易于备份和迁移，可以通过 `docker volume` 命令进行管理。           | 文件挂载通过复制文件或目录的方式进行备份或迁移。                  |

数据卷，更适合在生产环境中持久化数据，尤其是数据库等应用的数据，Docker 完全管理，具备高效的性能。文件挂载，更适合在开发环境中与主机文件系统共享文件或进行调试。

1. **存储位置**：

- 数据卷（Volumes）：由 Docker 自动管理，**默认**存储在 Docker 主机的 `/var/lib/docker/volumes/` 目录中，但这个**路径对用户不可见**，用户通常不需要直接访问它。
- 文件挂载（Bind Mounts）：直接映射主机文件系统上的某个路径到容器。可以是任何主机路径，用户可以选择共享的文件或目录。

2. **数据管理**：

- **数据卷（Volumes）**：由 Docker 管理，不直接暴露给主机操作系统，提供了较高的隔离性。可以使用 Docker 命令（如 `docker volume`）进行管理、备份、恢复等操作。
- **文件挂载（Bind Mounts）**：与主机文件系统直接交互，容器内对该目录或文件的修改也会直接反映到主机文件系统中。

3. **权限控制**：

- **数据卷（Volumes）**：容器的权限由 Docker 控制，通常不会受到主机文件系统权限问题的影响。Docker 会在后台自动管理卷的权限。
- **文件挂载（Bind Mounts）**：依赖于主机文件系统的权限，可能会遇到权限问题（如主机与容器之间的权限不匹配）。

4. **性能**：

- **数据卷（Volumes）**：通常能提供更好的性能，因为 Docker 在管理数据卷时进行了优化，尤其是在写入和读取数据时。
- **文件挂载（Bind Mounts）**：性能会受到主机文件系统的限制，特别是在高并发访问时，可能导致性能下降。

5. **用途**：

- **数据卷（Volumes）**：更适用于持久化存储，例如数据库、日志文件等，尤其是在需要容器跨多个主机或容器之间共享数据时。
- **文件挂载（Bind Mounts）**：适用于开发环境，通常用于将主机上的代码或配置文件共享到容器中。也常用于调试时查看容器内部的文件或与主机系统之间的同步。

### 举例

- 数据卷（Volumes）： 在 `docker-compose.yml` 中使用数据卷进行持久化：

  ```yaml
  volumes:
    my_volume:
  services:
    web:
      image: nginx
      volumes:
        - my_volume:/data
  ```

- 文件挂载（Bind Mounts）： 在 `docker-compose.yml` 中使用文件挂载：

  ```yaml
  services:
    web:
      image: nginx
      volumes:
        - /path/on/host:/path/in/container
  ```

Docker Compose 会使用当前目录名作为项目名来生成卷的名称。

假设你当前的工作目录是 test。Docker Compose 会将该目录名作为项目名，生成一个卷名为 `<项目名>_<卷名>`，即 test_my_volume。

或者可以更简单粗暴的认为，volumes 是没有路径的，那一般都是数据卷，如果有路径，比如 /path/on/host，那一般都是文件夹挂载。

### docker volume 常用命令

以下是一些常用的 Docker 数据卷（`docker volume`）命令，帮助你管理 Docker 数据卷：

| **命令**                                                   | **说明**                         |
|----------------------------------------------------------|--------------------------------|
| `docker volume create <volume_name>`                     | 创建一个新的数据卷。                     |
| `docker volume ls`                                       | 列出所有数据卷。                       |
| `docker volume inspect <volume_name>`                    | 显示数据卷的详细信息，包括其挂载路径、驱动、创建时间等。   |
| `docker volume rm <volume_name>`                         | 删除指定的数据卷。如果数据卷被容器使用，删除将失败。     |
| `docker volume prune`                                    | 删除所有未被任何容器使用的数据卷（不再被挂载的卷）。     |
| `docker volume inspect`                                  | 查看所有数据卷的详细信息。                  |
| `docker volume create --driver <driver>`                 | 创建一个使用特定驱动的数据卷（例如 `local` 驱动）。 |
| `docker volume mount <volume_name>`                      | 将数据卷挂载到容器中的指定位置（需要容器名）。        |
| `docker volume rm $(docker volume ls -qf dangling=true)` | 删除所有未使用的数据卷（悬空卷）。              |

1. **创建一个数据卷**：
   ```bash
   docker volume create my_volume
   ```

2. **查看所有数据卷**：
   ```bash
   docker volume ls
   ```

3. **查看某个数据卷的详细信息**：
   ```bash
   docker volume inspect my_volume
   ```

4. **删除一个数据卷**：
   ```bash
   docker volume rm my_volume
   ```

5. **删除所有未使用的数据卷**：
   ```bash
   docker volume prune
   ```

6. **删除所有悬空（没有使用的）数据卷**：
   ```bash
   docker volume rm $(docker volume ls -qf dangling=true)
   ```

### 默认数据卷

在 Docker 中，**默认数据卷**的长字符串通常是一个由 Docker 自动生成的卷名称，它是用于管理容器数据持久化的匿名卷（匿名卷是没有明确指定名称的数据卷）。

当你运行一个容器并且没有为它指定数据卷名称时，Docker 会自动生成一个长字符串作为数据卷的名字。例如：

```bash
docker run -v /data ubuntu
```

在这个命令中，如果没有指定卷名称，Docker 会为 `/data` 目录创建一个匿名卷，并自动分配一个名字，比如 `d7f3c081d6e19e2b1b6ac9b83172d1c1d531b34e4ad8234ac7398f59b54d6d77`。

这个长字符串（例如 `d7f3c081d6e19e2b1b6ac9b83172d1c1d531b34e4ad8234ac7398f59b54d6d77`）是卷的自动生成名称，它是 **Docker 默认卷名称的一部分**。

1. **匿名卷**：当你没有明确指定卷名称时，Docker 会为容器创建一个匿名数据卷。这个匿名卷会被分配一个随机的、长的字符串作为名称，这通常不是你自己指定的。

2. **存储位置**：这些数据卷存储在 Docker 的默认数据目录中，通常是在 `/var/lib/docker/volumes/` 目录下，具体路径会依赖于你所使用的操作系统和 Docker 配置。

3. **生命周期**：匿名数据卷的生命周期和容器绑定在一起。当容器删除时，默认情况下，这些匿名卷不会被自动删除，除非你使用 `docker volume prune` 清理未使用的卷。Docker 设计时希望保持数据的持久性，即使容器删除了，数据仍然可以被保留下来。这对于数据存储非常重要。在 Docker 中，匿名数据卷的生命周期并不完全绑定到容器本身。虽然它们与容器关联，但 Docker 默认不会在容器删除时自动删除匿名数据卷

### 如何控制数据卷名

```shell
  volumes:
      my_volume: {}
  services:
    web:
      image: nginx
      volumes:
        - my_volume:/data
```

docker compose up -d 后，数据卷的名称是 `test_my_volume`，而不是 `my_volume`，这是因为 Docker Compose 在生成数据卷名称时，会默认将 **项目名称** 作为前缀添加到数据卷名称中。这是 Docker Compose 的默认行为，目的是为了避免不同项目之间的数据卷名称冲突。

方法 1：使用 `-p` 参数，在运行 `docker-compose up` 时，使用 `-p` 参数指定项目名称：

```bash
docker-compose -p myproject up -d
```

这样，数据卷名称会变成 `myproject_my_volume`。

方法 2：设置环境变量。通过设置 `COMPOSE_PROJECT_NAME` 环境变量来指定项目名称：

```bash
export COMPOSE_PROJECT_NAME=myproject
docker-compose up -d
```

这样，数据卷名称也会变成 `myproject_my_volume`。

方法 3：可以使用外部数据卷（External Volume）。外部数据卷是完全由用户管理的，Docker Compose 不会修改其名称。

```yaml
volumes:
  my_volume:
    external: true  # 声明为外部数据卷

services:
  web:
    image: nginx
    volumes:
      - my_volume:/data
```

在这种情况下：

- 需要手动创建数据卷：
  ```bash
  docker volume create my_volume
  ```
- Docker Compose 会直接使用 `my_volume`，而不会添加项目名称前缀。

![使用外部数据卷](https://cdn.xiaobinqt.cn/xiaobinqt.io/20250220/59ad0c732b004497a3f2bbcfab351d4c.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '使用外部数据卷')

## 参考

+ [https://docs.docker.com/compose/](https://docs.docker.com/compose/)
+ [Docker-入门到实践](https://yeasy.gitbook.io/docker_practice/)











