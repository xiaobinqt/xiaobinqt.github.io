---
title: "go 函数式选项模式"
subtitle: "Golang Functional Options Pattern"

init_date: "2021-08-23T19:01:16+08:00"

date: 2021-08-23

lastmod: 2022-04-03

draft: false

author: "xiaobinqt"
description: "go构造函数,go初始化函数,go函数式选项模式,golang函数式编程"

featuredImage: ""

reproduce: false

tags: ["golang"]
categories: ["golang"]
lightgallery: true

toc:
    auto: false

math:
    enable: true
---

Go 语言没有构造函数，一般通过定义 New 函数来充当构造函数。但是，如果结构有较多字段，要初始化这些字段，就有很多种方式，有一种方式被认为是最优雅的，就是函数式选项模式（Functional Options Pattern）。

> 函数式选项模式用于构造函数和其他公共 API 中的**可选参数**，你预计这些参数需要扩展，尤其是在这些函数上已经有三个或更多参数的情况下。

## 常规方式

我们有如下结构体：

```code
type Server struct {
	host    string        // 必填
	port    int           // 必填
	timeout time.Duration // 可选
	maxConn int           // 可选
}
```

`host` 和 `port` 字段是必须的，`timeout` 和 `maxConn` 字段是可选的。

之前我的做法是这样处理的，定义一个 New 函数，初始化必填字段，对每个可选字段都定义了一个 SetXXX 函数，如下：

```go
package main

import "time"

type Server struct {
	host    string        // 必填
	port    int           // 必填
	timeout time.Duration // 可选
	maxConn int           // 可选
}

func New(host string, port int) *Server {
	return &Server{
		host:    host,
		port:    port,
		timeout: 0,
		maxConn: 0,
	}
}

func (s *Server) SetTimeout(timeout time.Duration) {
	s.timeout = timeout
}

func (s *Server) SetMaxConn(maxConn int) {
	s.maxConn = maxConn
}

func main() {

}

```

个人觉得这种方式其实已经很优雅了，一般情况下也是够用的。

## Functional Option Pattern

```go
package main

import (
	"log"
	"time"
)

type Server struct {
	host    string        // 必填
	port    int           // 必填
	timeout time.Duration // 可选
	maxConn int           // 可选
}

type Option func(*Server)

func New(options ...Option) *Server {
	svr := &Server{}
	for _, f := range options {
		f(svr)
	}
	return svr
}

func WithHost(host string) Option {
	return func(s *Server) {
		s.host = host
	}
}

func WithPort(port int) Option {
	return func(s *Server) {
		s.port = port
	}
}

func WithTimeout(timeout time.Duration) Option {
	return func(s *Server) {
		s.timeout = timeout
	}
}

func WithMaxConn(maxConn int) Option {
	return func(s *Server) {
		s.maxConn = maxConn
	}
}

func (s *Server) Run() error {
	// ...

	return nil
}

func main() {
	svr := New(
		WithHost("localhost"),
		WithPort(8080),
		WithTimeout(time.Minute),
		WithMaxConn(120),
	)
	if err := svr.Run(); err != nil {
		log.Fatal(err)
	}
}

```

在这个模式中，我们定义一个 Option 函数类型，它接收一个参数：*Server。然后，Server 的构造函数接收一个 Option 类型的不定参数。

```code
func New(options ...Option) *Server {
	svr := &Server{}
	for _, f := range options {
		f(svr)
	}
	return svr
}
```

选项的定义需要定义一系列相关返回 Option 的函数，如：

```code
func WithPort(port int) Option {
  return func(s *Server) {
    s.port = port
  }
}
```

如果增加选项，只需要增加对应的 WithXXX 函数即可。


## 参考

+ [Golang Functional Options Pattern](https://golang.cafe/blog/golang-functional-options-pattern.html)