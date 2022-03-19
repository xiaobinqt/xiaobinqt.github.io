---
title: "http入门笔记"

date: 2022-03-17T10:47:43+08:00

lastmod: 2022-03-17T10:47:43+08:00

draft: false

fontawesome: true

author: "xiaobinqt"
description: "http入门"
resources:

- name: ""
  src: ""

tags: ["http"]
categories: ["network"]
lightgallery: true

toc:
auto: false

math:
enable: true
---

该笔记是在学习《透视 HTTP 协议》时整理，还参考了网上的其他资料。鄙人只是网络世界的搬运整理工:joy:。

<!--more-->

## 总览

![http总览](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220317/6935d109cbc64fa58c3177a90fd33098.png?imageView2/0/interlace/1/q/50|imageslim " ")

## http 协议

http（超文本传输协议）是一个用在计算机世界里的协议。它使用计算机能够理解的语言确立了一种计算机之间交流通信的规范，以及相关的各种控制和错误处理方式。

http 是一个在计算机世界里专门在两点之间传输文字、图片、音频、视频等超文本数据的约定和规范。

http 不是编程语言，但是可以用编程语言去实现 HTTP，告诉计算机如何用 HTTP 来与外界通信。

在互联网世界里，HTTP 通常跑在 TCP/IP 协议栈之上，依靠 IP 协议实现寻址和路由、TCP 协议实现可靠数据传输、DNS 协议实现域名查找、SSL/TLS 协议实现安全通信。此外，还有一些协议依赖于 HTTP，例如
WebSocket、HTTPDNS 等。这些协议相互交织，构成了一个协议网，而 HTTP 则处于中心地位。

> HTTP 传输的不是 TCP/UDP 这些底层协议里被切分的杂乱无章的二进制包（datagram），而是完整的、有意义的数据，可以被浏览器、服务器这样的上层应用程序处理。

### 互联网和万维网的区别

我们通常所说的“上网”实际上访问的只是互联网的一个子集“万维网”（World Wide Web），它基于 HTTP 协议，传输 HTML 等超文本资源，能力被限制在 HTTP 协议之内。

互联网上还有许多万维网之外的资源，例如常用的电子邮件、BT 和 Magnet 点对点下载、FTP 文件下载、SSH 安全登录、各种即时通信服务等等，它们需要用各自的专有协议来访问。

不过由于 HTTP 协议非常灵活、易于扩展，而且“超文本”的表述能力很强，所以很多其他原本不属于 HTTP 的资源也可以“包装”成 HTTP 来访问，这就是我们为什么能够总看到各种“网页应用”——例如“微信网页版”“邮箱网页版”——的原因。

### TCP/IP

TCP/IP 协议实际上是一系列网络通信协议的统称， 其中最核心的两个协议是TCP（Transmission Control Protocol/传输控制协议）和IP（Internet Protocol），其他的还有 UDP、ICMP、ARP
等等，共同构成了一个复杂但有层次的协议栈。

> HTTP 是超文本传输协议，TCP 是传输控制协议，都是传输，区别是，HTTP 传输的是完整的、有意义的数据，可以被浏览器、
> 服务器这样的上层应用程序处理，HTTP 不关心寻址、路由、数据完整性等传输细节，而要求这些工作都由下层（基本都由 TCP）来处理。 TCP 传输的是可靠的、字节流和二进制包。

TCP 是 HTTP 得以实现的基础，HTTP 协议运行在 TCP/IP 上，HTTP 可以更准确地称为 “HTTP over TCP/IP”。

### URI/URL

URI（Uniform Resource Identifier），中文名称是 统一资源标识符，使用它就能够唯一地标记互联网上资源。

URI 另一个更常用的表现形式是 URL（Uniform Resource Locator）， 统一资源定位符，也就是我们俗称的“网址”，它实际上是 URI 的一个子集，这两者几乎是相同的，差异不大，除非写论文，否则不用特意区分。

### SSL/TSL

SSL 的全称是“Secure Socket Layer”，网景公司发明，当发展到 3.0 时被标准化，改名为 TLS，即“Transport Layer Security”。 所以 TLS 跟 SSL 是一个东西，相当于张君宝的 2.0
版本是张三丰。

SSL 是一个负责加密通信的安全协议，建立在 TCP/IP 之上，在 HTTP 协议之下。

### Proxy 代理

+ 匿名代理：完全“隐匿”了被代理的机器，外界看到的只是代理服务器；
+ 透明代理：顾名思义，它在传输过程中是“透明开放”的，外界既知道代理，也知道客户端；
+ 正向代理：靠近客户端，代表客户端向服务器发送请求；

![正向代理](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220317/22475408cd734b9c861b345040e356f4.png?imageView2/0/interlace/1/q/50|imageslim "正向代理")

+ 反向代理：靠近服务器端，代表服务器响应客户端的请求；

![反向代理](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220317/6a2b4d26c0bf43cd9494df793c48a814.png?imageView2/0/interlace/1/q/50|imageslim "反向代理")

{{< admonition type=tip title="Tip" open=true >}}

+ [如何理解反向代理服务器](https://www.jianshu.com/p/23b6775fbb91)

{{< /admonition >}}

## http 版本

万维网关键技术

+ URI：即统一资源标识符，作为互联网上资源的唯一身份；
+ HTML：即超文本标记语言，描述超文本文档；
+ HTTP：即超文本传输协议，用来传输超文本。

基于这三项关键技术就可以把超文本系统完美地运行在互联网上，让各地的人们能够自由地共享信息，这个系统称为“万维网”（World Wide Web），也就是我们现在所熟知的 Web。

### http/0.9

结构简单，设置之初设想系统里的文档都是只读的，所以只允许用 GET 动作从服务器上获取 HTML 纯文本格式的文档，并且在响应请求之后立即关闭连接，功能非常有限。

### http/1.0

HTTP/1.0 并不是一个标准，只是记录已有实践和模式的一份参考文档，不具有实际的约束力，相当于一个备忘录。

在多方面增强了 0.9 版，形式上已经和我们现在的 HTTP 差别不大了，例如：

+ 增加了 HEAD、POST 等新方法；
+ 增加了响应状态码，标记可能的错误原因；
+ 引入了协议版本号概念；
+ 引入了 HTTP Header（头部）的概念，让 HTTP 处理请求和响应更加灵活；
+ 传输的数据不再仅限于文本。

### http/1.1

是一个正式的标准，而不是一份可有可无的参考文档，只要用到 HTTP 协议，就必须严格遵守这个标准。

主要变更：

+ 增加了 PUT、DELETE 等新的方法；
+ 增加了缓存管理和控制；
+ 明确了连接管理，允许持久连接；
+ 允许响应数据分块（chunked），利于传输大文件；
+ 强制要求 Host 头，让互联网主机托管成为可能。

### http/2

由 google 主导，基于 google 的 SPDY 协议为基础开始制定新版本的 HTTP 协议，最终在 2015 年发布了 HTTP/2。

主要特点：

+ 二进制协议，不再是纯文本；
+ 可发起多个请求，废弃了 1.1 里的管道；
+ 使用专用算法压缩头部，减少数据传输量；
+ 允许服务器主动向客户端推送数据；
+ 增强了安全性，“事实上”要求加密通信。

### http/3

由 google 主导，基于 google 的 QUIC 协议为基础开始制定新版本的 HTTP 协议。

## 网络分层模型

### TCP/IP

![tcp/ip分层模型](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220317/87869e9a3d0d4eaba7c9d6fe0798674f.png?imageView2/0/interlace/1/q/50|imageslim "TCP/IP分层模型")

这里的层次顺序是“从下往上”数的，所以第一层就是最下面的一层。

#### 链接层

第一层叫“链接层”（link layer），负责在以太网、WiFi 这样的底层网络上发送原始数据包，工作在网卡这个层次，使用 MAC 地址来标记网络上的设备，所以有时候也叫 MAC 层。

#### 网络互联层

第二层叫“网际层”或者“网络互连层”（internet layer），IP 协议就处在这一层。因为 IP 协议定义了“IP 地址”的概念，所以就可以在“链接层”的基础上，用 IP 地址取代 MAC
地址，把许许多多的局域网、广域网连接成一个虚拟的巨大网络，在这个网络里找设备时只要把 IP 地址再“翻译”成 MAC 地址就可以了。

#### 传输层

第三层叫“传输层”（transport layer），这个层次协议的职责是保证数据在 IP 地址标记的两点之间“可靠”地传输，是 TCP 协议工作的层次，另外还有它的一个“小伙伴”UDP。

TCP 是一个有状态的协议，需要先与对方建立连接然后才能发送数据，而且保证数据不丢失不重复。而 UDP 则比较简单，它无状态，不用事先建立连接就可以任意发送数据，但不保证数据一定会发到对方。两个协议的另一个重要区别在于数据的形式。TCP
的数据是连续的“字节流”，有先后顺序，而 UDP 则是分散的小数据包，是顺序发，乱序收。

#### 应用层

协议栈的第四层叫“应用层”（application layer），由于下面的三层把基础打得非常好，所以在这一层就“百花齐放”了，有各种面向具体应用的协议。例如 Telnet、SSH、FTP、SMTP，HTTP 等等。

{{< admonition type=tip title="Tip" open=true >}}

MAC 层（链接层）的传输单位是帧（frame），IP 层（网络互联层）的传输单位是包（packet），TCP 层传输层的传输单位是段（segment）， HTTP
（应用层）的传输单位则是消息或报文（message）。这些名词并没有什么本质的区分，可以统称为数据包。

{{< /admonition >}}

### OSI 网络分层模型

OSI 分层模型在发布的时候就明确地表明是一个“参考”，不是强制标准。这是因为 TCP/IP 等协议已经在许多网络上实际运行，不可能推翻重来。

![OSI模型](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220317/4ddd78194c284518a2ce2db4cfab2a3c.png?imageView2/0/interlace/1/q/50|imageslim "OSI网络模型")

+ 第一层：物理层，网络的物理形式，例如电缆、光纤、网卡、集线器等等；
+ 第二层：数据链路层，它基本相当于 TCP/IP 的链接层；
+ 第三层：网络层，相当于 TCP/IP 里的网际层；
+ 第四层：传输层，相当于 TCP/IP 里的传输层；
+ 第五层：会话层，维护网络中的连接状态，即保持会话和同步；
+ 第六层：表示层，把数据转换为合适、可理解的语法和语义；
+ 第七层：应用层，面向具体的应用传输数据。

对比一下就可以发现，TCP/IP 是一个纯软件的栈，没有网络应有的最根基的电缆、网卡等物理设备的位置。而 OSI 则补足了这个缺失， 在理论层面上描述网络更加完整。

OSI 还为每一层标记了明确了编号，最底层是一层，最上层是七层，而 TCP/IP 的层次从来只有名字而没有编号。

### 两个分层模型的对应关系

![对应关系](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220317/539751215a0b45ada0a373f8289ca232.png?imageView2/0/interlace/1/q/50|imageslim "两个分层模型的对应关系")

所谓的“四层负载均衡”就是指工作在传输层上，基于 TCP/IP 协议的特性，例如 IP 地址、端口号等实现对后端服务器的负载均衡。

所谓的“七层负载均衡”就是指工作在应用层上，看到的是 HTTP 协议，解析 HTTP 报文里的 URI、主机名、资源类型等数据，再用适当的策略转发给后端服务器。

有一个辨别四层和七层比较好的（但不是绝对的）小窍门，“两个凡是”：**凡是由操作系统负责处理的就是四层或四层以下**，否则，**凡是需要由应用程序（也就是你自己写代码）负责处理的就是七层**。