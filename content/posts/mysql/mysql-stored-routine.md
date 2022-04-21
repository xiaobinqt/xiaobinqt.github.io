---
title: "mysql 存储程序"
subtitle: ""

init_date: "2022-04-20T13:45:47+08:00"

date: 2020-10-08

lastmod: 2022-04-20

draft: false

author: "xiaobinqt"
description: "xiaobinqt,mysql 存储程序,mysql 存储函数,存储过程,触发器,事件,mysql 游标,什么是游标,mysql 局部变量和自定义变量"

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

![存储程序](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220419/e92bc705bec14bcba089f2a8848359b2.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '存储程序')

存储程序可以封装一些语句，然后给用户提供一种简单的方式来调用这个存储程序，从而间接地执行某些语句。根据调用方式的不同，可以把存储程序分为`存储例程`、`触发器`和`事件`，存储例程又分为`存储函数`和`存储过程`，如:point_up:
上图。

## 存储函数

存储函数**只有一个返回值**，可以从 mysql 内置的函数理解，所有 mysql 内置的函数都是只有一个返回值，比如：

![mysql 内置函数](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220420/b1bfc8c3ac9a45dea2dfdc1fb901e54f.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'mysql 内置函数')

存储函数很好理解，就是一个函数，跟普通函数一样有`函数名`，`函数体`，`参数列表`和`返回值`。创建存储函数语句如下：

```sql
CREATE FUNCTION 存储函数名称([参数列表])
    RETURNS 返回值类型
BEGIN
    函数体内容
END
```

| CMD                                          | 说明        |
|----------------------------------------------|-----------|
| `SHOW FUNCTION STATUS [LIKE 需要匹配的函数名]`    | 查看所有存储函数  |
| `SHOW CREATE FUNCTION 函数名`                   | 查看某个存储函数  |
| `DROP FUNCTION 函数名`                          | 删除某个存储函数  |

### 示例

现在写一个存储函数，输入用户名 `name`，返回用户手机号 `phone`：

```sql
CREATE FUNCTION get_phone(qname VARCHAR (45))
    RETURNS VARCHAR(11)
BEGIN
RETURN (SELECT phone
        from t
        where name = qname);
END EOF
```

存储函数的调用跟普通函数的调用也是一样的:point_down:

![效果](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220419/fbbd1bb4c54341368ccda472619df5d2.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '效果')

## 局部变量和自定义变量

在存储函数中可以使用局部变量和自定义变量，二者的区别是，局部变量用 `DECLARE` 申明，不用加 `@`符，局部变量随着函数调用结束，变量销毁且只能在存储函数中使用。自定义变量需要加 `@` 符，且可以在函数外调用。

```shell
CREATE FUNCTION get_phone(qname VARCHAR (45))
    RETURNS VARCHAR(11)
BEGIN
    DECLARE ph varchar(11) default ""; # 局部变量
    SET @ii = 100; # 自定义变量
    SET ph = (select phone from t where name = qname); # 给局部变量赋值

    RETURN  ph ;
END EOF

```

![局部变量和自定义变量](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220419/40c4689ff9214887a6cfd46c761df53d.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '局部变量和自定义变量')

:point_up: 可知，在存储函数`get_phone`中有一个局部变量 `ph`和自定义变量 `@ii`，函数调用结束后 `@ii` 被赋值为`100` 且可以在函数执行完后访问，但是 `@ph` 是空的。

## 存储过程

存储函数侧重于执行某些语句并**返回一个值**，而存储过程更侧重于单纯的去执行这些语句。存储过程的定义**不需要声明返回值类型**。

```sql
CREATE PROCEDURE 存储过程名称([参数列表])
BEGIN
    需要执行的语句
END
```

调用存储过程使用 `CALL` 关键字。

| CMD                                           | 说明       |
|-----------------------------------------------|----------|
| `SHOW PROCEDURE STATUS [LIKE 需要匹配的存储过程名称]`    | 查看所有存储过程 |
| `SHOW CREATE PROCEDURE 存储过程名称`                | 查看某个存储过程 |
| `DROP PROCEDURE 存储过程名称`                       | 删除某个存储过程 |

### 示例

以下示例定义了一个 `my_operate` 的存储过程：

```shell
CREATE PROCEDURE my_operate(pname varchar (45))
BEGIN
     SELECT * FROM t;
     INSERT INTO t(phone, name) VALUES("15214254125", "卢俊义");
     SELECT * FROM t;
     SELECT * from t where name = pname;
END EOF
```

![存储过程](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220419/283408a351b74a758648f47b08fa347c.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '存储过程')

:point_up: `my_operate` 定义并执行了 4 条 sql，完美诠释了存储过程更侧重于单纯的去执行这些语句。

## 存储过程的参数前缀

存储过程在定义参数的时候可以选择添加一些前缀:point_down:，如果不写，**默认的前缀是`IN`**：

```shell
参数类型 [IN | OUT | INOUT] 参数名 数据类型
```

| 前缀   <div style="width: 55px;"> | 实际参数是否必须是变量  | 描述                                                      |
|---------------------------------|--------------|---------------------------------------------------------|
| `IN`                            | 否            | 用于调用者向存储过程传递数据，如果`IN`参数在过程中被修改，调用者不可见。                    |
| `OUT`                           | 是            | 用于把存储过程运行过程中产生的数据赋值给`OUT`参数，存储过程执行结束后，调用者可以访问到`OUT`参数。      |
| `INOUT`                         | 是            | 综合`IN`和`OUT`的特点，既可以用于调用者向存储过程传递数据，也可以用于存放存储过程中产生的数据以供调用者使用。 |

:point_down:以下的示例，综合了 `in`，`out`，`inout` 参数：

```shell
CREATE PROCEDURE my_arg(
            in pname varchar (45),
            out ophone char(11),
            inout io_name varchar(45)
          )
BEGIN
     SELECT * FROM t;
     INSERT INTO t(phone, name) VALUES("15225632145", "公孙胜");
     SELECT * FROM t;
     SELECT phone from t where name = pname into ophone;
     SET pname = "公孙胜";
     SET io_name = "公孙胜";
END EOF
```

![综合示例](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220420/c792415cd0e1476eb60c2f831a4f2fa6.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '综合示例')

由:point_up:可以看出，虽然在存储过程中修改了 `pname` 的值为 `公孙胜`，但是并**没有生效**，值依然是最初的`宋江`。`IN`参数只能被用于读取，对它赋值是不会被调用者看到的。

`out` 参数 `ophone` 最初是空的，通过存储过程赋值成功为`公孙胜`。

`inout` 参数 `io_name` 最初是空的，通过存储过程赋值成功为`公孙胜`，这里如果 `io_name` 不为空，也会被修改为`公孙胜`。

## 存储过程和存储函数的区别

+ 存储函数在定义时需要显式用`RETURNS`语句标明返回的数据类型，而且在函数体中必须使用`RETURN`语句来显式指定返回的值，而存储过程不需要。
+ 存储函数只支持`IN`参数，而存储过程支持`IN`参数、`OUT`参数、和`INOUT`参数。
+ 存储函数<font style="color:red">**只能返回一个值**</font>，而存储过程可以通过设置多个`OUT`参数或者`INOUT`参数来返回多个结果。
+ 存储函数执行过程中产生的结果集并**不会**被显示到客户端，而存储过程执行过程中产生的结果集**会**被显示到客户端。
+ 存储函数直接在表达式中调用，而存储过程只能通过`CALL`语句来显式调用。

## 游标

游标是为了方便访问结果集中的某一条记录，可以理解成循环。如果某个结果集中有 10 条记录，使用游标后，会一条一条的去访问这 10 条记录。

游标可以在存储函数和存储过程中使用。

![cursor](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220420/71873b26746f48f69a00761f46d21328.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'cursor')

使用游标分为 4 步：

1. 创建游标：`DECLARE 游标名称 CURSOR FOR 查询语句;`
2. 打开游标：`OPEN 游标名称;`
3. 通过游标访问记录
4. 关闭游标：`CLOSE 游标名称;`

> 不显式的使用`CLOSE`语句关闭游标的话，在该存储函数或存储过程执行完之后会自动关闭游标。

可以使用:point_down:来获取结果集中的记录：

```shell
FETCH 游标名 INTO 变量1, 变量2, ... 变量n
```

### 示例

:money_mouth_face:以下创建一个存储过程，在存储过程中使用游标。

创建游标`t_cursor`，游标执行语句为 `SELECT phone, name FROM t`。

`DECLARE CONTINUE HANDLER FOR NOT FOUND 处理语句;` 的作用是结果集遍历结束后会自动执行这句，这里也可以使用 `WHILE` 循环遍历，但是 `while`
有个弊端是需要提前知道结束条件，比如结果集的总数是多少。这样写的好处是直接遍历，遍历结束自动处理，将 `done` 变量设置为 `1`，也就是说只要 `done = 1` 就说明遍历结束了，利用 `LEAVE` 关键字跳出循环。

```shell
CREATE PROCEDURE my_cursor()
BEGIN
    DECLARE v_phone char(11);
    DECLARE v_name varchar(45);

    DECLARE done INT DEFAULT 0;
    DECLARE t_cursor CURSOR FOR SELECT `phone`, `name` FROM t;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

    OPEN t_cursor;

    flag: LOOP
        FETCH t_cursor INTO v_phone, v_name;
        IF done = 1 THEN
            LEAVE flag;
        END IF;
        SELECT v_phone, v_name, done;
    END LOOP flag;

    CLOSE t_cursor;

END EOF
```

![执行结果](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220420/5dfc58f6432548ff9ce5d3dd7b5dcec4.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '执行结果')

## 触发器和事件

存储例程是需要手动调用的，而触发器和事件是 MySQL 服务器在特定情况下自动调用的。

## 触发器

创建触发器

```shell
CREATE TRIGGER 触发器名
{BEFORE|AFTER}
{INSERT|DELETE|UPDATE}
ON 表名
FOR EACH ROW
BEGIN
    触发器内容
END
```

MySQL 目前只支持对`INSERT`、`DELETE`、`UPDATE`这三种类型的语句设置触发器。

`FOR EACH ROW BEGIN ... END`表示对具体语句影响的每一条记录都执行触发器内容。

对于`INSERT`语句来说，`FOR EACH ROW`影响的记录就是准备插入的那些新记录。

对于`DELETE`语句和`UPDATE`语句来说，`FOR EACH ROW`影响的记录就是符合条件的那些记录。

针对每一条受影响的记录，需要一种访问该记录中的内容的方式，MySQL提供了`NEW`和`OLD`两个单词来分别代表新记录和旧记录，它们在不同语句中的含义不同：

+ 对于`INSERT`语句设置的触发器来说，`NEW`代表准备插入的记录，`OLD`无效。
+ 对于`DELETE`语句设置的触发器来说，`OLD`代表删除前的记录，`NEW`无效。
+ 对于`UPDATE`语句设置的触发器来说，`NEW`代表修改后的记录，`OLD`代表修改前的记录。

### 示例

:man_facepalming:以下示例，对表 `t` 创建一个 `my_trigger`触发器，表 `t` 有三个字段，`name`，`phone`，`my_join`，对于每条 `insert` 的语句，在执行 `insert`
之前判断如果
`name = admin` 那么将即将插入的 `name` 值改为 `valid`，如果 `name` 值为`空`，将即将插入的 `name` 值改为`无名氏`，除此之外将 `name` 和 `phone` 拼接后赋给 `my_join`
字段。

```shell
CREATE TRIGGER my_trigger
     BEFORE INSERT ON t
     FOR EACH ROW
     BEGIN
         IF NEW.name = 'admin' THEN
             SET NEW.name = 'valid';
         ELSEIF NEW.name = '' THEN
            SET NEW.name = '无名氏';
         ELSE
            SET NEW.my_join = CONCAT(NEW.name, "--", NEW.phone);
         END IF;
 END EOF
```

![示例演示](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220420/f7108f5048cc42b9b3a4effb62dfd34c.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '示例演示')

| CMD                           | 说明      |
|-------------------------------|---------|
| `SHOW TRIGGERS;`              | 查看所有触发器 |
| `SHOW CREATE TRIGGER 触发器名;`   | 查看某个触发器 |
| `DROP TRIGGER 触发器名;`          | 删除某个触发器 |

### 注意事项

+ 触发器内容中不能有输出结果集的语句。
+ 触发器内容中`NEW`代表记录的列的值可以被更改，`OLD`代表记录的列的值无法更改。
+ 在`BEFORE`触发器中，我们可以使用`SET NEW.列名 = 某个值`的形式来更改待插入记录或者待更新记录的某个列的值，但是这种操作不能在`AFTER`触发器中使用，因为在执行`AFTER`
  触发器的内容时记录已经被插入完成或者更新完成了。
+ 如果我们的`BEFORE`触发器内容执行过程中遇到了错误，那这个触发器对应的具体语句将无法执行；如果具体的操作语句执行过程中遇到了错误，那与它对应的`AFTER`触发器的内容将无法执行。

## 事件

事件可以让 MySQL 服务器在某个时间点或者每隔一段时间自动地执行一些语句。

默认情况下，MySQL服务器并不会帮助我们执行事件，需要手动开启该功能：

```shell
SET GLOBAL event_scheduler = ON;
```

![开启事件功能](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220421/2892ec357bc54b3e90d1009886e36d26.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '开启事件功能')

```shell
CREATE EVENT 事件名
ON SCHEDULE
{
    AT 某个确定的时间点| 
    EVERY 期望的时间间隔 [STARTS datetime][END datetime]
}
DO
BEGIN
    具体的语句
END
```

### 某个时间点执行

```shell
CREATE EVENT insert_t1_event
ON SCHEDULE
AT '2022-01-03 11:20:11' # 或者 AT DATE_ADD(NOW(), INTERVAL 2 DAY)
DO
BEGIN
    INSERT INTO t(phone, name) VALUES('15210214254', '宋江');
END
```

### 每隔一段时间执行

```shell
CREATE EVENT insert_t1
ON SCHEDULE
EVERY 1 HOUR STARTS '2019-09-04 15:48:54' ENDS '2019-09-16 15:48:54'
DO
BEGIN
    INSERT INTO t(phone, name) VALUES('15210214254', '宋江');
END
```

在创建好事件之后，到了指定时间，MySQL 服务器会自动执行。

| CMD                            | 说明      |
|--------------------------------|---------|
| `SHOW EVENTS;`                 | 查看所有事件  |
| `SHOW CREATE EVENT 事件名;`     | 查看某个事件  |
| `DROP EVENT 事件名;`            | 删除某个事件  |


















