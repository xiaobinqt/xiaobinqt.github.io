# Go 使用原生 Swagger

<!-- author： xiaobinqt -->

<!-- email： xiaobinqt@163.com -->

<!-- https://xiaobinqt.github.io -->

<!-- https://www.xiaobinqt.cn -->

Swagger 是一个规范且完整的框架，用于生成、描述、调用和可视化 RESTful 风格的 Web 服务。

当通过 Swagger 进行正确定义，用户可以理解远程服务并使用最少实现逻辑与远程服务进行交互。

支持 API 自动生成同步的在线文档。使用 Swagger 后可以直接通过代码生成文档，不再需要自己手动编写接口文档了，对程序员来说非常友好，可以节约写文档的时间。

提供 Web 页面在线测试 API。光有文档还不够，Swagger 生成的文档还支持在线测试。参数和格式都定好了，直接在界面上输入参数对应的值即可在线测试接口。

## swag cli 安装

Swag 能将 Go 的注释转换为 Swagger 文档。

```shell
# 安装swag
go get github.com/swaggo/swag/cmd/swag
# 查看版本
swag -v
```

![swag cli](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220519/90cbf963f17a451187e3527877bd8172.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'swag cli')

## swagger-ui 库

从 [swagger-ui](https://github.com/swagger-api/swagger-ui)
库下载 [dist](https://github.com/swagger-api/swagger-ui/tree/master/dist)
文件夹到自己的项目中，并更名为 swagger（更名不是必须的）。

把 swagger 中的 swagger-initializer.js 文件中有个 url 参数，**全局替换** swagger 文件夹中的这个 url 参数值为 `./swagger.json`。

![swagger-initializer.js url](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220519/28a4221079dd478e926209292027748b.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'swagger-initializer.js url')

![替换所有](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220519/1fd26413ebe2426e8263e8cd7182526a.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '替换所有')

## swagger 文档

swagger 是以注释的方式描述的，然后使用 swag cli 生成的文档。

比如我有一个 main.go 文件，文件内容如下：

```go
package main

import (
	"embed"
	"net/http"

	"github.com/go-martini/martini"
)

//go:embed swagger
var embededFiles embed.FS

// @title 测试 API
// @version 4.0
// @description 测试 API V4.0
// @securityDefinitions.apiKey MyApiKey
// @in header
// @name Xiaobinqt-Api-Key
// @BasePath /
func main() {
	m := martini.Classic()
	m.Get("/swagger/**", http.FileServer(http.FS(embededFiles)).ServeHTTP)
	m.Post("/api/login", Login)
	m.Run()
}

type Req struct {
	Email    string `json:"email"` // 邮箱
	Password string `json:"password"`
}

// @Tags 用户管理
// @Summary 用户登录
// @Security MyApiKey
// @accept application/json
// @Produce application/json
// @Param data body Req true "email: 用户名，password: 密码"
// @Success 200 {object} EdgeInstanceList
// @Router /api/login [POST]
func Login(w http.ResponseWriter, r *http.Request) {
	w.Write([]byte("hello"))
}

type EdgeInstanceList struct {
	A string
	B string
}

```

使用 swag cli 生成 swagger 文档：

![生成 swagger 文档](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220519/41886c08ae484deaa904bec886cfa532.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '生成 swagger 文档')

访问 swagger 路由：

![访问 swagger 路由](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220519/5bdd5117ff644d37a9a895c781a6b5b0.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '访问 swagger 路由')

## 常见问题

### apiKey

有的 api 需要加上 header 头信息才能正确访问，这时可以添加注释信息：

```shell
// @securityDefinitions.apiKey MyApiKey
// @in header
// @name Xiaobinqt-Api-Key
```

`@in header` 设置，在请求 header 中，`@name Xiaobinqt-Api-Key` header 字段为`Xiaobinqt-Api-Key`，`@securityDefinitions.apiKey`
固定写法，`MyApiKey`在每个方法中的`@Security`注释信息值，如：

```shell
// @Tags 用户管理
// @Summary 用户登录
// @Security MyApiKey
// @accept application/json
// @Produce application/json
// @Param data body Req true "email: 用户名，password: 密码"
// @Success 200 {object} EdgeInstanceList
// @Router /api/login [POST]
func Login(w http.ResponseWriter, r *http.Request) {
	w.Write([]byte("hello"))
}
```

如果在 swagger 页面 Available authorizations 的值不为空，那么每次请求都会带着`Xiaobinqt-Api-Key`这个 header 头，值就是`Available authorizations`
填入的值。

![Available authorizations](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220519/17586935d9494b30b83b30be0e46f45a.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'Available authorizations')

![Execute](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220519/125010439aed41258b007ab94bba2309.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'Execute')

### paramType

具体可以参看：[https://swagger.io/docs/specification/describing-parameters/](https://swagger.io/docs/specification/describing-parameters/)

+ body

```shell

type Req struct {
	Email    string `json:"email"` // 邮箱
	Password string `json:"password"`
}

// @Param data body Req true "email: 用户名，password: 密码"
```

+ path

```shell
// @Param  user_id path string true "用户ID"
```

+ query

```shell
// @Param  search query string false "搜索内容"
```

完整注释如下：

```shell
// @Tags 用户管理
// @Summary 用户登录
// @Security MyApiKey
// @accept application/json
// @Produce application/json
// @Param  user_id path string true "用户ID"
// @Param  search query string false "搜索内容"
// @Param data body Req true "email: 用户名，password: 密码"
// @Success 200 {object} EdgeInstanceList
// @Router /api/login/{user_id} [POST]
func Login(w http.ResponseWriter, r *http.Request) {
	w.Write([]byte("hello"))
}
```

![效果_01](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220519/e46042ea6a5e4ce8bd4c85ec34223d9f.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '效果_01')

![效果_02](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220519/c068d1585a49494992af4e7993a5a4f8.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '效果_02')

## 参考

+ [:point_up:文章示例源码](https://github.com/xiaobinqt/go.src/tree/master/dev/martini-swagger)
+ [swagger官方文档](https://swagger.io/docs/)
+ [https://github.com/swaggo/swag/blob/master/README_zh-CN.md](https://github.com/swaggo/swag/blob/master/README_zh-CN.md)
+ [https://www.jianshu.com/p/9313d0c5395d](https://www.jianshu.com/p/9313d0c5395d)
+ [Go embed 简明教程](https://colobu.com/2021/01/17/go-embed-tutorial/)
+ [https://zhuanlan.zhihu.com/p/351931501](https://zhuanlan.zhihu.com/p/351931501)

