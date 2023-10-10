# Go 方法值接收者和指针接收者的区别


<!-- author： xiaobinqt -->
<!-- email： xiaobinqt@163.com -->
<!-- https://xiaobinqt.github.io -->
<!-- https://www.xiaobinqt.cn -->


如果方法的接收者是指针类型，无论调用者是对象还是对象指针，修改的都是对象本身，**会影响**调用者；

如果方法的接收者是值类型，无论调用者是对象还是对象指针，修改的都是对象的副本，**不影响**调用者；

```go
package main

import "fmt"

type Person struct {
	age int
}

// 如果实现了接收者是指针类型的方法，会隐含地也实现了接收者是值类型的 IncrAgePointer 方法。
//会修改 age 的值
func (p *Person) IncrAgePointer() {
	p.age += 1
}

// 如果实现了接收者是值类型的方法，会隐含地也实现了接收者是指针类型的 IncrAgeValue 方法。
//不会修改 age 的值
func (p Person) IncrAgeValue() {
	p.age += 1
}

// 如果实现了接收者是值类型的方法，会隐含地也实现了接收者是指针类型的 GetAge 方法。
func (p Person) GetAge() int {
	return p.age
}

func main() {
	// p1 是值类型
	p1 := Person{age: 10}

	// 值类型 调用接收者是指针类型的方法
	p1.IncrAgePointer()
	fmt.Println(p1.GetAge())

	// 值类型 调用接收者是值类型的方法
	p1.IncrAgeValue()
	fmt.Println(p1.GetAge())

	fmt.Println("------------------------")

	//p2 是指针类型
	p2 := &Person{age: 20}

	// 指针类型 调用接收者是指针类型的方法
	p2.IncrAgePointer()
	fmt.Println(p2.GetAge())

	// 指针类型 调用接收者是值类型的方法
	p2.IncrAgeValue()
	fmt.Println(p2.GetAge())
}
```

输出结果为：

```
11
11
------------------------
21
21
```

上述代码中，实现了接收者是指针类型的 IncrAgePointer 函数，不管调用者是值类型还是指针类型，都可以调用 IncrAgePointer 方法，并且它的 age 值都改变了。

实现了接收者是指针类型的 IncrAgeValue 函数，不管调用者是值类型还是指针类型，都可以调用 IncrAgeValue 方法，并且它的 age 值都没有被改变。

通常使用**指针类型作为方法的接收者的理由**：

1. 使用指针类型能够修改调用者的值。

2. 使用指针类型可以避免在每次调用方法时复制该值，在值的类型为大型结构体时，这样做会更加高效。






