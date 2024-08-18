---
title: "sqlite 常用命令"
subtitle: ""

init_date: "2024-08-18T13:08:47+08:00"

date: 2024-08-18

lastmod: 2024-08-18

draft: false

author: "xiaobinqt"
description: "xiaobinqt,"

featuredImage: ""

featuredImagePreview: ""

reproduce: false

translate: false

tags: ["sqlite"]
categories: ["开发者手册"]
lightgallery: true

series: []

series_weight:

toc: true

math: true
---

<!-- author： xiaobinqt -->
<!-- email： xiaobinqt@163.com -->
<!-- https://xiaobinqt.github.io -->
<!-- https://www.xiaobinqt.cn -->

## 安装/连接

关于 sqlite 的安装可以参考 [SQLite 安装](https://www.runoob.com/sqlite/sqlite-installation.html)。

![查看版本](https://cdn.xiaobinqt.cn/xiaobinqt.io/20240818/c3e3f409af4c48e48456d29a3cb9044a.png '查看版本')

## 常用命令

```shell
sqlite3 # 进入 sqlite
sqlite3 mytest # 连接数据库，不存在新建
> .databases # 显示数据库名称及对应文件
main: /Users/weibin/mytest r/w

sqlite3 /path/to/your/database.db # 以在启动 SQLite 时通过指定数据库文件的路径来设置保存位置

> .output FILE # 将输出定向到 FILE
> .show # 显示已经设置的值
> .dump # 以 SQL 格式 dump 数据库
> .dump users # dump 某张表
> .backup FILE # 备份数据库到文件
> .quit       # 退出

> .table # 查看所有的表
users books
> .schema users # 显示CREATE语句
CREATE TABLE users(name text PRIMARY KEY, age integer);
> .import FILE TABLE # 将文件的数据导入到表中。

> .head ON  # 查询时显示列名称
> select * from users
name|age
Tom|18
Jack|20

> .mode line # 每一列单独占一行

> .mode column # 将每一列数据对齐显示，适合小型数据集的表格展示
```

![新建库表](https://cdn.xiaobinqt.cn/xiaobinqt.io/20240818/578cf73c14634ba6bd0c05b2d8dd99cf.png '新建库表')

![常用查询设置](https://cdn.xiaobinqt.cn/xiaobinqt.io/20240818/cf4a02a5f5244ddbac3e1b02f61df018.png '常用查询设置')


## 常用语句

```sql
CREATE TABLE tab_name (
   col1 col1_type PRIMARY KEY,
   col2 INTEGER AUTOINCREMENT,
   col3 col3_type NOT NULL,
   .....
   colN colN_type,
);

/* 常用类型：
TEXT 字符串, CHAR(100) 固长字符串
INTEGER 整型, BIGINT 长整型, REAL 实数,
BOOL 布尔值
BLOB 二进制
DATETIME 时间

PRIMARY KEY 标记主键，NOT NULL标记非空。AUTOINCREMENT 自增，只能用于整型。

CREATE TABLE users (
   id INTEGER primary key AUTOINCREMENT,
   name char(20) not null,
   age INTEGER,
   address char(100)
);

*/

```

### 新增

```sql
-- 单条
INSERT INTO tab_name VALUES (xx, xx)
-- 指定列名
    INSERT INTO tab_name (col1, col3) VALUES (xx, xx)
-- 多条
INSERT INTO tab_name (col1, col2, col3) VALUES
    (xx, xx, xx),
    ...
    (xx, xx, xx);
```

### 删除/更新表

```sql
-- 删除表
DROP TABLE tab_name;
-- 新增列
ALTER TABLE ADD COLUMNS col_name col_type;

-- 重命名表
ALTER TABLE old_tab RENAME TO new_tab

-- 重命名列名(3.25.0+)
ALTER TABLE tab_name RENAME COLUMN old_col TO new_col

```

### 查询

```sql
-- 所有列
SELECT * FROM tab_name;
-- 去除重复
SELECT DISTINCT col1 FROM tab_name;
-- 统计个数
SELECT COUNT(*) FROM tab_name
-- 指定列
SELECT col1, col2 FROM table_name;
-- 带查询条件 >、<、=、LIKE、NOT、AND、OR 等
SELECT * FROM table_name WHERE col2 >= 18;
SELECT * FROM table_name
    WHERE col2 >= 18 AND col1 LIKE %stu%;
-- 限制数量
SELECT * FROM table_name LIMIT 1;
-- GROUP BY
SELECT col1, count(*) FROM tab_name
    WHERE [ conditions ]
    GROUP BY col1
-- Having
SELECT col1, count(*) FROM tab_name
    WHERE [ conditions ]
    GROUP BY col1
    HAVING [ conditions ]
-- 排序, DESC 降序，ASC 升序
SELECT * FROM table_name ORDER BY col2 DESC;
```

### 删除/更新

```sql
-- 删除满足条件的记录
DELETE FROM tab_name WHERE condition;
-- 更新记录
UPDATE tab_name SET col1=value1, col2=value2
-- 更新满足条件的记录
UPDATE tab_name
    SET col1=value1, col2=value2
    WHERE [ conditions ]

```

### 事务

```sql
-- 提交
BEGIN;
INSERT INTO ...
...
COMMIT;

-- 回滚
BEGIN;
...
ROLLBACK;
```

## 输出模式

```sql
> .mode csv # 设置输出模式为 csv
> select * from users
name,age
Tom,18
Jack,20
```
