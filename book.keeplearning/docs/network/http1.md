---
weight: 2

bookFlatSection: true

bookCollapseSection: false

bookToc: true

title: "HTTP（一）"
---

# HTTP（一）

## 基础概念

### 请求和响应报文

客户端发送一个请求报文给服务器，服务器根据请求报文中的信息进行处理，并将处理结果放入响应报文中返回给客户端。

请求报文结构：

+ 第一行是包含了请求方法、URL、协议版本；
+ 接下来的多行都是请求首部 Header，每个首部都有一个首部名称，以及对应的值。
+ 一个空行用来分隔首部和内容主体 Body
+ 最后是请求的内容主体

```
GET http://www.example.com/ HTTP/1.1
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8
Cache-Control: max-age=0
Host: www.example.com
If-Modified-Since: Thu, 17 Oct 2019 07:18:26 GMT
If-None-Match: "3147526947+gzip"
Proxy-Connection: keep-alive
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 xxx

param1=1&param2=2
```

响应报文结构：

+ 第一行包含协议版本、状态码以及描述，最常见的是 200 OK 表示请求成功了
+ 接下来多行也是首部内容
+ 一个空行分隔首部和内容主体
+ 最后是响应的内容主体

```
HTTP/1.1 200 OK
Age: 529651
Cache-Control: max-age=604800
Connection: keep-alive
Content-Encoding: gzip
Content-Length: 648
Content-Type: text/html; charset=UTF-8
Date: Mon, 02 Nov 2020 17:53:39 GMT
Etag: "3147526947+ident+gzip"
Expires: Mon, 09 Nov 2020 17:53:39 GMT
Keep-Alive: timeout=4
Last-Modified: Thu, 17 Oct 2019 07:18:26 GMT
Proxy-Connection: keep-alive
Server: ECS (sjc/16DF)
Vary: Accept-Encoding
X-Cache: HIT

<!doctype html>
<html>
<head>
    <title>Example Domain</title>
	// 省略... 
</body>
</html>
```

### URL

HTTP 使用 URL（ U niform Resource Locator，统一资源定位符）来定位资源，它是 URI（Uniform Resource Identifier，统一资源标识符）的子集，URL 在 URI 的基础上增加了定位能力。URI 除了包含 URL，还包含 URN（Uniform Resource Name，统一资源名称），它只是用来定义一个资源的名称，并不具备定位该资源的能力。例如 urn:isbn:0451450523 用来定义一个书籍名称，但是却没有表示怎么找到这本书。

![URL](https://cdn.xiaobinqt.cn/xiaobinqt.io/20221223/236ac92d43f74469b9f47f2422c44e6a.png)

## HTTP 方法

客户端发送的 请求报文 第一行为请求行，包含了方法字段。

### GET

> 获取资源

当前网络请求中，绝大部分使用的是 GET 方法。

### HEAD

> 获取报文首部

和 GET 方法类似，但是不返回报文实体主体部分。

主要用于确认 URL 的有效性以及资源更新的日期时间等。

### POST

> 传输实体主体

POST 主要用来传输数据，而 GET 主要用来获取资源。

更多 POST 与 GET 的比较请见第九章。

### PUT

> 上传文件

由于自身不带验证机制，任何人都可以上传文件，因此存在安全性问题，一般不使用该方法。

```
PUT /new.html HTTP/1.1
Host: example.com
Content-type: text/html
Content-length: 16

<p>New File</p>
```

### PATCH

> 对资源进行部分修改

PUT 也可以用于修改资源，但是只能完全替代原始资源，PATCH 允许部分修改。

```
PATCH /file.txt HTTP/1.1
Host: www.example.com
Content-Type: application/example
If-Match: "e0023aa4e"
Content-Length: 100

[description of changes]
```

### DELETE

> 删除文件

与 PUT 功能相反，并且同样不带验证机制。

### OPTIONS

> 查询支持的方法

查询指定的 URL 能够支持的方法。

会返回`Allow: GET, POST, HEAD, OPTIONS`这样的内容。

### CONNECT

> 要求在与代理服务器通信时建立隧道

使用 SSL（Secure Sockets Layer，安全套接层）和 TLS（Transport Layer Security，传输层安全）协议把通信内容加密后经网络隧道传输。

```
CONNECT www.example.com:443 HTTP/1.1
```

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20221223/bec31ed2a23d4d2aabb13e56dc128094.png)

### TRACE

> 追踪路径

服务器会将通信路径返回给客户端。

发送请求时，在 Max-Forwards 首部字段中填入数值，每经过一个服务器就会减 1，当数值为 0 时就停止传输。

通常不会使用 TRACE，并且它容易受到 XST 攻击（Cross-Site Tracing，跨站追踪）。

## GET 和 POST 比较

### 作用

GET 用于获取资源，而 POST 用于传输实体主体。

### 参数

GET 和 POST 的请求都能使用额外的参数，但是 GET 的参数是以查询字符串出现在 URL 中，而 POST 的参数存储在实体主体中。不能因为 POST 参数存储在实体主体中就认为它的安全性更高，因为照样可以通过一些抓包工具（Fiddler）查看。

因为 URL 只支持 ASCII 码，因此 GET 的参数中如果存在中文等字符就需要先进行编码。例如`中文`会转换为`%E4%B8%AD%E6%96%87`，而空格会转换为`%20`。POST 参数支持标准字符集。

```
GET /test/demo_form.asp?name1=value1&name2=value2 HTTP/1.1
```

```
POST /test/demo_form.asp HTTP/1.1
Host: w3schools.com
name1=value1&name2=value2
```

### 安全

安全的 HTTP 方法不会改变服务器状态，也就是说它只是可读的。

GET 方法是安全的，而 POST 却不是，因为 POST 的目的是传送实体主体内容，这个内容可能是用户上传的表单数据，上传成功之后，服务器可能把这个数据存储到数据库中，因此状态也就发生了改变。

安全的方法除了 GET 之外还有：HEAD、OPTIONS。

不安全的方法除了 POST 之外还有 PUT、DELETE。

### 幂等性

幂等的 HTTP 方法，同样的请求被执行一次与连续执行多次的效果是一样的，服务器的状态也是一样的。换句话说就是，幂等方法不应该具有副作用（统计用途除外）。

所有的安全方法也都是幂等的。

在正确实现的条件下，GET，HEAD，PUT 和 DELETE 等方法都是幂等的，而 POST 方法不是。

GET /pageX HTTP/1.1 是幂等的，连续调用多次，客户端接收到的结果都是一样的：

```
GET /pageX HTTP/1.1
GET /pageX HTTP/1.1
GET /pageX HTTP/1.1
GET /pageX HTTP/1.1
```

POST /add_row HTTP/1.1 不是幂等的，如果调用多次，就会增加多行记录：

```
POST /add_row HTTP/1.1   -> Adds a 1nd row
POST /add_row HTTP/1.1   -> Adds a 2nd row
POST /add_row HTTP/1.1   -> Adds a 3rd row
```

DELETE /idX/delete HTTP/1.1 是幂等的，即使不同的请求接收到的状态码不一样：

```
DELETE /idX/delete HTTP/1.1   -> Returns 200 if idX exists
DELETE /idX/delete HTTP/1.1   -> Returns 404 as it just got deleted
DELETE /idX/delete HTTP/1.1   -> Returns 404
```

### 可缓存

如果要对响应进行缓存，需要满足以下条件：

+ 请求报文的 HTTP 方法本身是可缓存的，包括 GET 和 HEAD，但是 PUT 和 DELETE 不可缓存，POST 在多数情况下不可缓存的。
+ 响应报文的状态码是可缓存的，包括：200, 203, 204, 206, 300, 301, 404, 405, 410, 414, and 501。
+ 响应报文的 Cache-Control 首部字段没有指定不进行缓存。

### XMLHttpRequest

为了阐述 POST 和 GET 的另一个区别，需要先了解 XMLHttpRequest：

> XMLHttpRequest 是一个 API，它为客户端提供了在客户端和服务器之间传输数据的功能。它提供了一个通过 URL 来获取数据的简单方式，并且不会使整个页面刷新。这使得网页只更新一部分页面而不会打扰到用户。XMLHttpRequest 在 AJAX 中被大量使用。

+ 在使用 XMLHttpRequest 的 POST 方法时，浏览器会先发送 Header 再发送 Data。但并不是所有浏览器会这么做，例如火狐就不会。
+ 而 GET 方法 Header 和 Data 会一起发送。

## HTTP 状态码

服务器返回的 响应报文 中第一行为状态行，包含了状态码以及原因短语，用来告知客户端请求的结果。

| 状态码 | 	类别	                    | 含义             |
|-----|-------------------------|----------------|
| 1XX | 	Informational（信息性状态码）  | 	接收的请求正在处理     |
| 2XX | 	Success（成功状态码）         | 	请求正常处理完毕      |
| 3XX | 	Redirection（重定向状态码）    | 	需要进行附加操作以完成请求 |
| 4XX | 	Client Error（客户端错误状态码） | 	服务器无法处理请求     |
| 5XX | 	Server Error（服务器错误状态码） | 	服务器处理请求出错     |

### 1XX 信息

+ 100 Continue ：表明到目前为止都很正常，客户端可以继续发送请求或者忽略这个响应。 ###2XX 成功
+ 200 OK

+ 204 No Content ：请求已经成功处理，但是返回的响应报文不包含实体的主体部分。一般在只需要从客户端往服务器发送信息，而不需要返回数据时使用。

+ 206 Partial Content ：表示客户端进行了范围请求，响应报文包含由 Content-Range 指定范围的实体内容。

### 3XX 重定向

+ 301 Moved Permanently ：永久性重定向

+ 302 Found ：临时性重定向

+ 303 See Other ：和 302 有着相同的功能，但是 303 明确要求客户端应该采用 GET 方法获取资源。

> 注：虽然 HTTP 协议规定 301、302 状态下重定向时不允许把 POST 方法改成 GET 方法，但是大多数浏览器都会在 301、302 和 303 状态下的重定向把 POST 方法改成 GET 方法。

+ 304 Not Modified ：如果请求报文首部包含一些条件，例如：If-Match，If-Modified-Since，If-None-Match，If-Range，If-Unmodified-Since，如果不满足条件，则服务器会返回 304 状态码。

+ 307 Temporary Redirect ：临时重定向，与 302 的含义类似，但是 307 要求浏览器不会把重定向请求的 POST 方法改成 GET 方法。

### 4XX 客户端错误

+ 400 Bad Request ：请求报文中存在语法错误。

+ 401 Unauthorized ：该状态码表示发送的请求需要有认证信息（BASIC 认证、DIGEST 认证）。如果之前已进行过一次请求，则表示用户认证失败。

+ 403 Forbidden ：请求被拒绝。

+ 404 Not Found

### 5XX 服务器错误

+ 500 Internal Server Error ：服务器正在执行请求时发生错误。

+ 503 Service Unavailable ：服务器暂时处于超负载或正在进行停机维护，现在无法处理请求。

## HTTP 首部

有 4 种类型的首部字段：通用首部字段、请求首部字段、响应首部字段和实体首部字段。

各种首部字段及其含义如下（不需要全记，仅供查阅）：

### 通用首部字段

| 首部字段名              | 	说明                    |
|--------------------|------------------------|
| Cache-Control      | 	控制缓存的行为               |
| Connection         | 	控制不再转发给代理的首部字段、管理持久连接 |
| Date	              | 创建报文的日期时间              |
| Pragma	            | 报文指令                   |
| Trailer            | 	报文末端的首部一览             |
| Transfer-Encoding	 | 指定报文主体的传输编码方式          |
| Upgrade	           | 升级为其他协议                |
| Via	               | 代理服务器的相关信息             |
| Warning            | 	错误通知                  |

### 请求首部字段

| 首部字段名	              | 说明                                 |
|---------------------|------------------------------------|
| Accept              | 	用户代理可处理的媒体类型                      |
| Accept-Charset      | 	优先的字符集                            |
| Accept-Encoding     | 	优先的内容编码                           |
| Accept-Language     | 	优先的语言（自然语言）                       |
| Authorization	      | Web 认证信息                           |
| Expect	             | 期待服务器的特定行为                         |
| From                | 	用户的电子邮箱地址                         |
| Host                | 	请求资源所在服务器                         |
| If-Match            | 	比较实体标记（ETag）                      |
| If-Modified-Since	  | 比较资源的更新时间                          |
| If-None-Match	      | 比较实体标记（与 If-Match 相反）              |
| If-Range	           | 资源未更新时发送实体 Byte 的范围请求              |
| If-Unmodified-Since | 	比较资源的更新时间（与 If-Modified-Since 相反） |
| Max-Forwards        | 	最大传输逐跳数                           |
| Proxy-Authorization | 	代理服务器要求客户端的认证信息                   |
| Range	              | 实体的字节范围请求                          |
| Referer             | 	对请求中 URI 的原始获取方                   |
| TE	                 | 传输编码的优先级                           |
| User-Agent	         | HTTP 客户端程序的信息                      |

### 响应首部字段

| 首部字段名              | 	说明             |
|--------------------|-----------------|
| Accept-Ranges	     | 是否接受字节范围请求      |
| Age                | 	推算资源创建经过时间     |
| ETag               | 	资源的匹配信息        |
| Location	          | 令客户端重定向至指定 URI  |
| Proxy-Authenticate | 	代理服务器对客户端的认证信息 |
| Retry-After        | 	对再次发起请求的时机要求   |
| Server             | 	HTTP 服务器的安装信息  |
| Vary	              | 代理服务器缓存的管理信息    |
| WWW-Authenticate   | 	服务器对客户端的认证信息   |

### 实体首部字段

| 首部字段名             | 	说明            |
|-------------------|----------------|
| Allow	            | 资源可支持的 HTTP 方法 |
| Content-Encoding	 | 实体主体适用的编码方式    |
| Content-Language	 | 实体主体的自然语言      |
| Content-Length	   | 实体主体的大小        |
| Content-Location	 | 替代对应资源的 URI    |
| Content-MD5	      | 实体主体的报文摘要      |
| Content-Range	    | 实体主体的位置范围      |
| Content-Type	     | 实体主体的媒体类型      |
| Expires	          | 实体主体过期的日期时间    |
| Last-Modified	    | 资源的最后修改日期时间    |



