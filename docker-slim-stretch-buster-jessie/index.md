# Docker slim、stretch、buster、jessie


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

所以`FROM debian:buster` 就是把 debian 10 作为基础镜像，`FROM node:14.16.1-stretch-slim` 就是把 debian 9 的精简版作为基础镜像。


