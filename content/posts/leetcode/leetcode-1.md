---
title: "LeetCode（一）"
subtitle: ""

init_date: "2022-12-07T23:10:42+08:00"

date: 2022-11-05

lastmod: 2022-12-07

draft: false

author: "xiaobinqt"
description: "xiaobinqt，"

featuredImage: "https://cdn.xiaobinqt.cn/xiaobinqt.io/20220326/750cc88f8c434944af5eec1c38b02b51.png"

featuredImagePreview: ""

reproduce: false

translate: false

tags: ["leetcode"]
categories: ["算法与数学"]
lightgallery: true

series: ["leetcode"]

series_weight:

toc: true

math: true
---

<!-- author： xiaobinqt -->
<!-- email： xiaobinqt@163.com -->
<!-- https://xiaobinqt.github.io -->
<!-- https://www.xiaobinqt.cn -->

{{< admonition type=info title="版权信息" open=true >}}

来源：[力扣（LeetCode）](https://leetcode.cn/)

{{< /admonition >}}

## 704. 二分查找

### 解题思路

参考 [https://www.bilibili.com/video/BV1fA4y1o715/?spm_id_from=333.788](https://www.bilibili.com/video/BV1fA4y1o715/?spm_id_from=333.788)

对于常规实现来说，其实要区分区间，也就是`左闭右闭`和`左闭右开`的两种解法，对于`左闭右闭`来说，包含最右边，那么`right`其实是`数组长度-1`，但是对于`左闭右开`来说，因为不包含最右元素，那个`right`其实就是数组长度。

### Go 实现

**区间左闭右闭**

```go
package main

import (
	"fmt"
)

func main() {
	arr := []int{0, 1, 2, 3, 4, 5, 10}
	fmt.Println(binarySearch(arr, 10))
}

func binarySearch(nums []int, target int) int {
	left := 0
	right := len(nums) - 1

	for left <= right {
		middle := (left + right) / 2
		if target > nums[middle] {
			left = middle + 1
		} else if target < nums[middle] {
			right = middle - 1
		} else {
			return middle
		}
	}

	return -1
}

```

**区间左闭右开**

```go
package main

import (
	"fmt"
)

func main() {
	arr := []int{0, 1, 2, 3, 4, 5, 10}
	fmt.Println(binarySearch(arr, 10))
}

func binarySearch(nums []int, target int) int {
	left := 0
	right := len(nums)

	for left < right {
		middle := (left + right) / 2
		if target > nums[middle] {
			left = middle + 1
		} else if target < nums[middle] {
			right = middle
		} else {
			return middle
		}
	}

	return -1
}

```

## 206. 反转链表

题目地址：[https://leetcode.cn/problems/reverse-linked-list/](https://leetcode.cn/problems/reverse-linked-list/)

类似/相同题目：[剑指 Offer 24. 反转链表](https://leetcode.cn/problems/fan-zhuan-lian-biao-lcof/)

### 解题思路

**迭代法**

[//]: # (一般采取遍历的形式。如果链表中只有 2 个节点，`1->2`，那么反转后就是`2->1`，也就是 2 的 next 节点是 1，1 的 next 节点是 nil，。当遍历第一个节点 1 时，此时 curr 就是 head，)


**递归法**

### Go 迭代实现

```go
package main

type ListNode struct {
	Val  int
	Next *ListNode
}

func reverseList(head *ListNode) *ListNode {
	if head == nil {
		return nil
	}

	var (
		prev, next *ListNode
		curr       = head
	)

	for curr != nil {
		next = curr.Next
		curr.Next = prev
		// 下一个
		prev = curr
		curr = next
	}

	return prev
}

func main() {
	reverseList(&ListNode{
		Val: 1, Next: &ListNode{Val: 2, Next: &ListNode{Val: 3, Next: &ListNode{Val: 4, Next: &ListNode{Val: 5}}}}})
}

```

### Go 递归实现

```go
package main

import (
	"fmt"
)

type ListNode struct {
	Val  int
	Next *ListNode
}

func reverseList(head *ListNode) *ListNode {
	if head == nil || head.Next == nil {
		return head
	}

	newHead := reverseList(head.Next)
	head.Next.Next = head
	head.Next = nil

	return newHead
}

func main() {
	x := reverseList(&ListNode{
		Val: 1,
		Next: &ListNode{
			Val: 2,
			Next: &ListNode{
				Val: 3,
				Next: &ListNode{
					Val:  4,
					Next: nil,
				},
			},
		},
	})
	fmt.Println(x)
}

```

## 21. 合并两个有序链表

题目地址：[https://leetcode.cn/problems/merge-two-sorted-lists/description/](https://leetcode.cn/problems/merge-two-sorted-lists/description/)

### 解题思路

**递归解法**

递归的核心在于，我只关注我这一层要干什么，返回什么，至于我的下一层（规模减 1），我不管，我就是甩手掌柜。

那么现在我要 merge L1，L2 我需要怎么做:question:

+ 但一条链表为空时，**返回对方**，因为如果返回自己，就退出了，返回对方，不管对方是什么，让下级去判断。
+ 如果 L1 第一个元素小于 L2 的？那我得把 L1 的这个元素放到最前面，至于后面的那串长啥样，我不管。我只要接过下级员工干完活后给我的包裹，然后把我干的活附上去（令 L1->next = 这个包裹）就行。
+ 这个包裹是下级员工干的活，即`merge(L1->next,L2)`。

我该返回啥:question:

+ 现在不管我的下一层干了什么，又返回了什么给我，我只要知道，假设我的工具人们都完成了任务，那我的任务也就完成了，可以返回最终结果了。
+ 最终结果就是我一开始接手的 L1 头结点+下级员工给我的大包裹，要一并交上去，这样我的 boss 才能根据我给它的 L1 头节点往下找，检查我完成的工作。

### Go 递归实现

```go
package main

import "fmt"

type ListNode struct {
	Val  int
	Next *ListNode
}

func mergeTwoLists(list1 *ListNode, list2 *ListNode) (x *ListNode) {
	if list1 == nil {
		return list2
	}
	if list2 == nil {
		return list1
	}

	if list1.Val <= list2.Val {
		list1.Next = mergeTwoLists(list1.Next, list2)
		return list1
	} else {
		list2.Next = mergeTwoLists(list2.Next, list1)
		return list2
	}
}

func main() {
	x := mergeTwoLists(&ListNode{Val: 1, Next: &ListNode{
		Val: 2,
		Next: &ListNode{
			Val:  4,
			Next: nil,
		},
	}}, &ListNode{Val: 1, Next: &ListNode{
		Val: 3,
		Next: &ListNode{
			Val:  4,
			Next: nil,
		},
	}})
	fmt.Println(x)
}

```

## 344. 反转字符串

题目地址：[https://leetcode.cn/problems/reverse-string/description/](https://leetcode.cn/problems/reverse-string/description/)

### 解题思路

**双指针法**

对于长度为`N`的待被反转的字符数组，我们可以观察反转前后下标的变化，假设反转前字符数组为`s[0] s[1] s[2] ... s[N - 1]`，那么反转后字符数组为`s[N - 1] s[N - 2] ... s[0]`。比较反转前后下标变化很容易得出`s[i]`的字符与`s[N - 1 - i]`的字符发生了交换的规律，因此我们可以得出如下双指针的解法：

+ 将`left`指向字符数组首元素，`right`指向字符数组尾元素。
+ 当`left < right`：
    + 交换`s[left]`和`s[right]`；
    + `left`指针右移一位，即`left = left + 1`；
    + `right`指针左移一位，即`right = right - 1`。
+ 当`left >= right`，反转结束，返回字符数组即可。

[//]: # (![双指针法]&#40;https://cdn.xiaobinqt.cn/xiaobinqt.io/20221208/3b9762938a9b4679974b7481e302cdd1.png '双指针法'&#41;)

### Go 双指针法

```go
package main

import (
	"fmt"
)

func reverseString(s []byte) {
	for left, right := 0, len(s)-1; left < right; left++ {
		s[left], s[right] = s[right], s[left]
		right--
	}
}

func main() {
	x := []byte{'1', '2', '3'}
	reverseString(x)
	fmt.Println(string(x))
}

```

## 24. 两两交换链表中的节点

题目地址：[https://leetcode.cn/problems/swap-nodes-in-pairs/](https://leetcode.cn/problems/swap-nodes-in-pairs/)

### 解题思路

参考 [https://leetcode.cn/problems/swap-nodes-in-pairs/solutions/444474/liang-liang-jiao-huan-lian-biao-zhong-de-jie-di-91/](https://leetcode.cn/problems/swap-nodes-in-pairs/solutions/444474/liang-liang-jiao-huan-lian-biao-zhong-de-jie-di-91/)

**递归法**

可以通过递归的方式实现两两交换链表中的节点。

递归的终止条件是链表中没有节点，或者链表中只有一个节点，此时无法进行交换。

如果链表中至少有两个节点，则在两两交换链表中的节点之后，原始链表的头节点变成新的链表的第二个节点，原始链表的第二个节点变成新的链表的头节点。链表中的其余节点的两两交换可以递归地实现。在对链表中的其余节点递归地两两交换之后，更新节点之间的指针关系，即可完成整个链表的两两交换。

用`head`表示原始链表的头节点，新的链表的第二个节点，用`newHead`表示新的链表的头节点，原始链表的第二个节点，则原始链表中的其余节点的头节点是`newHead.next`。令`head.next = swapPairs(newHead.next)`，表示将其余节点进行两两交换，交换后的新的头节点为`head`的下一个节点。然后令`newHead.next = head`，即完成了所有节点的交换。最后返回新的链表的头节点`newHead`。

:warning:好吧，再理解一下，关于递归，我只关注我这一层要干什么，返回什么，至于我的下一层（规模减 1），我不管，我就是一个甩手掌柜:see_no_evil:。

我其实只需要关心第一层，也就是`节点1`和`节点2`的交换，把`节点2`的`next`指向`节点1`，`节点2`的`next`给下一层也就是递归函数。而我最后返回的应该是头结点，其实也就是原始节点的`节点2`。

**迭代法**

### Go 递归实现

```go
package main

import (
	"fmt"
)

type ListNode struct {
	Val  int
	Next *ListNode
}

func swapPairs(head *ListNode) *ListNode {
	if head == nil || head.Next == nil {
		return head
	}

	newHead := head.Next
	head.Next = swapPairs(head.Next.Next)
	newHead.Next = head
	return newHead
}

func main() {
	x := swapPairs(&ListNode{
		Val: 1,
		Next: &ListNode{
			Val: 2,
			Next: &ListNode{
				Val: 3,
				Next: &ListNode{
					Val:  4,
					Next: nil,
				},
			},
		},
	})
	fmt.Println(x)
}

```

## 27. 移除元素

题目地址：[https://leetcode.cn/problems/remove-element/description/](https://leetcode.cn/problems/remove-element/description/)

### 解题思路

可以用双指针/快慢指针法来解决。快指针用来寻找新数组的元素，新数组就是不含有目标元素的数组。慢指针用来指向更新新数组下标的位置。这里需要的注意的是，“新数组”其实旧数组，因为一直都在在同一个数组上的操作。

### Go 双指针

```go
package main

import "fmt"

func removeElement(nums []int, val int) int {
	length := len(nums)
	low := 0
	for i := 0; i < length; i++ {
		if nums[i] != val {
			nums[low] = nums[i]
			low++
		}
	}

	return low
}

func main() {
	x := []int{1, 2, 6, 7, 9, 6, 6, 6}
	xx := removeElement(x, 6)
	fmt.Println(x, xx)
}

```

## 977. 有序数组的平方

题目地址：[https://leetcode.cn/problems/squares-of-a-sorted-array/description/](https://leetcode.cn/problems/squares-of-a-sorted-array/description/)

### 解题思路

**暴力法**可以直接先计算平方，然后再利用库函数排序。

**双指针法**
可以参考 [https://programmercarl.com/0977.%E6%9C%89%E5%BA%8F%E6%95%B0%E7%BB%84%E7%9A%84%E5%B9%B3%E6%96%B9.html#%E6%9A%B4%E5%8A%9B%E6%8E%92%E5%BA%8F](https://programmercarl.com/0977.%E6%9C%89%E5%BA%8F%E6%95%B0%E7%BB%84%E7%9A%84%E5%B9%B3%E6%96%B9.html#%E6%9A%B4%E5%8A%9B%E6%8E%92%E5%BA%8F)

数组其实是有序的，只不过负数平方之后可能成为最大数了。那么数组平方的最大值就在数组的两端，不是最左边就是最右边，不可能是中间。此时可以考虑双指针法了，`i`指向起始位置，`j`指向终止位置。定义一个新数组 result，和 A 数组一样的大小，让`k`指向 result 数组终止位置。

如果`A[i] * A[i] < A[j] * A[j]` 那么`result[k--] = A[j] * A[j]` 。

如果`A[i] * A[i] >= A[j] * A[j]`那么`result[k--] = A[i] * A[i]`。

### Go 暴力法

```go
package main

import "fmt"

func removeElement(nums []int, val int) int {
	length := len(nums)
	low := 0
	for i := 0; i < length; i++ {
		if nums[i] != val {
			nums[low] = nums[i]
			low++
		}
	}

	return low
}

func main() {
	x := []int{1, 2, 6, 7, 9, 6, 6, 6}
	xx := removeElement(x, 6)
	fmt.Println(x, xx)
}

```

### Go 双指针

```go
package main

import "fmt"

func sortedSquares02(nums []int) []int {
	if len(nums) == 0 {
		return []int{}
	}

	var (
		result = make([]int, len(nums))
		i, j   = 0, len(nums) - 1
		k      = len(nums) - 1
	)

	for i <= j {
		if nums[i]*nums[i] > nums[j]*nums[j] {
			result[k] = nums[i] * nums[i]
			k--
			i++
		} else {
			result[k] = nums[j] * nums[j]
			k--
			j--
		}
	}

	return result
}

func main() {
	fmt.Println(sortedSquares02([]int{-4, -1, 0, 3, 10}))
}

```

[//]: # (## 104. 二叉树的最大深度)

[//]: # ()

[//]: # (题目地址：[https://leetcode.cn/problems/maximum-depth-of-binary-tree/]&#40;https://leetcode.cn/problems/maximum-depth-of-binary-tree/&#41;)


[//]: # (## 汉诺塔问题)

[//]: # ()

[//]: # (题目地址：[https://leetcode.cn/problems/hanota-lcci/solutions/95934/tu-jie-yi-nuo-ta-de-gu-shi-ju-shuo-dang-64ge-pan-z/]&#40;https://leetcode.cn/problems/hanota-lcci/solutions/95934/tu-jie-yi-nuo-ta-de-gu-shi-ju-shuo-dang-64ge-pan-z/&#41;)

[//]: # (## 统计n以内的素数个数)

[//]: # ()

[//]: # (> 素数：只能被 1 和自身整除的自然数，0、1除外。比如 2 只能被 1 和自身整除，但是 4 能被 [1,2,4] 整除，那 4 就不是素数。)
