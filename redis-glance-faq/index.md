# Redis 学习笔记



Redis 是一个使用 C 语言开发的数据库，与传统数据库不同的是 Redis 的数据是存在内存中的，我们把这种数据库叫做内存数据库。因为在内存中，所以读写速度非常快，因此 Redis 被广泛应用于缓存方向。

Redis 提供了多种数据类型来支持不同的业务场景，所以 Redis 除了做缓存之外，Redis 还经常用来做分布式锁，消息队列等。Redis 还支持事务、持久化、Lua 脚本、多集群方案。

## 数据结构

![Redis 五种数据结构](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220407/a4e1db3070d54256bc00ae5b8cedc654.png 'Redis 五种数据结构')

> 在 Redis 中，所有的 key 都是字符串。

## 字符串

字符串类型是 Redis 中最基本的数据类型，一个 key 对应一个 value。

字符串类型是二进制安全的，也就是说 Redis 中的字符串可以包含任何数据。如数字，字符串，jpg 图片或者序列化的对象。

### 常用命令

1. SET key value：设置指定 key 的值为给定的 value。

2. GET key：获取指定 key 的值。

3. DEL key：删除指定 key 及其对应的值。

4. INCR key：将指定 key 的值递增 1。

5. INCRBY key increment：将指定 key 的值增加指定的 increment 值。

6. DECR key：将指定 key 的值递减 1。

7. DECRBY key decrement：将指定 key 的值减去指定的 decrement 值。

8. APPEND key value：将给定的 value 追加到指定 key 的值的末尾。

9. STRLEN key：返回指定 key 的值的长度。

10. GETRANGE key start end：获取指定 key 的子字符串，从 start 到 end 的位置。

11. SETEX key seconds value：设置指定 key 的值，并指定过期时间（单位为秒）。

12. SETNX key value：只有当指定 key 不存在时，设置 key 的值为给定的 value。

13. MSET key value [key value ...]：设置多个 key-value 对。

14. MGET key [key ...]：获取多个 key 对应的值。

15. STRCMP key1 key2：比较两个字符串类型的 key 的值，如果相同返回 0，否则返回非 0 值。

16. GETSET key value：设置指定 key 的新值，并返回旧值。

17. SETBIT key offset value：设置或清除指定 key 偏移量上的位（bit）。

18. BITCOUNT key [start end]：统计指定 key 的值中，被设置为 1 的位的数量。

19. BITOP operation destkey key [key ...]：对一个或多个 key 进行位操作，并将结果保存到 destkey 中。

20. SETRANGE key offset value：用指定的 value 替换指定 key 值从偏移量 offset 开始的子字符串。

## Hash

hash 值本身又是一种键值对结构：

![hash](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220407/052cc436d66d4ace833d57b4a56b499b.png 'hash')

> 所有 hash 的命令都是 h 开头，如 `hget`、`hset`、`hdel` 等

### 常用命令

1. HSET key field value：设置指定 key 中的 field 字段的值为 value。

2. HGET key field：获取指定 key 中的 field 字段的值。

3. HMSET key field value [field value ...]：同时设置多个 field-value 对。

4. HMGET key field [field ...]：获取指定 key 中多个字段的值。

5. HDEL key field [field ...]：删除指定 key 中的一个或多个字段。

6. HLEN key：获取指定 key 中字段的数量。

7. HEXISTS key field：检查指定 key 是否存在指定的 field。

8. HINCRBY key field increment：将指定 key 中的 field 字段的值增加指定的 increment 值。

9. HINCRBYFLOAT key field increment：将指定 key 中的 field 字段的值增加指定的浮点数 increment 值。

10. HKEYS key：获取指定 key 中所有字段的名称。

11. HVALS key：获取指定 key 中所有字段的值。

12. HGETALL key：获取指定 key 中所有字段和对应的值，返回一个包含所有字段和值的列表。

13. HSTRLEN key field：获取指定 key 中指定 field 字段的值的长度。

14. HSCAN key cursor [MATCH pattern] [COUNT count]：迭代指定 key 中的 Hash 字段。

## List

List 就是链表（redis 使用双端链表实现的 List），是有序的，value可以重复，可以通过下标取出对应的 value 值，左右两边都能进行插入和删除数据。

![List](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220407/576c692e2a984a0ea9bab845ae6d7039.png 'List')

List 在 Redis 中是一个非常实用的数据结构，可以用于实现消息队列、任务队列、最新消息列表等场景。它的插入和删除操作都是常数时间复杂度，支持从两端进行操作，非常高效。

### 常用命令

1. LPUSH key element [element ...]：将一个或多个元素从列表的左侧插入（推入）。

2. RPUSH key element [element ...]：将一个或多个元素从列表的右侧插入（推入）。

3. LPOP key：移除并获取列表的最左侧元素。

4. RPOP key：移除并获取列表的最右侧元素。

5. LINDEX key index：获取列表在给定索引上的元素。

6. LLEN key：获取列表的长度（元素数量）。

7. LRANGE key start stop：获取列表中指定范围内的元素，根据 start 和 stop 的索引位置获取。

8. LINSERT key BEFORE|AFTER pivot element：在列表中某个元素的前面或后面插入新的元素。

9. LSET key index element：将列表在给定索引上的元素设置为新的值。

10. LREM key count element：从列表中删除指定数量的元素。

11. LTRIM key start stop：修剪（截取）列表，只保留指定范围内的元素。

12. RPOPLPUSH source destination：将源列表中的最右侧元素弹出并推入目标列表的最左侧。

13. BLPOP key [key ...] timeout：阻塞式地从多个列表的最左侧弹出元素。

14. BRPOP key [key ...] timeout：阻塞式地从多个列表的最右侧弹出元素。

15. BRPOPLPUSH source destination timeout：阻塞式地将源列表中的最右侧元素弹出并推入目标列表的最左侧。

16. LLEN key：获取列表的长度（元素数量）。

### 使用技巧

+ `lpush` + `lpop` = Stack（栈）
+ `lpush` + `rpop` = Queue（队列）
+ `lpush` + `ltrim` = Capped Collection（有限集合）
+ `lpush` + `brpop` = Message Queue（消息队列）

## Set

![Set](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220407/a0cf4be1efc5403290a055a92d3350ca.png 'Set')

集合类型也是用来保存多个字符串的元素，但和列表有几个不同的点：

+ :point_right: 不允许有重复的元素
+ :point_right: 集合中的元素是无序的，不能通过索引下标获取元素
+ :point_right: 支持集合间的操作，可以取多个集合取交集、并集、差集

### 常用命令

1. SADD key member [member ...]：将一个或多个元素添加到集合中。

2. SMEMBERS key：获取集合中所有的成员（元素）。

3. SISMEMBER key member：检查一个元素是否是集合的成员。

4. SCARD key：获取集合的成员数量。

5. SREM key member [member ...]：从集合中移除一个或多个元素。

6. SPOP key [count]：随机移除并获取集合中一个或多个元素。

7. SRANDMEMBER key [count]：随机获取集合中一个或多个元素，但不移除它们。

8. SMOVE source destination member：将一个元素从源集合移动到目标集合。

9. SINTER key [key ...]：计算多个集合的交集。

10. SINTERSTORE destination key [key ...]：将多个集合的交集存储到新的集合中。

11. SUNION key [key ...]：计算多个集合的并集。

12. SUNIONSTORE destination key [key ...]：将多个集合的并集存储到新的集合中。

13. SDIFF key [key ...]：计算多个集合的差集。

14. SDIFFSTORE destination key [key ...]：将多个集合的差集存储到新的集合中。

15. SSCAN key cursor [MATCH pattern] [COUNT count]：迭代集合中的元素。

## ZSet

有序集合和集合有着必然的联系，保留了集合不能有重复成员的特性。

区别是，有序集合中的**元素是可以排序的**，它给每个元素设置一个分数，作为排序的依据。

> 有序集合中的元素不可以重复，但是 score 分数可以重复，就和一个班里的同学学号不能重复，但考试成绩可以相同。

### 常用命令

1. ZADD key score member [score member ...]：将一个或多个成员及其对应的分数添加到有序集合中。

2. ZRANGE key start stop [WITHSCORES]：按照元素的分数从低到高，获取有序集合中指定范围内的元素。如果使用 WITHSCORES 参数，还会返回元素的分数。

3. ZREVRANGE key start stop [WITHSCORES]：按照元素的分数从高到低，获取有序集合中指定范围内的元素。如果使用 WITHSCORES 参数，还会返回元素的分数。

4. ZRANGEBYSCORE key min max [WITHSCORES] [LIMIT offset count]：根据分数范围获取有序集合中的元素。可以指定最小和最大分数，并可选地使用 WITHSCORES 参数返回元素的分数，也可以使用 LIMIT 参数限制结果数量。

5. ZREVRANGEBYSCORE key max min [WITHSCORES] [LIMIT offset count]：根据分数范围从高到低获取有序集合中的元素。

6. ZCOUNT key min max：统计有序集合中分数在给定范围内的元素数量。

7. ZCARD key：获取有序集合中元素的数量。

8. ZSCORE key member：获取有序集合中指定成员的分数。

9. ZINCRBY key increment member：为有序集合中的指定成员增加分数。

10. ZREM key member [member ...]：从有序集合中移除一个或多个成员。

11. ZREMRANGEBYRANK key start stop：根据元素在有序集合中的排名范围，移除元素。

12. ZREMRANGEBYSCORE key min max：根据分数范围，移除有序集合中的元素。

13. ZRANK key member：获取有序集合中指定成员的排名（从低到高）。

14. ZREVRANK key member：获取有序集合中指定成员的排名（从高到低）。

15. ZSCAN key cursor [MATCH pattern] [COUNT count]：迭代有序集合中的元素。

## FAQ

### 分布式缓存

分布式缓存主要解决的是**单机缓存的容量受服务器限制并且无法保存通用的信息**
，因为，本地缓存只在当前服务里有效。比如部署了两个相同的服务，他们两者之间的缓存数据是无法共同的。

分布式缓存的话，使用的较多的较多的解决方案是是 Memcached 和 Redis。不过，随着近些年 Redis 的发展，大家慢慢都转而使用更加强大的 Redis 而放弃 Memcached。

### Redis 和 Memcached 的区别

#### 共同点

+ 都是基于内存的数据库。
+ 都有过期策略。
+ 两者的性能都非常高。

#### 区别

+ Redis 支持更丰富的数据类型，也就是说可以支持更复杂的应用场景。Redis 不仅仅支持简单的 k/v 类型的数据，同时还提供 `list`，`set`，`zset`，`hash` 等数据结构的存储。而 Memcached
  **只支持**最简单的 k/v 数据类型。
+ Redis 的容灾更好，支持数据的持久化，可以将内存中的数据保持在磁盘中，重启的时候可以再次加载进行使用，而 Memecache 把数据全部存在内存中。
+ Memcached 没有原生的集群模式，需要依靠客户端来实现往集群中分片写入数据，但是 Redis 目前是原生支持 cluster 模式的。
+ :warning:Redis 在服务器内存使用完之后，可以将不用的数据放到磁盘上。而 Memcached 在服务器内存使用完之后，就会直接报异常。
+ Memcached 是多线程，非阻塞 IO 复用的网络模型，Redis 使用单线程的多路 IO 复用模型（Redis 6.0 引入了多线程 IO ）。
+ Memcached 过期数据的删除策略只用了惰性删除，而 Redis 同时使用了惰性删除与定期删除。
+ Redis 支持发布订阅模型、Lua 脚本、事务等功能，而 Memcached 不支持。

### Redis 如何判断数据是否过期

Redis 通过一个叫做过期字典（可以看作是 hash 表）来保存数据过期的时间。过期字典的键指向 Redis 数据库中的某个key（键），过期字典的值是一个 long long 类型的整数，这个整数保存了 key 所指向的数据库键的过期时间（毫秒精度的 UNIX 时间戳）。

### 过期删除策略

如果 Redis 中一批 key 只能存活 1 分钟，那么 1 分钟后，Redis 是怎么对这批 key 进行删除的呢？

+ 惰性删除：只会在取出 key 的时候才对数据进行过期检查。这样对 CPU 最友好，但是**可能会造成太多过期 key 没有被删除**。
+ 定期删除：每隔一段时间抽取一批 key 执行删除过期 key 操作。Redis 底层会通过限制删除操作执行的时长和频率来减少删除操作对 CPU 时间的影响。

**定期删除对内存更加友好，惰性删除对 CPU 更加友好**。Redis 采用的是定期删除:heavy_plus_sign:惰性删除。

### 内存淘汰机制

我们通过给 key 设置过期时间还是有问题的，因为还是可能存在定期删除和惰性删除**漏掉**
了很多过期 key 的情况。这样就导致大量过期 key 堆积在内存里，然后就 OOM 了，Redis 的数据淘汰机制可以解决这个问题。

| 策略                | 说明                                                                         |
|-------------------|----------------------------------------------------------------------------|
| `volatile-lru`    | （least recently used），从已设置过期时间的数据集（`server.db[i].expires`）中挑选最近最少使用的数据淘汰   |
| `volatile-ttl`    | 从已设置过期时间的数据集（`server.db[i].expires`）中挑选将要过期的数据淘汰                           |
| `volatile-random` | 从已设置过期时间的数据集（`server.db[i].expires`）中任意选择数据淘汰                              |
| `allkeys-lru`     | （least recently used），当内存不足以容纳新写入数据时，在键空间中，移除最近最少使用的 key（这个是最常用的）          |
| `allkeys-random`  | 从数据集（`server.db[i].dict`）中任意选择数据淘汰                                         |
| `no-eviction`     | 禁止驱逐数据，也就是说当内存不足以容纳新写入数据时，新写入操作会报错:scream:。                                |
| `volatile-lfu`    | （least frequently used），从已设置过期时间的数据集(`server.db[i].expires`)中挑选最不经常使用的数据淘汰 |
| `allkeys-lfu`     | （least frequently used），当内存不足以容纳新写入数据时，在键空间中，移除最不经常使用的 key                 |

> LRU 是基于最近的**访问时间**来淘汰键，即淘汰最近最少被使用的键。
>
> LFU 是基于**访问频率**来淘汰键，即淘汰访问次数最少的键。

### 持久化机制

很多时候我们需要持久化数据也就是将内存中的数据写入到硬盘里面，大部分原因是为了备份数据，比如为了防止系统故障而将数据备份到一个另一台机器。

Redis 两种不同的持久化操作。一种持久化方式叫快照（snapshotting，RDB），另一种方式是只追加文件（append-only file, AOF）。

#### RDB

快照持久化是 Redis **默认采用**的持久化方式，在 Redis.conf 配置文件中默认有此下配置：

```
save 900 1     # 在 900 秒(15分钟)之后，如果至少有 1 个 key 发生变化，Redis 就会自动触发 BGSAVE 命令创建快照。
save 300 10    # 在 300 秒(5分钟)之后，如果至少有 10 个key发生变化，Redis 就会自动触发 BGSAVE 命令创建快照。
save 60 10000  # 在 60 秒(1分钟)之后，如果至少有 10000 个key发生变化，Redis 就会自动触发 BGSAVE 命令创建快照。
```

Redis 可以通过创建快照来获得存储在内存里面的数据在某个时间点上的副本。

Redis 创建快照之后，可以对快照进行备份，可以将快照复制到其他服务器从而创建具有相同数据的服务器副本，还可以将快照留在原地以便重启服务器的时候使用。

#### AOF

与快照持久化 RDB 相比，AOF 持久化 的**实时性更好**，基本已成为主流的持久化方案。**默认情况下 Redis 没有开启 AOF方式的持久化**。

开启 AOF 持久化后每执行一条会更改 Redis 中的数据的命令，Redis 就会将该命令写入硬盘中的 AOF 文件。AOF 文件的保存位置和 RDB 文件的位置相同，都是通过 dir 参数设置的，默认的文件名是 appendonly.aof。

Redis 的配置文件中存在三种不同的 AOF 持久化方式，它们分别是：

```
appendfsync always    # 每次有数据修改发生时都会写入 AOF 文件,这样会严重降低 Redis 的速度
appendfsync everysec  # 每秒同步一次，显示地将多个写命令同步到硬盘
appendfsync no        # 让操作系统决定何时进行同步
```

> 为了兼顾数据和写入性能，可以考虑 `appendfsync everysec` 选项 ，让 Redis 每秒同步一次 AOF 文件，Redis 性能几乎没受到任何影响。
> 这样即使出现系统崩溃，用户最多只会丢失一秒之内产生的数据。

## 参考

+ [Redis 命令参考](http://redisdoc.com/index.html)
+ [Redis(一)、Redis五种数据结构](https://www.cnblogs.com/haoprogrammer/p/11065461.html)
+ [Redis](https://blog.csdn.net/weixin_43230682/category_10241824.html)





