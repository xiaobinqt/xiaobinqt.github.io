---
title: "Golang 简单并发模式"
subtitle: ""

init_date: "2023-10-18T15:55:47+08:00"

date: 2022-08-03

lastmod: 2023-10-18

draft: true

author: "xiaobinqt"
description: "xiaobinqt,go 并发模型,流水线模型"

featuredImage: ""

featuredImagePreview: ""

reproduce: false

translate: false

tags: [ "golang" ]
categories: [ "golang" ]
lightgallery: true

series: [ ]

series_weight:

toc: true

math: true
---

<!-- author： xiaobinqt -->
<!-- email： xiaobinqt@163.com -->
<!-- https://xiaobinqt.github.io -->
<!-- https://www.xiaobinqt.cn -->

## 流水线模型

Go 并发核心思路是关注数据的流动。数据流动的过程交给 channel，数据处理的每个环节交给 goroutine，把这些流程画起来，有始有终形成一条线，这就是流水线模型。在 Go 中，流水线由多个阶段组成，每个阶段之间通过 channel 连接，每个节点可以由多个同时运行的 goroutine 组成。

下图的流水线由 3 个阶段组成，分别是 A、B、C，A 和 B 之间是通道 `aCh`，B 和 C 之间是通道 `bCh`，A 生成数据传递给 B，B 生成数据传递给 C。

流水线中，第一个阶段的协程是**生产者**，它们只生产数据。最后一个阶段的协程是**消费者**，它们只消费数据。下图中 A 是生成者，C 是消费者，而 B 只是中间过程的处理者。

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20231018/47f305e18d9a4294bd2bb1c07c954505.png '流水线模型')

举个例子，设计一个程序：计算一个整数切片中元素的平方值并把它打印出来。非并发的方式是使用 for 遍历整个切片，然后计算平方，打印结果。

使用流水线模型实现这个简单的功能，从流水线的角度，可以分为 3 个阶段：

1. 遍历切片，这是生产者。
2. 计算平方值。
3. 打印结果，这是消费者。

下面这段代码：

- `producer()`负责生产数据，它会把数据写入通道，并把它写数据的通道返回。
- `square()`负责从某个通道读数字，然后计算平方，将结果写入通道，并把它的输出通道返回。
- `main()`负责启动 producer 和 square，并且还是消费者，读取 square 的结果，并打印出来。

```
package main

import (
	"fmt"
)

func producer(nums ...int) <-chan int {
	out := make(chan int)
	go func() {
		defer close(out)
		for _, n := range nums {
			out <- n
		}
	}()
	return out
}

func square(inCh <-chan int) <-chan int {
	out := make(chan int)
	go func() {
		defer close(out)
		for n := range inCh {
			out <- n * n
		}
	}()

	return out
}

func main() {
	in := producer(1, 2, 3, 4)
	ch := square(in)

	for ret := range ch {
		fmt.Printf("%3d", ret)
	}
	fmt.Println()
}

```

结果：

```
1  4  9 16
```

这是一种原始的流水线模型，这种原始能让我们掌握流水线的思路。

流水线的特点：

1. 每个阶段把数据通过 channel 传递给下一个阶段。
2. 每个阶段要创建 1 个 goroutine 和 1 个通道，这个 goroutine 向里面写数据，函数要返回这个通道。
3. 有 1 个函数来组织流水线，这个例子中是 main 函数。

## 扇入扇出模式

- FAN-OUT（扇出）模式：多个 goroutine 从同一个通道读取数据，直到该通道关闭。OUT 是一种张开的模式，所以又被称为扇出，可以用来分发任务。
- FAN-IN（扇入）模式：1 个 goroutine 从多个通道读取数据，直到这些通道关闭。IN 是一种收敛的模式，所以又被称为扇入，用来收集处理的结果。

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20231018/82d80c81c63a4381a2950b36e4e71f62.png '扇入扇出模式')

### 扇入扇出实践

计算一个整数切片中元素的平方值并把它打印出来。

- `producer()` 负责生产数据。
- `squre()` 负责计算平方值。
- 修改`main()`，启动 3 个 square，这 3 个 square 从 producer 生成的通道读数据，这是扇出。
- 增加`merge()`，入参是 3 个 square 各自写数据的通道，给这 3 个通道分别启动 1 个协程，把数据写入到自己创建的通道，并返回该通道，这是扇入。

```go
package main

import (
	"fmt"
	"sync"
)

func producer(nums ...int) <-chan int {
	out := make(chan int)
	go func() {
		defer close(out)
		for _, n := range nums {
			out <- n
		}
	}()
	return out
}

func square(inCh <-chan int) <-chan int {
	out := make(chan int)
	go func() {
		defer close(out)
		for n := range inCh {
			out <- n * n
		}
	}()

	return out
}

func merge(cs ...<-chan int) <-chan int {
	out := make(chan int)

	var wg sync.WaitGroup

	collect := func(in <-chan int) {
		defer wg.Done()
		for n := range in {
			out <- n
		}
	}

	wg.Add(len(cs))
	// FAN-IN
	for _, c := range cs {
		go collect(c)
	}

	// 错误方式：直接等待是bug，死锁，因为merge写了out，main却没有读
	// wg.Wait()
	// close(out)

	// 正确方式
	go func() {
		wg.Wait()
		close(out)
	}()

	return out
}

func main() {
	in := producer(1, 2, 3, 4)

	// FAN-OUT
	c1 := square(in)
	c2 := square(in)
	c3 := square(in)

	// consumer
	for ret := range merge(c1, c2, c3) {
		fmt.Printf("%3d ", ret)
	}
	fmt.Println()
}

```

3 个 square 协程**并发**运行，结果顺序是无法确定的，所以得到的结果，不一定与下面的相同。

```
1   4  16   9
```

### 扇形模式是否能提升性能

对比一下简单的流水线和扇形模式的流水线，修改下代码，增加程序的执行时间：

- `produer()`使用参数生成指定数量的数据。
- `square()`增加阻塞操作，睡眠 1s，模拟阶段的运行时间。
- `main()`关闭对结果数据的打印，降低结果处理时的 IO 对扇形模式的对比。

```go
package main

import (
	"time"
)

func producer(n int) <-chan int {
	out := make(chan int)
	go func() {
		defer close(out)
		for i := 0; i < n; i++ {
			out <- i
		}
	}()
	return out
}

func square(inCh <-chan int) <-chan int {
	out := make(chan int)
	go func() {
		defer close(out)
		for n := range inCh {
			out <- n * n
			// simulate
			time.Sleep(time.Second)
		}
	}()

	return out
}

func main() {
	in := producer(10)
	ch := square(in)

	// consumer
	for _ = range ch {
	}
}

```

```go
package main

import (
	"sync"
	"time"
)

func producer(n int) <-chan int {
	out := make(chan int)
	go func() {
		defer close(out)
		for i := 0; i < n; i++ {
			out <- i
		}
	}()
	return out
}

func square(inCh <-chan int) <-chan int {
	out := make(chan int)
	go func() {
		defer close(out)
		for n := range inCh {
			out <- n * n
			// simulate
			time.Sleep(time.Second)
		}
	}()

	return out
}

func merge(cs ...<-chan int) <-chan int {
	out := make(chan int)

	var wg sync.WaitGroup

	collect := func(in <-chan int) {
		defer wg.Done()
		for n := range in {
			out <- n
		}
	}

	wg.Add(len(cs))
	// FAN-IN
	for _, c := range cs {
		go collect(c)
	}

	// 错误方式：直接等待是bug，死锁，因为merge写了out，main却没有读
	// wg.Wait()
	// close(out)

	// 正确方式
	go func() {
		wg.Wait()
		close(out)
	}()

	return out
}

func main() {
	in := producer(10)

	// FAN-OUT
	c1 := square(in)
	c2 := square(in)
	c3 := square(in)

	// consumer
	for _ = range merge(c1, c2, c3) {
	}
}

```

多次测试，每次结果近似，结果如下：

- 扇形模式利用了 7% 的 CPU，而普通流水线 CPU 只使用了 3%，**扇形模式能够更好的利用 CPU，提供更好的并发，提高 Go 程序的并发性能。**
- 扇形模式耗时 10s，普通流水线耗时 4s。**在协程比较费时时，扇形模式可以减少程序运行时间，同样的时间，可以处理更多的数据。**

```bash
➜  awesome git:(master) ✗ time go run hi_simple.go
go run hi_simple.go  0.17s user 0.18s system 3% cpu 10.389 total
➜  awesome git:(master) ✗
➜  awesome git:(master) ✗ time go run hi_fan.go
go run hi_fan.go  0.17s user 0.16s system 7% cpu 4.288 total
```

**也可以使用Benchmark进行测试，看2个类型的执行时间，结论相同**。为了节约篇幅，这里不再介绍，[方法和结果贴在Gist](https://gist.github.com/Shitaibin/9593a18989b6c81bb3aae5ccdf9b6470)了，想看的朋友瞄一眼，或自己动手搞搞。

在某些情况下，**扇形模式不一定能提升性能**。使用之前的问题，再次修改下代码，其他不变：

- `squre()` 去掉耗时。
- `main()` 增加 producer() 的入参，让 producer 生产 10,000,000 个数据。

[简单版流水线修改代码](https://github.com/Shitaibin/golang_pipeline_step_by_step/blob/fan_model_slow/hi_simple.go)：

```go
package main

import (
	"sync"
)

func producer(n int) <-chan int {
	out := make(chan int)
	go func() {
		defer close(out)
		for i := 0; i < n; i++ {
			out <- i
		}
	}()
	return out
}

func square(inCh <-chan int) <-chan int {
	out := make(chan int)
	go func() {
		defer close(out)
		for n := range inCh {
			out <- n * n
		}
	}()

	return out
}

func merge(cs ...<-chan int) <-chan int {
	out := make(chan int)

	var wg sync.WaitGroup

	collect := func(in <-chan int) {
		defer wg.Done()
		for n := range in {
			out <- n
		}
	}

	wg.Add(len(cs))
	// FAN-IN
	for _, c := range cs {
		go collect(c)
	}

	// 错误方式：直接等待是bug，死锁，因为merge写了out，main却没有读
	// wg.Wait()
	// close(out)

	// 正确方式
	go func() {
		wg.Wait()
		close(out)
	}()

	return out
}

func main() {
	in := producer(10000000)

	// FAN-OUT
	c1 := square(in)
	c2 := square(in)
	c3 := square(in)

	// consumer
	for _ = range merge(c1, c2, c3) {
	}
}

```

[扇形模式流水线修改代码](https://github.com/Shitaibin/golang_pipeline_step_by_step/blob/fan_model_slow/hi_fan.go)：

```go
package main

import (
	"sync"
	"time"
)

func producer(n int) <-chan int {
	out := make(chan int)
	go func() {
		defer close(out)
		for i := 0; i < n; i++ {
			out <- i
		}
	}()
	return out
}

func square(inCh <-chan int) <-chan int {
	out := make(chan int)
	go func() {
		defer close(out)
		for n := range inCh {
			out <- n * n
		}
	}()

	return out
}

func merge(cs ...<-chan int) <-chan int {
	out := make(chan int)

	var wg sync.WaitGroup

	collect := func(in <-chan int) {
		defer wg.Done()
		for n := range in {
			out <- n
		}
	}

	wg.Add(len(cs))
	// FAN-IN
	for _, c := range cs {
		go collect(c)
	}

	// 错误方式：直接等待是bug，死锁，因为merge写了out，main却没有读
	// wg.Wait()
	// close(out)

	// 正确方式
	go func() {
		wg.Wait()
		close(out)
	}()

	return out
}

func main() {
	in := producer(10000000)

	// FAN-OUT
	c1 := square(in)
	c2 := square(in)
	c3 := square(in)

	// consumer
	for _ = range merge(c1, c2, c3) {
	}
}
```

结果，可以跑多次，结果近似：

```bash
➜  awesome git:(master) ✗ time go run hi-simple.go
go run hi-simple.go  9.96s user 5.93s system 168% cpu 9.424 total
➜  awesome git:(master) ✗ time go run hi-fan.go
go run hi-fan.go  23.35s user 11.51s system 297% cpu 11.737 total
```

从这个结果可以看到 2 点：

- 扇形模式可以提高 CPU 利用率。
- 扇形模式不一定能提升效率，降低程序运行时间。

### 优化扇形模式

既然扇形模式不一定能提高性能，如何优化？

**不同的场景优化不同，要依具体的情况，解决程序的瓶颈。**

当前程序的瓶颈在扇入，square 函数很快就完成，merge 函数它把 3 个数据写入到 1 个通道的时候出现了瓶颈，**适当使用带缓冲通道可以提高程序性能**，[再修改下代码](https://github.com/Shitaibin/golang_pipeline_step_by_step/blob/optimize_fan_model/hi_fan_buffered.go)

- `merge()`中的`out`修改为：

```go
package main

import (
	"sync"
	"time"
)

func producer(n int) <-chan int {
	out := make(chan int)
	go func() {
		defer close(out)
		for i := 0; i < n; i++ {
			out <- i
		}
	}()
	return out
}

func square(inCh <-chan int) <-chan int {
	out := make(chan int)
	go func() {
		defer close(out)
		for n := range inCh {
			out <- n * n
		}
	}()

	return out
}

func merge(cs ...<-chan int) <-chan int {
	out := make(chan int, 100)

	var wg sync.WaitGroup

	collect := func(in <-chan int) {
		defer wg.Done()
		for n := range in {
			out <- n
		}
	}

	wg.Add(len(cs))
	// FAN-IN
	for _, c := range cs {
		go collect(c)
	}

	// 错误方式：直接等待是bug，死锁，因为merge写了out，main却没有读
	// wg.Wait()
	// close(out)

	// 正确方式
	go func() {
		wg.Wait()
		close(out)
	}()

	return out
}

func main() {
	in := producer(10000000)

	// FAN-OUT
	c1 := square(in)
	c2 := square(in)
	c3 := square(in)

	// consumer
	for _ = range merge(c1, c2, c3) {
	}
}
```

结果：

```bash
➜  awesome git:(master) ✗ time go run hi_fan-buffer.go
go run hi-fan-buffer.go  19.85s user 8.19s system 323% cpu 8.658 total
```

使用带缓存通道后，程序的性能有了较大提升，CPU 利用率提高到 323%，提升了 8%，运行时间从 11.7 降低到 8.6，降低了 26%。

## 参考

+ [https://gist.github.com/Shitaibin/9593a18989b6c81bb3aae5ccdf9b6470](https://gist.github.com/Shitaibin/9593a18989b6c81bb3aae5ccdf9b6470)
+ [Go并发模型：轻松入门流水线模型](https://segmentfault.com/a/1190000017142506?_ea=5178632)




