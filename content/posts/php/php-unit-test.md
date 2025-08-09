---
title: "php 中的单元测试"
subtitle: ""

weight:

init_date: "2025-05-17T19:10:07+08:00"

date: 2025-05-17

lastmod: 2025-05-17

draft: true

author: "xiaobinqt"
description: "xiaobinqt,单元测试，php 如何使用单元测试"

featuredImage: ""

featuredImagePreview: ""

reproduce: false

translate: false

tags: [ "php" ]
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

## 什么是单元测试

单元测试（Unit Testing）是针对程序中的最小可测试单元（通常是一个函数或类）进行的测试，目的是验证它的行为是否符合预期。

简单理解就是用程序写程序，验证自己的代码有没有问题。在 PHP 中使用单元测试是一种保障代码质量、提升开发效率的重要方式。

## 单元测试框架

### phpunit

[PHPUnit](https://phpunit.de/) 是 PHP 最主流的单元测试框架。

### co-phpunit

co-phpunit 是 [Swoole](https://openswoole.com/) 官方推荐的测试工具，它对 PHPUnit 做了封装，使其支持协程。

在使用 Swoole、Hyperf、EasySwoole 这类基于协程的框架，就需要用 co-phpunit 来替代标准的 phpunit。

## 使用 PHPUnit

### composer 项目中使用

对于使用了 Composer 的项目，推荐使用 Composer 安装 PHPUnit：

1. 安装 PHPUnit（本地依赖）：

```bash
composer require --dev phpunit/phpunit
```

2. 创建测试目录（一般命名为 `tests`）：

```
/your-project
├── src/
│   └── Calculator.php
├── tests/
│   └── CalculatorTest.php
├── vendor/
└── composer.json
```

3. 编写测试类（`tests/CalculatorTest.php`）：

```php
use PHPUnit\Framework\TestCase;
use YourNamespace\Calculator;

class CalculatorTest extends TestCase
{
    public function testAdd()
    {
        $calc = new Calculator();
        $this->assertEquals(4, $calc->add(2, 2));
    }
}
```

4. 执行测试：

```bash
./vendor/bin/phpunit tests
```

### 原生 PHP 项目中使用

如果项目没有使用 Composer，可以选择**全局安装 PHPUnit**：

1. 使用 `phar` 文件下载：

从 [https://phpunit.de/](https://phpunit.de/) 下载 `phpunit.phar` 文件：

```bash
wget https://phar.phpunit.de/phpunit-10.phar
chmod +x phpunit-10.phar
# 移动相应的环境变量目录
mv phpunit-10.phar /usr/local/bin/phpunit
```

确保执行后，输入：

```bash
phpunit --version
```

![](https://cdn.xiaobinqt.cn//xiaobinqt.io/20250517/303b7e3e286243929fc618d723c04096.png 'phpunit version')

2. 手动创建目录结构：

```
your-project/
├── lib/
│   └── Calculator.php        // 你的业务代码
├── tests/
│   └── CalculatorTest.php    // 测试类
├── phpunit.xml               // PHPUnit 配置文件（可选）
└── phpunit.phar              // 测试框架（如果未安装到系统）
```

3. 编写测试类

lib/Calculator.php

```php
<?php
// lib/Calculator.php
class Calculator
{
    public function add($a, $b)
    {
        return $a + $b;
    }

    public function divide($a, $b)
    {
        if ($b == 0) {
            throw new \Exception("Cannot divide by zero.");
        }
        return $a / $b;
    }
}

```

tests/CalculatorTest.php

```php
<?php

namespace tests;

require_once __DIR__ . '/../lib/Calculator.php';

use lib\Calculator;
use PHPUnit\Framework\TestCase;

class CalculatorTest extends TestCase
{
    public function testAdd()
    {
        $calc = new Calculator();
        $this->assertEquals(5, $calc->add(2, 3));
    }

    public function testDivide()
    {
        $calc = new Calculator();
        $this->assertEquals(2, $calc->divide(4, 2));
    }

    public function testDivideByZero()
    {
        $calc = new Calculator();
        $this->expectException(\Exception::class);
        $calc->divide(4, 0);
    }

    public function testAddErr()
    {
        $calc = new Calculator();
        $this->assertEquals(10, $calc->add(2, 3));  // ❌ 故意写错，2 + 3 实际是 5
    }
}
```

4. 运行测试：

```bash
phpunit tests/CalculatorTest.php
// 或者
php phpunit-10.phar tests/CalculatorTest.php

```

![](https://cdn.xiaobinqt.cn//xiaobinqt.io/20250517/09349f2ce7734c8ab28f41c4601b37d9.png '运行 phpunit')

## 配置文件 `phpunit.xml`

用于配置默认的测试路径、bootstrap 文件、测试套件等：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<phpunit bootstrap="vendor/autoload.php"
         colors="true">
    <testsuites>
        <testsuite name="Application Test Suite">
            <directory>./tests</directory>
        </testsuite>
    </testsuites>
</phpunit>
```

## 使用 co-phpunit





