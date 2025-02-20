---
title: "Ubuntu 22.04.5 LTS 部署 mongo 一主二从一选举"
subtitle: ""

weight:

init_date: "2024-09-11T22:45:03+08:00"

date: 2024-09-11

lastmod: 2024-09-11

draft: false

author: "xiaobinqt"
description: "xiaobinqt,mongodb 主从, docker compose mongodb, mongodb 主备"

featuredImage: "https://cdn.xiaobinqt.cn/xiaobinqt.io/20250220/58a5a44358db48e080ed9d2deb0aa434.png"

featuredImagePreview: ""

reproduce: false

translate: false

tags: [ "mongodb" ]
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

## 安装 mongosh

1. 入 MongoDB GPG 密钥

```bash
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
```

如果提示 `apt-key` 已弃用，可以使用以下命令替代：

```bash
sudo mkdir -p /etc/apt/keyrings
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo gpg --dearmor -o /etc/apt/keyrings/mongodb.gpg
```

2. 添加 MongoDB 软件源
   创建并编辑 `/etc/apt/sources.list.d/mongodb.list` 文件：

```bash
echo "deb [ arch=amd64,arm64 signed-by=/etc/apt/keyrings/mongodb.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb.list
```

上述命令中的 `jammy` 对应 Ubuntu 22.04，`6.0` 表示 MongoDB 的版本号，你可以根据需要调整。

3. 更新软件包列表并安装
   再次更新软件包列表：

```bash
sudo apt update
```

然后尝试安装 `mongodb-clients`：

```bash
sudo apt install mongodb-mongosh
```

在较新的 MongoDB 版本中，`mongosh` 替代了传统的 `mongodb-clients` 工具，它是 MongoDB 的交互式 shell，提供了与数据库交互的功能。

## docker compose 部署

文件目录结构如下

```shell
.
├── docker-compose.yaml
├── mongodb-keyfile(文件)
├── mongo-arbiter-data(文件夹)
├── mongo1-data(文件夹)
├── mongo2-data(文件夹)
└── mongo3-data(文件夹)

```

![目录结构](https://cdn.xiaobinqt.cn/xiaobinqt.io/20250220/3e6402e8e40244d7ad9ec18f7c79dbed.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '目录结构')

docker-compose.yaml

```yaml
services:
  mongo1:
    image: mongo:6.0.3
    container_name: mongo1
    restart: always
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: example
    volumes:
      - ./mongo1-data:/data/db
      - ./mongodb-keyfile:/etc/mongodb-keyfile
    command: mongod --replSet rs0 --bind_ip_all --keyFile /etc/mongodb-keyfile --auth
    entrypoint:
      - bash
      - -c
      - |
        chmod 400 /etc/mongodb-keyfile
        chown 999:999 /etc/mongodb-keyfile
        exec docker-entrypoint.sh $$@

  mongo2:
    image: mongo:6.0.3
    container_name: mongo2
    restart: always
    ports:
      - "27018:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: example
    volumes:
      - ./mongo2-data:/data/db
      - ./mongodb-keyfile:/etc/mongodb-keyfile
    command: mongod --replSet rs0 --bind_ip_all --keyFile /etc/mongodb-keyfile --auth
    entrypoint:
      - bash
      - -c
      - |
        chmod 400 /etc/mongodb-keyfile
        chown 999:999 /etc/mongodb-keyfile
        exec docker-entrypoint.sh $$@

  mongo3:
    image: mongo:6.0.3
    container_name: mongo3
    restart: always
    ports:
      - "27019:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: example
    volumes:
      - ./mongo3-data:/data/db
      - ./mongodb-keyfile:/etc/mongodb-keyfile
    command: mongod --replSet rs0 --bind_ip_all --keyFile /etc/mongodb-keyfile --auth
    entrypoint:
      - bash
      - -c
      - |
        chmod 400 /etc/mongodb-keyfile
        chown 999:999 /etc/mongodb-keyfile
        exec docker-entrypoint.sh $$@

  mongo-arbiter:
    image: mongo:6.0.3
    container_name: mongo-arbiter
    restart: always
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: example
    volumes:
      - ./mongo-arbiter-data:/data/db
      - ./mongodb-keyfile:/etc/mongodb-keyfile
    command: mongod --replSet rs0 --bind_ip_all --keyFile /etc/mongodb-keyfile --auth
    entrypoint:
      - bash
      - -c
      - |
        chmod 400 /etc/mongodb-keyfile
        chown 999:999 /etc/mongodb-keyfile
        exec docker-entrypoint.sh $$@

volumes:
  mongo1-data:
  mongo2-data:
  mongo3-data:
  mongo-arbiter-data:

```

mongodb-keyfile 它用于 MongoDB 节点之间的认证。你可以使用以下命令生成一个密钥文件：

```shell
openssl rand -base64 756 > mongo.key
```

该命令将生成一个 756 字节的随机密钥并将其保存到 mongo.key 文件中。**一定一定要修改 mongodb-keyfile 文件为 400 权限**。

```shell
chmod 400 mongodb-keyfile
```

执行 `docker compose up -d` 启动容器。将启动四个 MongoDB 实例：

- mongo1：主节点（Primary）
- mongo2：从节点（Secondary）
- mongo3：从节点（Secondary）
- mongo-arbiter：选举节点（Arbiter）

![容器列表](https://cdn.xiaobinqt.cn/xiaobinqt.io/20250220/6d3674208e4e45b68d568198a877b9f5.png '容器列表')

### 初始化副本

连接到其中一个 MongoDB 实例（例如 mongo1）：

```shell
docker exec -it mongo1 mongo -u root -p example
```

在 MongoDB shell 中，运行以下命令来初始化副本集：

```js
rs.initiate({
    _id: "rs0",
    members: [
        {_id: 0, host: "mongo1:27017"},  // 主节点
        {_id: 1, host: "mongo2:27017"},  // 从节点
        {_id: 2, host: "mongo3:27017"},  // 从节点
        {_id: 3, host: "mongo-arbiter:27017", arbiterOnly: true}  // 选举节点
    ]
})
```

![设置副本](https://cdn.xiaobinqt.cn/xiaobinqt.io/20250220/b9125063f0584db989ea39d4f0c8232f.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '设置副本')

过一两分钟，在 MongoDB shell 中，运行以下命令检查副本集的状态：

```js
rs.status()
```

会看到：

- mongo1 被选为主节点（Primary）。
- mongo2 和 mongo3 是从节点（Secondary）。
- mongo-arbiter 是选举节点（Arbiter）。

![副本状态](https://cdn.xiaobinqt.cn/xiaobinqt.io/20250220/09423aa4fb514c26b0cd4b70e991c588.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '副本状态')

## 测试副本

### 测试副本集

在主节点上插入数据，连接到主节点（mongo1）：

```shell
docker exec -it mongo1 mongosh -u root -p example
```

插入一些数据：

```shell
use testdb
db.testcollection.insert({name: "test"})
```

![插入数据](https://cdn.xiaobinqt.cn/xiaobinqt.io/20250220/a8d217470f3241598e0d3a97701c783a.png '插入数据')

在从节点上查询数据，连接到从节点（例如 mongo2）：

```shell
docker exec -it mongo2 mongosh -u root -p example
```

在 MongoDB shell 中，运行以下命令以允许从节点读取数据：

```js
rs.secondaryOk()
```

然后查询数据：

```shell
use testdb
db.testcollection.find()
```

![副本读取主节点插入的数据](https://cdn.xiaobinqt.cn/xiaobinqt.io/20250220/e099ef836c18426aa6cb5dbe32300271.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '副本读取主节点插入的数据')

能够看到在主节点上插入的数据。

### 测试选举节点

选举节点（Arbiter）不存储数据，仅用于选举。可以通过停止主节点来测试选举过程：

停止主节点（mongo1）：

```shell
docker stop mongo1
```

![stop主节点](https://cdn.xiaobinqt.cn/xiaobinqt.io/20250220/cc7a8bcbe8da4660a22644f93e909875.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'stop主节点')

连接到另一个从节点（例如 mongo2），检查副本集状态：

```shell
docker exec -it mongo2 mongosh -u root -p example
rs.status()
```

会看到新的主节点被选举出来（可能是 mongo2 或 mongo3）。

![从节点选举成功](https://cdn.xiaobinqt.cn/xiaobinqt.io/20250220/01d89f18ae4e4b6eb4f87cca80f900b0.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '从节点选举成功')

## 为什么需要 rs.secondaryOk()

`rs.slaveOk()` 是 MongoDB 早期版本（3.x 及之前）中用于允许从节点（Secondary）读取数据的命令。从 MongoDB 4.0 开始，这个命令已经被弃用，取而代之的是 `rs.secondaryOk()`。

默认情况下，MongoDB 副本集的从节点（Secondary）是**不允许客户端直接读取数据的。这是为了防止应用程序意外读取到未同步完成的数据**。如果希望从从节点读取数据，需要显式地调用 `rs.secondaryOk()` 来允许读取操作。

1. **是否可以省略？**

如果不调用 `rs.secondaryOk()`，客户端将无法从从节点读取数据，只能从主节点（Primary）读取。如果的应用程序只需要从主节点读取数据，那么可以省略 `rs.secondaryOk()`。

2. **自动同步数据到副本**

MongoDB 副本集会自动将数据从主节点同步到从节点，这是副本集的核心功能之一。但是，**数据同步和允许读取是两个不同的概念**。即使数据已经同步到从节点，客户端默认也不能直接从从节点读取数据，除非显式调用 `rs.secondaryOk()`。

### 如何配置从节点允许读取

如果希望从从节点读取数据，可以在连接 MongoDB 时设置读取偏好（Read Preference），或者在 MongoDB Shell 中调用 `rs.secondaryOk()`。

**方法 1：在 MongoDB Shell 中调用 `rs.secondaryOk()`**

连接到从节点后，运行以下命令：

```javascript
rs.secondaryOk()
```

然后就可以从从节点读取数据了。

**方法 2：在客户端设置读取偏好**

如果使用的是 MongoDB 驱动程序（如 Node.js、Python 等），可以在连接字符串或客户端配置中设置读取偏好为 `secondary` 或 `secondaryPreferred`。例如：

- Node.js 示例：

  ```javascript
  const { MongoClient } = require('mongodb');

  const uri = 'mongodb://root:example@mongo1:27017,mongo2:27017,mongo3:27017/testdb?replicaSet=rs0';
  const client = new MongoClient(uri, {
    readPreference: 'secondaryPreferred' // 优先从从节点读取
  });

  async function run() {
    try {
      await client.connect();
      const db = client.db('testdb');
      const collection = db.collection('testcollection');
      const result = await collection.find({}).toArray();
      console.log(result);
    } finally {
      await client.close();
    }
  }

  run().catch(console.dir);
  ```

- Python 示例：

  ```python
  from pymongo import MongoClient

  client = MongoClient(
      'mongodb://root:example@mongo1:27017,mongo2:27017,mongo3:27017/testdb?replicaSet=rs0',
      read_preference='secondaryPreferred'  # 优先从从节点读取
  )

  db = client.testdb
  collection = db.testcollection
  result = collection.find({})
  for doc in result:
      print(doc)
  ```









