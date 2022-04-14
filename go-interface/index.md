# Go interface


[//]: # (author： xiaobinqt)

[//]: # (email： xiaobinqt@163.com)

[//]: # (https://xiaobinqt.github.io)

[//]: # (https://www.xiaobinqt.cn)

## 定义

+ interface 可以表示任意一种类型
+ interface 是接口的方法集合，只要实现了接口中的所有方法，那么就认为实现了这个接口

## 用途

### 实现多态

```go
package main

import (
	"fmt"
)

type animal interface {
	Say() string
	Color() string
}

type Cat struct{}

func (c Cat) Say() string {
	return "i am a cat"
}

func (c Cat) Color() string {
	return "i am black"
}

type Dog struct{}

func (d Dog) Say() string {
	return "i am a dog"
}

func (d Dog) Color() string {
	return "i am white"
}

type Car struct{}

func introduceSelf(input animal) {
	fmt.Println(input.Say() + " and " + input.Color())
}

func main() {
	c := Cat{}
	d := Dog{}
	introduceSelf(c)
	introduceSelf(d)

	// car 没有实现 animal 接口
	//car := Car{}
	//introduceSelf(car)
}

```

### 隐藏具体实现

以 go 中的 `context` 包为例，`context.Context()` 是一个接口：

```go
// A Context carries a deadline, a cancellation signal, and other values across
// API boundaries.
//
// Context's methods may be called by multiple goroutines simultaneously.
type Context interface {
// Deadline returns the time when work done on behalf of this context
// should be canceled. Deadline returns ok==false when no deadline is
// set. Successive calls to Deadline return the same results.
Deadline() (deadline time.Time, ok bool)

// Done returns a channel that's closed when work done on behalf of this
// context should be canceled. Done may return nil if this context can
// never be canceled. Successive calls to Done return the same value.
// The close of the Done channel may happen asynchronously,
// after the cancel function returns.
//
// WithCancel arranges for Done to be closed when cancel is called;
// WithDeadline arranges for Done to be closed when the deadline
// expires; WithTimeout arranges for Done to be closed when the timeout
// elapses.
//
// Done is provided for use in select statements:
//
//  // Stream generates values with DoSomething and sends them to out
//  // until DoSomething returns an error or ctx.Done is closed.
//  func Stream(ctx context.Context, out chan<- Value) error {
//  	for {
//  		v, err := DoSomething(ctx)
//  		if err != nil {
//  			return err
//  		}
//  		select {
//  		case <-ctx.Done():
//  			return ctx.Err()
//  		case out <- v:
//  		}
//  	}
//  }
//
// See https://blog.golang.org/pipelines for more examples of how to use
// a Done channel for cancellation.
Done() <-chan struct{}

// If Done is not yet closed, Err returns nil.
// If Done is closed, Err returns a non-nil error explaining why:
// Canceled if the context was canceled
// or DeadlineExceeded if the context's deadline passed.
// After Err returns a non-nil error, successive calls to Err return the same error.
Err() error

// Value returns the value associated with this context for key, or nil
// if no value is associated with key. Successive calls to Value with
// the same key returns the same result.
//
// Use context values only for request-scoped data that transits
// processes and API boundaries, not for passing optional parameters to
// functions.
//
// A key identifies a specific value in a Context. Functions that wish
// to store values in Context typically allocate a key in a global
// variable then use that key as the argument to context.WithValue and
// Context.Value. A key can be any type that supports equality;
// packages should define keys as an unexported type to avoid
// collisions.
//
// Packages that define a Context key should provide type-safe accessors
// for the values stored using that key:
//
// 	// Package user defines a User type that's stored in Contexts.
// 	package user
//
// 	import "context"
//
// 	// User is the type of value stored in the Contexts.
// 	type User struct {...}
//
// 	// key is an unexported type for keys defined in this package.
// 	// This prevents collisions with keys defined in other packages.
// 	type key int
//
// 	// userKey is the key for user.User values in Contexts. It is
// 	// unexported; clients use user.NewContext and user.FromContext
// 	// instead of using this key directly.
// 	var userKey key
//
// 	// NewContext returns a new Context that carries value u.
// 	func NewContext(ctx context.Context, u *User) context.Context {
// 		return context.WithValue(ctx, userKey, u)
// 	}
//
// 	// FromContext returns the User value stored in ctx, if any.
// 	func FromContext(ctx context.Context) (*User, bool) {
// 		u, ok := ctx.Value(userKey).(*User)
// 		return u, ok
// 	}
Value(key interface{}) interface{}
}
```

`WithCancel` 和 `WithValue` 返回的第一个参数都是 context，但是各自返回的 `Context` 结构体又不是一样的：

`WithCancel` 返回结构体为 `cancelCtx`

`WithValue` 返回的结构体为 `valueCtx`

这样的话尽管返回的都是 `context`，但是具体实现却不一样，实现了功能的多样化。

### 解耦依赖

下面的示例:point_down:，如果缓存从 Redis 换成了 MemoryCache, 我们只需要修改 MemoryCache 的实现和初始化的地方，而不需要修改 Redis 的实现，这样就解耦了依赖，更加灵活。

```go
package main

type Cache interface {
	GetValue(key string) string
}

// 假设这是redis客户端
type Redis struct {
}

func (r Redis) GetValue(key string) string {
	panic("not implement")
}

// 假设这是自定义的一个缓存器
type MemoryCache struct {
}

func (m MemoryCache) GetValue(key string) string {
	panic("not implement")
}

// 通过接口实现：检查用户是否有权限的功能
func AuthExpire(token string, cache Cache) bool {
	res := cache.GetValue(token)
	if res == "" {
		return false
	} else {
		// 正常处理
		return true
	}
}

func main() {
	token := "test"

	cache := Redis{} //	cache := MemoryCache{},修改这一句即可
	AuthExpire(token, cache)
}

```

## FAQ

### var _ Interface = (*Type)(nil)

```shell
var _ Person = (*Student)(nil)
```

以上:point_up:的语句：将空值 `nil` 转换为 `*Student` 类型，再转换为 `Person` 接口，如果转换失败，说明 `Student` 并没有实现 `Person` 接口的所有方法。

这是**确保接口被实现**常用的方式。即利用强制类型转换，确保 struct Student 实现了接口 Person。这样 IDE 和编译期间就可以检查，而不是等到使用的时候。

### 实例、接口相互转换

实例可以强制类型转换为接口，接口也可以强制类型转换为实例。

```shell
package main

import "fmt"

type Student struct {
	name string
	age  int
}

type Person interface {
	getName() string
}

func (stu *Student) getName() string {
	return stu.name
}

func (stu *Student) getAge() int {
	return stu.age
}

func main() {
	var s *Student = &Student{
		name: "narcissus",
		age:  20,
	}
	var p Person = &Student{
		name: "Tom",
		age:  18,
	}

	stu := p.(*Student) // 接口转为实例
	fmt.Println(stu.getName(), "---", stu.getAge())

	var pp Person = (*Student)(s) // 实例转为接口
	// var _ Person = s           // 实例转为接口
	fmt.Println(pp.getName()) // 这里不能调用 pp.getAge() 因为 Person 接口中没有 getAge() 方法
}

```

通过运行后的打印结果:point_down:可知，结果复合预期。

![运行打印](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220414/a5a29410ab9b42d1a3ce7d18bbe83263.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '运行打印')

### 接口是否实现了某个接口

[http/server.go](https://github.com/golang/go/blob/d2552037426fe5a190c74172562d897d921fe311/src/net/http/server.go#L3047)
中有这样的判断语句：

```shell
		rw, err := l.Accept()
		if err != nil {
			select {
			case <-srv.getDoneChan():
				return ErrServerClosed
			default:
			}
			if ne, ok := err.(net.Error); ok && ne.Temporary() {
				if tempDelay == 0 {
					tempDelay = 5 * time.Millisecond
				} else {
					tempDelay *= 2
				}
				if max := 1 * time.Second; tempDelay > max {
					tempDelay = max
				}
				srv.logf("http: Accept error: %v; retrying in %v", err, tempDelay)
				time.Sleep(tempDelay)
				continue
			}
			return err
		}
```

`ne, ok := err.(net.Error)` 就是判断 `err` 变量是不是 `err.Error` 接口类型：

```
// An Error represents a network error.
type Error interface {
	error
	Timeout() bool   // Is the error a timeout?
	Temporary() bool // Is the error temporary?
}
```

以下示例自定了一个 `MyError` 接口验证以上推断：

```go
package main

import "fmt"

type MyError interface {
	Msg() string
}

type myErrorStruct struct {
	errMsg string
}

func (e *myErrorStruct) Msg() string {
	return e.errMsg
}

func myNew(msg string) MyError {
	return &myErrorStruct{errMsg: msg}
}

func main() {
	err1 := fmt.Errorf("error")
	e1, ok1 := err1.(MyError)
	fmt.Println("e1 = ", e1, "ok1 = ", ok1)

	err2 := myNew("我是一个错误")
	e2, ok2 := err2.(MyError)
	fmt.Printf("e2 = %#v ,,ok2: %t", e2, ok2)

}

```

从 :point_down: 运行打印结果来看，符合预期。

![运行结果](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220414/cb78ee48a0624ea28fbcbb350216e41a.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15)

## 参考

+ [Consider adding "var _ Interface = (*Type)(nil)" to the list of recommendations](https://github.com/uber-go/guide/issues/25)
+ [类似var _ PeerPicker = (*HTTPPool)(nil)这种设计目的是什么](https://github.com/geektutu/7days-golang/issues/10)


