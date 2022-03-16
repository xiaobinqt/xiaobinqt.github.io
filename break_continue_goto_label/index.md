# golang break，continue，goto label 的区别



在 php 中可以直接在 break 和 continue 后加 num ，比如 `break 2`或 `continue 2`。

break num 是结束外层第 num 层整个循环体，continue num 是结束外层第 num 层单次循环。

类比 php ，go 中不能直接在关键字后加 num ，但是可以用 label 关键字代替 num。

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
				break next // 跳出循环到 label 处
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


