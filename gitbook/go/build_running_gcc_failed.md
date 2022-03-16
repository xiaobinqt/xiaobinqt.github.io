# running gcc failed: exit status 1

今天在编译 go 项目时出现了如下错误：

```shell
/usr/local/go/pkg/tool/linux_amd64/link: running gcc failed: exit status 1
/usr/bin/ld: cannot find -lpthread
/usr/bin/ld: cannot find -lc
collect2: error: ld returned 1 exit status
```

解决办法：

```shell
yum install glibc-static.x86_64 -y
```

