# Docker slim、stretch、buster、jessie、alpine


<!-- author： xiaobinqt -->
<!-- email： xiaobinqt@163.com -->
<!-- https://xiaobinqt.github.io -->
<!-- https://www.xiaobinqt.cn -->


在写 Dockerfile 时，在引用基础镜像时经常会看到这样的写法：

```dockerfile
FROM debian:buster
```

或是

```dockerfile
FROM node:14.16.1-stretch-slim
```

那这里的 `buster` 和 `stretch` 具体是什么呢？其实 `buster`、`stretch`还有`jessie`针对的是不同 Debian 代号：

| tag     | debian 版本 |
|---------|-----------|
| `buster`  | Debian 10 |
| `stretch` | Debian 9  |
| `jessie`  | Debian 8  |

`slim` 可以理解为精简版，跟 `Minimal`是一样的。

> 所以`FROM debian:buster` 就是把 debian 10 作为基础镜像，`FROM node:14.16.1-stretch-slim` 就是把 debian 9 的精简版作为基础镜像。

镜像标签中的 `Alpine` 其实指的是这个镜像内的文件系统内容，是基于 Alpine Linux 这个操作系统的。Alpine Linux 是一个相当精简的操作系统，而基于它的镜像可以仅有数 MB
的尺寸。如果软件基于这样的系统镜像之上构建而得，可以想象新的镜像也是十分小巧的。

`Alpine` 镜像的缺点就在于它实在**过于精简**，以至于麻雀虽小，也无法做到五脏俱全了。在 `Alpine` 中缺少很多常见的工具和类库，以至于如果想基于 `Alpine`
标签的镜像进行二次构建，那搭建的过程会相当烦琐。所以如果想要对软件镜像进行改造，并基于其构建新的镜像，那么 `Alpine` 镜像不是一个很好的选择。
