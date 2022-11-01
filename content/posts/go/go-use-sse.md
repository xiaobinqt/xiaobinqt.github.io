---
title: "Go 使用 sse"
subtitle: ""

init_date: "2022-08-26T13:38:10+08:00"

date: 2021-09-08

lastmod: 2022-08-26

draft: false

author: "xiaobinqt"
description: "xiaobinqt,"

featuredImage: "https://cdn.xiaobinqt.cn/xiaobinqt.io/20220826/8b29290860a04491bfdaa11a5b5e0f28.png"

featuredImagePreview: ""

reproduce: false

translate: false

tags: ["sse","golang"]
categories: ["web","开发者手册"]
lightgallery: true

toc: true

math:
    enable: true
---

<!-- author： xiaobinqt -->
<!-- email： xiaobinqt@163.com -->
<!-- https://xiaobinqt.github.io -->
<!-- https://www.xiaobinqt.cn -->

## SSE 的本质

严格地说，HTTP 协议无法做到服务器主动推送信息。但是，有一种变通方法，就是服务器向客户端声明，接下来要发送的是流信息（streaming）。

也就是说，发送的不是一次性的数据包，而是一个数据流，会连续不断地发送过来。这时，客户端不会关闭连接，会一直等着服务器发过来的新的数据流，视频播放就是这样的例子。本质上，这种通信就是以流信息的方式，完成一次用时很长的下载。

SSE 就是利用这种机制，使用流信息向浏览器推送信息。它基于 HTTP 协议，目前除了 IE/Edge，其他浏览器都支持。

## SSE 的特点

SSE 与 WebSocket 作用相似，都是建立浏览器与服务器之间的通信渠道，然后服务器向浏览器推送信息。

总体来说，WebSocket 更强大和灵活。因为它是全双工通道，可以双向通信；SSE 是单向通道，只能服务器向浏览器发送，因为流信息本质上就是下载。如果浏览器向服务器发送信息，就变成了另一次 HTTP 请求。

### 优点

+ SSE 使用 HTTP 协议，现有的服务器软件都支持。WebSocket 是一个独立协议。
+ SSE 属于轻量级，使用简单；WebSocket 协议相对复杂。
+ SSE 默认支持断线重连，WebSocket 需要自己实现。
+ SSE 一般只用来传送文本，二进制数据需要编码后传送，WebSocket 默认支持传送二进制数据。
+ SSE 支持自定义发送的消息类型。

## go 实现

```go
package main

import (
	"fmt"
	"net/http"
	"time"
)

type SSE struct {
}

func (sse *SSE) ServeHTTP(rw http.ResponseWriter, req *http.Request) {
	flusher, ok := rw.(http.Flusher)

	if !ok {
		http.Error(rw, "Streaming unsupported!", http.StatusInternalServerError)
		return
	}

	rw.Header().Set("Content-Type", "text/event-stream")
	rw.Header().Set("Cache-Control", "no-cache")
	rw.Header().Set("Connection", "keep-alive")
	rw.Header().Set("Access-Control-Allow-Origin", "*")

	for {

		select {
		case <-req.Context().Done():
			fmt.Println("req done...")
			return
		case <-time.After(500 * time.Millisecond):
			fmt.Fprintf(rw, "id: %d\nevent: ping \ndata: %d\n\n", time.Now().Unix(), time.Now().Unix())
			flusher.Flush()
		}

	}

}

func main() {
	//route := gin.New()
	//route.GET("sse", gin.WrapH(&SSE{}))
	//route.Run(":8080")

	http.Handle("/sse", &SSE{})
	http.ListenAndServe(":8080", nil)
}

```

index.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>


<h2>SSE</h2>

</body>


<script>
    const source = new EventSource('http://127.0.0.1:8080/sse');
    source.onopen = () => {
        console.log('链接成功');
    }
    source.onmessage = (res) => {
        console.log('获得的数据是:' + res.data);
    }
    source.onerror = (err) => {
        console.log(err);
    }
</script>
</html>
```

![直接访问](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220826/7e44b78245ef4e1e99981e91184cc66c.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '直接访问')

![前端访问](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220826/828118df01ca4d1882735dc1a96a3c93.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '前端访问')

## 参考

+ [Example SSE server in Golang](https://gist.github.com/ismasan/3fb75381cd2deb6bfa9c)
+ [Server-Sent Events 教程](https://www.ruanyifeng.com/blog/2017/05/server-sent_events.html)




