---
title: "nodeJS 调用 C 语言"
subtitle: "How to call C function from nodeJS"

init_date: "2022-04-11T10:47:02+08:00"

date: 2021-11-18

lastmod: 2022-04-11

draft: false

author: "xiaobinqt"
description: "xiaobinqt,node-addon-api,js 调用 c 语言,jc call c function,How to call C function from nodeJS,node 调用C/C++ 方法"

featuredImage: ""

reproduce: false

tags: ["js"]
categories: ["web"]
lightgallery: true

toc:
auto: false

math:
enable: true
---

最近在 node 项目开发中，有个需求是 nodeJS 需要支持调用 C 语言的函数，[node-addon-api](https://www.npmjs.com/package/node-addon-api) 可以支持这个需求。

## 开发环境

我用的开发环境 docker 起的 code-server 环境，code-server
版本为 [code-server:version-v3.11.1](https://hub.docker.com/r/linuxserver/code-server/tags?page=1&name=3.11.1) 。可以把
code-server 理解成一个在线 vscode 环境，就像 github 的在线 web 编辑器一样。

```docker
docker pull linuxserver/code-server:version-v3.11.1
```

![code-server](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220412/9a6234c147f34cfe86d67b72902aa1cf.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'code-server')

![github web 编辑器](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220412/1452c3a995af4dd480963de599766c73.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'github web 编辑器')

## 加法器

开发环境搭建成功后，可以实现一个小功能，以熟悉 node-addon-api 的使用。

现在实现一个加法器，JS 调用 C 语言的 add 方法，传入 2 个参数，C 语言累加后返回结果。

### 项目初始化

创建项目并进行 `npm init` 初始化：

![创建项目并初始化](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220412/f3f108e8c5664b1390766008751decb0.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '创建项目并初始化')

安装 node-addon-api：

```npm
npm i node-addon-api
```

![安装 npm 依赖包](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220412/eecca630b11b49bf840351bd5c6dfe06.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '安装 npm 依赖包')

### c 代码

新建一个 cal.cc 文件，内容如下：

```c
#include <napi.h>

// 定义一个 Add() 方法
Napi::Value Add(const Napi::CallbackInfo& info) {
  Napi::Env env = info.Env(); // 获取 js 上下文信息

  if (info.Length() < 2) {
    Napi::TypeError::New(env, "Wrong number of arguments")
        .ThrowAsJavaScriptException();
    return env.Null();
  }

  if (!info[0].IsNumber() || !info[1].IsNumber()) {
    Napi::TypeError::New(env, "Wrong arguments").ThrowAsJavaScriptException();
    return env.Null();
  }

  int arg0 = info[0].As<Napi::Number>().Int32Value();
  int arg1 = info[1].As<Napi::Number>().Int32Value();

  int arg2 = arg0 + arg1;
  
  Napi::Number num = Napi::Number::New(env, arg2);

  return num;
}

// 导出函数，可使用 exports.Set() 导出多个函数
Napi::Object Init(Napi::Env env, Napi::Object exports) {
  exports.Set(Napi::String::New(env, "add"), Napi::Function::New(env, Add));
  return exports;
}

NODE_API_MODULE(addon, Init)

```

### binding.gyp

编译带第三方扩展库的 c/c++ 程序，通常需要在编译时指定额外的头文件包含路径和链接第三方库，这些都是在 binding.gyp 文件中指定的，这些指定在 nodeJS 自动编译的时候，会解析并应用在命令行的编译工具中。

新建一个 binding.gyp 文件，内容如下：

```json
{
  "targets": [
    {
      "target_name": "test",
      "sources": [
        "cal.cc"
      ],
      "include_dirs": [
        "<!@(node -p \"require('node-addon-api').include\")"
      ],
      "libraries": [
      ],
      "dependencies": [
        "<!(node -p \"require('node-addon-api').gyp\")"
      ],
      "cflags!": [
        "-fno-exceptions"
      ],
      "cflags_cc!": [
        "-fno-exceptions"
      ],
      "defines": [
        "NAPI_CPP_EXCEPTIONS"
      ],
      "xcode_settings": {
        "GCC_ENABLE_CPP_EXCEPTIONS": "YES"
      }
    }
  ]
}

```

+ `target_name` 指定了编译之后模块的名称。
+ `sources` 指明 c/c++ 的源文件，如果有多个文件，需要用逗号隔开，放到同一个数组中。
+ `include_dirs` 是编译时使用的头文件引入路径，这里使用 `node -p` 执行 node-addon-api 模块中的预置变量。
+ `dependencies` 是必须的，一般不要改变。
+ `cflags!`，`cflags_cc!`，`defines` 三行指定如果c++程序碰到意外错误的时候，由 NAPI 接口来处理，而不是通常的由 c/c++ 程序自己处理。这防止因为 c/c++
  部分程序碰到意外直接就退出了程序，而是由 nodeJS 程序来捕获处理，如果是在Linux中编译使用，有这三行就够了。

### 编译调用

![编译](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220412/04a96bb9ac254b30a65ffa2939134d05.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '编译')

> 每次修改代码后都需要执行 `npm i` 重新编译

```npm
npm i 
```

编译后，进入 nodeJS 中可以直接 require 调用。

![调用](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220412/0eac8fccb7334cb5bbde15a5bd25c573.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '调用')

这里 require 的 `test.node`，`.node` 后缀是固定的，`test` 就是 binding.gyp 文件里 `target_name` 的值。

`1+3=4` 从调用结果来看，符合预期。

### bindings 包

现在我们 require 编译后的 node 需要这样写：

```js
require('./build/Release/nodecamera.node');
```

可以用 `bindings` 包简化 require 。

```npm
npm i bindings --save
```

通估:point_up_2:命令安装 `bindings` 包。

![bindings 包使用](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220412/518e631de25144c0a7558b36a50c4375.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'bindings 包使用')

所以以上示例简化后的 require 为：

```js
const addon = require('bindings')('test.node');
```

## 常见数据类型转换

JS 与 C 的数据类型有较大差别，比如 C 中没有字符串的概念，只有字节数组等。node-addon-api 可以很好的支持 JS 与 C 数据类型的转换。

### 字符串

```c
std::string temp = info[0].As<Napi::String>().ToString();
```

![字符串转换示例](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220412/bd714b564556421b83480d47b7c00c9e.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '字符串转换示例')

### ArrayBuffer

```c
Napi::ArrayBuffer ABuffer(const Napi::CallbackInfo& info) {
  Napi::Env env = info.Env(); 
  int8_t num[4] = {14,25,45,88};
  Napi::ArrayBuffer x = Napi::ArrayBuffer::New(env,num,4);
  return x;
}
```

![ArrayBuffer 示例](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220412/d6d3e0a559f14e7db556152c7e165a33.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'ArrayBuffer 示例')

### 数组

JS 将数组作为 C 函数参数。

```c
Napi::Value ArrayArg(const Napi::CallbackInfo& info) {
  Napi::Env env = info.Env(); 
  Napi::Array b = info[0].As<Napi::Array>();
  for (int i = 0; i < b.Length(); i++)
  {
      Napi::Value v = b[i];
      if (v.IsString()){
          std::string value = (std::string)v.As<Napi::String>();
          return Napi::String::New(env,value);
      }
  }
}
```

![编译可能有 warning](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220412/a5e1c3db4491444394f51cbee383df45.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '编译可能有 warning')

编译时可能有 warning，但是不影响。

![数组参数](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220412/3a4b15094092464b8608c0d3f8bdda85.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '数组参数')

## FAQ

### 持久化函数

这个功能可以理解成在 C 的内存空间中有一个 JS 的函数对象且在生命周期内不会被 C 垃圾回收，可以直接在 C 中调用这个 JS 函数。

以下示例，C 提供了 debug 函数，但是参数是一个函数，这个函数会持久在 C 的内存中，在 C 的 Str 函数中用 Call 来调用这个函数并传入对应的参数。

js-call-c-demo.js

```js
const addon = require('bindings')('test.node');

// 调用 c 中的 debug 函数，将函数注入到 c 中
addon.debug(msg => {
    console.log("debug console, c 中传入的 msg 需要打印的参数值为：", msg)
})

// 调用 c 的 str 函数，在 str 函数中会调用 debug 函数中的 console.log()
console.log("str 函数的返回值为: ", addon.str("xiaobinqt"))
```

cal.cc

```c
#include <napi.h>


Napi::FunctionReference Debug;
napi_env DebugEnv;


Napi::Value DebugFun(const Napi::CallbackInfo& info) {
  Napi::Env env = info.Env(); 
  Debug = Napi::Persistent(info[0].As<Napi::Function>());
  DebugEnv = env; 
  return Napi::String::New(env,"OK");
}


Napi::Value Str(const Napi::CallbackInfo& info) {
  Napi::Env env = info.Env(); 
  std::string temp = info[0].As<Napi::String>().ToString();
  Napi::String s = Napi::String::New(env, temp);
  // 调用 Debug 函数
  Debug.Call({Napi::String::New(DebugEnv,"我是一个测试 debug")});
  return s;
}


// 定义一个 Add() 方法
Napi::Value Add(const Napi::CallbackInfo& info) {
  Napi::Env env = info.Env(); // 获取 js 上下文信息

  if (info.Length() < 2) {
    Napi::TypeError::New(env, "Wrong number of arguments")
        .ThrowAsJavaScriptException();
    return env.Null();
  }

  if (!info[0].IsNumber() || !info[1].IsNumber()) {
    Napi::TypeError::New(env, "Wrong arguments").ThrowAsJavaScriptException();
    return env.Null();
  }

  int arg0 = info[0].As<Napi::Number>().Int32Value();
  int arg1 = info[1].As<Napi::Number>().Int32Value();

  int arg2 = arg0 + arg1;
  
  Napi::Number num = Napi::Number::New(env, arg2);

  return num;
}



Napi::ArrayBuffer ABuffer(const Napi::CallbackInfo& info) {
  Napi::Env env = info.Env(); 
  int8_t num[4] = {14,25,45,88};
  Napi::ArrayBuffer x = Napi::ArrayBuffer::New(env,num,4);
  return x;
}


Napi::Value ArrayArg(const Napi::CallbackInfo& info) {
  Napi::Env env = info.Env(); 
  Napi::Array b = info[0].As<Napi::Array>();
  for (int i = 0; i < b.Length(); i++)
  {
      Napi::Value v = b[i];
      if (v.IsString()){
          std::string value = (std::string)v.As<Napi::String>();
          return Napi::String::New(env,value);
      }
  }
}



// 导出函数，可使用 exports.Set() 导出多个函数
Napi::Object Init(Napi::Env env, Napi::Object exports) {
  exports.Set(Napi::String::New(env, "add"), Napi::Function::New(env, Add));
  exports.Set(Napi::String::New(env, "str"), Napi::Function::New(env, Str));
  exports.Set(Napi::String::New(env, "ab"), Napi::Function::New(env, ABuffer));
  exports.Set(Napi::String::New(env, "arr"), Napi::Function::New(env, ArrayArg));
  exports.Set(Napi::String::New(env, "debug"), Napi::Function::New(env, DebugFun));
  return exports;
}

NODE_API_MODULE(addon, Init)

```

![测试结果](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220412/0329f648225d4aac9b0201a4fe8a1589.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '测试结果')

## 参考

+ [简单上手nodejs调用c++(c++和js的混合编程)](https://www.cnblogs.com/andrewwang/p/9409876.html)
+ [node-addon-api-doc](https://github.com/nodejs/node-addon-api/tree/9bea434326d5e6c6fa355a51b6f232a503521a21/doc)
+ [https://github.com/nodejs/node-addon-api](https://github.com/nodejs/node-addon-api)
+ [https://nodejs.github.io/node-addon-examples/special-topics/object-function-refs#persistent-reference](https://nodejs.github.io/node-addon-examples/special-topics/object-function-refs#persistent-reference)