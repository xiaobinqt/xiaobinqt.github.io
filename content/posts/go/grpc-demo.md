---
title: "grpc 入门应用"

date: 2021-04-05

lastmod: 2022-03-16

draft: false

author: "xiaobinqt"
description: "golang grpc,golang,rpc,grpc,grpc 入门"
resources:

- name: ""
  src: ""

tags: ["golang"]
categories: ["golang"]
lightgallery: true

toc: true

math: true
---


RPC 是一种跨语言的协议，它可以让我们在不同的语言之间进行通信。 远程过程调用（英语：Remote Procedure Call，缩写为 RPC）是一个计算机通信协议。该协议允许运行于一台计算机的程序调用另一个
地址空间（通常为一个开放网络的一台计算机）的子程序，而程序员就像调用本地程序一样，无需额外地为这个交互作用编程（无需关注细节）。
RPC是一种服务器-客户端（Client/Server）模式，经典实现是一个通过发送请求-接受回应进行信息交互的系统。

## 安装

```shell 
go install github.com/golang/protobuf/protoc-gen-go@v1.4.0
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@v1.1
```

不推荐使用 `google.golang.org/protobuf/cmd/protoc-gen-go@v1.26` 这个版本太高了，可能会遇到以下这个问题，

```shell
--go_out: protoc-gen-go: plugins are not supported; use 'protoc --go-grpc_out=...' to generate gRPC

See https://grpc.io/docs/languages/go/quickstart/#regenerate-grpc-code for more information.
```

![生成代码遇到的问题](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220311/46740c77e070406d9f7611dfa146eb51.png?imageView2/0/interlace/1/q/50|imageslim " ")

参考解决方案[记一次奇妙的go-protobuf包升级之旅](https://zhuanlan.zhihu.com/p/133253979)

protoc 工具安装

下载[地址](https://github.com/protocolbuffers/protobuf/tags)，下载解压将 bin 目录添加到环境变量中。

![protoc](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220311/b0f2aa7f2c4e452a90f99c9b6aeba00c.png?imageView2/0/interlace/1/q/50|imageslim " ")

## 定义 proto 文件

```proto
syntax = "proto3"; // 使用protobuf版本3

option go_package = "./protobuf"; // 这个影响生成的目录及go的package命名

// 定义一个计算服务, 输入为CalcRequest, 输出为CalcResponse
service CalculatorService {
  rpc calc(CalcRequest) returns (CalcResponse) {};
}

// 计算两个数某种运算(如加法)的参数
message CalcRequest {
  double a = 1;
  double b = 2;
  string op = 3;
}

// 计算结果
message CalcResponse {
  double r = 1;
}

```

## 生成 .pb.go 文件

```shell
protoc  --go_out=plugins=grpc:. calculator.proto
```

![整体目录结构](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220314/38302da622eb4c55a9056ed69d9807c6.png?imageView2/0/interlace/1/q/50|imageslim "  ")

## rpc server

```go
package main

import (
	"context"
	"fmt"
	"net"

	"go.src/grpc/calculator/protobuf"
	"google.golang.org/grpc"
)

// 实现: CalculatorServiceServer接口, 在calculator.pb.go中定义
type server struct{}

func (s server) Calc(ctx context.Context, req *protobuf.CalcRequest) (resp *protobuf.CalcResponse, err error) {
	a := req.GetA()
	b := req.GetB()
	op := req.GetOp()
	resp = &protobuf.CalcResponse{}

	switch op {
	case "+":
		resp.R = a + b
	case "-":
		resp.R = a - b
	case "*":
		resp.R = a * b
	case "/":
		if b == 0 {
			err = fmt.Errorf("divided by zero")
			return
		}
		resp.R = a / b
	}
	return
}

// 启动rpc server
func main() {
	listener, err := net.Listen("tcp", "localhost:3233")
	if err != nil {
		panic(err)
	}

	s := grpc.NewServer()
	protobuf.RegisterCalculatorServiceServer(s, &server{})
	fmt.Println("server start")
	err = s.Serve(listener)
	if err != nil {
		panic(err)
	}
}

```

## rpc client

```go
package main

import (
	"context"
	"fmt"
	"log"

	"go.src/grpc/calculator/protobuf"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

func main() {
	// 连上grpc server
	//conn, err := grpc.Dial("localhost:3233", grpc.WithInsecure())
	conn, err := grpc.Dial("localhost:3233", grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}

	defer conn.Close()

	c := protobuf.NewCalculatorServiceClient(conn)

	// 调用远程方法
	resp, err := c.Calc(context.Background(), &protobuf.CalcRequest{
		A:  1,
		B:  2,
		Op: "+",
	})
	if err != nil {
		fmt.Println("calc err: ", err.Error())
		return
	}
	fmt.Println("calc success,respR: ", resp.GetR()) // 3
}

```

## 运行测试

![server](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220314/49db64ec83ab42abad90a0fab35e393c.png?imageView2/0/interlace/1/q/50|imageslim "server")

![client](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220314/b9f69f2cd62d4eb4abfa2aa449fa772d.png?imageView2/0/interlace/1/q/50|imageslim "client")

## 示例下载

[示例源码地址](https://github.com/xiaobinqt/go.src/tree/master/grpc/calculator)
