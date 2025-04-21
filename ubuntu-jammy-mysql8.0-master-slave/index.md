# Ubuntu Jammy Mysql8.0 搭建主从


<!-- author： xiaobinqt -->
<!-- email： xiaobinqt@163.com -->
<!-- https://xiaobinqt.github.io -->
<!-- https://www.xiaobinqt.cn -->

## 简介

MySQL 主从复制（Master-Slave Replication）是一种常见的数据复制技术，主要有如下功能：

1. 高可用性

当主节点（Master）发生故障时，可以从从节点（Slave）中选举一个新的主节点，继续提供服务，减少系统停机时间。

2. 读写分离

主节点负责写操作（如 INSERT、UPDATE、DELETE），从节点负责读操作（如 SELECT），从而分担主节点的负载，提高系统性能。

3. 故障恢复：

当主节点发生故障时，可以快速切换到从节点，保证服务的连续性。

4. 分布式扩展

通过增加从节点，可以扩展读能力，适用于读多写少的场景。

## 主从搭建

在使用 Docker Compose 搭建 MySQL 8.0 主从架构时，需要设置两个 MySQL 容器：一个作为主节点，另一个作为从节点。主节点将负责处理写入操作，而从节点将同步主节点的数据。

准备一个目录结构用于存放证书文件、配置文件等：

```
/path/to/project/
|-- docker-compose.yml
|-- mysql.cnf
|-- ssl/
    |-- ca-cert.pem
    |-- client-cert.pem
    |-- client-key.pem
```

步骤 1：准备 SSL 证书

在项目目录下，创建一个 `ssl/` 文件夹并生成所需的 SSL 证书：

```bash
mkdir -p /path/to/project/ssl
cd /path/to/project/ssl

# 生成根证书
openssl genrsa 2048 > ca-key.pem
openssl req -new -x509 -nodes -sha256 -key ca-key.pem -out ca-cert.pem -subj "/CN=MySQL Root CA"

# 生成服务器证书
openssl genrsa 2048 > server-key.pem
openssl req -new -sha256 -key server-key.pem -out server-req.pem -subj "/CN=mysql-master"
openssl x509 -req -in server-req.pem -sha256 -CA ca-cert.pem -CAkey ca-key.pem -CAcreateserial -out server-cert.pem -days 36500

# 生成客户端证书
openssl genrsa 2048 > client-key.pem
openssl req -new -sha256 -key client-key.pem -out client-req.pem -subj "/CN=mysql-client"
openssl x509 -req -in client-req.pem -sha256 -CA ca-cert.pem -CAkey ca-key.pem -CAcreateserial -out client-cert.pem -days 36500
```

步骤 2：创建 `docker-compose.yml` 文件，配置 MySQL 主从复制和 SSL。

```yaml
version: '3.8'

services:
  mysql-master:
    image: mysql:8.0
    container_name: mysql-master
    environment:
      MYSQL_ROOT_PASSWORD: root_password
      MYSQL_DATABASE: mydatabase
    volumes:
      - ./mysql.cnf:/etc/mysql/my.cnf
      - ./ssl:/etc/mysql/ssl
    networks:
      - mysql-network
    ports:
      - "3307:3306"
    command:
      --server-id=1
      --binlog-do-db=mydatabase # 只记录特定数据库的更改，而不是全部数据库
      --require-secure-transport=ON
      --ssl-ca=/etc/mysql/ssl/ca-cert.pem
      --ssl-cert=/etc/mysql/ssl/server-cert.pem
      --ssl-key=/etc/mysql/ssl/server-key.pem
      --default-authentication-plugin=caching_sha2_password
    restart: always

  mysql-slave:
    image: mysql:8.0
    container_name: mysql-slave
    environment:
      MYSQL_ROOT_PASSWORD: root_password
      MYSQL_DATABASE: mydatabase
    volumes:
      - ./mysql.cnf:/etc/mysql/my.cnf
      - ./ssl:/etc/mysql/ssl
    networks:
      - mysql-network
    ports:
      - "3308:3306"
    command:
      --server-id=2
      --relay-log=mysql-relay-bin
      --binlog-do-db=mydatabase # 只想复制特定数据库的数据
      --require-secure-transport=ON
      --ssl-ca=/etc/mysql/ssl/ca-cert.pem
      --ssl-cert=/etc/mysql/ssl/client-cert.pem
      --ssl-key=/etc/mysql/ssl/client-key.pem
      --default-authentication-plugin=caching_sha2_password
    restart: always

networks:
  mysql-network:
    driver: bridge
```

步骤 3：配置 MySQL 配置文件

在同一目录下，创建 `mysql.cnf` 文件，确保启用 SSL 和必要的复制配置。

```ini
[mysqld]
# 其他 MySQL 配置
secure-file-priv = NULL
```

步骤 4：启动容器

在 `docker-compose.yml` 和证书文件都配置好之后，可以启动 MySQL 主从复制环境：

```bash
docker-compose up -d
```

步骤 5：初始化 MySQL 主从复制

1. **配置主服务器：**

   进入主服务器容器并设置二进制日志：

   ```bash
   docker exec -it mysql-master bash
   mysql -u root -p
   ```

   登录后执行以下命令启用二进制日志并创建复制用户：

   ```shell
   # 创建一个用户名为 'replica'，密码为 'replica_password'，可以从任何主机（'%'）连接的 MySQL 用户。
   CREATE USER 'replica'@'%' IDENTIFIED BY 'replica_password';

   # 授予 'replica' 用户从任何主机（'%'）访问数据库的复制权限，允许该用户读取 MySQL 主库的二进制日志
   GRANT REPLICATION SLAVE ON *.* TO 'replica'@'%';

   # 确保权限更改生效，使得 replica 用户能立即开始使用刚才授予的权限
   FLUSH PRIVILEGES;

   # 获取主服务器的日志位置（用于从服务器配置）
   SHOW MASTER STATUS;
   ```

   记下 `File` 和 `Position` 字段的值，用于从服务器配置。

![主库配置](https://cdn.xiaobinqt.cn/xiaobinqt.io/20250220/09708471fc0544f8943d9c85f18ea26a.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '主库配置')

2. **配置从服务器：**

   进入从服务器容器并执行以下命令：

   ```bash
   docker exec -it mysql-slave bash
   mysql -u root -p
   ```

   登录后，执行以下命令配置从服务器连接到主服务器并启动复制：

   ```shell
   CHANGE MASTER TO
     MASTER_HOST='mysql-master',
     MASTER_USER='replica',
     MASTER_PASSWORD='replica_password',
     MASTER_SSL=1,
     MASTER_SSL_CA='/etc/mysql/ssl/ca-cert.pem',
     MASTER_SSL_CERT='/etc/mysql/ssl/client-cert.pem',
     MASTER_SSL_KEY='/etc/mysql/ssl/client-key.pem',
     MASTER_LOG_FILE='<master_log_file>',  -- 从主服务器获取的日志文件名
     MASTER_LOG_POS=<master_log_pos>;  -- 从主服务器获取的日志位置

   START SLAVE;

   -- 检查复制状态
   SHOW SLAVE STATUS\G;
   ```

![从库配置](https://cdn.xiaobinqt.cn/xiaobinqt.io/20250220/c4f8793fd6294ffc836d0997a20e0ae9.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '从库配置')

## 常用参数

`CHANGE MASTER TO` 语句用于在从服务器上配置与主服务器的连接信息，启动从库的复制。每个配置项都具有特定的含义：

1. **MASTER_HOST**

```shell
MASTER_HOST='mysql-master',
```

- **含义**：指定主服务器的主机名或 IP 地址。这个地址将被用来连接主服务器。
- **例子**：`MASTER_HOST='mysql-master'`，假设主库的 Docker 服务名或主机名为 `mysql-master`，该配置会告诉从库连接到这个主机。

2. **MASTER_USER**

```shell
MASTER_USER='replica',
```

- **含义**：指定用于连接主服务器的用户名。从库需要使用该用户权限来读取主库的二进制日志。这个用户必须具备 `REPLICATION SLAVE` 权限。
- **例子**：`MASTER_USER='replica'`，从库将使用 `replica` 用户进行连接。该用户应该在主库上创建，并且拥有 `REPLICATION SLAVE` 权限。

3. **MASTER_PASSWORD**

```shell
MASTER_PASSWORD='replica_password',
```

- **含义**：指定与 `MASTER_USER` 配套使用的密码。这个密码用于认证从库与主库的连接。
- **例子**：`MASTER_PASSWORD='replica_password'`，从库将使用密码 `replica_password` 与主库的 `replica` 用户进行连接。

4. **MASTER_SSL**

```shell
MASTER_SSL=1,
```

- **含义**：启用 SSL 加密连接。当从库与主库的通信需要加密时，将这个选项设置为 `1`。如果不需要加密连接，可以将其设置为 `0` 或不设置。
- **例子**：`MASTER_SSL=1`，表示启用 SSL 加密连接。

5. **MASTER_SSL_CA**

```shell
MASTER_SSL_CA='/etc/mysql/ssl/ca-cert.pem',
```

- **含义**：指定 SSL 连接的 CA (证书颁发机构) 证书路径。用于验证主库服务器的 SSL 证书是否合法。
- **例子**：`MASTER_SSL_CA='/etc/mysql/ssl/ca-cert.pem'`，这是主库 SSL 证书的 CA 文件路径。

6. **MASTER_SSL_CERT**

```shell
MASTER_SSL_CERT='/etc/mysql/ssl/client-cert.pem',
```

- **含义**：指定从库用来与主库进行 SSL 握手的客户端证书路径。客户端证书用于验证从库的身份。
- **例子**：`MASTER_SSL_CERT='/etc/mysql/ssl/client-cert.pem'`，是从库的客户端证书路径。

7. **MASTER_SSL_KEY**

```shell
MASTER_SSL_KEY='/etc/mysql/ssl/client-key.pem',
```

- **含义**：指定从库用于 SSL 握手的私钥路径，通常与客户端证书匹配。确保从库能够安全地进行身份验证。
- **例子**：`MASTER_SSL_KEY='/etc/mysql/ssl/client-key.pem'`，是从库的客户端私钥路径。

8. **MASTER_LOG_FILE**

```shell
MASTER_LOG_FILE='<master_log_file>',
```

- **含义**：指定主库的二进制日志文件名，表示从哪里开始读取数据。通常需要通过主库的 `SHOW MASTER STATUS` 获取当前的日志文件名。
- **例子**：`MASTER_LOG_FILE='mysql-bin.000001'`，该值表示从主库的二进制日志文件 `mysql-bin.000001` 开始读取。

9. **MASTER_LOG_POS**

```shell
MASTER_LOG_POS=<master_log_pos>;
```

- **含义**：指定主库的二进制日志位置（offset），从该位置开始读取数据。通常需要通过主库的 `SHOW MASTER STATUS` 获取当前日志的位置。
- **例子**：`MASTER_LOG_POS=154`，表示从 `mysql-bin.000001` 文件的 154 位置开始读取。

10. 启动复制

```shell
START SLAVE;
```

- **含义**：启动从库的复制进程，使其开始从主库获取二进制日志并同步数据。

11. 检查复制状态

```shell
SHOW SLAVE STATUS\G;
```

- **含义**：显示从库的复制状态，检查复制是否正常运行。

常见的输出字段：

- **Slave_IO_Running**：是否正在接收主库的日志。显示 `Yes` 表示接收正常。
- **Slave_SQL_Running**：是否正在执行主库的日志。显示 `Yes` 表示执行正常。
- **Seconds_Behind_Master**：从库的延迟时间，单位是秒。如果显示 `NULL`，可能表示从库无法连接主库或复制配置有问题。

### 其他配置选项

除了上述配置，MySQL 复制中还有一些常用的配置项：

1. **MASTER_PORT**

```shell
MASTER_PORT=3306;
```

- **含义**：指定主库的端口号，默认是 `3306`。如果主库使用了非默认端口，可以在这里指定。

2. **MASTER_CONNECT_RETRY**

```shell
MASTER_CONNECT_RETRY=60;
```

- **含义**：指定从库在主库断开连接时尝试重新连接的间隔，单位是秒。默认为 60 秒。

3. **REPLICATE_DO_DB**

```shell
REPLICATE_DO_DB='mydatabase';
```

- **含义**：指定从库只复制特定数据库的数据。这是一个限制性过滤，通常用于复制指定的数据库。

4. **REPLICATE_IGNORE_DB**

```shell
REPLICATE_IGNORE_DB='mydatabase';
```

- **含义**：指定从库忽略特定数据库的操作，不进行同步。

5. **REPLICATE_WILD_DO_TABLE**

```shell
REPLICATE_WILD_DO_TABLE='mydatabase.%';
```

- **含义**：指定从库只复制某些表的数据。可以使用通配符（例如 `%`）来匹配多个表。

6. **REPLICATE_WILD_IGNORE_TABLE**

```shell
REPLICATE_WILD_IGNORE_TABLE='mydatabase.%.tmp';
```

- **含义**：指定从库忽略某些表的数据复制，使用通配符（例如 `%`）来匹配多个表。

7. **SYNC_BINLOG**

```shell
SYNC_BINLOG=1;
```

- **含义**：指定 MySQL 在每次提交事务后同步 binlog。通常用于增强数据的持久性和一致性。

## 测试主从

在主节点上插入数据：

```shell
USE mydatabase;
CREATE TABLE test_table (id INT PRIMARY KEY, value VARCHAR(100));
INSERT INTO test_table (id, value) VALUES (1, 'Hello, Master!');
select * from test_table;
```

![主库写一条数据](https://cdn.xiaobinqt.cn/xiaobinqt.io/20250220/bcc6b65f2d37421ba03fc4ba4f7f85b9.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '主库写一条数据')

在从节点上查询数据：

```shell
USE mydatabase;
show tables;
SELECT * FROM test_table;
```

![从库读取数据成功](https://cdn.xiaobinqt.cn/xiaobinqt.io/20250220/d3d905e915cd41be9dfe194164253cfa.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '从库读取数据成功')

如果看到 Hello, Master!，说明主从复制配置成功。

{{< admonition type=info title="info" open=true >}}

Reading table information for completion of table and column names You can turn off this feature to get a quicker startup with -A

这个信息是 MySQL 客户端的一条提示，意味着 MySQL 正在尝试加载所有数据库的表和列信息，以便在你输入表名或列名时提供自动补全功能。

这对于某些大型数据库可能会导致启动较慢，因为 MySQL 会查询所有数据库的表信息。为了加速启动，你可以禁用自动补全功能，方法是使用 -A 参数。

```shell
mysql -u root -p -A
```

{{< /admonition >}}

## 常用命令

```shell
STOP SLAVE;
START SLAVE;
SHOW SLAVE STATUS\G
```





