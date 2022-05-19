# Go select 用法简述


<!-- author： xiaobinqt -->
<!-- email： xiaobinqt@163.com -->
<!-- https://xiaobinqt.github.io -->
<!-- https://www.xiaobinqt.cn -->

## select 功能

在多个通道上进行读或写操作，让函数可以处理多个事情，但 1 次只处理 1 个。select 有以下特征：

1. 每次执行 `select` ，都会只执行其中 1 个 `case` 或者执行 `default` 语句。
2. 当没有 `case` 或者 `default` 可以执行时，`select` 则阻塞，等待直到有 1 个 `case` 可以执行。
2. 当有多个 `case` 可以执行时，则随机选择 1 个 `case` 执行。
4. `case`后面跟的必须是读或者写通道的操作，否则编译出错。

由`select`和`case`组成，`default`不是必须的。

```go   
package main

import "fmt"

func main() {
	readCh := make(chan int, 1)
	writeCh := make(chan int, 1)

	y := 1
	select {
	case x := <-readCh:
		fmt.Printf("Read %d\n", x)
	case writeCh <- y:
		fmt.Printf("Write %d\n", y)
	default:
		fmt.Println("Do what you want")
	}
}

```

我们创建了`readCh`和`writeCh`2个通道：

1. `readCh`中没有数据，所以`case x := <-readCh`读不到数据，所以这个case不能执行。
2. `writeCh`是带缓冲区的通道，它里面是空的，可以写入1个数据，所以`case writeCh <- y`可以执行。
3. 有`case`可以执行，所以`default`不会执行。

这个测试的结果是

[//]: # (![执行结果]&#40;https://cdn.xiaobinqt.cn/xiaobinqt.io/20220519/9e225a005b3344429d5e1d0fa6d69983.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '执行结果'&#41;)

```shell
λ go run t.go
Write 1
```

## 用打豆豆实践 select

有句话说，“吃饭睡觉打豆豆”，这一句话里包含了3件事：

+ 妈妈喊你吃饭，你去吃饭。
+ 时间到了，要睡觉。
+ 没事做，打豆豆。

+ 在Golang里，select 就是干这个事的：到吃饭了去吃饭，该睡觉了就睡觉，没事干就打豆豆。

我们看看select怎么实现打豆豆：`eat()`函数会启动1个协程，该协程先睡几秒，事件不定，然后喊你吃饭，`main()`函数中的`sleep`是个定时器，每3秒喊你吃1次饭，`select`则处理3种情况：

1. 从`eatCh`中读到数据，代表有人喊我吃饭，我要吃饭了。
2. 从`sleep.C`中读到数据，代表闹钟时间到了，我要睡觉。
3. `default`是，没人喊我吃饭，也不到时间睡觉，我就打豆豆。

```go
package main

import (
	"fmt"
	"math/rand"
	"time"
)

func eat() chan string {
	out := make(chan string)
	go func() {
		rand.Seed(time.Now().UnixNano())
		time.Sleep(time.Duration(rand.Intn(5)) * time.Second)
		out <- "Mom call you eating"
		close(out)
	}()
	return out
}

func main() {
	eatCh := eat()
	sleep := time.NewTimer(time.Second * 3)
	select {
	case s := <-eatCh:
		fmt.Println(s)
	case <-sleep.C:
		fmt.Println("Time to sleep")
	default:
		fmt.Println("Beat DouDou")
	}
}

```

由于前2个case都要等待一会，所以都不能执行，所以执行`default`，运行结果一直是打豆豆：

```bash
λ go run t.go
Beat DouDou
```

现在不打豆豆了，把`default`的逻辑删掉，多运行几次，有时候会吃饭，有时候会睡觉，比如这样：

```bash
λ go run x.go
Mom call you eating
λ go run x.go
Time to sleep
λ go run x.go
Time to sleep
```

## `nil`通道永远阻塞

**当`case`上读一个通道时，如果这个通道是`nil`，则该`case`永远阻塞**。

这个功能有1个妙用，`select`通常处理的是多个通道，当某个读通道关闭了，但不想`select`再继续关注此`case`，继续处理其他`case`，把该通道设置为`nil`即可。

下面是一个合并程序等待两个输入通道都关闭后才退出的例子，就使用了这个特性。

```go
package main

import (
	"fmt"
	"time"
)

func main() {
	ch1 := gen(0, 1)
	ch2 := gen(5, 25)

	out := combine(ch1, ch2)

	for x := range out {
		fmt.Println(x)
	}

	time.Sleep(20 * time.Second)
}

func gen(min, max int) chan int {
	ch := make(chan int)

	go func() {
		defer close(ch)

		for i := min; i <= max; i++ {
			x := i
			ch <- x
		}
	}()

	return ch
}

// inCh1,inCh2 只读
func combine(inCh1, inCh2 <-chan int) <-chan int {
	// 输出通道
	out := make(chan int)

	// 启动协程合并数据
	go func() {
		defer close(out)

		for {
			select {
			case x, open := <-inCh1:
				fmt.Printf("inCh1: %v, %v\n", x, open)
				if !open {
					fmt.Println("inCh1 closed break")
					inCh1 = nil
					break // 这里 break 不会跳出 for 循环，只会跳出 select,下次再次进入 select 将会从 inCh2 中读取数据
				}
				out <- x
			case x, open := <-inCh2:
				if !open {
					fmt.Println("inCh2 closed break")
					inCh2 = nil
					break
				}
				out <- x
			}

			fmt.Println("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")

			// 当ch1和ch2都关闭时才退出
			if inCh1 == nil && inCh2 == nil {
				fmt.Printf("222222222 inCh1:%v, inCh2:%v, inCh1 is nil: %t ,inCh2 is nil: %t \n",
					inCh1, inCh2, inCh1 == nil, inCh2 == nil)
				break
			}
		}
	}()

	return out
}

```

## 如何跳出for-select

**`break`在`select`内的并不能跳出`for-select`循环**。

:point_down:下面的例子，`consume`函数从通道`inCh`不停读数据，期待在`inCh`关闭后退出`for-select`循环，但结果是永远没有退出。

```go
package main

import (
	"fmt"
	"time"
)

func main() {
	ch := make(chan int)
	go func(ch chan int) {
		defer close(ch)
		for i := 0; i < 5; i++ {
			ch <- i
			time.Sleep(1 * time.Second)
		}
	}(ch)

	consume(ch)
	time.Sleep(1 * time.Hour)
}

func consume(inCh <-chan int) {
	i := 0
	for {
		fmt.Printf("for: %d\n", i)
		select {
		case x, open := <-inCh:
			if !open {
				fmt.Println("closed................")
				time.Sleep(3 * time.Second)
				break
			}
			fmt.Printf("read: %d\n", x)
		}
		i++
	}

	fmt.Println("consume-routine exit")
}

```

运行结果：

```bash
λ go run t.go
for: 0
read: 0
for: 1
read: 1
for: 2
read: 2
for: 3
read: 3
for: 4
read: 4
for: 5
closed................
for: 6
closed................
... // never stop
```

既然`break`不能跳出`for-select`，那怎么办呢:cry:？以下是三种方式：

1. 在满足条件的`case`内，使用`return`，如果有结尾工作，尝试交给`defer`。
2. 在`select`外`for`内使用`break`挑出循环，如`combine`函数。
3. 使用`goto`。

## `select{}`永远阻塞

```go
package main

import (
	"fmt"
	"time"
)

func main() {
	ch := make(chan int)
	go func(ch chan int) {
		defer close(ch)
		var i = 0
		for {
			fmt.Printf("i: %d\n", i)
			ch <- time.Now().Second()
			time.Sleep(1 * time.Second)
			i++
		}
	}(ch)

	go func(ch <-chan int) {
		for x := range ch {
			fmt.Printf("read: %d\n", x)
		}
	}(ch)

	select {}
}

```

`select{}`的效果等价于创建了1个通道，直接从通道读数据:point_down:

```shell
ch := make(chan int)
<-ch
```

但是，这个写起来多麻烦，没`select{}`简洁。

永远阻塞能有什么用呢！？ 当你开发一个并发程序的时候，`main`函数千万不能在子协程干完活前退出啊，不然所有的协程都**被迫退出**了，还怎么提供服务呢？
比如，写了个Web服务程序，端口监听、后端处理等等都在子协程跑起来了，`main`函数这时候能退出吗？

## 参考

+ [https://github.com/Shitaibin/golang_step_by_step/tree/master/golang_select](https://github.com/Shitaibin/golang_step_by_step/tree/master/golang_select)





