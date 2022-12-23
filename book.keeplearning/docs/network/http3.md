---
weight: 3

bookFlatSection: true

bookCollapseSection: false

bookToc: true

title: "HTTP（三）"
---

# HTTP（三）

## 通信数据转发

### 1. 代理

代理服务器接受客户端的请求，并且转发给其它服务器。

使用代理的主要目的是：

+ 缓存
+ 负载均衡
+ 网络访问控制
+ 访问日志记录

代理服务器分为正向代理和反向代理两种：

+ 用户察觉得到正向代理的存在。

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20221223/673481d10517468fb51e75f6246e48e9.png)

+ 而反向代理一般位于内部网络中，用户察觉不到。

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20221223/c5b2a087567b4600918eb77d9c1a3a7a.png)

### 2. 网关

与代理服务器不同的是，网关服务器会将 HTTP 转化为其它协议进行通信，从而请求其它非 HTTP 服务器的服务。

### 3. 隧道

使用 SSL 等加密手段，在客户端和服务器之间建立一条安全的通信线路。

## HTTPS

HTTP 有以下安全性问题：

+ 使用明文进行通信，内容可能会被窃听；
+ 不验证通信方的身份，通信方的身份有可能遭遇伪装；
+ 无法证明报文的完整性，报文有可能遭篡改。

HTTPS 并不是新协议，而是让 HTTP 先和 SSL（Secure Sockets Layer）通信，再由 SSL 和 TCP 通信，也就是说 HTTPS 使用了隧道进行通信。

通过使用 SSL，HTTPS 具有了加密（防窃听）、认证（防伪装）和完整性保护（防篡改）。

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20221223/d1607d22011e4e84be34784b8cab4266.png)

### 加密

#### 1. 对称密钥加密

对称密钥加密（Symmetric-Key Encryption），加密和解密使用同一密钥。

+ 优点：运算速度快；
+ 缺点：无法安全地将密钥传输给通信方。

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20221223/1082f49968c6419c83b17d1fe498bbd7.png)

#### 2.非对称密钥加密

非对称密钥加密，又称公开密钥加密（Public-Key Encryption），加密和解密使用不同的密钥。

公开密钥所有人都可以获得，通信发送方获得接收方的公开密钥之后，就可以使用公开密钥进行加密，接收方收到通信内容后使用私有密钥解密。

非对称密钥除了用来加密，还可以用来进行签名。因为私有密钥无法被其他人获取，因此通信发送方使用其私有密钥进行签名，通信接收方使用发送方的公开密钥对签名进行解密，就能判断这个签名是否正确。

+ 优点：可以更安全地将公开密钥传输给通信发送方；
+ 缺点：运算速度慢。

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20221223/8eb9b65f45c64cf28952d36125947f18.png)

#### 3. HTTPS 采用的加密方式

上面提到对称密钥加密方式的传输效率更高，但是无法安全地将密钥 Secret Key 传输给通信方。而非对称密钥加密方式可以保证传输的安全性，因此我们可以利用非对称密钥加密方式将 Secret Key 传输给通信方。HTTPS 采用混合的加密机制，正是利用了上面提到的方案：

+ 使用非对称密钥加密方式，传输对称密钥加密方式所需要的 Secret Key，从而保证安全性;
+ 获取到 Secret Key 后，再使用对称密钥加密方式进行通信，从而保证效率。（下图中的 Session Key 就是 Secret Key）

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20221223/1f68b72ffccb4c70b22a32224740a570.png)

### 认证

通过使用 证书 来对通信方进行认证。

数字证书认证机构（CA，Certificate Authority）是客户端与服务器双方都可信赖的第三方机构。

服务器的运营人员向 CA 提出公开密钥的申请，CA 在判明提出申请者的身份之后，会对已申请的公开密钥做数字签名，然后分配这个已签名的公开密钥，并将该公开密钥放入公开密钥证书后绑定在一起。

进行 HTTPS 通信时，服务器会把证书发送给客户端。客户端取得其中的公开密钥之后，先使用数字签名进行验证，如果验证通过，就可以开始通信了。

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20221223/a555f0e32fed4de5804956ac42f23ab2.png)

### 完整性保护

SSL 提供报文摘要功能来进行完整性保护。

HTTP 也提供了 MD5 报文摘要功能，但不是安全的。例如报文内容被篡改之后，同时重新计算 MD5 的值，通信接收方是无法意识到发生了篡改。

HTTPS 的报文摘要功能之所以安全，是因为它结合了加密和认证这两个操作。试想一下，加密之后的报文，遭到篡改之后，也很难重新计算报文摘要，因为无法轻易获取明文。

### HTTPS 的缺点

+ 因为需要进行加密解密等过程，因此速度会更慢；
+ 需要支付证书授权的高额费用。

## HTTP/2.0

### HTTP/1.x 缺陷

HTTP/1.x 实现简单是以牺牲性能为代价的：

+ 客户端需要使用多个连接才能实现并发和缩短延迟；
+ 不会压缩请求和响应首部，从而导致不必要的网络流量；
+ 不支持有效的资源优先级，致使底层 TCP 连接的利用率低下。

### 二进制分帧层

HTTP/2.0 将报文分成 HEADERS 帧和 DATA 帧，它们都是二进制格式的。

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20221223/a832e38a1548493c9fd1d3adc4ee05d0.png)

在通信过程中，只会有一个 TCP 连接存在，它承载了任意数量的双向数据流（Stream）。

+ 一个数据流（Stream）都有一个唯一标识符和可选的优先级信息，用于承载双向信息。
+ 消息（Message）是与逻辑请求或响应对应的完整的一系列帧。
+ 帧（Frame）是最小的通信单位，来自不同数据流的帧可以交错发送，然后再根据每个帧头的数据流标识符重新组装。

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20221223/afd8a3b361e04a049121cae535381e1b.png)

### 服务端推送

HTTP/2.0 在客户端请求一个资源时，会把相关的资源一起发送给客户端，客户端就不需要再次发起请求了。例如客户端请求 page.html 页面，服务端就把 script.js 和 style.css 等与之相关的资源一起发给客户端。

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20221223/3107ca0b881a4cb39ee8a5136cc08d67.png)

### 首部压缩

HTTP/1.1 的首部带有大量信息，而且每次都要重复发送。

HTTP/2.0 要求客户端和服务器同时维护和更新一个包含之前见过的首部字段表，从而避免了重复传输。

不仅如此，HTTP/2.0 也使用 Huffman 编码对首部字段进行压缩。

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20221223/3da44c14ea194bc2b17372109f3a97c0.png)

## HTTP/1.1 新特性

+ 默认是长连接
+ 支持流水线
+ 支持同时打开多个 TCP 连接
+ 支持虚拟主机
+ 新增状态码 100
+ 支持分块传输编码
+ 新增缓存处理指令 max-age







