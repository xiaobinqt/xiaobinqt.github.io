---
title: "mysql where 和 having 的区别"
subtitle: ""

init_date: "2022-04-18T11:38:38+08:00"

date: 2018-07-05

lastmod: 2022-04-18

draft: false

author: "xiaobinqt"
description: "xiaobinqt,mysql where 和 having 的区别,what difference between where and having"

featuredImage: ""

reproduce: false

tags: ["mysql"]
categories: ["mysql"]
lightgallery: true

toc:
auto: false

math:
enable: true
---

<!-- author： xiaobinqt -->
<!-- email： xiaobinqt@163.com -->
<!-- https://xiaobinqt.github.io -->
<!-- https://www.xiaobinqt.cn -->

## 总览

where 是一个**约束声明**，在查询数据库的结果返回之前对数据库中的条件进行约束，**where 后面要跟的必须是数据表里真实存在的字段**，即在**结果返回之前起作用**。

那么为什么 where 后面不能写聚合函数这个问题也好理解了，因为聚合函数的列不是数据库表里的字段。

having 是一个**过滤声明**，是在查询数据库结果返回之后进行过滤，即在**结果返回值后起作用**。

那么为什么 having 后面可以写聚合函数也好理解了，因为 having 只是根据前面查询出来的是什么就可以后面接什么。

## 示例

### 示例 1

```sql
select *
from edge
where edge_id = '0104932b-8edc-4f2d-9d51-c0450867e373'; -- sql1 正确

select *
from edge
having edge_id = '0104932b-8edc-4f2d-9d51-c0450867e373'; -- sql2 正确
```

这 2 句 sql 的效果是一样的，sql1 用 where 过滤相当于在返回结果**前**过滤，sql2 用 having 过滤相当于在返回结果**后**过滤。

### 示例 2

```sql
select token name
from edge
where edge_id = '0104932b-8edc-4f2d-9d51-c0450867e373'; -- sql1 正确

select token name
from student
having edge_id = '0104932b-8edc-4f2d-9d51-c0450867e373'; -- sql2 错误
```

sql1 是正确的，表中存在 edge_id 这个字段可以过滤。

sql2 是错误的，因为 select **后**没有 edge_id 这个字段，所以不能过滤。

### 示例 3

```sql
select count(instance_id) as c, instance_id
from edge
group by instance_id
having c > 10; -- sql1 正确

select count(instance_id) as c, instance_id
from edge
where c > 10
group by instance_id; -- sql2 错误
```

sql1 是正确的，因为 c 在 select 的字段中是存在，是 `count(instance_id)` 的别名，所以这里写成 `having count(instance_id) > 10` 也是正确的。

sql2 是错误的，因为 c 这个字段在表中是不存在的，所以不能过滤，即使写成 `count(instance_id) > 10` 也是错误的。

## 总结

where 只能过滤数据库真实存在的字段，having 可以过滤 select 后的查询字段。

where 子句在分组前进行过滤，作用于每一条记录，where 子句过滤掉的记录将不包括在分组中。而 having 子句在数据分组后进行过滤，作用于整个分组。





