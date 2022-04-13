# Mongodb 学习笔记


[//]: # (https://xiaobinqt.github.io)

[//]: # (https://www.xiaobinqt.cn)

## win10 安装

在 windows 下安装可以参考这篇文章[mongodb-window-install](https://www.runoob.com/mongodb/mongodb-window-install.html)。

### 小坑

我使用的是 windows 10 企业版，在安装时出现了个问题，如下：

![问题截图](https://img-blog.csdnimg.cn/202104142157593.png '问题截图')

我是在网上找了大半天没有找到解决的办法，都是写文章作者可用，但是我一直不生效，我觉得的必须要用管理员权限安装导致的。后来我直接忽略了，用管理员权限运行。

### 运行服务端

用管理员 power shell 运行 具体命令可以参看[文档](https://www.runoob.com/mongodb/mongodb-window-install.html)

![运行 mongodb 服务 01](https://img-blog.csdnimg.cn/20210414220324785.png '运行 mongodb 服务 01')

```shell
 .\mongod.exe  --dbpath D:\mySoft\mongoDB\data\db
```

![运行 mongodb 服务 02](https://img-blog.csdnimg.cn/20210414220357328.png '运行 mongodb 服务 02')

### 运行客户端

```shell
 .\mongo.exe
```

![客户端连接](https://img-blog.csdnimg.cn/20210414220831739.png '客户端连接')

## Navicat Premium

navicat premium 是一个数据库管理工具，可以支持 mysql，mongodb，oracle 等几乎所有的数据库。

![navicat premium](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220413/c2ef76e02ba6449dacdb7fa856d4da3d.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'navicat premium')

![navicat premuim 使用](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220413/d47621d94a1e4f68abe30d8fb35e02a0.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'navicat premuim 使用')

windows 安转教程可以参考[navicat premium15破解教程](http://www.downcc.com/soft/430673.html)

## 概念解析

| SQL术语/概念    | MongoDB术语/概念 | 说明                           |
|-------------|--------------|------------------------------|
| database    | database     | 数据库                          |
| table       | collection   | 数据库表/集合                      |
| row         | document     | 数据记录行/文档                     |
| column      | field        | 数据字段/域                       |
| index       | index        | 索引                           |
| table joins | -            | 表连接，MongoDB 不支持              |
| primary key | primary key  | 主键，MongoDB 自动将 `_id` 字段设置为主键 |

| RDBMS（关系型数据库） |    MongoDB|
|---------------|--------|
| 数据库           |数据库|
| 表格            |    集合|
| 行             |    文档|
| 列             |    字段|
| 表联合           |    嵌入文档|
| 主键            |主键 (MongoDB 提供了 key 为 `_id` )|

![对比图](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220413/c1e37e969c744f2bb82f3f68d4b73804.png '对比图')

## 常用命令

| CMD                                            | 说明                                                     | 
|------------------------------------------------|--------------------------------------------------------|
| `db.help()`                                    | 查看命令帮助                                                 |
| `show dbs`                                     | 查看所有数据库                                                |
| `use db_name`                                  | 如果数据库不存在，则创建数据库，否则切换到指定数据库                             |
| `show tables`                                  | 查看该库下的所有表                                              |
| `db.getName()`                                 | 查看当前所在的库                                               |
| `db`                                           | 命令可以显示当前数据库对象或集合                                       |
| `db.version()`                                 | 当前db版本                                                 |
| `db.stats()`                                   | 当前db状态                                                 |
| `db.getMongo()`                                | 查看当前db的链接机器地址                                          |
| `db.dropDatabase()`                            | 删除当前使用的数据库                                             |
| `db.copyDatabase("mydb", "temp", "127.0.0.1")` | 从指定的机器上复制指定数据库数据到某个数据库，本示例为：将本机的 mydb 的数据复制到 temp 数据库中 |
| `db.cloneDatabase("127.0.0.1")`                | 将指定机器上的数据库的数据克隆到当前数据库                                  |
| `db.repairDatabase()`                          | 修复当前数据库                                                |
| `show collections`/`show tables`               | 查看已有集合                                                 |
| `db.yourColl.help()`                           | 查看帮助                                                   | 
| `db.yourColl.count()`                          | 查询当前集合的数据条数                                            | 
| `db.yourColl.dataSize()`                       | 查看数据空间大小                                               | 
| `db.yourColl.getDB()`                          | 得到当前聚集集合所在的 db                                         | 
| `db.yourColl.stats()`                          | 得到当前集合的状态                                              | 
| `db.yourColl.totalSize()`                      | 得到集合总大小                                                | 
| `db.yourColl.storageSize()`                    | 聚集集合储存空间大小                                             | 
| `db.yourColl.getShardVersion()`                | Shard版本信息                                              | 
| `db.userInfo.renameCollection("users")`        | 集合重命名。示例为：将 userInfo 重命名为 users                        | 
| `db.yourColl.drop()`                           | 删除当前集合                                                 | 

> `yourColl` 表示集合名

## 集合查询

+ :pushpin: 查询所有记录

```shell
db.mgotest.find()
# 格式化输出
db.mgotest.find().pretty()
```

对比 SQL：`select * from mgotest;`

+ :pushpin: 查询去掉后的当前集合中的某列的重复数据

```shell
db.mgotest.distinct("interests")
```

对比 SQL：`select distinct interests from mgotest;`

![distinct](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220413/7c011741b7fb4de8aafbdec1602462cb.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'distinct')

+ :pushpin: 查询 age = 22 的记录

```shell
db.userInfo.find({"age": 22});
```

对比 SQL：`select * from userInfo where age = 22;`

+ :pushpin: 查询 age > 22 的记录

```shell
db.userInfo.find({age: {$gt: 22}})
```

对比 SQL：`select * from userInfo where age >22;`

+ :pushpin: 查询 age < 22 的记录

```shell
db.userInfo.find({age: {$lt: 22}});
```

对比 SQL：`select * from userInfo where age < 22;`

+ :pushpin: 查询 age >= 25 的记录

```shell
db.userInfo.find({age: {$gte: 25}});
```

对比 SQL：`select * from userInfo where age >= 25;`

+ :pushpin: 查询 age <= 25 的记录

```shell
db.userInfo.find({age: {$lte: 25}});
```

+ :pushpin: 查询 age >= 23 并且 age <= 26

```shell
db.userInfo.find({age: {$gte: 23, $lte: 26}});
```

+ :pushpin: 查询 name 中包含 mongo 的数据

```shell
db.userInfo.find({name: /mongo/});
```

对比 SQL：`select * from userInfo where name like ‘%mongo%';`

+ :pushpin: 查询 name 中以 mongo 开头的

```shell
db.userInfo.find({name: /^mongo/});
```

对比 SQL：`select * from userInfo where name like ‘mongo%';`

+ :pushpin: 查询指定列 name、age 数据

```shell
db.userInfo.find({}, {name: 1, age: 1});
```

对比 SQL：`select name, age from userInfo;`

+ :pushpin: 查询指定列 name、age 数据, age > 25

````shell
db.userInfo.find({age: {$gt: 25}}, {name: 1, age: 1});
````

对比 SQL：`select name, age from userInfo where age >25;`

+ :pushpin: 按照年龄排序

```shell
# 升序
db.userInfo.find().sort({age: 1});
# 降序
db.userInfo.find().sort({age: -1});
```

+ :pushpin: 查询 name = zhangsan, age = 22 的数据

```shell
db.userInfo.find({name: 'zhangsan', age: 22});
```

对比 SQL：`select * from userInfo where name = 'zhangsan' and age = '22';`

+ :pushpin: 查询前 5 条数据

```shell
db.userInfo.find().limit(5);
```

对比 SQL：`select  * from userInfo limit 5;`

+ :pushpin: 查询 10 条以后的数据

```shell
db.userInfo.find().skip(10);
```

对比 SQL：

```sql
select *
from userInfo
where id not in (
    select id
    from userInfo limit 10
    );
```

+ :pushpin: 查询在 5-10 之间的数据

```shell
db.userInfo.find().limit(10).skip(5);
```

可用于分页，limit 是 pageSize，skip 是 (第几页 * pageSize)

+ :pushpin: or 查询

```shell
db.userInfo.find({$or: [{age: 22}, {age: 25}]});
```

对比 SQL：`select * from userInfo where age = 22 or age = 25;`

+ :pushpin: 查询某个结果集的记录条数

```shell
db.userInfo.find({age: {$gte: 25}}).count();
```

对比 SQL：`select count(*) from userInfo where age >= 20;`

+ :pushpin: 按照某列进行排序

```shell
db.userInfo.find({sex: {$exists: true}}).count();
```

对比 SQL：`select count(sex) from userInfo;`

## 更新文档

```shell
db.collection.update(
   <query>,
   <update>,
   {
     upsert: <boolean>,
     multi: <boolean>,
     writeConcern: <document>
   }
)
  
# 示例
db.col.update({'title':'MongoDB 教程'},{$set:{'title':'MongoDB'}})  
```

参数说明：

+ query : update 的查询条件，类似 sql update 查询内 where 后面的。
+ update : update 的对象和一些更新的操作符（如$,$inc...）等，也可以理解为 sql update 查询内 set 后面的
+ upsert : 可选，这个参数的意思是，如果不存在 update 的记录，是否插入 objNew, true 为插入，默认是 false ，不插入。
+ multi : 可选，mongodb 默认是 false,只更新找到的第一条记录，如果这个参数为 true, 就把按条件查出来多条记录全部更新。
+ writeConcern :可选，抛出异常的级别。

## globalsign/mgo 使用

```go
package main

import (
	"fmt"
	"time"

	"github.com/globalsign/mgo"
	"github.com/globalsign/mgo/bson"
)

type User struct {
	Id        bson.ObjectId `bson:"_id" json:"id"`
	Username  string        `bson:"name" json:"username"`
	Pass      string        `bson:"pass" json:"pass"`
	Regtime   int64         `bson:"regtime" json:"regtime"`
	Interests []string      `bson:"interests" json:"interests"`
}

const URL string = "127.0.0.1:27017"

var (
	c       *mgo.Collection
	session *mgo.Session
)

func (user User) ToString() string {
	return fmt.Sprintf("%#v", user)
}

func init() {
	session, _ = mgo.Dial(URL)
	// 切换到数据库
	db := session.DB("blog")
	// 切换到collection
	c = db.C("mgotest")
}

// 新增数据
func add() {
	//    defer session.Close()
	stu1 := new(User)
	stu1.Id = bson.NewObjectId()
	stu1.Username = "stu_name" + time.Now().String()
	stu1.Pass = "stu1_pass"
	stu1.Regtime = time.Now().Unix()
	stu1.Interests = []string{"象棋", "游泳", "跑步"}
	err := c.Insert(stu1)
	if err == nil {
		fmt.Println("insert success")
	} else {
		fmt.Printf("insert error:%s \n", err.Error())
	}
}

// 查询
func find() {
	//    defer session.Close()
	var (
		users []User
		err   error
	)
	//    c.Find(nil).All(&users)
	err = c.Find(bson.M{"name": "stu_name"}).All(&users)
	if err != nil {
		fmt.Printf("find err:%s \n", err.Error())
		return
	}
	for index, value := range users {
		fmt.Printf("index:%d,val:%s \n", index, value.ToString())
	}
	// 根据ObjectId进行查询
	// idStr := "577fb2d1cde67307e819133d"
	// objectId := bson.ObjectIdHex(idStr)
	// user := new(User)
	// err = c.Find(bson.M{"_id": objectId}).One(user)
	// if err != nil {
	// 	fmt.Printf("db find err:%s \n", err.Error())
	// 	return
	// }
	// fmt.Println("查找成功..", user)
}

// 根据id进行修改
func update() {
	interests := []string{"象棋", "游泳", "跑步"}
	err := c.Update(bson.M{"_id": bson.ObjectIdHex("6076c3954e947b3944d4a38b")}, bson.M{"$set": bson.M{
		"name":      "修改后的name",
		"pass":      "修改后的pass",
		"regtime":   time.Now().Unix(),
		"interests": interests,
	}})
	if err != nil {
		fmt.Println("修改失败")
	} else {
		fmt.Println("修改成功")
	}
}

// 删除
func del() {
	err := c.Remove(bson.M{"_id": bson.ObjectIdHex("6076c3954e947b3944d4a38b")})
	if err != nil {
		fmt.Println("删除失败" + err.Error())
	} else {
		fmt.Println("删除成功")
	}
}
func main() {
	add()
	find()
	update()
	del()
}

```

## FAQ

### 空库不显示

![show dbs](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220413/a9027333e1aa4ac59dfe1271a4b8c43d.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'show dbs')

上图:point_up_2:用 `use test1` 新建了一个数据库 `test1`，但是用 `show dbs` 却没有显示 `test1`，这是因为 `test1` 是空的，插入一条数据就可以显示。

![显示新建的库](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220413/2d55f00bf1dc4aff97f652b8d0fbceaa.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '显示新建的库')

## 参考

+ [MongoDB 教程](https://www.runoob.com/mongodb/mongodb-tutorial.html)
+ [MongoDB高级查询](http://cw.hubwiz.com/card/c/543b2f3cf86387171814c026/1/1/1/)
+ [MongoDB常用操作命令大全](https://www.jb51.net/article/48217.htm)
+ [查询, 更新, 投射, 和集合算符](https://mongodb-documentation.readthedocs.io/en/latest/reference/operator.html#gsc.tab=0)
+ [Field Update Operators](https://www.mongodb.com/docs/manual/reference/operator/update-field/)

