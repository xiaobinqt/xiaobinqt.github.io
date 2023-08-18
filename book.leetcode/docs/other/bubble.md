---
weight: 2

bookFlatSection: true

BookToC: true

title: "冒泡排序"
---

# 冒泡排序

## 题目描述

输入一个整数数组，按从小到大的顺序排序。

## 具体实现

```go
package main

import "fmt"

func Bubble(arr []int) []int {
	length := len(arr)
	for i := 0; i < length-1; i++ {
		// 注意这里 j 是从 0 开始而不是从 i 开始
		for j := 0; j < length-i-1; j++ {
			if arr[j] > arr[j+1] {
				tmp := arr[j]
				arr[j] = arr[j+1]
				arr[j+1] = tmp
			}
		}
	}

	return arr
}

func main() {
	fmt.Println(Bubble([]int{1, 10, 25, 30}))
}

```
