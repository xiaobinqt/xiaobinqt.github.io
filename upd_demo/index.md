# golang udp 示例


## server

```go
package main

import (
	"fmt"
	"net"
	"time"
)

func main() {
	// 创建监听
	socket, err := net.ListenUDP("udp4", &net.UDPAddr{
		IP:   []byte{127, 0, 0, 1},
		Port: 8080,
	})
	if err != nil {
		fmt.Println("监听失败!", err)
		return
	}
	defer socket.Close()

	for {
		// 读取数据
		data := make([]byte, 4096)
		read, remoteAddr, err := socket.ReadFromUDP(data)
		if err != nil {
			fmt.Println("读取数据失败!", err)
			continue
		}
		fmt.Println(read, remoteAddr)
		fmt.Printf("接收到客户端数据，%s\n\n", data)

		// 发送数据
		senddata := []byte("server send data，hello client!" + time.Now().Format("2006-01-02 15:04:05"))
		_, err = socket.WriteToUDP(senddata, remoteAddr)
		if err != nil {
			fmt.Println("发送数据失败!", err.Error())
			return
		}
	}
}

```

## client

```go
package main

import (
	"fmt"
	"net"
	"time"
)

func main() {
	// 创建连接
	socket, err := net.DialUDP("udp4", nil, &net.UDPAddr{
		IP:   []byte{127, 0, 0, 1},
		Port: 8080,
	})
	if err != nil {
		fmt.Println("连接失败!", err)
		return
	}
	defer socket.Close()

	// 发送数据
	senddata := []byte("client send message，hello server!" + time.Now().Format("2006-01-02 15:04:05"))
	_, err = socket.Write(senddata)
	if err != nil {
		fmt.Println("发送数据失败!", err)
		return
	}

	// 接收数据
	data := make([]byte, 4096)
	read, remoteAddr, err := socket.ReadFromUDP(data)
	if err != nil {
		fmt.Println("读取数据失败!", err)
		return
	}
	fmt.Println(read, remoteAddr)
	fmt.Printf("接收到服务器端数据，%s\n", data)
}

```

## 代码地址

[源码地址](https://github.com/xiaobinqt/go.src/tree/master/dev/udp)
