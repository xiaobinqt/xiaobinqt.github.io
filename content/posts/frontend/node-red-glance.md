---
title: "Node-RED 节点开发"
subtitle: "Low-code programming for event-driven applications"

init_date: "2022-04-01T10:45:32+08:00"

date: 2021-11-01

lastmod: 2022-04-01

draft: false

author: "xiaobinqt"
description: "Node-red,Low-code,自定义nodered节点,nodered,节点开发,how to create node-red node"

featuredImage: ""

reproduce: false

tags: ["low-code", "node-red"]
categories: ["开发者手册"]
lightgallery: true

toc: true

math:
    enable: true
---

## 概述

Node-RED 是构建物联网 (IOT,Internet of Things) 应用程序的一个强大工具，其重点是简化代码块的“连接"以执行任务。它使用可视 化编程方法，允许开发人员将预定义的代码块（称为“节点”，Node)
连接起来执行任务。连接的节点，通常是输入节点、处理节点和输出节点的组合，当它们连接在一起时，构成一个“流”(Flows)。

## 安装node-red

安装 node-red 的方式大致有 2 种，使用 docker 和 npm ，docker 安装可以[参考](https://hub.docker.com/r/nodered/node-red)。这里使用 npm 安装。个人觉得在本地调试
npm 比 docker 更方便一点，源码都在本地，docker 的话还需要把目录映射出来。

npm 安装直接一行命令就可以搞定，具体可以[参考](https://www.npmjs.com/package/node-red)

```npm
npm i node-red
```

安装成功后，会在用户目录下生成一个 .node-red 目录，我用的是 Windows 系统，所以这里的目录是 `C:\Users\weibin\.node-red`，这个目录下有配置文件 `settings.js`，里面有一些
node-red 配置项，比如默认端口等。

![node-red 目录](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220401/b9f737df274442a7b420a3f42c21e28d.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'node-red 目录')

## 启动

安装完成后，直接执行

```npm
node-red
```

就可以启动服务。

![cmd 启动 node-red](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220401/3d6ba253b0b143299d2dc813b5f80d26.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'cmd 启动 node-red')

node-red 的默认端口是 `1880`，直接用浏览器访问 `http://127.0.0.1:1880` 就可以看到 node-red 的页面。

![node-red 界面](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220401/91898a6735a64fb58df297e07d8b9f63.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'node-red 界面')

## 创建自定义节点

每一个 node-red 节点都是一个 npm 包，开发 npm 节点跟开发 npm 组件包是一样。

一个 node-red 节点主要包括两个文件，一个是 html 文件，一个是 js 文件。html 是界面配置，js 处理逻辑，加上 npm 的 package.json 文件，正常**三个文件就可以实现一个 node-red 节点**。

### 加法器节点开发

我们创建一个自定义节点实现一个加法器，输入两个数字，输出两个数字的和。

### 新建项目

我们新建一个节点项目 node-sum，这个项目随便放在那个目录下都行，这里我的目录是 `D:\tmp\node-sum`。

![新建项目](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220401/41153959469246afa75dca44d467a863.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '新建项目')

### npm 初始化

切到项目目录下，执行

```npm
npm init
```

将项目进行 npm 初始化，然后根据提示填写即可。

![npm init](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220401/c0026a5e7cd34a4bb1bdcdbeeb5b4379.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'npm init')

用 IDE 打开 node-sum 项目就可以看到已经给我们初始化好了 package.json 文件。

![package.json](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220401/4be9b27c770847b4ae7d46888eaefb48.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'package.json')

### 功能实现

sum.html

```html

<script type="text/javascript">
    RED.nodes.registerType('sum', { // 这个值 必须和 js 中 RED.nodes.registerType 的值一致
        category: '自定义节点', // 分类
        color: '#a6bbcf', // 节点颜色
        defaults: {
            name: {value: ""}, // name 默认是空
            add1: {value: 0}, // add1 默认值 0
            add2: {value: 0}, // add2 默认值 0
        },
        inputs: 0, // 节点有多少输入 0 或者多个
        outputs: 1, // 节点有多少输出 0 或者多个
        icon: "file.png", // 节点使用的图标
        paletteLabel: "加法器", // 节点显示的名称
        label: function () { // 节点的工作区的标签
            return this.name || "加法器";
        },
        // 钩子函数,双节节点调出 template 时触发
        oneditprepare: function () {
            console.log("oneditprepare 被调用");
        },
        // 钩子函数,点击 template 中的完成按钮时触发
        oneditsave: function () {
            console.log("oneditsave 被调用");
        }
    });
</script>

<!--data-template-name 必须和 js 中 RED.nodes.registerType 的值一致 -->
<!--template 是模板，可以理解成表单，节点需要的信息可以从这里输入-->
<script type="text/html" data-template-name="sum">
    <div class="form-row">
        <label for="node-input-name"><i class="fa fa-tag"></i> Name</label>
        <input type="text" id="node-input-name" placeholder="Name">
    </div>
    <div class="form-row">
        <label for="node-input-add1"><i class="fa fa-tag"></i>加数1</label>
        <input type="text" id="node-input-add1" placeholder="加数1">
    </div>
    <div class="form-row">
        <label for="node-input-add2"><i class="fa fa-tag"></i>加数2</label>
        <input type="text" id="node-input-add2" placeholder="加数2">
    </div>
</script>

<!--data-help-name 必须和 js 中 RED.nodes.registerType 的值一致 -->
<!--help 是节点的帮助文档-->
<script type="text/html" data-help-name="sum">
    <p>一个简单的加法器</p>
</script>
```

***

sum.js

```js
module.exports = function (RED) {
    function Sum(config) {
        RED.nodes.createNode(this, config);
        var node = this;

        // 获取输入的参数
        let add1 = parseInt(config.add1)
        let add2 = parseInt(config.add2)
        node.send({ // 向下一个节点输出信息
            payload: `${add1} + ${add2} 结果为 ` + (add1 + add2)
        });

        node.on('input', function (msg) { // 接收上游节点接收消息

        });
    }

    // 注册一个节点 sum,注册的节点不能重复也就是说同一个 node-red 项目不能有 2 个 registerType sum 节点
    RED.nodes.registerType("sum", Sum);
}
```

***

需要在 package.json 文件里添加 node-red 信息，完整的 package.json 如下：

```json
{
  "name": "node-sum",
  "version": "1.0.0",
  "description": "node-red 加法器",
  "main": "index.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "keywords": [
    "node-red",
    "add"
  ],
  "author": "xiaobinqt@163.com",
  "license": "ISC",
  "node-red": {
    "nodes": {
      "sum": "sum.js"
    }
  }
}

```

在 package.json 中添加的 node-red 信息是固定写法，可以理解成向 node-red 中注册了 nodes 的名称为 sum，注册的 js 文件为 sum.js。

```code
"node-red": {
    "nodes": {
      "sum": "sum.js"
    }
  }
```

### 本地安装

可以通过 `npm i ` 安装刚才的 sum 节点到 node-red 中。**切到`.node-red` 目录**下，执行

```code
npm i d:\tmp\node-sum
```

![安转本地节点并重启](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220401/ca420dae84014b20b6240bbf3bc43cea.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '安转本地节点并重启')

然后重启 node-red 就可以看到刚才安装的节点了。

![节点安装成功](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220401/b6e7c77292a64f69924bf9e29c758748.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '节点安装成功')

### 测试功能

把节点拖到工作区，双击节点（会触发`oneditprepare`函数）打开编辑区

![双节节点填写编辑区](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220401/4b0152769e1a4380bdd53f293076ef10.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '双节节点填写编辑区')

填写完编辑区内容后点击完成（会触发`oneditsave`函数），点击部署就会在调试窗口输出 `node.send` 信息。

![部署](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220401/adc4ec6a9f5442a584eff58a95a07496.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '部署')

## 参考

+ [Creating your first node](https://nodered.org/docs/creating-nodes/first-node)
+ [Design: i18n](https://github.com/node-red/node-red/wiki/Design:-i18n)