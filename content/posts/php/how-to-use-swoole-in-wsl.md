---
title: "windows10 WSL 使用 swoole"
subtitle: ""

weight:

init_date: "2025-02-17T12:54:22+08:00"

date: 2025-02-17

lastmod: 2025-02-17

draft: false

author: "xiaobinqt"
description: "xiaobinqt,"

featuredImage: ""

featuredImagePreview: "https://cdn.xiaobinqt.cn/xiaobinqt.io/20250219/ac56ee88b27b4ddfbd6a7deeb9f3949b.png"

reproduce: false

translate: false

tags: [ "swoole","php" ,"wsl" ]
categories: [ "php" ]
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


前几天一个同学问了我几个 swoole 的问题，好吧，我承认我已经好多年没写 php 了。刚好今天有空看了下 swoole 文档，学习了一下。

在 Windows 上使用 Swoole 可能会遇到一些限制（我今年一定要换一个 mac:cry:），因为 Swoole 主要是为 Linux 环境设计的，依赖于 Linux 的一些特性（如 epoll、信号处理等）。如果一定要在 windows 上使用 swoole，推荐使用 WSL。

## PPA

PPA 是 **Personal Package Archive** 的缩写，是 Ubuntu 系统中一种由个人或团队维护的软件仓库。它允许开发者将自己编写的软件或更新发布到一个独立的仓库中，用户可以通过添加这些仓库来安装官方软件源中没有的软件或更新版本。

当你添加一个 PPA 时，系统会将该仓库的地址添加到 `/etc/apt/sources.list.d/` 目录下的配置文件中，然后通过 `apt` 工具从该仓库下载和安装软件。

### PPA 的作用

1. 提供更新的软件版本：

Ubuntu 官方软件源中的软件版本通常比较稳定，但可能不是最新版本。PPA 可以提供最新的软件版本。

2. 提供官方软件源中没有的软件：

一些软件可能没有被收录到 Ubuntu 官方软件源中，但可以通过 PPA 安装。

3. 方便开发者分发软件：

开发者可以通过 PPA 快速发布自己的软件或更新，用户只需添加 PPA 仓库即可安装。

### 常见的 PPA 仓库

1. `ondrej/php`：
    - 提供最新版本的 PHP 和相关扩展。
    - 添加命令：
      ```bash
      sudo add-apt-repository ppa:ondrej/php
      ```

### 如何使用 PPA

1. 添加 PPA 仓库

使用 `add-apt-repository` 命令添加 PPA 仓库。例如，添加 `ondrej/php` PPA：

```bash
sudo add-apt-repository ppa:ondrej/php
```

2. 更新软件包列表

添加 PPA 后，需要更新本地的软件包列表：

```bash
sudo apt update
```

3. 安装软件

从 PPA 仓库中安装软件。例如，安装 PHP 7.4：

```bash
sudo apt install php7.4
```

### 删除 PPA 仓库

如果你不再需要某个 PPA，可以将其删除。

1. 删除 PPA 配置文件：
   ```bash
   sudo rm /etc/apt/sources.list.d/ppa_name.list
   ```
   （将 `ppa_name` 替换为实际的 PPA 名称）

2. 更新软件包列表：
   ```bash
   sudo apt update
   ```

## 安装 php

```shell
sudo apt install software-properties-common
sudo add-apt-repository ppa:ondrej/php
sudo apt update
sudo apt install php8.4
```

![搜索 php](https://cdn.xiaobinqt.cn/xiaobinqt.io/20250219/4256e7df01a842e4951a5557689b6776.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '搜索 php')

## pecl

### pecl 是什么

PECL（**PHP Extension Community Library**）是 PHP 官方提供的扩展库，专门用于管理和安装 PHP 扩展。它类似于 Composer 之于 PHP 包管理，但 PECL 主要用于 C 语言编写的 PHP 扩展，而不是 PHP 代码库。如果你需要安装 PHP 代码库（如 Laravel），应使用 Composer，而不是 PECL。

PECL 允许你下载、安装和管理 PHP 扩展，如：

- Swoole（高性能协程服务器）
- Redis（Redis 客户端）
- Xdebug（PHP 调试工具）
- Imagick（图像处理）

### 如何使用 PECL

检查 PECL 是否安装，在终端（CMD / PowerShell）中运行：

```bash
pecl version
```

### PECL 和 Composer 的区别

| 对比项          | PECL                            | Composer                    |
|--------------|---------------------------------|-----------------------------|
| 作用           | 安装 PHP 扩展（C 语言编写）               | 安装 PHP 库（PHP 代码）            |
| 管理的内容        | PHP 扩展（如 Swoole, Redis, Xdebug） | PHP 代码包（如 Laravel, Monolog） |
| 依赖的工具        | PHP 和 PEAR                      | PHP                         |
| 是否需要重新启动 PHP | 需要（因为是 C 扩展）                    | 不需要                         |

### 安装 pecl

php 默认不包含 pecl，可以手动安装 pecl。需要先安装 PEAR，这样 PECL 才能工作。PEAR 是 PHP 的扩展和应用仓库，PECL 是 PEAR 的一部分。

1. 下载 go-pear.phar 文件：

```shell
 curl -o go-pear.phar https://pear.php.net/go-pear.phar
```

[//]: # (![下载 pear 文件]&#40;https://cdn.xiaobinqt.cn/xiaobinqt.io/20250219/90fa455450084f7dbfed818456a696de.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '下载 pear 文件' &#41;)

2. 执行命令来安装 PEAR

```shell
php go-pear.phar
```

[//]: # (![安装 pear]&#40;https://cdn.xiaobinqt.cn/xiaobinqt.io/20250219/166bb29b42124597a34dad22f3555351.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '安装 pear'&#41;)

![安装 pecl](https://cdn.xiaobinqt.cn/xiaobinqt.io/20250219/d8829bb4e1314c1a9cbbae8e95cc948d.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '安装 pecl')

在安装过程中可能会提示缺少扩展，比如

```shell
XML Extension not found
```

这时安装上对应的扩展即可。

![安装缺少的扩展](https://cdn.xiaobinqt.cn/xiaobinqt.io/20250219/000ca51700fe4823aec44a42a82503b1.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '安装缺少的扩展')

安装 pecl 成功后可能会提示，需要把路径添加到环境变量中：

![添加环境变量](https://cdn.xiaobinqt.cn/xiaobinqt.io/20250219/8d50f5b7bd1643c28541ec5f15123959.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '添加环境变量')

![添加环境变量](https://cdn.xiaobinqt.cn/xiaobinqt.io/20250219/1e42802019fb4a29be9a7f483f091952.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '添加环境变量')

pecl 安装成功

![pecl 安装成功](https://cdn.xiaobinqt.cn/xiaobinqt.io/20250219/fca28af9ef5f40ff891aabbb56c288dd.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'pecl 安装成功')

## 安装 swoole

照着官方文档安装即可，[安装文档](https://wiki.swoole.com/zh-cn/#/environment?id=pecl:~:text=Copied-,PECL,-%E6%B3%A8%E6%84%8F%3A%20PECL%20%E5%8F%91%E5%B8%83)

```
pecl install --configureoptions 'enable-sockets="no" enable-openssl="yes" enable-http2="yes" enable-mysqlnd="yes" enable-swoole-json="no" enable-swoole-curl="yes" enable-cares="yes"' swoole
```

![安装成功](https://cdn.xiaobinqt.cn/xiaobinqt.io/20250219/4a2af9dbf3bf4826acfe395d6fda85a4.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '安装成功')

### 一些安装提示

在编译和安装 PHP 扩展（如 Swoole）时，你看到的这些选项是在询问你是否启用某些功能或支持。每个选项都是扩展或功能的一个特性，下面是这些选项的详细解释：

![安装提示](https://cdn.xiaobinqt.cn/xiaobinqt.io/20250219/b2e1489f02054a0fa9295e28f356743d.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '安装提示')

**1. `enable brotli support? [yes] : yes`**

- **Brotli** 是一种压缩算法，通常用于 HTTP 压缩。如果你选择 `yes`，则在编译时启用 Brotli 压缩支持，通常是为了提高 Web 资源的压缩和传输效率。
- **默认**：`yes`（启用 Brotli 支持）

**2. `enable zstd support? [no] : y`**

- **Zstandard (zstd)** 是一种高效的压缩算法，它提供比传统压缩算法（如 gzip）更好的压缩比和速度。如果你选择 `y`，则启用 Zstandard 压缩支持。
- **用途**：通常用于高效的文件压缩和流式数据压缩。
- **默认**：`no`（不启用 Zstd 支持）

**3. `enable PostgreSQL database support? [no] : y`**

- **PostgreSQL** 是一种强大的关系型数据库管理系统。如果你选择 `y`，则启用对 PostgreSQL 数据库的支持。
- **用途**：用于通过 PHP 连接并操作 PostgreSQL 数据库。
- **默认**：`no`（不启用 PostgreSQL 支持）

**4. `enable ODBC database support? [no] : y`**

- **ODBC**（开放数据库连接）是一个允许不同类型的数据库通过统一接口访问的标准。如果你选择 `y`，则启用 ODBC 数据库的支持。
- **用途**：通常用于支持多种数据库（如 Microsoft SQL Server 或其他兼容 ODBC 的数据库）通过 ODBC 连接。
- **默认**：`no`（不启用 ODBC 支持）

**5. `enable Oracle database support? [no] : y`**

- **Oracle** 数据库是一个广泛使用的商业关系型数据库管理系统。如果你选择 `y`，则启用对 Oracle 数据库的支持。
- **用途**：允许 PHP 脚本连接和操作 Oracle 数据库。
- **默认**：`no`（不启用 Oracle 支持）

**6. `enable Sqlite database support? [no] : yes`**

- **SQLite** 是一种轻量级的关系型数据库，它存储在一个单独的文件中，非常适用于嵌入式应用。选择 `yes` 将启用 SQLite 支持。
- **用途**：用于开发轻量级应用程序或嵌入式数据库解决方案。
- **默认**：`no`（不启用 SQLite 支持）

**7. `enable swoole thread support (need php zts support)? [no] : yes`**

- **Swoole 线程支持**：如果你选择 `yes`，则启用 Swoole 扩展的线程支持。这要求 PHP 使用 **ZTS（Zend Thread Safety）** 模式编译。
- **用途**：使得 Swoole 支持多线程，并提升并发性能。
- **默认**：`no`（不启用线程支持）

**8. `enable iouring for file async support? [no] : yes`**

- **io_uring** 是 Linux 内核提供的一个异步 I/O 框架。启用此功能将允许 Swoole 使用 `io_uring` 来进行高效的异步文件 I/O 操作。
- **用途**：提高文件操作的异步性能，减少阻塞。
- **默认**：`no`（不启用 io_uring 支持）

如果你希望启用所有这些功能，你可以继续按提示选择 `y` 来启用它们。**启用 Brotli、Zstd、数据库支持和线程支持**：可以提高你的应用的性能，尤其是在高并发环境中。**启用 io_uring** 可以优化 I/O 性能，特别适合需要处理大量文件操作的场景。

如果这些功能适用于你的应用场景，选择 `yes` 启用它们是一个不错的选择。如果你不需要某些数据库支持或其他功能，可以保持默认的 `no`。

### 添加 swoole 到 php.ini

执行命令 `php.ini` 的路径，会看到类似以下的输出，显示了 `php.ini` 的文件路径：

   ```bash
   Loaded Configuration File:         /etc/php/8.4/cli/php.ini
   ```

vim 打开 `php.ini` 文件进行编辑。启用 Swoole 扩展，在 `php.ini` 文件中，找到并确保以下行没有被注释（去掉行首的分号 `;`）：

   ```ini
   extension=swoole.so
   ```

如果该行没有找到，可以手动添加它。在文件的底部添加：

   ```ini
   extension=swoole.so
   ```

修改完成后，保存文件并退出。

验证 Swoole 扩展是否成功启用，使用 `php -m` 命令检查已加载的扩展。

   ```bash
   php -m | grep swoole
   ```

如果 Swoole 已成功加载，你会看到输出类似于：

   ```bash
   swoole
   ```

![安装成功](https://cdn.xiaobinqt.cn/xiaobinqt.io/20250219/95278673c3954adaaa1a18f13f882dc0.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '安装成功')

### 注意点

这里直接看官方文档就好了，[在 phpinfo 中有在 php -m 中没有](https://wiki.swoole.com/zh-cn/#/question/install:~:text=%E5%9C%A8%20phpinfo%20%E4%B8%AD%E6%9C%89%E5%9C%A8%20php%20%2Dm%20%E4%B8%AD%E6%B2%A1%E6%9C%89)

## swoole 基本使用

### HTTP 服务器

安装完 Swoole 后，可以用它来启动一个简单的 HTTP 服务器，监听请求并处理路由。

1. 创建 HTTP 服务器

   你可以创建一个 `server.php` 文件，使用 Swoole 启动 HTTP 服务器，并设置两个路由 `/api/info` 和 `/api/userInfo`。

   ```php
   <?php
   // server.php

   // 创建 HTTP 服务器
   $server = new Swoole\Http\Server("127.0.0.1", 9501);

   // 设置路由
   $server->on("request", function ($request, $response) {
       $uri = $request->server['request_uri'];
       if ($uri == "/api/info") {
           // 处理 /api/info 请求
           $response->header("Content-Type", "application/json");
           $response->end(json_encode(["message" => "This is the api/info path.."]));
       } elseif ($uri == "/api/userInfo") {
           // 处理 /api/userInfo 请求
           $response->header("Content-Type", "application/json");
           $response->end(json_encode(["user" => "John Doe", "age" => 30,"path" => "api/userInfo"]));
       } else {
           // 其他路由
           $response->status(404);
           $response->end("Not Found");
       }
   });

   // 启动服务器
   $server->start();
   ```

2. 启动服务器
   在命令行中，进入到 `server.php` 所在的目录，运行以下命令启动服务器：
   ```bash
   php server.php
   ```

3. 访问路由
   启动后，服务器会在 `127.0.0.1:9501` 上监听请求。你可以通过浏览器或 Postman 等工具访问以下 URL：
    - `http://127.0.0.1:9501/api/info`
    - `http://127.0.0.1:9501/api/userInfo`

![response 返回](https://cdn.xiaobinqt.cn/xiaobinqt.io/20250219/8ab909b9f0fa479cbce9f942d38c3025.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'response 返回')

### 路由优化

#### 官方 router

很多时候需要路由分组等情况，可以使用 Swoole 官方 Router，它提供了更接近框架风格的路由管理方式。虽然，Swoole 提供了 HTTP 服务器和基本的请求处理方式，**但是**它并不直接包含类似 Swoole\Router 的路由类。

这玩意好像还要再装扩展，累了，下次再搞吧。TODO

#### nikic/fast-route

```shell
composer require nikic/fast-route
```

```php
<?php
require_once 'vendor/autoload.php';

// 创建路由调度器
$dispatcher = FastRoute\simpleDispatcher(function(FastRoute\RouteCollector $r) {
    // 路由分组
    $r->addGroup('/api', function(FastRoute\RouteCollector $r) {
        $r->addRoute('GET', '/info', 'infoHandler');
        $r->addRoute('GET', '/userInfo', 'userInfoHandler');
    });
});

// 创建 HTTP 服务器
$server = new Swoole\Http\Server("127.0.0.1", 9501);

$server->on("request", function ($request, $response) use ($dispatcher) {
    $uri = $request->server['request_uri'];
    $httpMethod = $request->server['request_method'];

    // 解析路由
    $routeInfo = $dispatcher->dispatch($httpMethod, $uri);

    switch ($routeInfo[0]) {
        case FastRoute\Dispatcher::NOT_FOUND:
            $response->status(404);
            $response->end("Not Found");
            break;
        case FastRoute\Dispatcher::METHOD_NOT_ALLOWED:
            $response->status(405);
            $response->end("Method Not Allowed");
            break;
        case FastRoute\Dispatcher::FOUND:
            $handler = $routeInfo[1];
            $handler($request, $response); // 调用对应的处理方法
            break;
    }
});

// 启动服务器
$server->start();

// 处理路由
function infoHandler($request, $response) {
    $response->header("Content-Type", "application/json");
    $response->end(json_encode(["message" => "This is the info endpoint."]));
}

function userInfoHandler($request, $response) {
    $response->header("Content-Type", "application/json");
    $response->end(json_encode(["user" => "John Doe", "age" => 30]));
}

```

![nikic/fast-route使用](https://cdn.xiaobinqt.cn/xiaobinqt.io/20250219/68197d88abbf4bcd88374015681c90cd.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'nikic/fast-route使用')

## 其他

### PHP 版本

```
php -v
PHP 8.2.0 (cli) (built: Dec 6 2022 12:45:32) (ZTS Visual C++ 2019 x64)
```

- **ZTS（线程安全）** 版本：WAMP 使用 **线程安全（Thread Safe, TS）** 版本的 PHP。
- **VC 版本**（Visual C++）：WAMP 通常使用 **VC15 或 VC16** 编译的 PHP。

### 常见错误

**缺少扩展**

```shell
553 source files, building
running: phpize
sh: 1: phpize: not found
ERROR: `phpize' failed
```

当你遇到 sh: 1: phpize: not found 错误时，说明系统中没有安装 phpize 工具。phpize 是一个用于编译 PHP 扩展的工具，通常与 PHP 开发包一起安装。

解决方法就是安装 PHP 开发包： phpize 工具通常包含在 PHP 的开发包中。在 Ubuntu 或 Debian 系统上，你需要安装相应版本的 PHP 开发包。

如果你使用的是 PHP 8.x，执行以下命令：

```shell
sudo apt install php8.4-dev
```

---

```shell
configure: error: Package requirements (libcares) were not met:
No package 'libcares' found

No package 'liburing' found
```

这个错误表明在编译或安装某个软件时，系统缺少 libcares 库。libcares 是一个用于异步 DNS 请求的 C 库，许多网络相关的软件（如 Swoole）依赖它。

```shell
sudo apt install libc-ares2 libc-ares-dev
sudo apt install liburing-dev
```

---

一些其他的扩展

```shell
sudo apt install php8.4-curl
sudo apt install php8.4-mysql
```

### php 常用命令

| **命令**                       | **用途**                               | **示例**                                                  |
|------------------------------|--------------------------------------|---------------------------------------------------------|
| `php -v` 或 `php --version`   | 查看当前安装的 PHP 版本                       | `php -v`<br>输出：`PHP 8.4.0 (cli) (built: Jan  1 2023)`   |
| `php -m`                     | 查看当前加载的 PHP 扩展                       | `php -m`<br>输出：列出所有已加载的扩展                               |
| `php -i`                     | 显示详细的 PHP 配置信息，包括 PHP 的信息、扩展等        | `php -i`<br>输出：详细的 PHP 配置信息                             |
| `php -l <file>`              | 检查指定 PHP 文件的语法错误                     | `php -l test.php`<br>输出：`No syntax errors detected`     |
| `php -r <code>`              | 直接执行 PHP 代码（无需创建文件）                  | `php -r 'echo "Hello, world!";'`<br>输出：`Hello, world!`  |
| `php -S <host>:<port>`       | 启动 PHP 内置 Web 服务器                    | `php -S localhost:8080`<br>启动内置服务器                      |
| `php -a`                     | 启动 PHP 交互模式（REPL）                    | `php -a`<br>进入交互模式并直接执行 PHP 代码                          |
| `php -d <directive>=<value>` | 临时修改 PHP 配置指令的值（不会改变 `php.ini` 配置文件） | `php -d display_errors=1 script.php`<br>启用错误显示          |
| `php -c <path_to_php.ini>`   | 指定使用的 `php.ini` 配置文件路径               | `php -c /path/to/custom/php.ini -m`<br>使用自定义的 `php.ini` |
| `php -h`                     | 查看 PHP 命令行的帮助信息，列出所有可用的命令选项          | `php -h`<br>显示所有 PHP 命令行选项                              |
| `php -z <file>`              | 加载指定的 Zend 扩展                        | `php -z /path/to/zend_extension.so`<br>加载扩展             |
| `php-fpm`                    | 管理 PHP FastCGI 进程管理器（用于 Web 服务器）     | `sudo systemctl restart php8.4-fpm`<br>重启 PHP-FPM       |
| `php-config`                 | 显示与 PHP 配置相关的信息，通常用于编译 PHP 扩展时获取配置参数 | `php-config --help`<br>显示配置参数                           |

## 参考

- [swoole 文档](https://wiki.swoole.com/zh-cn/#/)
