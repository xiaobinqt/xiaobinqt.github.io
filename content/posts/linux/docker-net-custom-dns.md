---
title: "Docker bridge 网络与自定义 DNS 解析"
subtitle: ""

init_date: "2023-05-24T16:38:09+08:00"

date: 2023-05-24

lastmod: 2023-05-24

draft: false

author: "xiaobinqt"
description: "xiaobinqt,dnsmasq,powerdns"

featuredImage: ""

featuredImagePreview: ""

reproduce: false

translate: false

tags: [ "dns" ,"docker" ]
categories: [ "开发者手册" ]
lightgallery: true

series: [ ]

series_weight:

toc: true

math: true
---

<!-- author： xiaobinqt -->
<!-- email： xiaobinqt@163.com -->
<!-- https://xiaobinqt.github.io -->
<!-- https://www.xiaobinqt.cn -->

## 常见 DNS 记录类型

+ A 记录（Address Record）

记录格式：`example.com. IN A 192.0.2.1`，将域名映射到 IPv4 地址，不包含端口信息。

+ AAAA 记录（IPv6 Address Record）

记录格式：`example.com. IN AAAA 2001:db8::1`，将域名映射到 IPv6 地址。

+ CNAME 记录（Canonical Name Record）

记录格式：`www.example.com. IN CNAME example.com.`，将一个域名指向另一个域名，实现域名的别名或重定向。

+ TXT 记录（Text Record）

记录格式：`example.com. IN TXT "Some text here"`，存储与域名相关的文本信息，常用于验证域名所有权、防止电子邮件欺诈等。

+ SRV 记录（Service Record）

记录格式：`_service._proto.name. IN SRV priority weight port target`。`priority`表示优先级，用于指定备用服务器的顺序。值越小，优先级越高。`weight`表示权重，用于在具有相同优先级的记录之间进行负载均衡。值越大，权重越高。`port`表示服务的端口号。`target`表示提供该服务的目标主机的域名。

SRV 用于指定特定服务的域名、端口和优先级等信息，它用于在 DNS 中提供服务发现的功能，让客户端能够通过域名查找到提供特定服务的目标主机和端口。

+ PTR 记录（Pointer Record）

记录格式：`1.2.0.192.in-addr.arpa. IN PTR example.com.`，用于进行反向 DNS 查找，将 IP 地址解析为域名。

> IN（表示Internet）在 DNS 记录中是可选的，可以省略。当省略 IN 时，默认为 IN，因为大多数 DNS 记录都是针对互联网的。

## resolv.conf 配置文件

resolv.conf 配置文件，存储了用于解析域名的 DNS 服务器的相关信息，用于指定系统的 DNS 解析配置。

resolv.conf 文件通常位于 Linux 系统中的 /etc/resolv.conf。每行包含一个配置项，配置项由关键字和对应的值组成，以空格或制表符分隔。常见的配置项包括：

+ nameserver：指定 DNS 服务器的 IP 地址。可以有多个 nameserver 行，按照优先级从上到下进行解析。
+ search：指定默认的搜索域名列表。当使用不完全限定的域名时，系统会自动尝试附加这些域名来进行解析。
+ domain：指定系统的默认域名。当使用不完全限定的主机名时，系统会自动尝试附加默认域名来进行解析。
+ options：指定其他的解析选项，如超时时间、转发等。

```shell
nameserver 8.8.8.8
nameserver 8.8.4.4
search example.com

```

比如以下的这个配置

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230529/8b4dd5e7b70a4e17870780c2f4708751.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'resolv.conf')

```shell
search xae-zcbus-20230523.28e5df10.csphere.local csphere.local
```

这条 search 配置表示系统默认的搜索域名列表包括两个域名：`xae-zcbus-20230523.28e5df10.csphere.local` 和 `csphere.local`。

当进行 DNS 解析时，如果使用一个不完全限定的域名（没有包含点号），系统会按照 search 配置中的顺序尝试逐个附加这些搜索域名，以尝试解析域名。例如，如果要解析的域名是 example，系统会依次尝试解析 `example.xae-zcbus-20230523.28e5df10.csphere.local` 和 `example.csphere.local`。

这样配置搜索域名列表可以简化 DNS 查询过程，特别是在本地网络内部使用内部域名时，通过设置合适的搜索域名，可以直接使用不完全限定的主机名进行解析，而无需每次都输入完整的域名。

ndots 参数控制着系统在进行 DNS 解析时是否自动追加搜索域名。它指定了一个域名中至少要包含的点号`.`的数量。点号在域名中的数量表示域名的层级结构，例如`example.com`有一个点号，而`www.example.com`有两个点号。当一个域名的层级结构中点号的数量达到或超过 ndots 参数指定的值时，系统将**不再追加**搜索域名。

如上的配置`options ndots:2`，表示当进行 DNS 解析时，如果域名中包含至少两个点号（层级结构至少为三级），系统将不会自动追加搜索域名。如果域名的层级结构不足三级（点号少于两个），系统会自动尝试使用 /etc/resolv.conf 中指定的搜索域名列表进行解析。

`nameserver 172.17.0.1`用于指定 DNS 解析时要使用的 DNS 服务器的 IP 地址。这里的`172.17.0.1`是 Docker bridge 网络下虚拟网桥 docker0 的 IP 地址。

因为容器中没有 dns 解析服务，不管是 dnsmasq 还是 pdns 都是装在宿主机上的，所以最后肯定是到宿主机上来解析的域名，但是这里如果直接写宿主机 IP 会影响效率「TODO 待补充」。

## /etc/hosts 配置文件

/etc/hosts 是本地的主机名解析文件，用于将主机名映射到对应的 IP 地址。/etc/hosts 文件包含了主机名和对应 IP 地址的映射关系。每行的格式为 `<IP 地址> <主机名>` 或者 `<IP 地址> <主机别名> <主机名>`。

/etc/hosts 文件中的条目优先于 DNS（Domain Name System）解析，当系统需要解析主机名时，会首先查看 /etc/hosts 文件，如果找到匹配的主机名，则直接使用对应的 IP 地址进行通信，无需进行 DNS 查询。

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230524/16561b7c30f74809822274beff9af838.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'hosts')

## PDNS

PDNS 是 PowerDNS 的简称，它是一款开源的域名系统（DNS）服务器软件。

```shell
# 安装 pdns
yum install pdns pdns-backend-pipe -y

# pdns 启动,停止和查看是否运行正常
systemctl start/stop/status pdns

```

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230525/fa40c2fa19674bd1a29c4edd0496ff5b.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '查看 dnsmasq 是否正常')

如果有问题需要排查，可以使用如下命令让 pdns 在前台运行

```shell
/usr/sbin/pdns_server --guardian=no --daemon=no --disable-syslog --log-timestamp=no --write-pid=no

```

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230527/fc4df6cc9be049929788893a037ccd6f.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '前台运行模式')

`--guardian=no`: 禁用 Guardian 模式。Guardian 模式是 PowerDNS 的守护进程管理机制，它负责监控和重启 PowerDNS 进程。通过将此参数设置为 no，禁用了 Guardian 模式。

`--daemon=no`: 禁用守护进程模式。默认情况下，PowerDNS 以守护进程的形式运行，即在后台作为系统服务运行。通过将此参数设置为 no，PowerDNS 将在前台运行，输出日志和调试信息到终端。

`--disable-syslog`: 禁用使用系统日志。默认情况下，PowerDNS 会将日志信息写入系统日志。通过使用此参数，禁用了将日志写入系统日志的功能。

`--log-timestamp=no`: 禁用日志时间戳。默认情况下，PowerDNS 在日志中添加时间戳以指示每个日志条目的时间。通过将此参数设置为 no，禁用了时间戳的添加。

`--write-pid=no`: 禁用写入 PID 文件。默认情况下，PowerDNS 会将其进程 ID 写入 PID 文件。通过将此参数设置为 no，禁用了 PID 文件的写入。

### pipe backend

在 PowerDNS 中，pipe 是一种后端（Backend）类型，用于将 DNS 查询通过管道（Pipe）方式传递给外部程序进行处理。这种后端类型被称为 "pipe backend"。

使用 pipe backend，PowerDNS 可以将接收到的 DNS 查询通过管道发送给一个外部的自定义脚本或程序，然后由该脚本或程序处理查询并返回结果给 PowerDNS。这种方式允许用户根据自己的需求编写自定义逻辑来处理 DNS 查询，从而实现更灵活的功能。

在 PowerDNS 中配置 pipe backend 需要以下步骤：

1. 编写自定义脚本或程序：根据需求，编写一个能够接收 DNS 查询并返回结果的脚本或程序。该脚本或程序可以使用任何编程语言来实现，例如 Python、Perl、Shell 等。

2. 配置 PowerDNS：在 PowerDNS 的配置文件中指定使用 pipe backend，并设置要执行的脚本或程序的路径。通常需要修改 PowerDNS 的配置文件（例如 pdns.conf）来进行配置。

```shell
launch=pipe
pipe-command=/path/to/your/script.py
```

上述示例中，pipe-command 指定了自定义脚本或程序的路径。在修改完配置文件后，**需要重新启动** PowerDNS 服务，使配置生效。

当 PowerDNS 接收到 DNS 查询时，它将会将查询数据通过管道传递给指定的脚本或程序。脚本或程序可以处理查询并返回结果给 PowerDNS，然后由 PowerDNS 将结果返回给客户端。

通过配置 pipe backend，可以根据自己的需求编写自定义的逻辑来处理 DNS 查询，例如基于外部数据源、自定义策略、过滤等操作。

## dnsmasq

```shell
# 安装 dnsmasq
yum install dnsmasq

# 一些状态命令
systemctl start/stop/restart/status dnsmasq

# 检查配置文件语法是否正确
dnsmasq --test

```

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230529/21042ad8bf514e519d55c93d7431336d.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'dnsmasq 命令')

Dnsmasq 是一个轻量级的 DNS 和 DHCP 服务器软件，用于提供本地域名解析和网络地址分配功能，配置文件通常位于 /etc/dnsmasq.conf。下面是一些常用的配置文件字段说明：

+ port（端口）：指定 Dnsmasq 监听的 DNS 查询端口。默认为 53，但可以根据需要进行更改。

+ cache-size（缓存大小）：指定DNS缓存的最大大小（以条目数量表示）。缓存可以提高解析性能，减少对上游 DNS 服务器的查询次数。例如，cache-size=1000 表示最多缓存 1000 条 DNS 解析记录。

+ server（服务器）：用于指定要使用的上游 DNS 服务器。可以配置多个 server 字段，每个字段后面跟随一个有效的 DNS 服务器地址。Dnsmasq 会按顺序向这些服务器发送 DNS 查询请求。

```shell
server=8.8.8.8
server=8.8.4.4
```

server 的另一种写法是用来指定特定域名的 DNS 服务器映射。比如：

```shell
server=/domain.org/192.168.14.5

```

这个配置表示将域名 domain.org 解析到 IP 地址 192.168.14.5 上。当 Dnsmasq 收到对`domain.org`域名的解析请求时，它将使用指定的 IP 地址作为响应。这在本地网络中创建自定义的域名解析规则非常有用，可以用于内部域名解析或重定向特定域名到特定 IP 地址。

+ address 参数用于指定域名解析的静态映射，将特定域名解析到指定的IP地址。它的语法如下：

```shell
address=/域名/IP地址
address=/example.com/192.168.1.100
```

这个配置将域名 example.com 解析为 IP 地址 192.168.1.100。当 Dnsmasq 接收到关于 example.com 的解析请求时，它将使用指定的 IP 地址进行解析，而不会向上游 DNS 服务器发送查询请求。

## 演练

现在有 2 台机器，分别是`192.168.14.103`用来做控制器，安装有 powerDNS，作为上游 DNS，用来最后解析 DNS，`192.168.14.100`用来做 agent，安装有 dnsmasq 解析本地 DNS，通过配置 server 参数，将域名交给上游 DNS 服务器解析，也就是交给`192.168.14.103`解析处理。 pdns 通过 pipe backend 的 python 脚本，对所有的以`domain.org`结尾的域名请求都返回`192.168.40.223`的 IP，以下是 backend.py 的 python 脚本，python 版本是 python 3.6.8。

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random
import sys
import time


class DNSLookup(object):
    """Handle PowerDNS pipe-backend domain name lookups."""
    ttl = 30

    def __init__(self, query):
        """parse DNS query and produce lookup result.

        query: a sequence containing the DNS query as per PowerDNS manual appendix A:
        http://downloads.powerdns.com/documentation/html/backends-detail.html#PIPEBACKEND-PROTOCOL
        """
        (_type, qname, qclass, qtype, _id, ip) = query
        self.has_result = False  # has a DNS query response
        qname_lower = qname.lower()

        """List of servers to round-robin"""
        servers = ['192.168.40.223']
        server = random.choice(servers)

        self.results = []

        # if (qtype == 'A' or qtype == 'ANY') and qname_lower.endswith('domain.org'):
        if qtype == 'ANY' and qname_lower.endswith('domain.org'):
            self.results.append('DATA\t%s\t%s\tA\t%d\t-1\t%s' % (qname, qclass, DNSLookup.ttl, server))
            self.has_result = True
        elif qtype == 'SOA':
            self.results.append(
                'DATA\t%s\t%s\t%s\t3600\t-1\tns1.test.soa\tadmin.test.soa\t2014032110\t10800\t3600\t604800\t3600'
                % (qname, qclass, qtype))
            self.has_result = True

    def str_result(self):
        """return string result suitable for pipe-backend output to PowerDNS."""
        if self.has_result:
            return '\n'.join(self.results)
        else:
            return ''


class Logger(object):
    def __init__(self):
        pid = os.getpid()
        self.logfile = '/tmp/backend.log'
        """self.logfile = '/tmp/backend-%d.log' % pid"""

    def write(self, msg):
        logline = '%s|%s\n' % (time.asctime(), msg)
        f = open(self.logfile, 'a')
        f.write(logline)
        f.close()


def debug_log(msg):
    logger.write(msg)


class PowerDNSbackend(object):
    """The main PowerDNS pipe backend process."""

    def __init__(self, filein, fileout):
        """initialise and run PowerDNS pipe backend process."""
        self.filein = filein
        self.fileout = fileout

        self._process_requests()  # main program loop

    def _process_requests(self):
        """main program loop"""
        first_time = True
        while 1:
            rawline = self.filein.readline()
            if rawline == '':
                debug_log('EOF')
                return  # EOF detected
            line = rawline.rstrip()

            debug_log('received from pdns:%s' % line)

            if first_time:
                if line == 'HELO\t1':
                    self._fprint('OK\tPython backend firing up')
                else:
                    self._fprint('FAIL')
                    debug_log('HELO input not received - execution aborted')
                    rawline = self.filein.readline()  # as per docs - read another line before aborting
                    debug_log('calling sys.exit()')
                    sys.exit(1)
                first_time = False
            else:
                query = line.split('\t')
                if len(query) != 6:
                    self._fprint('LOG\tPowerDNS sent unparseable line')
                    self._fprint('FAIL')
                else:
                    debug_log('Performing DNSLookup(%s)' % repr(query))
                    lookup = DNSLookup(query)
                    if lookup.has_result:
                        pdns_result = lookup.str_result()
                        self._fprint(pdns_result)
                        debug_log('DNSLookup result(%s)' % pdns_result)
                    self._fprint('END')

    def _fprint(self, message):
        """Print the given message with newline and flushing."""
        self.fileout.write(message + '\n')
        self.fileout.flush()
        debug_log('sent to pdns:%s' % message)


if __name__ == '__main__':
    logger = Logger()
    infile = sys.stdin
    # sys.stdout.close()
    # outfile = os.fdopen(1, 'w', 1)
    outfile = sys.stdout
    try:
        PowerDNSbackend(infile, outfile)
    except:
        debug_log('execution failure:' + str(sys.exc_info()[0]))
        raise

```

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230529/a1a644dcf7bb425e9cd4eb4606c554a9.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'pipe backend')

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230529/761e93174f9d4763be59cef6711c3fe0.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'dig 解析正常')

现在在 agent 机器也就是`192.168.14.100`上通过 [xiaobinqt/redis:7-ping](https://hub.docker.com/r/xiaobinqt/redis/tags) 镜像启动一个 redis 容器，容器名为 c-redis：

```docker
docker run --name c-redis --dns 172.17.0.1 --dns-search domain.org --dns-opt "ndots:2" -d  xiaobinqt/redis:7-ping
```

比如，当在容器中执行 `ping abdd`时，正常会先走 hosts 但是这里的 hosts 都没有对应的域名，所以 hosts 失效，再去 nameserver 指定的 DNS 服务器解析域名，由于配置了 ndots:2 ，系统会自动追加搜索域名`domain.org`，所以会去 172.17.0.1 DNS 服务器搜索域名 `abdd.domain.org`，172.17.0.1 对应的是宿主机的 docker0 虚拟网桥，最后会走到**宿主机的 dns 服务**，也就是`192.168.14.100` 的 dnsmasq 服务，对应的端口是 53。

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230529/ae90a8281d72406ca0bf831fc375f36c.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '调试结果')

## 参考

+ [pdns-pipebackend.py](https://gist.github.com/sokratisg/10069682)
+ [PowerDNS : libpipebackend.so no such file or directory](https://www.linuxhelp.com/questions/powerdns-libpipebackend-so-no-such-file-or-directory)
+ [Installing DNS Server on CentOS/RHEL using dnsmasq | Zimbra](https://community.zextras.com/dns-server-installation-guide-on-centos-7-rhel-7-and-centos-8-rhel-8-using-dnsmasq/)






