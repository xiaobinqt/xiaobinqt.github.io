---
title: "个人简历"

init_date: "2022-11-06"

date: 2022-11-06

lastmod: 2022-11-06

author: "xiaobinqt"
description: "xiaobinqt的个人简历,萧十一郎的个人简历,简历"
resources:

tags: [ "" ]
categories: [ "" ]
lightgallery: true

toc: true

math: true

header:
  number:
    enable: false
---

## 个人信息

+ 卫彬/男/1994
+ 手机/微信：15209272743
+ Github：[https://github.com/xiaobinqt](https://github.com/xiaobinqt)
+ DockerHub：[https://hub.docker.com/u/xiaobinqt](https://hub.docker.com/u/xiaobinqt)
+ 个人网站：[https://www.xiaobinqt.cn](https://www.xiaobinqt.cn) / [https://xiaobinqt.github.io](https://xiaobinqt.github.io/)
+ Email：[xiaobinqt@163.com](mailto:xiaobinqt@163.com)
+ 开源项目：[Go微信机器人](https://github.com/xiaobinqt/go-wxbot) / [豆奶签到](https://github.com/xiaobinqt/dounai-checkin)

## 教育经历

[西安培华学院](https://www.peihua.cn/)

通信工程 &emsp; &emsp; 本科 &emsp; &emsp; 2012 - 2016

## 个人技能

+ 熟练使用 Go 语言进行项目开发，对 Slice、Map、Goroutine、Channel 有深入了解，擅长并发编程；
+ 熟练使用 Gin、GRPC、GoFrame、Go-kratos 等 web 和微服务框架，熟悉熔断，限流，服务治理等；
+ 深入理解 CSP 模型，深入理解 GC 垃圾回收机制和三色标记法，有过实际性能调优经验;
+ 熟悉 MySQL 的存储引擎、事务隔离级别、锁、索引，有 MySQL 的性能调优经验;
+ 熟悉 Redis 持久化机制、过期策略以及集群部署;
+ 熟悉 RabbitMQ 消息队列事务消息底层原理，掌握消息丢失、消息重复等问题的解决方案;
+ 熟练使用 Docker 和 K8S，有 CICD 经验；擅长敏捷开发；熟练使用常见的设计模式；
+ 精通基于 LNMP 环境的编程，具备扎实的 PHP 基础知识，理解面向对象编程思想。
+ 熟练使用 Yii、ThinkPHP 和 Laravel 等框架进行快速开发，了解基本的核心源代码，熟悉 swoole 扩展。
+ 熟练使用 python 编写脚本。

## 自我评价

+ 热爱代码，对开源抱有极大的热情，曾给多个开源项目贡献代码。有坚持做一件事的毅力和决心。
+ 良好的沟通能力，学习能力，适应能力强及团队协作意识，具有主人翁意识。

## 期望职位

+ 期望职位：Golang 开发 / PHP 开发

## 工作经历

### [希云科技（北京）有限公司](http://xii.cloud/) （ 2021/4 ~ 2024/6）

在公司担任 Go 开发，参与研发了 [柔性开发仿真一体化项目](http://g.xii.cloud:42225/) 和 xae 项目。目前柔性开发仿真一体化项目已上线，服务于国家电网，该项目是组态化微应用开发仿真发布一体化云平台，可以帮助客户快速开发应用并部署。信创项目 xae 项目，目的是赋能企业数字化转型，快速搭建迁徙适配测试平台。

### 北京腾讯公司 （ 2019/4 ~ 2021/4 ）

在北京腾讯总部参与了星盘数据平台和烽火统一 PUSH 平台的开发。星盘数据平台使用 php 开发。PUSH 平台使用 Go 开发，主要使用了 Go 协程，channel 等提高系统整体性能和并发。

### [西安维客软件科技有限公司](https://www.victtech.com/) （ 2017/4 ~ 2019/3 ）

在公司担任 PHP 开发并在项目中接触到 Go，主动学习并使用 Go 开发一些小功能。主要在公司参与了 pop 商城，医疗器械租赁项目，小程序和一些 [wordpress](https://wordpress.com) 项目的开发，如 [西班牙旅游网站](http://aragontourism.cn)。

## 项目经验

### 柔性云

**项目描述**

柔性云是组态化微应用开发仿真发布一体化云平台，后端技术栈使用 go-kratos + mysql + rabbitmq + docker + nodered + gitea + verdaccio。项目旨在帮助国家电网开发人员通过低代码，组件化快速构建微应用，测试并发布。用户注册成功后生成独立的开发盘和虚拟机，通过容器自动部署 [Node-RED](https://github.com/node-red) 低代码平台和在线 IDE [code-server](https://github.com/coder/code-server) 环境，用户可以在开发环境开发节点和测试。用户测试成功的节点包可以发布到中心的 [npm](https://github.com/verdaccio/verdaccio) 仓库。

**项目职责**

+ 负责项目整体的搭建和研发，架构的设计，日常问题的解决。
+ 负责低代码平台 [node-red](https://github.com/node-red/node-red) 基于源码问题的修改。
+ 负责项目上线后客户问题的实时解决。

**项目成果**

+ 支持业务快速迭代，客户在使用过程中系统稳定运行。
+ 获得反向代理，多路复用和 node，npm，docker 等使用经验。
+ 参与开源并贡献代码 [mojocn/base64Captcha#7c33ebb7](https://github.com/mojocn/base64Captcha/commit/7c33ebb78373a5dd5f7e9a4988e09bbcbc01bd14)，[node-red/node-red#380a0824](https://github.com/node-red/node-red/commit/380a08242af44b1ee54453790b0df076b445bbd5)，[node-red/node-red#fd42becb](https://github.com/node-red/node-red/commit/fd42becbdcb6546351474c4966b189d3ced68c3c)。

### xae

**项目描述**

后端技术栈使用 go + gin + mysql + docker + elasticsearch，该项目以数字化引领信创技术，以信创筑牢数字化建设。可以通过 xae 平台给公司赋能，快速搭建迁徙适配测试平台。xae 平台包括厂商管理，产品管理，适配测试，数据迁徙，CI/CD，知识库，证书管理，自动化部署等功能。

**项目职责**

+ 需求分析评审，主要业务功能的开发与开发维护。
+ 跟合作伙伴博睿共同推进项目，将博睿的产品 ZCBUS 嵌入 xae 系统。

**项目成果**

+ 一期目前已通过太极演示，正在太极内网试运行。大唐，北控已经上线使用。

### 烽火统一 PUSH 平台

**项目描述**

后端技术栈使用 go + trpc + redis + kafka。本项目是看点快报和 QQ 浏览器的运营后台。项目使用 Go 开发。接入腾讯视频，新闻文章等，帮助编辑快速审核文章，将优质文章快速 push 给移动端用户。接入监控平台，实时观测接口调用耗时等情况。

**项目职责**

+ 文章自动化接入，日常需求开发和维护。
+ 腾讯 007 监控平台，polaris，trpc-go 等平台和技术的调研和使用。

**项目成果**

+ 腾讯年度业务突破奖。
+ PHP 迁徙到 Go 的项目，熟悉了 Go 语法，Go 中 channel，协程和并发编程的使用，获得了 Go 项目的实战经验。
+ 熟悉腾讯的开发规范，内部 trpc-go 框架的使用。

### 星盘数据平台

**项目描述**

星盘主要是由 php 开发，是由 PCG 兴趣阅读产品部设计并研发的综合型数据平台，面向产品，运营，业务研发和数据发等各类需求方，提供数据生产消费各个环节的相关服务。平台主要功能有数据分析，数据管理和专题工具几大类。主要功能有仪表盘、实时数据，元数据，数据模型和权限等功能。

**项目成果**

+ 腾讯年度技术突破奖

### 聚美医后台

**项目描述**

后端技术栈包括 php + laravel + mysql + redis + docker，该项目是一个医学器材租借管理系统。采用前后端分离。项目工作流为商务部新建合同，合同转到财务交租，交租成功后仓储部发货，运营负责数据的报表管理。

**项目职责**

+ 日常需求的开发与维护，跟需求方的日常沟通。
+ 微信服务的相关调研与开发，如公众号/小程序推送。七牛云服务的相关使用。

**项目成果**

+ 支持业务的开度更迭和稳定运行。
+ 获取 docker，微信SDK [EasyWeChat](https://easywechat.com) 和七牛云服务的相关使用经验。
+ 参与开源并贡献代码 [SocialiteProviders/Weixin#44bc75b7](https://github.com/SocialiteProviders/Weixin/commit/44bc75b7d98760ce32e71331f28871ccb186546a)。

### 潘帕斯 pop 商城

**项目描述**

后端技术栈由 php + laravel + mysql + docker 组成。商城功能包括用户管理，商品分类，商品搜索，购物车功能。平台端可以管理健身房和教练，查看教练的销售业绩和销售提成，供应商端可以对平台端的订单进行管理和发货，对商品进行管理操作。

**项目成果**

+ 熟悉 [Laravel5.5](https://learnku.com/docs/laravel/5.5) 框架和 [composer](https://getcomposer.org/) 在项目中的使用。
+ 获得企业微信开发经验，微信支付和 Redis 相关使用经验。
+ 参与 [Laravel 社区](https://learnku.com/laravel) 的 [Laravel 5.8 中文文档](https://learnku.com/docs/laravel/5.8?mode=translators#:~:text=Narcissus%20%E4%B8%BA%E6%9C%AC%E6%96%87%E6%A1%A3%E8%B4%A1%E7%8C%AE%E4%BA%86%202%20%E4%B8%AA%E7%BF%BB%E8%AF%91) 翻译。
