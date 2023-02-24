---
title: "Docker 安装 mysql8.0"
subtitle: ""

init_date: "2022-11-21T10:24:03+08:00"

date: 2021-09-08

lastmod: 2022-11-21

draft: false

author: "xiaobinqt"
description: "xiaobinqt,安装mysql8.0,docker 安装mysql8,如何设置docker国内镜像，如果开启mysql远程连接，如果修改mysql8密码，flush privileges"

featuredImage: ""

featuredImagePreview: ""

reproduce: false

translate: false

tags: ["mysql","docker"]
categories: ["mysql"]
lightgallery: true

series: []

series_weight:

toc: true

math: true
---

[//]: # (https://cdn.xiaobinqt.cn/xiaobinqt.io/20221121/63ec306e51a44dc2a3ca8ff24d6be941.png)

<!-- author： xiaobinqt -->
<!-- email： xiaobinqt@163.com -->
<!-- https://xiaobinqt.github.io -->
<!-- https://www.xiaobinqt.cn -->

## 设置镜像源

国内的网络环境，使用官方的镜像源，下载速度很慢，所以我们需要使用国内的镜像源。

```shell
cat /etc/docker/daemon.json
```

如果没有`daemon.json`文件可以手动创建一个。可以设置中国区镜像或是网易镜像，也可以设置阿里云镜像（推荐使用阿里云的加速器，因为快:rofl:）。

+ 中国区镜像

```json
{
  "registry-mirrors": [
    "https://registry.docker-cn.com"
  ]
}
```

+ 网易镜像

```json
{
  "registry-mirrors": [
    "https://hub-mirror.c.163.com"
  ]
}
```

+ 阿里云镜像

![阿里云镜像地址](https://cdn.xiaobinqt.cn/xiaobinqt.io/20221121/db638d8f1d5447bca5e54227203de932.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '阿里云镜像地址')

![设置镜像源](https://cdn.xiaobinqt.cn/xiaobinqt.io/20221121/96866e63f1ca4b9d9f5e3b129c405cd4.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '设置镜像源')

设置完成后，重启docker服务。

```shell
systemctl restart docker
```

可以通过 `docker info` 查看镜像源是否设置成功。

```shell
docker info | grep Mirrors -A 1
```

![查看镜像源](https://cdn.xiaobinqt.cn/xiaobinqt.io/20221121/bd599a600ab44a73a6f21de4167a4446.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '查看镜像源')

## 下载镜像

可以去 [https://hub.docker.com/_/mysql/tags](https://hub.docker.com/_/mysql/tags) 仓库找需要的 mysql 版本:point_down:

![镜像下载](https://cdn.xiaobinqt.cn/xiaobinqt.io/20221121/09ed0f1adae443d3a22a34796c8b3c0e.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '镜像下载')

通过 `docker pull`下载需要的镜像。

![下载镜像](https://cdn.xiaobinqt.cn/xiaobinqt.io/20221121/569c7174b200474f9e20724d2f7c4e35.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '下载镜像')

## 配置并启动容器

### 主机挂载目录

```shell
mkdir -p mysql8.0/{conf,data} # conf 存放配置文件,data 存放数据库文件
touch mysql8.0/conf/my.cnf # 创建配置文件
chown -R 999:999 mysql8.0 # 修改权限
```

将`my.cnf`文件中写入以下配置

```shell
[mysqld]
pid-file        = /var/run/mysqld/mysqld.pid
socket          = /var/run/mysqld/mysqld.sock
datadir         = /var/lib/mysql
secure-file-priv= /var/lib/mysql
```

具体可以参考[https://github.com/docker-library/mysql/blob/master/8.0/config/my.cnf](https://github.com/docker-library/mysql/blob/master/8.0/config/my.cnf)

`secure-file-priv` 设置为 `/var/lib/mysql`是为了解决 [MySQL 8 docker-compose :Failed to access directory for --secure-file-priv](https://github.com/docker-library/mysql/issues/541) 问题。

![设置挂载目录](https://cdn.xiaobinqt.cn/xiaobinqt.io/20221121/014c2fb94bb74b0b8f42178efaff315c.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '设置挂载目录')

### 启动容器

```shell
docker run -d \
    -p 3310:3306 \
    --name mysql8.0 \
    -v /root/weibin/mysql8.0/conf/my.cnf:/etc/mysql/cnf \
    -v /root/weibin/mysql8.0/data:/var/lib/mysql \
    -e MYSQL_ROOT_PASSWORD=123456 \
    mysql:8.0
```

![启动容器](https://cdn.xiaobinqt.cn/xiaobinqt.io/20221121/2c0a7dbf9628400a98fcfaaa341c6970.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '启动容器')

## 开启远程连接

如果不能远程连接可以进入容器后连接数据库，修改 mysql 库的 user 表。

```shell
docker exec -it 容器ID bash
````

![进入容器](https://cdn.xiaobinqt.cn/xiaobinqt.io/20221121/c086da058f074cfc96f93ce87d8d2cfb.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '进入容器')

查看 user 表中的`user='root'`的账号的 host 是否是`%`，如果不是则设置为`%`。如果已存在多个 root 账号，其中只要有一个的 host 为`%`就可以了。

![设置host](https://cdn.xiaobinqt.cn/xiaobinqt.io/20221121/534fccacb5c44d9e8dcc9db8df1d6ee3.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '设置host')

```shell
update user set host='%' where user = 'root';
```

如果修改了用户需要执行

```shell
flush privileges;
```

这样在不重启的 mysql 服务的情况下就可以生效。

## 修改密码

```shell
ALTER USER 'root'@'localhost' IDENTIFIED WITH caching_sha2_password BY 'yourpasswd';
```

![修改密码](https://cdn.xiaobinqt.cn/xiaobinqt.io/20221121/3ca7bd00dfaf402d871581aca72d2e93.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '修改密码')

## FAQ

+ :question: **secure-file-priv**

```shell
Failed to access directory for --secure-file-priv. Please make sure that directory exists and is accessible by MySQL Server. Supplied value : /var/lib/mysql-files
```

![FAQ1](https://cdn.xiaobinqt.cn/xiaobinqt.io/20221121/22c2b7f4e7f24aaba10ede6b043cbb55.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'FAQ1')

宿主机的映射目录需要设置用户和用户组为`999:999`，因为 docker 容器里的用户也是 999，可以启动一个临时容器进去查看。

![999:999](https://cdn.xiaobinqt.cn/xiaobinqt.io/20221121/8591686d90444944a3b3aaefed189b26.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '999:999')

+ :question: **flush privileges**

`flush privileges`命令本质上的作用是将当前 user 和 privilige 表中的用户信息/权限设置从 mysql 库中提取到内存里。

MySQL 用户数据和权限有修改后，希望在**不重启MySQL服务**的情况下直接生效，就可以执行这个命令。

## 参考

+ [MySQL 8 docker-compose :Failed to access directory for --secure-file-priv](https://github.com/docker-library/mysql/issues/541)
+ [docker安装mysql 8](https://www.jianshu.com/p/000fee62e786)
+ [How to reset the root password in MySQL 8.0.11?](https://stackoverflow.com/questions/50691977/how-to-reset-the-root-password-in-mysql-8-0-11)
+ [How To Create a New User and Grant Permissions in MySQL8 on CentOS8](https://www.atlantic.net/dedicated-server-hosting/how-to-create-a-new-user-and-grant-permissions-in-mysql8-on-centos8/)

