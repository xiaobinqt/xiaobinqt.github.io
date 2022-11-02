---
title: "Redis 学习笔记"
subtitle: "Redis study notes and FAQ"

init_date: "2022-04-07T10:40:45+08:00"

date: 2021-02-20

lastmod: 2022-04-07

draft: false

author: "xiaobinqt"
description: "Redis, Redis 数据结构,redis 缓存击穿,redis 布隆过滤器,redis 淘汰机制,redis 持久化机制,redis 分布式缓存"

featuredImage: "https://cdn.xiaobinqt.cn/xiaobinqt.io/20220407/2ecceb8af82e4695938c77dcc452eba2.png"

reproduce: false

tags: ["redis"]
categories: ["开发者手册"]
lightgallery: true

toc: true

math: true
---


Redis 是一个使用 C 语言开发的数据库，与传统数据库不同的是 Redis 的数据是存在内存中的，我们把这种数据库叫做内存数据库。因为在内存中，所以读写速度非常快，因此 Redis 被广泛应用于缓存方向。

Redis 提供了多种数据类型来支持不同的业务场景，所以 Redis 除了做缓存之外，Redis 还经常用来做分布式锁，消息队列等。Redis 还支持事务、持久化、Lua 脚本、多集群方案。

## 数据结构

![Redis 五种数据结构](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220407/a4e1db3070d54256bc00ae5b8cedc654.png 'Redis 五种数据结构')

> 在 Redis 中，所有的 key 都是字符串。

### 字符串

字符串类型是 Redis 中最基本的数据类型，一个 key 对应一个 value。

字符串类型是二进制安全的，也就是说 Redis 中的字符串可以包含任何数据。如数字，字符串，jpg 图片或者序列化的对象。

### Hash

hash 值本身又是一种键值对结构：

![hash](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220407/052cc436d66d4ace833d57b4a56b499b.png 'hash')

> 所有 hash 的命令都是 h 开头，如 `hget`、`hset`、`hdel` 等

### List

List 就是链表（redis 使用双端链表实现的 List），是有序的，value可以重复，可以通过下标取出对应的 value 值，左右两边都能进行插入和删除数据。

![List](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220407/576c692e2a984a0ea9bab845ae6d7039.png 'List')

#### 常用命令

#### 使用技巧

+ `lpush` + `lpop` = Stack(栈)
+ `lpush` + `rpop` = Queue（队列）
+ `lpush` + `ltrim` = Capped Collection（有限集合）
+ `lpush` + `brpop` = Message Queue（消息队列）

### Set

![Set](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220407/a0cf4be1efc5403290a055a92d3350ca.png 'Set')

集合类型也是用来保存多个字符串的元素，但和列表有几个不同的点：

+ :point_right: 不允许有重复的元素
+ :point_right: 集合中的元素是无序的，不能通过索引下标获取元素
+ :point_right: 支持集合间的操作，可以取多个集合取交集、并集、差集

### ZSet

有序集合和集合有着必然的联系，保留了集合不能有重复成员的特性。

区别是，有序集合中的**元素是可以排序的**，它给每个元素设置一个分数，作为排序的依据。

> 有序集合中的元素不可以重复，但是 score 分数可以重复，就和一个班里的同学学号不能重复，但考试成绩可以相同。

## FAQ

### 分布式缓存

分布式缓存主要解决的是**单机缓存的容量受服务器限制并且无法保存通用的信息**，因为，本地缓存只在当前服务里有效。比如部署了两个相同的服务，他们两者之间的缓存数据是无法共同的。

分布式缓存的话，使用的较多的较多的解决方案是是 Memcached 和 Redis。不过，随着近些年 Redis 的发展，大家慢慢都转而使用更加强大的 Redis 而放弃 Memcached。

### Redis 和 Memcached 的区别

#### 共同点

+ 都是基于内存的数据库。
+ 都有过期策略。
+ 两者的性能都非常高。

#### 区别

+ Redis 支持更丰富的数据类型，也就是说可以支持更复杂的应用场景。Redis 不仅仅支持简单的 k/v 类型的数据，同时还提供 `list`，`set`，`zset`，`hash` 等数据结构的存储。而 Memcached
  只支持最简单的 k/v 数据类型。
+ Redis 的容灾更好，支持数据的持久化，可以将内存中的数据保持在磁盘中，重启的时候可以再次加载进行使用,而 Memecache 把数据全部存在内存中。
+ Memcached 没有原生的集群模式，需要依靠客户端来实现往集群中分片写入数据，但是 Redis 目前是原生支持 cluster 模式的。
+ Redis 在服务器内存使用完之后，可以将不用的数据放到磁盘上。而 Memcached 在服务器内存使用完之后，就会直接报异常。
+ Memcached 是多线程，非阻塞 IO 复用的网络模型，Redis 使用单线程的多路 IO 复用模型（Redis 6.0 引入了多线程 IO ）。
+ Memcached过期数据的删除策略只用了惰性删除，而 Redis 同时使用了惰性删除与定期删除。
+ Redis 支持发布订阅模型、Lua 脚本、事务等功能，而 Memcached 不支持。

### Redis 如何判断数据是否过期

Redis 通过一个叫做过期字典（可以看作是hash表）来保存数据过期的时间。过期字典的键指向 Redis 数据库中的某个key(键)，过期字典的值是一个long long 类型的整数，这个整数保存了 key
所指向的数据库键的过期时间（毫秒精度的UNIX时间戳）。

### 过期删除策略

如果 Redis 中一批 key 只能存活 1 分钟，那么 1 分钟后，Redis 是怎么对这批 key 进行删除的呢？

+ 惰性删除：只会在取出 key 的时候才对数据进行过期检查。这样对 CPU 最友好，但是**可能会造成太多过期 key 没有被删除**。
+ 定期删除：每隔一段时间抽取一批 key 执行删除过期 key 操作。Redis 底层会通过限制删除操作执行的时长和频率来减少删除操作对 CPU 时间的影响。

**定期删除对内存更加友好，惰性删除对CPU更加友好**。Redis 采用的是定期删除:heavy_plus_sign:惰性删除。

### 内存淘汰机制

我们通过给 key 设置过期时间还是有问题的，因为还是可能存在定期删除和惰性删除**漏掉**了很多过期 key 的情况。这样就导致大量过期 key 堆积在内存里，然后就 OOM 了，Redis 的数据淘汰机制可以解决这个问题。

| 策略                | 说明                                                                         |
|-------------------|----------------------------------------------------------------------------|
| `volatile-lru`    | （least recently used），从已设置过期时间的数据集（`server.db[i].expires`）中挑选最近最少使用的数据淘汰   |
| `volatile-ttl`    | 从已设置过期时间的数据集（`server.db[i].expires`）中挑选将要过期的数据淘汰                           |
| `volatile-random` | 从已设置过期时间的数据集（`server.db[i].expires`）中任意选择数据淘汰                              |
| `allkeys-lru`     | （least recently used），当内存不足以容纳新写入数据时，在键空间中，移除最近最少使用的 key（这个是最常用的）          |
| `allkeys-random`  | 从数据集（`server.db[i].dict`）中任意选择数据淘汰                                         |
| `no-eviction`     | 禁止驱逐数据，也就是说当内存不足以容纳新写入数据时，新写入操作会报错:scream:。                                      |
| `volatile-lfu`    | （least frequently used），从已设置过期时间的数据集(`server.db[i].expires`)中挑选最不经常使用的数据淘汰 |
| `allkeys-lfu`     | （least frequently used），当内存不足以容纳新写入数据时，在键空间中，移除最不经常使用的 key                 |

### 持久化机制

很多时候我们需要持久化数据也就是将内存中的数据写入到硬盘里面，大部分原因是为了备份数据，比如为了防止系统故障而将数据备份到一个另一台机器。

Redis 两种不同的持久化操作。一种持久化方式叫快照（snapshotting，RDB），另一种方式是只追加文件（append-only file, AOF）。

#### RDB

快照持久化是 Redis 默认采用的持久化方式，在 Redis.conf 配置文件中默认有此下配置：

```
save 900 1     # 在 900 秒(15分钟)之后，如果至少有1个key发生变化，Redis就会自动触发BGSAVE命令创建快照。
save 300 10    # 在 300 秒(5分钟)之后，如果至少有10个key发生变化，Redis就会自动触发BGSAVE命令创建快照。
save 60 10000  # 在 60 秒(1分钟)之后，如果至少有10000个key发生变化，Redis就会自动触发BGSAVE命令创建快照。
```

Redis 可以通过创建快照来获得存储在内存里面的数据在某个时间点上的副本。

Redis 创建快照之后，可以对快照进行备份，可以将快照复制到其他服务器从而创建具有相同数据的服务器副本，还可以将快照留在原地以便重启服务器的时候使用。

#### AOF

与快照持久化 RDB 相比，AOF 持久化 的**实时性更好**，基本已成为主流的持久化方案。默认情况下 Redis 没有开启 AOF方式的持久化。

开启 AOF 持久化后每执行一条会更改 Redis 中的数据的命令，Redis 就会将该命令写入硬盘中的 AOF 文件。AOF 文件的保存位置和 RDB 文件的位置相同，都是通过 dir 参数设置的，默认的文件名是
appendonly.aof。

Redis 的配置文件中存在三种不同的 AOF 持久化方式，它们分别是：

```
appendfsync always    # 每次有数据修改发生时都会写入AOF文件,这样会严重降低Redis的速度
appendfsync everysec  # 每秒钟同步一次，显示地将多个写命令同步到硬盘
appendfsync no        # 让操作系统决定何时进行同步
```

> 为了兼顾数据和写入性能，可以考虑 `appendfsync everysec` 选项 ，让 Redis 每秒同步一次 AOF 文件，Redis 性能几乎没受到任何影响。
> 这样即使出现系统崩溃，用户最多只会丢失一秒之内产生的数据。

## 参考

+ [Redis 命令参考](http://redisdoc.com/index.html)
+ [Redis(一)、Redis五种数据结构](https://www.cnblogs.com/haoprogrammer/p/11065461.html)
+ [Redis](https://blog.csdn.net/weixin_43230682/category_10241824.html)




