# Go 编译标签 build tag


<!-- author： xiaobinqt -->
<!-- email： xiaobinqt@163.com -->
<!-- https://xiaobinqt.github.io -->
<!-- https://www.xiaobinqt.cn -->

## 简介

在 Go 中，build tag 是添加到代码中第一行，来标识编译相关信息的，build tag 决定了当前文件是否会被当前 package 所包含，用于限制一整个文件是否应该被编译入最终的二进制文件，而不是一个文件中的部分代码片段。

Go [编译标签]^(build tag)语法如下：

```
// +build [tag]
```

- build tags 文件顶部附近，前面只能有空行和其他行注释。
- 编译标记必须出现在 package 子句之前，并且为了与包文档区分开来，它**必须**后跟一个空行。

## 编译标签的逻辑

当在一个包中使用多个标签时会使用 bool 逻辑进行交互，具体取决于我们如何进行声明的。

Build tags 遵循以下三个规则：

- 以空格分隔的标签将在`OR`逻辑下进行解释。
- 逗号分隔的标签将在`AND`逻辑下进行解释。
- 每个术语都是一个字母数字单词，如果前面有`!`它意味着它被否定。

### or 标签逻辑

给定标签：

```
// +build tag1 tag2
```

OR 解释是，如果在执行 build 构建命令时存在 tag1 或 tag2，则将包含此文件。

### and 标签逻辑

如果我们使用标签：

```
// +build tag1, tag2
```

解释是 tag1 且（AND） tag2 必须存在于 build 构建命令中，我们的文件才能包含在编译中。

### ！非标签逻辑

如果我们使用标签

```
 // +build !tag1
```

解释是，非 tag1，我们的文件才会 build 编译

## 如何使用

### 新建 build tag

我们新建一个 buildtag 文件夹，并在文件夹下新建如下4个空文件，如下：

```
.
├── dev.go
├── main.go
├── prod.go
├── test.go
└── without.go
```

我们打开 main.go 输入代码如下：

```go
package main

import "fmt"

var configArr []string

func main() {
	for _, conf := range configArr {
		fmt.Println(conf)
	}
}

```

我们打开 dev.go 输入代码如下：

```go
// +build dev
package main

func init() {
	configArr = append(configArr, "mysql dev")
}
```

我们打开 prod.go 输入代码如下：

```go
// +build prod

package main

func init() {
	configArr = append(configArr, "mysql prod")
}

```

我们打开 test.go 输入代码如下：

```go
// +build test1
package main

func init() {
	configArr = append(configArr, "mysql test")
}

```

我们打开 without.go 输入代码如下：

```go
// +build !without

package main

func init() {
	configArr = append(configArr, "mysql without")
}

```

### 使用 tags 编译

#### 1. 没有tag编译

我们使用

```
go build
```

在文件夹里生成了二进制执行文件 buildtag，我们执行一下：

```
➜ ./buildtag 
```

输出：

```
mysql without
```

#### 2. 单个tag编译

我们使用

```
go build  -tags "dev" 
```

在文件夹里生成了二进制执行文件 buildtag，我们执行一下：

```
➜ ./buildtag 
```

输出：

```
mysql dev

```

#### 3. 多个tag编译

我们使用

```
go build  -tags "dev prod" 
```

在文件夹里生成了二进制执行文件 buildtag，我们执行一下：

```
➜ ./buildtag 
```

输出：

```
mysql dev
mysql prod

```

## go:build 与 +build 的区别

```
//go:build
```

:point_up:是 Go 1.17 中引入的新条件编译指令格式。它旨在替换

```
// +build
```

指令。那么为何要采用新的格式呢？对比一下新旧格式的区别就知道了:point_down:

```
// go:build linux && amd64 || darwin
// +build linux,amd64 darwin
```

`go:build`这种格式，对 coder 来说，更容易理解其逻辑组合，与`//go:embed`和`//go:generate`这些命令相比较，格式上进行了统一。

## 参考

+ [代码地址](https://github.com/xiaobinqt/go.src/tree/master/dev/buildtag)
+ [go 编译标签( build tag)-注释里的编译语法](https://segmentfault.com/a/1190000042007310)
+ [golang: netgo vs cgo](https://wrfly.kfd.me/posts/golang-netgo-vs-cgo/)



