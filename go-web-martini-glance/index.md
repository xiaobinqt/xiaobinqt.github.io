# Go Web 框架 martini 笔记


<!-- author： xiaobinqt -->
<!-- email： xiaobinqt@163.com -->
<!-- https://xiaobinqt.github.io -->
<!-- https://www.xiaobinqt.cn -->

之前在[CSDN](https://blog.csdn.net/xiaobinqt)写过一个关于 martini
的笔记[golang martini 包的简单使用](https://blog.csdn.net/xiaobinqt/article/details/115749581)
，最近读来感觉不是很清楚，而且也有一些错误，花了点时间重新整理了下那篇笔记。

## 中间件的使用

根据文档中间件的使用有 2 种方法，我总结为通过 `Handlers` 函数方法和非 `Handlers` 函数方法，其实主要区别就是 **`Handlers`
函数方法优先级更高，它将会替换掉之前的任何设置过的中间件，但是`group`组中的中间件还是会执行。**。

### 非 Handlers 方式的中间件

```go
package main

import (
	"github.com/go-martini/martini"
	"fmt"
)

func main() {
	m := martini.Classic()

	m.Use(func(c martini.Context) {
		fmt.Println("第 1 个中间件 before a request")
	})

	m.Use(func() {
		fmt.Println("第 2 个中间件 111111111111")
	})

	m.Use(func(c martini.Context) {
		fmt.Println("第 3 个中间件 group middleware")
	})

	m.Group("/api", func(r martini.Router) {
		r.Get("/test", func() string {
			return "...... return success ....."
		})
	}, func() {
		fmt.Println("第 4 个中间件 group middleware")
	})

	m.RunOnAddr(":8081")
}

```

:point_up:是一个例子，从请求后的打印结果可以看出是按着代码顺序执行的。

![执行结果](https://img-blog.csdnimg.cn/20210416101310431.png '执行结果')

### Handlers 方式的中间件

可以把上面代码稍微改下，如下：

```go
package main

import (
	"github.com/go-martini/martini"
	"fmt"
)

func main() {
	m := martini.Classic()

	m.Use(func(c martini.Context) {
		fmt.Println("第 1 个中间件 before a request")
	})

	m.Use(func() {
		fmt.Println("第 2 个中间件 111111111111")
	})

	m.Use(func(c martini.Context) {
		fmt.Println("第 3 个中间件 group middleware")
	})

	m.Handlers(
		func() {
			fmt.Println("其他中间件都失效，只有我执行了..")
		},
	)

	m.Group("/api", func(r martini.Router) {
		r.Get("/test", func() string {
			return "...... return success ....."
		})
	}, func() {
		fmt.Println("第 4 个中间件 group middleware")
	})

	m.RunOnAddr(":8081")
}

```

执行后打印结果如下:point_down:，说明只执行了 `Handlers` 函数中的中间件和 `group` 组中的中间件。

![示例结果](https://img-blog.csdnimg.cn/20210416101629300.png '示例结果')

## Next 函数的使用

`Context.Next()`是一个可选的函数用于中间件处理器暂时放弃执行直到其他的处理器都执行完毕. 这样就可以很好的处理在 http 请求完成后需要做的操作。

对于 Next 我觉得可以理解成遇到 `Next()` 后就**入栈**，先进后出。 以下我也是通过有没有 `Handlers` 函数中间件来举例。

### Next 在非 Handlers 中间件中使用

```go
package main

import (
	"github.com/go-martini/martini"
	"fmt"
)

func main() {
	m := martini.Classic()

	m.Use(func(c martini.Context) {
		fmt.Println("第 1 个中间件 before a request")
		c.Next()
		fmt.Println("第 6 个中间件 after a request") // 入栈等待处理
	})

	m.Use(func() {
		fmt.Println("第 2 个中间件 111111111111")
	})

	m.Use(func(c martini.Context) {
		fmt.Println("第 3 个中间件 group middleware")
		c.Next()
		fmt.Println("第 5 个中间件 group middleware") // 入栈等待处理
	})

	m.Group("/api", func(r martini.Router) {
		r.Get("/test", func() string {
			fmt.Println("......last 最后执行........")
			return "...... return success ....."
		})
	}, func() {
		fmt.Println("分组中的中间件 group middleware")
	})

	m.RunOnAddr(":8080")
}

```

执行后的打印结果如下：

![示例结果](https://img-blog.csdnimg.cn/20210416104629946.png '示例结果')

请注意第 5 和第 6 个中间件是最后执行的，是在 **http请求完成后** 执行的。

### Next 在 Handlers 中间件中使用

```go
package main

import (
	"github.com/go-martini/martini"
	"fmt"
)

func main() {
	m := martini.Classic()

	m.Handlers(
		func() {
			fmt.Println("第 1 次执行....")
		},
		func(c martini.Context) {
			c.Next()
			fmt.Println("http 请求完成后执行....")
		},
		func() {
			fmt.Println("第 2 次执行....")
		},
	)

	m.Group("/api", func(r martini.Router) {
		r.Get("/test", func() string {
			fmt.Println("......last........")
			return "...... return success ....."
		})
	}, func() {
		fmt.Println("组中的中间件 group middleware")
	})

	m.RunOnAddr(":8081")
}

```

执行后的打印结果如下：

![示例结果](https://img-blog.csdnimg.cn/20210416105157390.png '示例结果')

## 依赖注入和控制反转

正常情况下，对函数或方法的调用是调用方的主动直接行为，调用方清楚地知道被调的函数名是什么，参数有哪些类型，直接主动地调用；包括对象的初始化也是显式地直接初始化。所谓的“控制反转”就是将这种主动行为变为间接的行为，主调方不是直接调用函数或对象，而是借助框架代码进行间接的调用和初始化，这种行为被称为“控制反转”，控制反转可以解耦调用方和被调方。

一般情况下，使用库的程序是程序主动地调用库的功能，但使用框架的程序常常由框架驱动整个程序，在框架下写的业务代码是被框架驱动的，这种模式就是“控制反转”。

“依赖注入”是实现“控制反转”的一种方法，是通过注入的参数或实例的方式实现控制反转。

控制反转的价值在哪里？一句话就是“解耦”，可以让控制反转的框架代码读取配置，动态地构建对象。

控制反转是解决复杂问题的一种方法，特别是在 web 框架中为路由和中间件的灵活注入提供了很好的方法。

## 服务

服务即是被注入到处理器中的`参数`，你可以映射一个服务到`全局`或者`请求`的级别。

关于服务最强悍的地方之一就是它能够映射服务到接口。例如说，假设你想要覆盖`http.ResponseWriter`成为一个对象，那么你可以封装它并包含你自己的额外操作。

### 全局映射

```go
package main

import (
	"fmt"
	"net/http"

	"github.com/go-martini/martini"
)

func myHandle(w http.ResponseWriter, ttt int, s1, s2 string) {
	ret := fmt.Sprintf("Hello, World! %d,%s , %s", ttt, s1, s2)
	w.Write([]byte(ret))
}

func registerMyRouter(r martini.Router) {
	r.Group("/api", func(r martini.Router) {
		r.Get("/test", myHandle)
	}, func() {
		fmt.Println("组中的中间件 group middleware")
	})
}

func main() {
	m := martini.Classic()

	gv1 := "1111111"
	gv2 := "2222222"
	m.Map(gv1)
	m.Map(gv2)
	age := 23
	m.Map(age)

	registerMyRouter(m)

	m.RunOnAddr(":8083")
}

```

这是一个简单的全局映射的服务，`gv1`，`gv2`，`age` 这几个服务(参数) 将可以在所有的处理器中被使用到。我们的 `myHandle()` 处理器(方法) 就直接用了，且没有报错。执行后打印的结果如下：

![示例结果](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220603/5f3712dec1824fa399279589a14f8bff.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '示例结果')

:warning:这里有个点需要**注意**，同一个类型的服务，如果多次 map 映射，后面的值会把前面的**覆盖**，:point_up:上面的，`gv2`的值就把 `gv1`的值覆盖了。

### 请求级别的映射

```go
package main

import (
	"github.com/go-martini/martini"
	"fmt"
	"net/http"
	"time"
)

type ReqContext struct {
	ExString string
	Req      *http.Request
}

func do(reqCtx *ReqContext) string {
	return fmt.Sprintf(`handle return....%s, ex val= :%s `, reqCtx.Req.URL.Query().Encode(), reqCtx.ExString)
}

func myHandle(req *http.Request, c martini.Context) {
	reqC := &ReqContext{
		ExString: "1112323 " + time.Now().Format("2006-01-02 15:04:05"),
		Req:      req,
	}
	c.Map(reqC)
}

func myHandle2(reqCtx *ReqContext) string {
	return fmt.Sprintf(`handle return....%s, ex val= :%s `, reqCtx.Req.URL.Query().Encode(), reqCtx.ExString)
}

func myHandle3(req *http.Request) string {
	return fmt.Sprintf(`handle return....%s`, req.URL.Query().Encode())
}

func registerMyRouter(r martini.Router) {
	r.Group("/api", func(r martini.Router) {
		r.Get("/test", myHandle, do)
		r.Get("/test2", myHandle2)
		r.Get("/test3", myHandle3)
	}, func() {
		fmt.Println("组中的中间件 group middleware")
	})
}

func main() {
	m := martini.Classic()
	registerMyRouter(m)

	m.RunOnAddr(":8085")
}

```

执行后打印结果如下：

![执行结果](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220603/806cccbc956b4b30802b11a34167da4e.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '执行结果')

:heavy_check_mark:这是一个简单的请求级别的映射，我们对 `/api/test` 做了映射，所以在 `/api/test` 请求中 `ReqContext` 参数是全局可以用，这也就是 `do()`
方法中的参数 `do(reqCtx *ReqContext)` 中的来历。

:heavy_check_mark:在 `/api/test3` 中我们没有用任何其他的参数，上下文用的是`*http.Request`，所以可以正确执行请求。

:x:在 `/api/test2` 中我们用到了 `ReqContext` 参数，这是 `/api/test` 请求映射的，只能在 `/api/test` 中使用，这就是报错是原因。

### 映射值到接口

假设你想要覆盖`http.ResponseWriter`成为一个对象, 那么你可以封装它并包含你自己的额外操作。

我个人理解的就是一种**类型覆盖**。

```go
package main

import (
	"github.com/go-martini/martini"
	"fmt"
	"net/http"
	"time"
)

type ReqContext struct {
	Svr      interface{}
	ExString string
	Req      *http.Request
}

type ServiceGetXIImpl interface {
	GetXI()
}

type Tmp struct {
}

func (s *Tmp) GetXI() {
	fmt.Println("tmp GetXI()")
}

type Service struct {
	Name string
	Age  int
}

func (s *Service) printXX() {
	fmt.Println("我是 service printXX() 方法")
}

func (s *Service) GetXI() {
	fmt.Println("我是 Service 实现了 ServiceGetXIImpl 接口中的 GetXI() 方法")
}

func myHandle(reqCtx *ReqContext) string {
	fmt.Printf("最后 myHandle 中的 reqCtx.Svr 类型为 %T \n ", reqCtx.Svr)
	return fmt.Sprintf(`handle return....%s, ex val= :%s `, reqCtx.Req.URL.Query().Encode(), reqCtx.ExString)
}

func registerMyRouter(r martini.Router) {
	r.Group("/api", func(r martini.Router) {
		r.Get("/test", myHandle)
	}, func() {
		fmt.Println("组中的中间件 group middleware")
	})
}

func ExecMapTo(ctx *ReqContext) *ReqContext {
	ctx.Svr = &Service{}
	return ctx
}

func WrapMapTo(reqCtx *ReqContext, c martini.Context) {
	fmt.Printf("MapTo 前 Svr 类型为: %T \n", reqCtx.Svr)
	rw := ExecMapTo(reqCtx)
	c.MapTo(rw, (*ServiceGetXIImpl)(nil)) // 覆盖 reqCtx.Svr 的 Tmp 类型为 Service
	fmt.Printf("MapTo 后 Svr 类型为: %T \n", reqCtx.Svr)
}

func main() {
	m := martini.Classic()

	m.Use(func(req *http.Request, c martini.Context) {
		reqC := &ReqContext{
			Svr:      Tmp{},
			ExString: "1112323 " + time.Now().Format("2006-01-02 15:04:05"),
			Req:      req,
		}
		c.Map(reqC)
	})

	m.Use(func(reqCtx *ReqContext, c martini.Context) {
		WrapMapTo(reqCtx, c)
	})

	registerMyRouter(m)

	m.RunOnAddr(":8086")
}
```

这个例子主要是想把 ReqContext 中的 Svr 从 Tmp 类型替换为 Service 类型。
执行后的打印结果如下：

![执行结果](https://img-blog.csdnimg.cn/20210416145026148.png '执行结果')

## 参考

+ [https://github.com/go-martini/martini/blob/master/translations/README_zh_cn.md](https://github.com/go-martini/martini/blob/master/translations/README_zh_cn.md)
+ [inject库](https://blog.csdn.net/ARPOSPF/article/details/118652145)





