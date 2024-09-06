# 内网穿透工具 Ngrok


<!-- author： xiaobinqt -->
<!-- email： xiaobinqt@163.com -->
<!-- https://xiaobinqt.github.io -->
<!-- https://www.xiaobinqt.cn -->

## 安装

Ngrok是一款实现内网穿透的工具，它通过在公共的端点和本地运行的 Web 服务器之间建立一个安全的通道。并且可以捕获和分析所有通道上的流量。

有时候我们需要临时地将一个本地的 Web 网站或是接口部署到到线上，供他人体验或调试等，通常我们会这么做：

1. 找到一台服务器
2. 服务器上有网站所需要的环境
3. 将项目部署到服务器上
4. 调试结束后，再将网站从服务器上删除

有没有感觉很麻烦！有了 ngrok 可以非常丝滑的解决这个问题。

进入 Ngrok 官网 [https://ngrok.com/](https://ngrok.com/)，注册并安装 ngrok [https://dashboard.ngrok.com/get-started/setup/macos](https://dashboard.ngrok.com/get-started/setup/macos)。

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20240906/3296852c59d84b349f64be2118a43689.png?imageView2/0/q/75%7cwatermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '选择自己的 platform')

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20240906/b27a332a575c4dbc840c3073be89d46f.png?imageView2/0/q/75%7cwatermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '安装使用')

## 使用

我用 golang 写了一个简单的接口，监听 8080 端口。

> 端口号并不是固定的。

```golang
package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
)

func main() {
	http.HandleFunc("/receive/message", handle)
	fmt.Println("start ...")
	log.Fatal(http.ListenAndServe(":8080", nil))
}

func handle(w http.ResponseWriter, r *http.Request) {
	fmt.Println("method: ", r.Method)

	if r.Method != http.MethodPost {
		fmt.Fprintf(w, "request method is %s", r.Method)
		return
	}

	// 读取请求 body
	body, err := ioutil.ReadAll(r.Body)
	if err != nil {
		http.Error(w, "Error reading request body", http.StatusInternalServerError)
		return
	}
	defer r.Body.Close()

	fmt.Println("body: ", string(body))
	// 打印 body 内容
	fmt.Fprintf(w, "Received body: %s\n", string(body))
}

```

运行这个服务

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20240906/09dcb8bf7c184d4ab5b704535bf8949e.png 'start server')

运行 `ngrok http http://localhost:8080` 这样 ngrok 就可以监听本地的 8080 服务，并暴露在公网上

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20240906/0e0840c57bd64c588b74fdafd0b55611.png)

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20240906/dae2789f4fe54195bd22a72ad0ec47c8.png?imageView2/0/q/75%7cwatermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15)

此时访问 `https://6f96-111-199-187-249.ngrok-free.app` 这个外网地址，就会直接访问到我们本地的服务。

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20240906/644faa22611543f3832775c165b63384.png?imageView2/0/q/75%7cwatermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15)

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20240906/028633d22b97465f8ac9b7c492fdd531.png?imageView2/0/q/75%7cwatermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15)

## 常见问题

### 终端 http_proxy

```go
ERROR:  authentication failed: Running the agent with an http/s proxy is an enterprise feature.If this is unexpected, verify that there is no proxy_url value in your ngrok configuration file and that the http_proxy environment variable is not set.
ERROR:
ERROR:  If you need this capability, upgrade to an Enterprise plan at: https: //dashboard.ngrok.com/billing/subscription
ERROR:
ERROR:  ERR_NGROK_9009
ERROR:  https: //ngrok.com/docs/errors/err_ngrok_9009
ERROR:
```

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20240906/f061a7bae8144923adf40ece69669b4f.png?imageView2/0/q/75%7cwatermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15)

这是代理问题导致的，由于我的终端设置了代理，**关掉代理即可**。

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20240906/6f3dee0288d24111b7b12b700e2d5cc8.png 'http proxy')





