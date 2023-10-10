# Golang 内存逃逸


<!-- author： xiaobinqt -->
<!-- email： xiaobinqt@163.com -->
<!-- https://xiaobinqt.github.io -->
<!-- https://www.xiaobinqt.cn -->

在 C/C++ 开发中，动态分配内存（new/malloc）需要开发者手动释放资源。这样做的好处是，需要申请多少内存空间可以很好的掌握怎么分配。但是这有个缺点，如果忘记释放内存，则会导致内存泄漏。在很多高级语言中（python/Go/java）都加上了垃圾回收机制。

## 堆和栈

栈可以简单得理解成一次函数调用内部申请到的内存，它们会随着函数的返回把内存还给系统。下面来看看一个例子：

```
func F() {
    temp := make([]int, 0, 20)
    ...
}
```

上面的例子，内函数内部申请的临时变量，即使是用 make 申请到的内存，如果发现在退出函数后没有用了，那么就把丢到栈上，毕竟栈上的内存分配比堆上快很多。

再看一个堆的例子：

```
func F() []int{
    a := make([]int, 0, 20)
    return a
}
```

上面这段代码，申请的代码和上面的一模一样，但是申请后作为返回值返回了，编译器会认为在退出函数之后还有其他地方在引用，当函数返回之后并不会将其内存归还。那么就申请到堆里。

如果变量都分配到堆上，堆不像栈可以自动清理。它会引起 Go 频繁地进行垃圾回收，而垃圾回收会占用比较大的系统开销。

### 堆和栈相比

堆适合不可预知的大小的内存分配。但是为此付出的代价是分配速度较慢，而且会形成内存碎片。

栈内存分配则会非常快，栈分配内存只需要两个 CPU 指令：PUSH 和 RELEASE 分配和释放；而堆分配内存首先需要去找到一块大小合适的内存块。之后要通过垃圾回收才能释放。

{{< admonition type=info title="内存碎片" open=true >}}

内存碎片（Memory Fragmentation）是指计算机系统中存在的一种内存分配和释放的情况，它可能导致系统中的可用内存不连续、零散分布，使得系统效率下降或者无法有效地利用可用内存。内存碎片通常分为两种类型：外部碎片和内部碎片。

1. 外部碎片（External Fragmentation）：
    - 外部碎片指的是在可用内存中存在的未分配的小块内存空间，虽然总的可用内存大小足够，但是这些小块内存分散在不同的地方，无法被有效地利用。
    - 外部碎片通常发生在动态内存分配和释放的过程中。当程序请求分配一块内存时，系统会找到一个足够大的连续内存块来满足需求，但是如果可用内存被分割成多个小块，就可能出现无法分配所需大小的内存块的情况。

2. 内部碎片（Internal Fragmentation）：
    - 内部碎片是指已经分配给程序的内存块中，有一部分内存没有被程序有效利用，造成了浪费。
    - 内部碎片通常发生在内存分配时，分配了比实际需要更大的内存块，但程序没有充分利用这些额外的内存空间。

内存碎片的重要性和影响：

- 内存碎片会导致系统性能下降，因为操作系统需要更多的时间来寻找足够大的连续内存块来满足程序的需求。
- 内存碎片也可能导致程序崩溃或运行不稳定，特别是当内存碎片积累到一定程度时。
- 为了减少内存碎片的影响，程序员和操作系统通常采用不同的策略，如内存合并、内存池等，以更有效地管理内存。

{{< /admonition >}}

## 逃逸分析

逃逸分析是一种确定指针动态范围的方法。简单来说就是分析在程序的哪些地方可以访问到该指针。编译器会根据变量是否被外部引用来决定是否逃逸：

1. 如果函数外部没有引用，则优先放到栈中；
2. 如果函数外部存在引用，则必定放到堆中；

对此可以理解为，逃逸分析是编译器用于决定变量分配到堆上还是栈上的一种行为。

**go 在编译阶段确立逃逸，并不是在运行时**。

## 指针逃逸

提问：函数传递指针真的比传值效率高吗？

传递指针可以减少底层值的拷贝，可以提高效率，但是如果拷贝的数据量小，由于指针传递会产生逃逸，可能会使用堆，也可能会增加 GC 的负担，所以传递指针不一定是高效的。

官网上上有一个关于变量分配的问题 [How do I know whether a variable is allocated on the heap or the stack?](https://go.dev/doc/faq#stack_or_heap:~:text=From%20a%20correctness,on%20the%20stack.)

Go 可以返回局部变量指针，这其实是一个典型的变量逃逸案例，示例代码如下：

```go
package main

type Student struct {
	Name string
	Age  int
}

func StudentRegister(name string, age int) *Student {
	s := new(Student) //局部变量s逃逸到堆

	s.Name = name
	s.Age = age

	return s
}

func main() {
	StudentRegister("Jim", 18)
}
```

虽然在函数 StudentRegister() 内部 s 为局部变量，其值通过函数返回值返回，s 本身为一指针，其指向的内存地址不会是栈而是堆，这就是典型的逃逸案例。

```
λ go build -gcflags=-m main.go
# command-line-arguments
.\main.go:8:6: can inline StudentRegister
.\main.go:17:6: can inline main
.\main.go:18:17: inlining call to StudentRegister
.\main.go:8:22: leaking param: name
.\main.go:9:10: new(Student) escapes to heap
.\main.go:18:17: new(Student) does not escape
```

指令集 -gcflags 用于将标识参数传递给 Go 编译器，-m 会打印出逃逸分析的优化策略。

可见在 StudentRegister() 函数中，也即代码第 9 行显示 escapes to heap，代表该行内存分配发生了逃逸现象。

### 栈空间不足逃逸

```go
package main

func main() {

	s := make([]int, 1000, 1000)

	for index, _ := range s {
		s[index] = index
	}
}
```

上面代码主函数中分配了一个 1000 个长度的切片，是否逃逸取决于栈空间是否足够大。直接查看编译提示，如下：

```
λ go build -gcflags=-m main.go
# command-line-arguments
.\main.go:3:6: can inline main
.\main.go:5:11: make([]int, 1000, 1000) does not escape
```

根据上面的信息，没有发生逃逸。分配了一个 1000 的长度还不足以发生逃逸现象。x10 倍后，再看看情况。

```go
package main

func main() {

	s := make([]int, 5, 10000)

	for index, _ := range s {
		s[index] = index
	}
}
```

```
λ go build -gcflags=-m main.go
# command-line-arguments
.\main.go:3:6: can inline main
.\main.go:5:11: make([]int, 10000, 10000) escapes to heap
```

当切片长度扩大到 10000 时就会逃逸。实际上当栈空间不足以存放当前对象时或无法判断当前切片长度时会将对象分配到堆中。

### 动态类型逃逸

很多函数参数为 interface 类型。比如：

```
func Printf(format string, a ...interface{}) (n int, err error)
func Sprintf(format string, a ...interface{}) string
func Fprint(w io.Writer, a ...interface{}) (n int, err error)
func Print(a ...interface{}) (n int, err error)
func Println(a ...interface{}) (n int, err error)
```

编译期间很难确定其参数的具体类型，也能产生逃逸。

如下代码所示：

```go
package main

import "fmt"

func main() {
	fmt.Println("hello 123")
	fmt.Print("hello 456")
}

```

```
λ go build -gcflags=-m main.go
# command-line-arguments
.\main.go:6:13: inlining call to fmt.Println
.\main.go:7:11: inlining call to fmt.Print
.\main.go:6:13: ... argument does not escape
.\main.go:6:14: "hello 123" escapes to heap
.\main.go:7:11: ... argument does not escape
.\main.go:7:12: "hello 456" escapes to heap
```

## 逃逸分析的作用

1. 逃逸分析的好处是为了减少 gc 的压力，不逃逸的对象分配在栈上，当函数返回时就回收了资源，不需要 gc 标记清除。

2. 逃逸分析完后可以确定哪些变量可以分配在栈上，栈的分配比堆快，性能好（逃逸的局部变量会在堆上分配，而没有发生逃逸的则有编译器在栈上分配）。

3. 同步消除，如果定义的对象的方法上有同步锁，但在运行时，却只有一个线程在访问，此时逃逸分析后的机器码，会去掉同步锁运行。

{{< admonition type=info title="info" open=true >}}

当涉及到同步锁（Mutex）以及只有一个线程在访问的情况时，逃逸分析可能会起到关键作用。下面是一个简单的示例来解释这个情况：

```go
package main

import "sync"

func main() {
	var mu sync.Mutex
	var data int

	mu.Lock()
	data = 42
	mu.Unlock()

	// 在这里，编译器会执行逃逸分析
	// 如果编译器能够确定 data 不会逃逸到堆上，它可能会去除同步锁
	// 因为只有一个线程在访问 data，不涉及并发竞争
}
```

在这个示例中，虽然我们使用了同步锁来保护 `data` 的访问，但是在逃逸分析的过程中，编译器可以发现 `data` 没有逃逸到堆上，因此它可以选择去掉同步锁，因为只有一个线程在访问 `data`，不存在并发竞争的情况。

这种优化可以提高程序的性能，因为同步锁的获取和释放操作可能会引入一些开销。不过需要注意的是，编译器会根据具体情况进行判断，而不是简单地因为只有一个线程就去掉所有同步锁。在多线程情况下，同步锁是必要的，以确保数据的安全访问。因此，在编写多线程程序时，仍然需要谨慎使用同步锁以确保线程安全。

{{< /admonition >}}

## 总结

1. 堆上动态分配内存比栈上静态分配内存，开销大很多。

2. 变量分配在栈上需要能在编译期确定它的作用域，否则会分配到堆上。

3. Go 编译器会在编译期对考察变量的作用域，并作一系列检查，如果它的作用域在运行期间对编译器一直是可知的，那么就会分配到栈上。简单来说，**编译器会根据变量是否被外部引用来决定是否逃逸**。

4. 编译器的这些逃逸分析规则其实不需要掌握，只需通过 `go build -gcflags=-m` 命令来观察变量逃逸情况就行了。

5. 不要盲目使用变量的指针作为函数参数，虽然它会减少复制操作。但其实当参数为变量自身的时候，复制是在栈上完成的操作，开销远比变量逃逸后动态地在堆上分配内存少的多。

6. 逃逸分析在编译阶段完成的。

## 参考

+ [Golang 内存分配 - stack and heap](https://colynn.github.io/2020-07-16-go-memory-allocation/)





