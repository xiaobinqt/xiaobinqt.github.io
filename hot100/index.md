# LeetCode 热题 HOT 100


[//]: # (https://cdn.xiaobinqt.cn/xiaobinqt.io/20220326/750cc88f8c434944af5eec1c38b02b51.png)

[//]: # (https://cdn.xiaobinqt.cn/xiaobinqt.io/20220326/45ef828b089c4dd18ec699336bc2499f.png)


{{< admonition type=info title="版权信息" open=true >}}

链接：[https://leetcode-cn.com/problem-list/2cktkvj](https://leetcode-cn.com/problem-list/2cktkvj/)

来源：力扣（LeetCode）

{{< /admonition >}}

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

## 20. 有效的括号

题目地址：[https://leetcode-cn.com/problems/valid-parentheses/](https://leetcode-cn.com/problems/valid-parentheses/)

### 解题思路

判断括号的有效性可以使用「栈」这一数据结构来解决。

我们遍历给定的字符串 s。当我们遇到一个**左括号**时，我们会期望在后续的遍历中，有一个相同类型的**右括号**将其闭合。由于
**后遇到的左括号要先闭合**，因此我们可以将这个**左括号放入栈顶**。

当我们遇到一个右括号时，我们需要将一个相同类型的左括号闭合。此时，我们可以取出栈顶的左括号并判断它们是否是相同类型的括号。如果不是相同的类型，或者栈中并没有左括号，那么字符串 s 无效，返回
`False`。为了快速判断括号的类型，我们可以使用哈希表存储每一种括号。**哈希表的键为右括号，值为相同类型的左括号**。

在遍历结束后，如果栈中没有左括号，说明我们将字符串 s 中的所有左括号闭合，返回 `True`，否则返回 `False`。

注意到有效字符串的长度一定为偶数，因此如果字符串的长度为奇数，我们可以直接返回 `False`，省去后续的遍历判断过程。

### go 实现

```go
package main

import "fmt"

func isValid(s string) bool {
	n := len(s)

	if n%2 != 0 { // 奇数直接退出
		return false
	}

	pairs := map[byte]byte{
		')': '(',
		']': '[',
		'}': '{',
	}

	stack := []byte{}
	for i := 0; i < n; i++ {
		if pairs[s[i]] > 0 { // 如果是右括号,判断栈顶是否是对应的左括号,果然有对应的左括号,则弹出栈顶元素,否则直接退出
			if len(stack) == 0 || stack[len(stack)-1] != pairs[s[i]] {
				return false
			}
			stack = stack[:len(stack)-1]
		} else {
			stack = append(stack, s[i])
		}
	}

	return len(stack) == 0
}

func main() {
	fmt.Println(isValid("()[]{}"))
}

```





