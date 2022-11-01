# mysql 常见问题

<!-- author： xiaobinqt -->

<!-- email： xiaobinqt@163.com -->

<!-- https://xiaobinqt.github.io -->

<!-- https://www.xiaobinqt.cn -->

## 主键和 `UNIQUE` 的区别

主键和`UNIQUE`约束都能保证某个列或者列组合的唯一性，但是：

+ 一张表中只能定义一个主键，却可以定义多个`UNIQUE`约束！
+ 主键列不允许存放`NULL`，而声明了`UNIQUE`属性的列可以存放`NULL`，而且`NULL`可以重复地出现在多条记录中。

## 结束符

```shell
delimiter EOF  # 将结束符改为 EOF
```

![修改结束符](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220419/fdd2e38117284a7f8b46ba3af60c26c9.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 "修改结束符")

由:point_up:图可知，将默认的结束符从 `;` 改为 `EOF`。

## 什么是外键

如果`A`表中的某个列或者某些列依赖与`B`表中的某个列或者某些列，那么就称`A`表为子表，`B`表为父表。子表和父表可以使用外键来关联起来。

**父表中被子表依赖的列或者列组合必须建立索引**，如果该列或者列组合已经是主键或者有`UNIQUE`属性，那么也就被默认建立了索引。

定义外键的语法：

```sql
CONSTRAINT [外键名称] FOREIGN KEY(列1, 列2, ...) REFERENCES 父表名(父列1, 父列2, ...);
```

### 示例

```sql
CREATE TABLE student_score
(
    number  INT, -- 学号
    subject VARCHAR(30),
    score   TINYINT,
    PRIMARY KEY (number, subject),
    CONSTRAINT FOREIGN KEY (number) REFERENCES student_info (number)
);
```

:point_up: 如上，在对`student_score`表插入数据的时候，MySQL都会检查插入的学号是否能在`student_info`
表中找到，如果找不到则会报错，因为`student_score`表中的`number`
列依赖于`student_info`表的`number`列，也就是，如果没有这个学生，何来成绩？

## ZEROFILL

对于**无符号整数类型**的列，可以在查询数据的时候让数字左边补 0，如果想实现这个效果需要给该列加一个`ZEROFILL`属性：

```sql
CREATE TABLE zerofill_table
(
    i1 INT(10) UNSIGNED ZEROFILL,
    i2 INT UNSIGNED
);
```

INT后边的`(5)`，这个 5 就是显示宽度，默认是10，也就是 `INT` 也 `INT(10)` 效果是一样的。

### 注意

+ 该列必须是整数类型
+ 该列必须有 `UNSIGNED ZEROFILL`的属性
+ 该列的实际值的位数必须小于显示宽度
+ 在创建表的时候，如果声明了`ZEROFILL`属性的列没有声明`UNSIGNED`属性，MySQL会为该列自动生成`UNSIGNED`属性
+ **显示宽度并不会影响实际类型的实际存储空间**
+ 对于没有声明`ZEROFILL`属性的列，显示宽度没有任何作用，只有在查询声明了`ZEROFILL`属性的列时，显示宽度才会起作用，否则可以忽略显示宽度这个东西的存在。

## limit、offset 区别

> 从 0 开始计数，第1条记录在 MYSQL 中是第 0 条。

limit 和 offset 都可以用来限制查询条数，一般用做分页。

+ 当 limit 后面跟一个参数的时候，该参数表示要取的数据的数量

```sql
select*
from user limit 3 
```

表示直接取前三条数据。

+ 当 limit 后面跟两个参数的时候，第一个数表示**开始行**，后一位表示要取的数量，例如

```sql
select *
from user limit 1,3;
```

从 0 行开始计算，取第 1 - 3 条数据，也就是取 1,2,3 三条数据。

+ 当 limit 和 offset 组合使用的时候，limit 后面只能有一个参数，表示要取的的数量，offset 表示开始行。

```sql
select *
from user limit 3
offset 1;
```

从 0 行开始计算，取第 1 - 3 条数据，也就是取 1,2,3 三条数据。

## 常用函数

### 文本处理函数

| 名称        | 调用示例                      | 示例结果    | 描述                                   |
| ----------- | ----------------------------- | ----------- | -------------------------------------- |
| `LEFT`      | `LEFT('abc123', 3)`           | `abc`       | 给定字符串从左边取指定长度的子串       |
| `RIGHT`     | `RIGHT('abc123', 3)`          | `123`       | 给定字符串从右边取指定长度的子串       |
| `LENGTH`    | `LENGTH('abc')`               | `3`         | 给定字符串的长度                       |
| `LOWER`     | `LOWER('ABC')`                | `abc`       | 给定字符串的小写格式                   |
| `UPPER`     | `UPPER('abc')`                | `ABC`       | 给定字符串的大写格式                   |
| `LTRIM`     | `LTRIM(' abc')`               | `abc`       | 给定字符串左边空格去除后的格式         |
| `RTRIM`     | `RTRIM('abc ')`               | `abc`       | 给定字符串右边空格去除后的格式         |
| `SUBSTRING` | `SUBSTRING('abc123', 2, 3)`   | `bc1`       | 给定字符串从指定位置截取指定长度的子串 |
| `CONCAT `   | `CONCAT('abc', '123', 'xyz')` | `abc123xyz` | 将给定的各个字符串拼接成一个新字符串   |

### 时间处理函数

| 名称          | 调用示例                                          | 示例结果              | 描述                                                         |
| ------------- | ------------------------------------------------- | --------------------- | ------------------------------------------------------------ |
| `NOW`         | `NOW()`                                           | `2019-08-16 17:10:43` | 返回当前日期和时间                                           |
| `CURDATE`     | `CURDATE()`                                       | `2019-08-16`          | 返回当前日期                                                 |
| `CURTIME`     | `CURTIME()`                                       | `17:10:43`            | 返回当前时间                                                 |
| `DATE`        | `DATE('2019-08-16 17:10:43')`                     | `2019-08-16`          | 将给定日期和时间值的日期提取出来                             |
| `DATE_ADD`    | `DATE_ADD('2019-08-16 17:10:43', INTERVAL 2 DAY)` | `2019-08-18 17:10:43` | 将给定的日期和时间值添加指定的时间间隔                       |
| `DATE_SUB`    | `DATE_SUB('2019-08-16 17:10:43', INTERVAL 2 DAY)` | `2019-08-14 17:10:43` | 将给定的日期和时间值减去指定的时间间隔                       |
| `DATEDIFF`    | `DATEDIFF('2019-08-16', '2019-08-17')`            | `-1`                  | 返回两个日期之间的天数（负数代表前一个参数代表的日期比较小） |
| `DATE_FORMAT` | `DATE_FORMAT(NOW(),'%m-%d-%Y')`                   | `08-16-2019`          | 用给定的格式显示日期和时间                                   |

常见时间单位

| 时间单位      | 描述 |
| ------------- | ---- |
| `MICROSECOND` | 毫秒 |
| `SECOND`      | 秒   |
| `MINUTE`      | 分钟 |
| `HOUR`        | 小时 |
| `DAY`         | 天   |
| `WEEK`        | 星期 |
| `MONTH`       | 月   |
| `QUARTER`     | 季度 |
| `YEAR`        | 年   |

### 数值处理函数

| 名称   | 调用示例      | 示例结果             | 描述               |
| ------ | ------------- | -------------------- | ------------------ |
| `ABS`  | `ABS(-1)`     | `1`                  | 取绝对值           |
| `Pi`   | `PI()`        | `3.141593`           | 返回圆周率         |
| `COS`  | `COS(PI())`   | `-1`                 | 返回一个角度的余弦 |
| `EXP`  | `EXP(1)`      | `2.718281828459045`  | 返回e的指定次方    |
| `MOD`  | `MOD(5,2)`    | `1`                  | 返回除法的余数     |
| `RAND` | `RAND()`      | `0.7537623539136372` | 返回一个随机数     |
| `SIN`  | `SIN(PI()/2)` | `1`                  | 返回一个角度的正弦 |
| `SQRT` | `SQRT(9)`     | `3`                  | 返回一个数的平方根 |
| `TAN`  | `TAN(0)`      | `0`                  | 返回一个角度的正切 |

## COUNT 函数

COUNT函数使用来统计**行数**的，有下边两种使用方式：

+ `COUNT(*)`：对表中行的数目进行计数，不管列的值是不是NULL。
+ `COUNT(列名)`：对特定的列进行计数，会忽略掉该列为NULL的行。

**两者的区别是会不会忽略统计列的值为NULL的行**。

## 查询

`where` 竟然可以这么写:innocent:

```sql
select *
from edge
where (ip, mode) = ('192.168.50.101', 2);
```

`in` 竟然可以这么写:joy:

```sql
select *
from edge
where (ip, mode) in (select '192.168.50.101', 2);
```

## 判断语句

### if then

```shell
IF 表达式 THEN
    处理语句列表
[ELSEIF 表达式 THEN
    处理语句列表]
... # 这里可以有多个ELSEIF语句
[ELSE
    处理语句列表]
END IF;
```

### case when

```shell
CASE WHEN 表达式 THEN 处理语句
    else 表达式 end 
  
## 或者  
CASE when 表达式 then 处理语句
    when 表达式 then 处理语句
    ... 可以与多个 when 表达式 then 处理语句
   END
```

示例：

```shell
select *, 
	CASE WHEN name='大彬' THEN '角色1' 
    else '角色2' end as processed_name ,
    case when status = 1 then '已处理'
    when status = 0 then '未处理'
    when status = 2 then '待处理' end as processed_status
    from user;
```

## 循环语句

### WHILE

```shell
WHILE 表达式 DO
    处理语句列表
END WHILE;
```

### REPEAT

```shell
REPEAT
    处理语句列表
UNTIL 表达式 END REPEAT;
```

### LOOP

```shell
LOOP
    处理语句列表
END LOOP;
```

在使用 `LOOP` 时可以使用`RETURN`语句直接让函数结束就可以达到停止循环的效果，也可以使用`LEAVE`语句，不过使用`LEAVE`
时，需要先在`LOOP`语句前边放置一个所谓的标记。

```shell
CREATE FUNCTION sum_all(n INT UNSIGNED)
RETURNS INT
BEGIN
    DECLARE result INT DEFAULT 0;
    DECLARE i INT DEFAULT 1;
    flag:LOOP
        IF i > n THEN
            LEAVE flag;
        END IF;
        SET result = result + i;
        SET i = i + 1;
    END LOOP flag;
    RETURN result;
END
```

:point_up:示例中，在`LOOP`语句前加了一个`flag:`，相当于为这个循环打了一个名叫`flag`的标记，然后在对应的`END LOOP`
语句后边也把这个标记名`flag`
给写上了。在存储函数的函数体中使用`LEAVE flag`语句来结束`flag`这个标记所代表的循环。

> 标记主要是为了可以跳到指定的语句中

## DUPLICATE KEY UPDATE

对于**主键**或者有**唯一性约束**
的列或列组合来说，新插入的记录如果和表中已存在的记录重复的话，我们可以选择的策略不仅仅是忽略（`INSERT IGNORE`
）该条记录的插入，也可以选择更新这条重复的旧记录。

```sql
CREATE TABLE `t`
(
    `idt`   int(11) NOT NULL AUTO_INCREMENT,
    `phone` char(11)    DEFAULT NULL,
    `name`  varchar(45) DEFAULT NULL,
    PRIMARY KEY (`idt`),
    UNIQUE KEY `idt_UNIQUE` (`idt`),
    UNIQUE KEY `phone_UNIQUE` (`phone`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8
```

如上表，`idt` 是唯一主键，`phone` 是 UNIQUE 唯一约束。

![图1](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220419/1ba316643e874fcb9e90dcaa9b333f60.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 "图1")

表里有条记录 `phone = 15212124125`，`name = '吴彦祖'`，现在再添加一条记录，phone 跟 `name = '吴彦祖'`
是一样的，但是 `name='宋江'`

```sql
INSERT INTO t (phone, name)
VALUES ('15212124125', '宋江') ON DUPLICATE KEY
UPDATE name = '宋江';

-- 对于批量插入可以这么写，`VALUES(列名)`的形式来引用待插入记录中对应列的值
INSERT INTO t (phone, name)
VALUES ('15212124125', '宋江'),
       ('15212124126', '李逵') ON DUPLICATE KEY
UPDATE name =
VALUES (`name`);
```

结果：

![图2](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220419/6998e509ee9f4c3eacb72f9c5b42080b.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 "图2")

由结果可知，phone 电话的值没有改变，但是 name 被修改成了宋江。

也就是说，如果 `t` 表中已经存在 `phone` 的列值为 `15212124125` 的记录（因为 `phone`列具有`UNIQUE`
约束），那么就把该记录的 `name`列更新为`'宋江'`。

对于那些是主键或者具有UNIQUE约束的列或者列组合来说，如果表中已存在的记录中有与待插入记录在这些列或者列组合上重复的值，我们可以使用VALUES(
列名)的形式来引用待插入记录中对应列的值

## 自定义变量

### 单个变量

设置单个变量可以使用 `SET` 关键字。

![设置单个变量](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220419/7d7a7bc57efa43e1ba30412b76c53917.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 "设置单个变量")

### 多个变量

设置多个变量可以使用 `INTO` 关键字。

![设置多个变量](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220419/9c894c060ac34628abd1b9071d4e7e27.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 "设置多个变量")

## innodb 和 myisam 的区别

+ innodb 支持事务，而 myisam 不支持事务。
+ innodb 支持外键，而 myisam 不支持外键。
+ innodb 默认表锁，使用索引检索条件时是行锁，而myisam是表锁（每次更新增加删除都会锁住表）。
+ innodb 和 myisam 的索引都是基于b+树，但他们具体实现不一样，innodb 的 `b+` 树的叶子节点是存放数据的，myisam 的 `b+`
  树的叶子节点是存放指针的。
+ innodb 是聚簇索引，必须要有主键，一定会基于主键查询，但是辅助索引就会查询两次，myisam是非聚簇索引，索引和数据是分离的，索引里保存的是数据地址的指针，主键索引和辅助索引是分开的。
+ innodb 不存储表的行数，所以`select count(*)`的时候会全表查询，而 myisam 会存放表的行数，`select count(*）`的时候会查的很快。

总结：mysql 默认使用 innodb，如果要用事务和外键就使用 innodb，如果这张表只用来查询，可以用 myisam。如果更新删除增加频繁就使用
innodb。

## 索引

### 功能逻辑

#### 唯一索引

指索引中的索引节点值不允许重复，一般配合唯一约束使用。

#### 主键索引

主键索引是一种特殊的唯一索引，和普通唯一索引的区别在于不允许有空值。

#### 普通索引

通过`KEY`、`INDEX`关键字创建的索引就是这个类型，没什么限制，就是单纯的可以让查询快一点。

#### 全文索引

在 5.7 版本之前，只有 MyISAM 引擎支持。

全文索引只能创建在`CHAR`、`VARCHAR`、`TEXT`等这些文本类型字段上，而且使用全文索引查询时，条件字符数量必须**大于** 3
才生效。如果想要创建出的全文索引支持中文，需要在最后指定解析器：`with parser ngram`。

具体的使用可以参看 [全文索引的创建与使用](https://juejin.cn/post/7147609139974242317#heading-16)

### 存储方式

#### 聚簇索引

在聚簇索引中，索引数据和表数据在磁盘中的位置是一起的。

一张表中只能存在一个聚簇索引，一般都会选用主键作为聚簇索引。

一般聚簇索引要求索引必须是非空唯一索引才行。

#### 非聚簇索引

在非聚簇索引中，索引节点和表数据之间用物理地址的方式维护两者的联系。

### 回表

参看 [索引查询时的回表问题](https://juejin.cn/post/7149074488649318431#heading-9)

### 建立原则

+ 经常频繁用作查询条件的字段应酌情考虑为其创建索引。
+ 表的主外键或连表字段，必须建立索引，因为能很大程度提升连表查询的性能。
+ 建立索引的字段，一般值的区分性要足够高，这样才能提高索引的检索效率。
+ 建立索引的字段，值不应该过长，如果较长的字段要建立索引，可以选择前缀索引。
+ 建立联合索引，应当遵循最左前缀原则，将多个字段之间按优先级顺序组合。
+ 经常根据范围取值、排序、分组的字段应建立索引，因为索引有序，能加快排序时间。
+ 对于唯一索引，如果确认不会利用该字段排序，那可以将结构改为`Hash`结构。
+ 尽量使用联合索引代替单值索引，联合索引比多个单值索引查询效率要高。

### 注意点

+ 值经常会增删改的字段，不合适建立索引，因为每次改变后需维护索引结构。
+ 一个字段存在大量的重复值时，不适合建立索引，比如之前举例的性别字段。
+ 索引不能参与计算，因此经常带函数查询的字段，并不适合建立索引。
+ 一张表中的索引数量并不是越多越好，一般控制在**3**，最多不能超过**5**。
+ 建立联合索引时，一定要考虑优先级，查询频率最高的字段应当放首位。
+ 当表的数据较少，不应当建立索引，因为数据量不大时，维护索引反而开销更大。
+ 索引的字段值无序时，不推荐建立索引，因为会造成页分裂，尤其是主键索引。

### 正确使用

+ 查询 SQL 中尽量不要使用`OR`关键字，可以使用多 SQL 或子查询代替。
+ 模糊查询尽量不要以`%`开头，如果实在要实现这个功能可以建立全文索引。
+ :warning:编写 SQL 时一定要注意字段的数据类型，否则 MySQL 的隐式转换会导致索引失效。
+ 一定不要在编写 SQL 时让索引字段执行计算工作，尽量将计算工作放在客户端中完成。
+ 对于索引字段尽量不要使用计算类函数，一定要使用时请记得将函数计算放在`=`后面。
+ 多条件的查询 SQL 一定要使用联合索引中的第一个字段，否则会打破最左匹配原则。
+ 对于需要对比多个字段的查询业务时，可以拆分为连表查询，使用临时表代替。
+ 在 SQL 中不要使用反范围性的查询条件，大部分反范围性、不等性查询都会让索引失效。

### 索引失效

哪些情况下会导致索引失效，参看 [索引失效的一些场景](https://juejin.cn/post/7149074488649318431#heading-15)

### 索引覆盖，索引下推，MRR

要查询的列，在使用的索引中已经包含，被所使用的索引覆盖，这种情况称之为索引覆盖。

参看 [索引覆盖，索引下推，MRR](https://juejin.cn/post/7149074488649318431#heading-25)

### 索引为何选择 B+Tree

为什么 mysql 选择 B+Tree
作为索引的数据结构。参看[索引为何要选择B+Tree？](https://juejin.cn/post/7151275584218202143#heading-8)

## Explain

参看 [执行分析工具 - ExPlain](https://juejin.cn/post/7149074488649318431#heading-14)

## 事务

### 事务的 ACID 原则

+ `A/Atomicity`：原子性
+ `C/Consistency`：一致性
+ `I/Isolation`：独立性/隔离性
+ `D/Durability`：持久性

+ 原子性要求事务中所有操作要么全部成功，要么全部失败，这点是基于`undo-log`来实现的，因为在该日志中会生成相应的反
  SQL，执行失败时会利用该日志来回滚所有写入操作。
+ 持久性要求的是所有 SQL 写入的数据都必须能落入磁盘存储，确保数据不会丢失，这点则是基于`redo-log`实现的。
+ 隔离性的要求是一个事务不会受到另一个事务的影响，对于这点则是通过锁机制和 MVCC 机制实现的，只不过 MySQL 屏蔽了加锁和 MVCC
  的细节。
+ 一致性要求数据库的整体数据变化，只能从一个一致性状态变为另一个一致性状态，其实前面的原子性、持久性、隔离性都是为了确保这点而存在的。

+ `undo-log`：主要记录 SQL 的撤销日志，比如目前是`insert`语句，就记录一条`delete`日志。
+ `redo-log`：记录当前 SQL 归属事务的状态，以及记录修改内容和修改页的位置。
+ `bin-log`：记录每条 SQL 操作日志，只要是用于数据的主从复制与数据恢复/备份。

### 两阶段提交

redo log 保证的是数据库的 crash-safe 能力。采用的策略就是常说的“两阶段提交”。

一条 update 的 SQL 语句是按照这样的流程来执行的：

将数据页加载到内存 → 修改数据 → 更新数据 → 写redo log（状态为prepare） → 写binlog → 提交事务（数据写入成功后将redo
log状态改为commit）

只有当两个日志都提交成功（刷入磁盘），事务才算真正的完成。

一旦发生系统故障（不管是宕机、断电、重启等等），都可以配套使用 redo log 与 binlog 做数据修复。

| binlog状态 | redo log 状态 | 对策 |
| ---- | ---- | ---- |
| 有记录 |	commit	|事务已经正常完成 |
| 有记录 |	prepare	|在binlog写完、提交事务之前发生故障。此时数据完整。恢复策略：提交事务|
| 无记录 |	prepare	|在binglog写完之前发生故障。恢复策略：回滚|
| 无记录 |	无记录	|在写redo log之前发生故障。恢复策略：回滚|

### 脏读、幻读、不可重复读

参考 [脏读、幻读、不可重复读问题](https://juejin.cn/post/7152765784299667487#heading-10)

脏读：指一个事务读到了其他事务还未提交的数据，也就是当前事务读到的数据，由于还未提交，因此有可能会回滚。

幻读：另外一个事务在第一个事务要处理的目标数据范围之内新增了数据，然后先于第一个事务提交造成的问题。

> 幻读是对自己来说的，比如，事务 A 在对表中多行数据进行修改，将性别「男、女」改为「0、1」，此时事务 B 又插入了一条性别为男的数据，
> 当事务 A 提交后，再次查询表时，会发现表中依旧存在一条性别为男的数据。

### 事务的隔离级别

1. Read uncommitted/RU：读未提交，处于该隔离级别的数据库，脏读、不可重复读、幻读问题都有可能发生。

2. Read committed/RC：读已提交，处于该隔离级别的数据库，解决了脏读问题，不可重复读、幻读问题依旧存在。

3. Repeatable read/RR：可重复读，处于该隔离级别的数据库，解决了脏读、不可重复读问题，幻读问题依旧存在。

4. Serializable：序列化/串行化，处于该隔离级别的数据库，解决了脏读、不可重复读、幻读问题都不存在。

上述四个级别，越靠后并发控制度越高，也就是在多线程并发操作的情况下，出现问题的几率越小，但对应的也性能越差，MySQL 的事务隔离级别，
默认为第三级别：`Repeatable read`可重复读。

## 参考

+ [建立索引的正确姿势与使用索引的最佳指南](https://juejin.cn/post/7149074488649318431)
+ [MySQL的redo log、undo log、binlog](https://blog.csdn.net/shudaqi2010/article/details/122744651)

