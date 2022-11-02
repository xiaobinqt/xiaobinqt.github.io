---
title: "跨域问题"
subtitle: ""

init_date: "2022-04-18T14:15:18+08:00"

date: 2019-03-18

lastmod: 2022-04-18

draft: false

author: "xiaobinqt"
description: "xiaobinqt,什么是跨域,如何解决跨域问题,什么是JSONP,什么是 CORS,简单请求,复杂请求,跨域预检机制"

featuredImage: ""

reproduce: false

tags: ["web"]
categories: ["web"]
lightgallery: true

toc: true

math: true
---

<!-- author： xiaobinqt -->
<!-- email： xiaobinqt@163.com -->
<!-- https://xiaobinqt.github.io -->
<!-- https://www.xiaobinqt.cn -->

## 同源策略

同源策略是浏览器的一个安全行为，是指浏览器对不同源的脚本或文本的访问方式进行限制。比如，ajax 在进行请求时，浏览器要求当前网页和请求地址必须同源，也就是协议，域名和端口必须相同。

同源指的就是相同的协议，域名，端口号。

浏览器是公共资源，假如没有同源策略，A 网站的接口可以被任意来源的 ajax 请求访问，这样就会出现问题，这是浏览器出于对用户数据的保护。

比如在使用淘宝的过程中，淘宝返回了一个
cookie，下次请求你会带上cookie，这样子服务器就知道你登录过了。

假设，你买东西过程中，又点来了一个链接，由于没有同源策略，他就在后台操作向淘宝发起请求，那么就相当于不法网站利用你的账号为所欲为了。

同源策略限制的不同源之间的交互，主要是针对 JS 中的 XMLHttpRequest 请求。有一些情况是不受影响的如：html 的一些标签的请求，链接 a 标签，图片 img 标签等，这些标签的请求可以为不同源地址。

同源策略限制了 Cookie、LocalStorage 和 IndexDB 无法读取，DOM 和 JS 对象无法获取，Ajax 请求无法发送。

所以，**协议，域名，端口号只要有一个不同就存在跨域**。

解决跨域问题常用的有 JSONP 和 CORS 这两种方案，以下对他们分别进行介绍。

## jsonp

jsonp 虽然能解决跨域问题，它**只支持`GET`请求**:cry:。

jsonp 是利用`<script>`标签没有跨域限制的“漏洞”来达到与第三方通讯的目的。当需要通讯时，本站脚本创建一个`<script>`元素，地址指向第三方的API网址，形如：

```javascript
<script src="http://www.example.net/api?param1=1&param2=2"></script> 
```

并**提供一个回调函数**来接收数据（函数名可约定，或通过地址参数传递）。 第三方产生的响应为 json 数据的包装，所以称之为 [jsonp]^(json padding)，形如：

```json
callback({
  "name": "吴彦祖",
  "age": "28"
})
```

这样浏览器会调用 `callback` 函数，并传递解析后json对象作为参数。本站脚本可在`callback`函数里处理所传入的数据。

> 接口返回的函数名一定要跟定义的函数一致

有一个接口`http://127.0.0.1:8080/cb`返回 jsonp 数据:point_down:

![jsonp 接口](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220429/bf6cb2d030c34c05930e9a9b0d86948f.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'jsonp 接口')

html 文件：

```html
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>


<script>
    let script = document.createElement('script');
    script.type = 'text/javascript';  //请求接口地址和参数
    script.src = 'http://127.0.0.1:8080/cb';
    document.body.appendChild(script); //请求后的回调函数
    function callback(res) {
        console.log(res)
    }
</script>

</body>
</html>

```

效果:point_down:

![执行效果](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220429/bc4a3d24c10d4b06a24cd3d4005fa092.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '执行效果')

## CORS

整个[CORS]^(Cross-origin resource sharing)
通信过程，都是浏览器自动完成，不需要用户参与。对于开发者来说，CORS通信与同源的AJAX通信没有差别，代码完全一样。

因此，实现CORS通信的**关键是服务器**。只要服务器实现了CORS接口，就可以跨源通信。它允许浏览器向跨源服务器，发出`XMLHttpRequest`
请求，浏览器一旦发现AJAX请求跨源，就会自动添加一些附加的头信息，有时还会多出一次附加的请求，从而克服了 AJAX
只能同源使用的限制。

### 两种请求

浏览器将CORS请求分成两类：[简单请求]^(simple request)和[非简单请求]^(not-so-simple request)。只要**同时满足**:point_down:两大条件，就属于简单请求。

1. 请求方法是以下三种方法之一：

+ `HEAD`
+ `GET`
+ `POST`

2. HTTP 头信息不超出以下几种字段：

+ `Accept`
+ `Accept-Language`
+ `Content-Language`
+ `Last-Event-ID`
+ `Content-Type`：只限于三个值`application/x-www-form-urlencoded`、`multipart/form-data`、`text/plain`

> 除了由用户代理自动设置的头（如，`Connection`、 `User-Agent`）

这是为了兼容[表单]^(form)，历史上表单一直可以发出跨域请求。**AJAX 的跨域设计就是，只要表单可以发，AJAX 就可以直接发**。

凡是不同时满足上面两个条件，就属于非简单请求。

浏览器对这两种请求的处理，是不一样的。

### 简单请求

对于简单请求，浏览器直接发出CORS请求。在头信息之中，增加一个`Origin`字段。

下面的例子，浏览器发现这次跨源 AJAX 请求是简单请求，就自动在头信息之中，添加一个`Origin`字段。

```shell
GET /cors HTTP/1.1
Origin: http://api.bob.com
Host: api.alice.com
Accept-Language: en-US
Connection: keep-alive
User-Agent: Mozilla/5.0...
```

上面的头信息中，`Origin`字段用来说明，本次请求来自哪个源（协议 + 域名 + 端口）。服务器根据这个值，决定是否同意这次请求。

如果`Origin`
指定的源，**不在许可范围内**，服务器会返回一个**正常的**
HTTP回应。浏览器发现，这个回应的头信息没有包含A`ccess-Control-Allow-Origin`字段（详见下文），就知道出错了，从而抛出一个错误，被`XMLHttpRequest`的`onerror`
回调函数捕获。这种错误无法通过状态码识别，因为HTTP回应的状态码有可能是200。

如果`Origin`指定的域名在许可范围内，服务器返回的响应，会多出几个头信息字段。

```shell
Access-Control-Allow-Origin: http://api.bob.com
Access-Control-Allow-Credentials: true
Access-Control-Expose-Headers: FooBar
Content-Type: text/html; charset=utf-8
```

上面的头信息之中，有三个与CORS请求相关的字段，都以`Access-Control-`开头。

+ **Access-Control-Allow-Origin**

该字段是必须的。它的值要么是请求时`Origin`字段的值，要么是一个`*`，表示接受任意域名的请求。

+ **Access-Control-Allow-Credentials**

该字段可选。它的值是一个布尔值，表示是否允许发送Cookie。默认情况下，Cookie不包括在CORS请求之中。设为true，即表示服务器明确许可，Cookie可以包含在请求中，一起发给服务器。这个值也只能设为true，如果服务器不要浏览器发送Cookie，删除该字段即可。

+ **Access-Control-Expose-Headers**

该字段可选。CORS请求时，`XMLHttpRequest`对象的`getResponseHeader()`
方法只能拿到6个基本字段：`Cache-Control`、`Content-Language`、`Content-Type`、`Expires`、`Last-Modified`、`Pragma`
。如果想拿到其他字段，就必须在`Access-Control-Expose-Headers`里面指定。上面的例子指定，`getResponseHeader('FooBar')`可以返回`FooBar`字段的值。

#### withCredentials 属性

CORS请求默认不发送Cookie和HTTP认证信息。如果要把Cookie发到服务器，一方面要服务器同意，指定`Access-Control-Allow-Credentials`字段。

```shell
Access-Control-Allow-Credentials: true
```

另一方面，开发者必须在AJAX请求中打开`withCredentials`属性。

```shell
var xhr = new XMLHttpRequest();
xhr.withCredentials = true;
```

否则，即使服务器同意发送Cookie，浏览器也不会发送。或者，服务器要求设置Cookie，浏览器也不会处理。

但是，如果省略`withCredentials`设置，有的浏览器还是会一起发送Cookie。这时，可以显式关闭`withCredentials`。

```shell
xhr.withCredentials = false;
```

需要注意的是，如果要发送Cookie，`Access-Control-Allow-Origin`就不能设为星号`*`
，必须指定明确的、与请求网页一致的域名。同时，Cookie依然遵循同源政策，只有用服务器域名设置的Cookie才会上传，其他域名的Cookie并不会上传，且（跨源）原网页代码中的`document.cookie`
也无法读取服务器域名下的Cookie。

### 非简单请求

#### 预检请求

非简单请求是那种对服务器有特殊要求的请求，比如请求方法是`PUT`或`DELETE`，或者`Content-Type`字段的类型是`application/json`。

非简单请求的CORS请求，会在正式通信之前，增加一次HTTP查询请求，称为["预检"请求]^(preflight request)。

浏览器先询问服务器，当前网页所在的域名是否在服务器的许可名单之中，以及可以使用哪些HTTP动词和头信息字段。只有得到肯定答复，浏览器才会发出正式的`XMLHttpRequest`请求，否则就报错。

下面是一段浏览器的JavaScript脚本。

```javascript
var url = 'http://api.alice.com/cors';
var xhr = new XMLHttpRequest();
xhr.open('PUT', url, true);
xhr.setRequestHeader('X-Custom-Header', 'value');
xhr.send();
```

上面代码中，HTTP请求的方法是`PUT`，并且发送一个自定义头信息`X-Custom-Header`。

浏览器发现，这是一个非简单请求，就自动发出一个"预检"请求，要求服务器确认可以这样请求。下面是这个"预检"请求的HTTP头信息。

```shell
OPTIONS /cors HTTP/1.1
Origin: http://api.bob.com
Access-Control-Request-Method: PUT
Access-Control-Request-Headers: X-Custom-Header
Host: api.alice.com
Accept-Language: en-US
Connection: keep-alive
User-Agent: Mozilla/5.0...
```

"预检"请求用的请求方法是`OPTIONS`，表示这个请求是用来询问的。头信息里面，关键字段是`Origin`，表示请求来自哪个源。

除了`Origin`字段，"预检"请求的头信息包括两个特殊字段。

+ **Access-Control-Request-Method**

该字段是必须的，用来列出浏览器的CORS请求会用到哪些HTTP方法，上例是PUT。

+ **Access-Control-Request-Headers**

该字段是一个**逗号分隔**的字符串，指定浏览器CORS请求会额外发送的头信息字段，上例是`X-Custom-Header`。

#### 预检请求的回应

服务器收到"预检"请求以后，检查了`Origin`、`Access-Control-Request-Method`和`Access-Control-Request-Headers`字段以后，确认允许跨源请求，就可以做出回应。

```shell
HTTP/1.1 200 OK
Date: Mon, 01 Dec 2008 01:15:39 GMT
Server: Apache/2.0.61 (Unix)
Access-Control-Allow-Origin: http://api.bob.com
Access-Control-Allow-Methods: GET, POST, PUT
Access-Control-Allow-Headers: X-Custom-Header
Content-Type: text/html; charset=utf-8
Content-Encoding: gzip
Content-Length: 0
Keep-Alive: timeout=2, max=100
Connection: Keep-Alive
Content-Type: text/plain
```

上面的HTTP回应中，关键的是`Access-Control-Allow-Origin`字段，表示`http://api.bob.com`可以请求数据。该字段也可以设为星号，表示同意任意跨源请求。

```shell
Access-Control-Allow-Origin: *
```

如果服务器否定了"预检"请求，会返回一个正常的HTTP回应，但是没有任何CORS相关的头信息字段。这时，浏览器就会认定，服务器不同意预检请求，因此触发一个错误，被`XMLHttpRequest`对象的`onerror`
回调函数捕获。控制台会打印出如下的报错信息。

```shell
XMLHttpRequest cannot load http://api.alice.com.
Origin http://api.bob.com is not allowed by Access-Control-Allow-Origin.
```

服务器回应的其他CORS相关字段如下。

```shell
Access-Control-Allow-Methods: GET, POST, PUT
Access-Control-Allow-Headers: X-Custom-Header
Access-Control-Allow-Credentials: true
Access-Control-Max-Age: 1728000
```

+ **Access-Control-Allow-Methods**

该字段必需，它的值是**逗号分隔**的一个字符串，表明服务器支持的所有跨域请求的方法。注意，返回的是所有支持的方法，而不单是浏览器请求的那个方法。这是为了避免多次"预检"请求。

+ **Access-Control-Allow-Headers**

如果浏览器请求包括`Access-Control-Request-Headers`字段，则`Access-Control-Allow-Headers`字段是必需的。它也是一个逗号分隔的字符串，表明服务器支持的所有头信息字段，不限于浏览器在"
预检"中请求的字段。

+ **Access-Control-Allow-Credentials**

该字段与[简单请求](#withcredentials-属性)时的含义相同。

+ **Access-Control-Max-Age**

该字段可选，用来指定本次预检请求的有效期，单位为**秒**。上面结果中，有效期是20天（1728000秒），即允许缓存该条回应1728000秒（即20天），在此期间，不用发出另一条预检请求。

#### 浏览器的正常请求和回应

一旦服务器通过了"预检"请求，以后每次浏览器正常的CORS请求，就都跟简单请求一样，会有一个`Origin`头信息字段。服务器的回应，也都会有一个`Access-Control-Allow-Origin`头信息字段。

下面是"预检"请求之后，浏览器的正常CORS请求。

```shell
PUT /cors HTTP/1.1
Origin: http://api.bob.com
Host: api.alice.com
X-Custom-Header: value
Accept-Language: en-US
Connection: keep-alive
User-Agent: Mozilla/5.0...
```

上面头信息的`Origin`字段是浏览器自动添加的。

下面是服务器正常的回应。

```shell
Access-Control-Allow-Origin: http://api.bob.com
Content-Type: text/html; charset=utf-8
```

上面头信息中，`Access-Control-Allow-Origin`字段是每次回应都必定包含的。

## 参考

+ [跨域及其解决方案](https://blog.csdn.net/qq_42625428/article/details/108099755)
+ [https://developer.mozilla.org/en-US/docs/web/http/cors#simple_requests](https://developer.mozilla.org/en-US/docs/web/http/cors#simple_requests)
+ [跨域资源共享 CORS 详解](http://www.ruanyifeng.com/blog/2016/04/cors.html)
