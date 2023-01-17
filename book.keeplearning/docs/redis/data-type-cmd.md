---
weight: 1

bookFlatSection: true

bookCollapseSection: false

bookToc: true

title: "数据类型和常用命令"
---

# 数据类型和常用命令

## 数据类型

| 数据类型   | 可以存储的值      | 操作                                                             |
|--------|-------------|----------------------------------------------------------------|
| STRING | 字符串、整数或者浮点数 | 对整个字符串或者字符串的其中一部分执行操作<br> 对整数和浮点数执行自增或者自减操作                    |
| LIST   | 列表          | 从两端压入或者弹出元素 <br> 对单个或者多个元素进行修剪，<br> 只保留一个范围内的元素                |
| SET    | 无序集合        | 添加、获取、移除单个元素<br> 检查一个元素是否存在于集合中<br> 计算交集、并集、差集<br> 从集合里面随机获取元素 |
| HASH   | 包含键值对的无序散列表 | 添加、获取、移除单个键值对</br> 获取所有键值对<br> 检查某个键是否存在                       |
| ZSET   | 有序集合        | 添加、获取、删除元素</br> 根据分值范围或者成员来获取元素<br> 计算一个键的排名                   |

## STRING

<div align="center"> <img src="https://cdn.xiaobinqt.cn/xiaobinqt.io/20221223/4cd2f8dfd39c41b0a14a9f8cad3d9ee7.png" width="400"/> </div><br>

```html
> set hello world
OK
> get hello
"world"
> del hello
(integer) 1
> get hello
(nil)
```

## LIST

<div align="center"> <img src="https://cdn.xiaobinqt.cn/xiaobinqt.io/20221223/dc2b3cf5d03b41119a00820944579611.png" width="400"/> </div><br>

```html
> rpush list-key item
(integer) 1
> rpush list-key item2
(integer) 2
> rpush list-key item
(integer) 3

> lrange list-key 0 -1
1) "item"
2) "item2"
3) "item"

> lindex list-key 1
"item2"

> lpop list-key
"item"

> lrange list-key 0 -1
1) "item2"
2) "item"
```

## SET

<div align="center"> <img src="https://cdn.xiaobinqt.cn/xiaobinqt.io/20221223/9352e7d62d574d7a8c4287d7b326fb08.png" width="400"/> </div><br>

```html
> sadd set-key item
(integer) 1
> sadd set-key item2
(integer) 1
> sadd set-key item3
(integer) 1
> sadd set-key item
(integer) 0

> smembers set-key
1) "item"
2) "item2"
3) "item3"

> sismember set-key item4
(integer) 0
> sismember set-key item
(integer) 1

> srem set-key item2
(integer) 1
> srem set-key item2
(integer) 0

> smembers set-key
1) "item"
2) "item3"
```

## HASH

<div align="center"> <img src="https://cdn.xiaobinqt.cn/xiaobinqt.io/20221223/786b12641c13468b920d52f674ca1e4d.png" width="400"/> </div><br>

```html
> hset hash-key sub-key1 value1
(integer) 1
> hset hash-key sub-key2 value2
(integer) 1
> hset hash-key sub-key1 value1
(integer) 0

> hgetall hash-key
1) "sub-key1"
2) "value1"
3) "sub-key2"
4) "value2"

> hdel hash-key sub-key2
(integer) 1
> hdel hash-key sub-key2
(integer) 0

> hget hash-key sub-key1
"value1"

> hgetall hash-key
1) "sub-key1"
2) "value1"
```

## ZSET

<div align="center"> <img src="https://cdn.xiaobinqt.cn/xiaobinqt.io/20221223/dc2c35b63788455e9a80310b3cd9a33a.png" width="400"/> </div><br>

```html
> zadd zset-key 728 member1
(integer) 1
> zadd zset-key 982 member0
(integer) 1
> zadd zset-key 982 member0
(integer) 0

> zrange zset-key 0 -1 withscores
1) "member1"
2) "728"
3) "member0"
4) "982"

> zrangebyscore zset-key 0 800 withscores
1) "member1"
2) "728"

> zrem zset-key member1
(integer) 1
> zrem zset-key member1
(integer) 0

> zrange zset-key 0 -1 withscores
1) "member0"
2) "982"
```
