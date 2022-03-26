# LeetCode 热题 HOT 100


[//]: # (https://cdn.xiaobinqt.cn/xiaobinqt.io/20220326/750cc88f8c434944af5eec1c38b02b51.png)

[//]: # (https://cdn.xiaobinqt.cn/xiaobinqt.io/20220326/45ef828b089c4dd18ec699336bc2499f.png)

## 1. 两数之和

题目地址：[https://leetcode-cn.com/problems/two-sum/](https://leetcode-cn.com/problems/two-sum/)

### 解题思路

嵌套遍历数组，外层遍历的值和内层遍历的值相加，如果相加等于目标值，则返回结果，否则继续遍历。内层遍历开始的位置是外层遍历的位置加 1，结束的位置是数组长度。

### go 实现

```go
package main

import "fmt"

func twoSum(nums []int, target int) []int {
	for index, value := range nums {
		for i := index + 1; i < len(nums); i++ {
			if (value + nums[i]) == target {
				return []int{index, i}
			}
		}
	}

	return nil
}

func main() {
	fmt.Println(twoSum([]int{3, 2, 4}, 6))
}
```






