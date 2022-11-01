---
title: "golang break，continue，goto label 的区别"

date: 2020-05-16

lastmod: 2022-03-16

draft: false

author: "xiaobinqt"
description: "go,continue,break,goto label的区别,Golang"
resources:

- name: ""
  src: ""

tags: ["golang"]
categories: ["golang"]
lightgallery: true

toc:
  auto: false

math:
  enable: true
---

<!-- author： xiaobinqt -->
<!-- email： xiaobinqt@163.com -->
<!-- https://xiaobinqt.github.io -->
<!-- https://www.xiaobinqt.cn -->

在其他语言，比如 php 中可以直接在 break 和 continue 后加 num ，比如 `break 2`或 `continue 2`。 break num 是结束外层第 num 层整个循环体，continue num 是结束外层第
num 层单次循环。

go 中不能直接在关键字后加 num ，但是可以用 label 关键代替 num。支持 goto label，也可以用 break label 和 continue label。

`goto` 可以跳到代码的任何地方，比如跳到 `A` 处，再从 `A` 继续往下执行。break label 如果跳到了循环外，不会再执行循环。continue label 如果跳出了循环，会再执行循环。

## continue label

```go
package main

import (
	"fmt"
	"math"
)

func main() {
	// 找出 int 切片的最小值
	var matrix = []int{10, 2, 4, 0}
	var min = math.MinInt64

next:
	for _, v := range matrix {
		for _, v1 := range matrix {
			if v > v1 {
				continue next // 终止当前循环，跳到 label 继续下一次循环
			}
		}
		min = v
	}

	fmt.Println("最小值为: ", min)
}

```

## break label

:point_down: 以下例子，虽然 break 跳出循环到 label 处, label 在 for 循环上，但是不会再执行 for 循环，直接执行`fmt.Println()`。

```go
package main

import (
	"fmt"
	"math"
)

func main() {
	// 获取 index 2 的值，这里使用 2 层循环主要是为了说明问题
	var matrix = []int{10, 2, 4, 0}
	var index2Val = math.MinInt64

next:
	for _, v := range matrix {
		fmt.Println(v)
		for index, v1 := range matrix {
			index2Val = v1
			if index == 2 {
				break next
			}
		}
	}

	fmt.Println("index 3 值为: ", index2Val)
}
```

## goto label

非必要不使用，可以跳到任何地方。

```go
package main

import (
	"fmt"
	"math"
)

func main() {
	var matrix = []int{10, 2, 4, 0}
	var index2Val = math.MinInt64

	for _, v := range matrix {
		fmt.Println(v)
		for index, v1 := range matrix {
			index2Val = v1
			if index == 2 {
				goto next
			}
		}
	}

	fmt.Println("index 3 值为: ", index2Val)

next:
	fmt.Println("goto this....")

}

```

