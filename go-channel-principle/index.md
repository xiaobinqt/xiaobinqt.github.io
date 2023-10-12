# Go channel 使用分析


<!-- author： xiaobinqt -->
<!-- email： xiaobinqt@163.com -->
<!-- https://xiaobinqt.github.io -->
<!-- https://www.xiaobinqt.cn -->

## 概念

Go 中的 channel 是一个队列，遵循先进先出的原则，负责协程之间的通信。Go 语言提倡不要通过共享内存来通信，而要通过通信来实现内存共享，CSP（Communicating Sequential Process）并发模型，就是通过 goroutine 和 channel 来实现的。

channel 常用的使用场景有：

+ 停止信号监听

+ 定时任务

+ 生产方和消费方解耦

+ 控制并发数

## 数据结构

通过 var 声明或者 make 函数创建的 channel 变量是一个存储在函数栈帧上的指针，占用 8 个字节，指向堆上的 hchan 结构体。源码包中 src/runtime/chan.go 定义了 hchan 的数据结构：

<div align="center"><img src="https://cdn.xiaobinqt.cn/xiaobinqt.io/20231011/6c71b30703d44077bd3df99eabb9b681.png" width=800  /></div>

hchan结构体：

```
type hchan struct {
	closed   uint32 // channel是否关闭的标志
	elemtype *_type // channel中的元素类型，

	// channel分为无缓冲和有缓冲两种。
	// 对于有缓冲的 channel 存储数据，使用了 ring buffer（环形缓冲区) 来缓存写入的数据，本质是循环数组
	// 为啥是循环数组？普通数组不行吗，普通数组容量固定更适合指定的空间，弹出元素时，普通数组需要全部都前移
	// 当下标超过数组容量后会回到第一个位置，所以需要有两个字段记录当前读和写的下标位置
	buf      unsafe.Pointer // 指向底层循环数组的指针（环形缓冲区）
	qcount   uint           // 循环数组中的元素数量
	dataqsiz uint           // 循环数组的长度
	elemsize uint16         // 元素的大小
	sendx    uint           // 下一次写下标的位置
	recvx    uint           // 下一次读下标的位置

	// 尝试读取 channel 或向 channel 写入数据而被阻塞的goroutine
	recvq waitq // 读等待队列
	sendq waitq // 写等待队列
	lock  mutex //互斥锁，保证读写 channel 时不存在并发竞争问题
}
```

等待队列：

双向链表，包含一个头结点和一个尾结点。每个节点是一个 sudog 结构体变量，记录哪个协程在等待，等待的是哪个 channel，等待发送/接收的数据在哪里。

```
type waitq struct {
	first *sudog
	last  *sudog
}

type sudog struct {
	g    *g
	next *sudog
	prev *sudog
	elem unsafe.Pointer
	c    *hchan
	// ...
}
```

### 创建

使用 make(chan T, cap) 来创建 channel，make 语法会在编译时，转换为 makechan64 和 makechan

```
func makechan64(t *chantype, size int64) *hchan {
	if int64(int(size)) != size {
		panic(plainError("makechan: size out of range"))
	}
	return makechan(t, int(size))
}
```

创建 channel 有两种，一种是带缓冲的 channel，一种是不带缓冲的 channel

```
// 带缓冲
ch := make(chan int, 3)

// 不带缓冲
ch := make(chan int)
```

创建时会做一些检查:

- 元素大小不能超过 64K

- 元素的对齐大小不能超过 maxAlign 也就是 8 字节

- 计算出来的内存是否超过限制

创建时的策略:

- 如果是无缓冲的 channel，会直接给 hchan 分配内存

- 如果是有缓冲的 channel，并且元素不包含指针，那么会为 hchan 和底层数组分配一段连续的地址

- 如果是有缓冲的 channel，并且元素包含指针，那么会为 hchan 和底层数组分别分配地址

### 发送

发送操作，编译时转换为 runtime.chansend 函数

```
func chansend(c *hchan, ep unsafe.Pointer, block bool, callerpc uintptr) bool
```

阻塞式：

调用 chansend 函数，并且 block=true

```
ch <- 10
```

非阻塞式：

调用 chansend 函数，并且 block=false

```
select {
    case ch <- 10:

      ...

    default:
 }
```

向 channel 中发送数据时大概分为两大块：检查和数据发送，数据发送流程如下：

- 如果 channel 的读等待队列存在接收者goroutine

    - 将数据**直接发送**给第一个等待的 goroutine，**唤醒接收的 goroutine**

- 如果 channel 的读等待队列不存在接收者 goroutine

    - 如果循环数组 buf 未满，那么将会把数据发送到循环数组buf的队尾

    - 如果循环数组 buf 已满，这个时候就会走阻塞发送的流程，将当前 goroutine 加入写等待队列，并**挂起等待唤醒**

### 接收

接收操作，编译时转换为 runtime.chanrecv 函数

```
func chanrecv(c *hchan, ep unsafe.Pointer, block bool) (selected, received bool)
```

阻塞式：

调用 chanrecv 函数，并且 block=true

```
<-ch

v := <-ch

v, ok := <-ch

// 当 channel 关闭时，for 循环会自动退出，无需主动监测 channel 是否关闭，可以防止读取已经关闭的 channel,造成读到数据为通道所存储的数据类型的零值

for i := range ch {
	fmt.Println(i)
}
```

非阻塞式：

调用 chanrecv 函数，并且 block=false

```
select {
    case <-ch:
    ...

    default
  }
```

向 channel 中接收数据时大概分为两大块，检查和数据发送，而数据接收流程如下：

- 如果 channel 的写等待队列存在发送者 goroutine

    - 如果是无缓冲 channel，**直接**从第一个发送者 goroutine 那里把数据拷贝给接收变量，**唤醒发送的 goroutine**

    - 如果是有缓冲 channel（已满），将循环数组buf的队首元素拷贝给接收变量，将第一个发送者 goroutine 的数据拷贝到 buf循 环数组队尾，**唤醒发送的 goroutine**

- 如果 channel 的写等待队列不存在发送者 goroutine

    - 如果循环数组 buf 非空，将循环数组 buf 的队首元素拷贝给接收变量

    - 如果循环数组 buf 为空，这个时候就会走阻塞接收的流程，将当前 goroutine 加入读等待队列，并**挂起等待唤醒**

**关闭**

关闭操作，调用 close 函数，编译时转换为 runtime.closechan 函数

```
close(ch)
```

```
func closechan(c *hchan)
```

**案例分析：**

```go
package main

import (
	"fmt"
	"time"
	"unsafe"
)

func main() {
	// ch 是长度为 4 的带缓冲的 channel
	//初始 hchan 结构体重的 buf 为空，sendx 和 recvx 均为 0
	ch := make(chan string, 4)
	fmt.Println(ch, unsafe.Sizeof(ch))
	go sendTask(ch)
	go receiveTask(ch)
	time.Sleep(1 * time.Second)
}

// G1 是发送者

// 当 G1 向 ch 里发送数据时，首先会对 buf 加锁，然后将 task 存储的数据 copy 到 buf 中，然后 sendx++，然后释放对 buf 的锁

func sendTask(ch chan string) {
	taskList := []string{"this", "is", "a", "demo"}
	for _, task := range taskList {
		ch <- task
		//发送任务到 channel
	}
}

// G2 是接收者
// 当 G2 消费 ch 的时候，会首先对 buf 加锁，然后将 buf 中的数据 copy 到 task 变量对应的内存里，然后 recvx++,并释放锁

func receiveTask(ch chan string) {
	for {
		task := <-ch
		//接收任务
		fmt.Println("received", task)
		//处理任务
	}
}

```

hchan 结构体的主要组成部分有四个：

- 用来保存 goroutine 之间传递数据的循环数组：buf

- 用来记录此循环数组当前发送或接收数据的下标值：sendx 和 recvx

- 用于保存向该 chan 发送和从该 chan 接收数据被阻塞的 goroutine 队列： sendq 和 recvq

- 保证 channel 写入和读取数据时线程安全的锁：lock

## 特点

channel 有 2 种类型：无缓冲、有缓冲

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20231012/bfb659b1a9aa4a05b86ef43ae0090a86.png '有无缓冲')

channel 有 3 种模式：写操作模式（单向通道）、读操作模式（单向通道）、读写操作模式（双向通道）

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20231012/77e1a773bb3c4b5cb64c2fea9ce00876.png '模式')

channel有 3 种状态：未初始化、正常、关闭

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20231012/307a5fbdc807419db471dd49cbe3f920.png '状态')

**注意点**：

1. 一个 channel不能多次关闭，会导致 panic

2. 如果多个 goroutine 都监听同一个 channel，那么 channel 上的数据都**可能随机被某一个 goroutine 取走进行消费**

3. 如果多个 goroutine 监听同一个 channel，如果这个 channel 被关闭，则所有 goroutine **都能收到退出信号**

### 线程安全

不同协程通过 channel 进行通信，本身的使用场景就是多线程，为了保证数据的一致性，必须实现线程安全。

channel 的底层实现中，hchan 结构体中采用 Mutex 锁来保证数据读写安全。在对循环数组 buf 中的数据进行入队和出队操作时，必须先获取互斥锁，才能操作 channel 数据。

### 控制并发顺序

多个 goroutine 并发执行时，每一个 goroutine 抢到处理器的时间点不一致，goroutine 的执行本身不能保证顺序。goroutine 并不能保证先执行。

可以使用 channel 进行通信通知，用 channel 去传递信息，从而控制并发执行顺序：

```go
package main

import (
	"fmt"
	"sync"
	"time"
)

var wg sync.WaitGroup

func main() {
	ch1 := make(chan struct{}, 1)
	ch2 := make(chan struct{}, 1)
	ch3 := make(chan struct{}, 1)
	ch1 <- struct{}{}

	wg.Add(3)

	start := time.Now().Unix()

	go myPrint("gorouine1", ch1, ch2)
	go myPrint("gorouine2", ch2, ch3)
	go myPrint("gorouine3", ch3, ch1)

	wg.Wait()

	end := time.Now().Unix()
	fmt.Printf("duration:%d\n", end-start)
}

func myPrint(gorouine string, inputchan chan struct{}, outchan chan struct{}) {
	// 模拟内部操作耗时
	time.Sleep(1 * time.Second)
	select {
	case <-inputchan:
		fmt.Printf("%s\n", gorouine)
		outchan <- struct{}{}
	}

	wg.Done()
}

```

输出：

```
gorouine1
gorouine2
gorouine3
duration:1
```

## 死锁问题

**死锁：**

- 单个协程永久阻塞

- 两个或两个以上的协程的执行过程中，由于竞争资源或由于彼此通信而造成的一种阻塞的现象。

**channel 死锁场景：**

- 非缓存 channel 只写不读

- 非缓存 channel 读在写后面

- 缓存 channel 写入超过缓冲区数量

- 空读

- 多个协程互相等待


1. 非缓存 channel 只写不读

```
func deadlock1() {
	ch := make(chan int)
	ch <- 3 //  这里会发生一直阻塞的情况，执行不到下面一句
}
```

2. 非缓存 channel 读在写后面

```
func deadlock2() {
	ch := make(chan int)
	ch <- 3 //  这里会发生一直阻塞的情况，执行不到下面一句
	num := <-ch
	fmt.Println("num=", num)
}

func deadlock2() {
	ch := make(chan int)
	ch <- 100 //  这里会发生一直阻塞的情况，执行不到下面一句

	go func() {
		num := <-ch
		fmt.Println("num=", num)
	}()

	time.Sleep(time.Second)
}
```

3. 缓存 channel 写入超过缓冲区数量

```
func deadlock3() {
	ch := make(chan int, 3)
	ch <- 3
	ch <- 4
	ch <- 5
	ch <- 6 //  这里会发生一直阻塞的情况
}
```

4. 空读

```
func deadlock4() {
	ch := make(chan int)
	// ch := make(chan int, 1)
	fmt.Println(<-ch) //  这里会发生一直阻塞的情况
}
```

5. **多个协程互相等待**

```
func deadlock5() {
	ch1 := make(chan int)
	ch2 := make(chan int)

	// 互相等对方造成死锁

	go func() {
		for {
			select {
			case num := <-ch1:
				fmt.Println("num=", num)
				ch2 <- 100
			}
		}
	}()

	for {
		select {
		case num := <-ch2:
			fmt.Println("num=", num)
			ch1 <- 300
		}
	}
}
```

## 参考

+ [golang——channel](https://blog.csdn.net/weixin_45627369/article/details/127193703)





