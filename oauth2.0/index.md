# OAuth2.0的理解与应用


## 什么是 OAuth2.0

**OAuth 的核心就是向第三方应用颁发令牌**，比如网站 A 想用 Github 的信息，那么对于 Github 来说，网站 A 就是第三方应用。

第三方应用申请令牌之前，都必须先到系统备案，比如申请 Github 的令牌，得先到[github备案登记](https://github.com/settings/applications/new)， 说明自己的身份，然后会拿到两个身份识别码：客户端 ID（client ID）和客户端密钥（client secret）。这是为了防止令牌被滥用，没有备案过的第三方应用，是不会拿到令牌的。

**令牌的请求和响应标准化之后就是 OAuth2.0**。

## 认证和授权的区别

认证是要输入帐号和密码来证明我是我。

授权是并非通过帐号和密码来把我的东西借给其他人。

这其中的关键就是，是否需要输入帐号密码。OAuth 不需要输入帐号和密码，要做的只是授权。

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20231007/57c69a8f1a854cd6ade04482fa7a3d29.png '认证和授权')

## 授权方式

OAuth 2.0 规定了四种获得令牌的流程。可以选择最适合自己的那一种，向第三方应用颁发令牌。下面就是这四种授权方式。

- 授权码（authorization-code）
- 隐藏式（implicit）
- 密码式（password）：
- 客户端凭证（client credentials）

不管哪一种授权方式，第三方应用申请令牌之前，都**必须先**到系统备案，说明自己的身份，然后会拿到两个身份识别码：客户端 ID（client ID）和客户端密钥（client secret）。这是为了防止令牌被滥用，没有备案过的第三方应用，是不会拿到令牌的。

### 授权码式

**授权码（authorization code）方式，指的是第三方应用先申请一个授权码，然后再用该码获取令牌。**

这种方式是最常用的流程，安全性也最高，它适用于那些有后端的 Web 应用。授权码通过前端传送，令牌则是储存在后端，而且所有与资源服务器的通信都在后端完成。这样的前后端分离，可以避免令牌泄漏。

第一步，A 网站提供一个链接，用户点击后就会跳转到 B 网站，授权用户数据给 A 网站使用。下面就是 A 网站跳转 B 网站的一个示意链接。

```
https://b.com/oauth/authorize?
  response_type=code&
  client_id=CLIENT_ID&
  redirect_uri=CALLBACK_URL&
  scope=read
```

上面 URL 中，`response_type`参数表示要求返回授权码（`code`），`client_id`参数让 B 知道是谁在请求，`redirect_uri`参数是 B 接受或拒绝请求后的跳转网址，`scope`参数表示要求的授权范围（这里是只读）。

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20231007/4d7a9455425044f59eb446c21a1fa41d.png '授权码方式')

第二步，用户跳转后，B 网站**会要求用户登录**，然后询问是否同意给予 A 网站授权。用户表示同意，这时 B 网站就会跳回`redirect_uri`参数指定的网址。跳转时，会传回一个授权码，就像下面这样：

```
https://a.com/callback?code=AUTHORIZATION_CODE
```

上面 URL 中，`code`参数就是授权码。

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20231007/22444456bfb44698b8fdb258b235257a.png '授权码')

第三步，A 网站拿到授权码以后，就可以在后端，向 B 网站请求令牌。

```
https://b.com/oauth/token?
 client_id=CLIENT_ID&
 client_secret=CLIENT_SECRET&
 grant_type=authorization_code&
 code=AUTHORIZATION_CODE&
 redirect_uri=CALLBACK_URL
```

上面 URL 中，`client_id` 参数和 `client_secret` 参数用来让 B 确认 A 的身份（`client_secret` 参数是保密的，因此只能在后端发请求），`grant_type` 参数的值是 `AUTHORIZATION_CODE`，表示采用的授权方式是授权码，`code` 参数是上一步拿到的授权码，`redirect_uri` 参数是令牌颁发后的回调网址。

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20231007/6dae999866de4b03a717457e8346a768.png '请求令牌')

第四步，B 网站收到请求以后，就会颁发令牌。具体做法是向 `redirect_uri` 指定的网址，发送一段 JSON 数据。

```
{
  "access_token":"ACCESS_TOKEN",
  "token_type":"bearer",
  "expires_in":2592000,
  "refresh_token":"REFRESH_TOKEN",
  "scope":"read",
  "uid":100101,
  "info":{...}
}
```

上面 JSON 数据中，`access_token` 字段就是令牌，A 网站在后端拿到了。

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20231007/08ebd9e1384c4cb498b81c1325730053.png '获取令牌')

### 隐藏式

有些 Web 应用是纯前端应用，没有后端。这时就不能用上面的方式了，必须将令牌储存在前端。允许直接向前端颁发令牌。这种方式没有授权码这个中间步骤，所以称为 “隐藏式”（implicit）。

第一步，A 网站提供一个链接，要求用户跳转到 B 网站，授权用户数据给 A 网站使用。

```
https://b.com/oauth/authorize?
  response_type=token&
  client_id=CLIENT_ID&
  redirect_uri=CALLBACK_URL&
  scope=read
```

上面 URL 中，`response_type`参数为`token`，表示要求直接返回令牌。

第二步，用户跳转到 B 网站，登录后同意给予 A 网站授权。这时，B 网站就会跳回 `redirect_uri` 参数指定的跳转网址，并且把令牌作为 URL 参数，传给 A 网站。

```
https://a.com/callback#token=ACCESS_TOKEN
```

上面 URL 中，`token`参数就是令牌，A 网站因此直接在前端拿到令牌。

注意，令牌的位置是 URL 锚点（fragment），而不是查询字符串（querystring），这是因为 OAuth 2.0 允许跳转网址是 HTTP 协议，因此存在 “中间人攻击” 的风险，而浏览器跳转时，锚点不会发到服务器，就减少了泄漏令牌的风险。

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20231008/fe54254647d442d287babeb7c1b6eb30.png '令牌')

这种方式把令牌直接传给前端，是很不安全的。因此，**只能用于一些安全要求不高的场景**，并且令牌的有效期必须非常短，通常就是会话期间（session）有效，浏览器关掉，令牌就失效了。

### 密码式

如果你**高度信任**某个应用也允许用户把用户名和密码，直接告诉该应用。该应用就使用你的密码，申请令牌，这种方式称为 “密码式”（password）。

第一步，A 网站要求用户提供 B 网站的用户名和密码。拿到以后，A 就直接向 B 请求令牌。

```
https://oauth.b.com/token?
  grant_type=password&
  username=USERNAME&
  password=PASSWORD&
  client_id=CLIENT_ID
```

上面 URL 中，`grant_type`参数是授权方式，这里的`password`表示 “密码式”，`username`和`password`是 B 的用户名和密码。

第二步，B 网站验证身份通过后，直接给出令牌。注意，这时不需要跳转，而是把令牌放在 JSON 数据里面，作为 HTTP 回应，A 因此拿到令牌。

这种方式需要用户给出自己的用户名/密码，显然风险很大，因此只适用于其他授权方式都无法采用的情况，而且必须是用户高度信任的应用。

### 凭证式

最后一种方式是凭证式（client credentials），适用于没有前端的命令行应用，即在命令行下请求令牌。

第一步，A 应用在命令行向 B 发出请求。

```
https://oauth.b.com/token?
  grant_type=client_credentials&
  client_id=CLIENT_ID&
  client_secret=CLIENT_SECRET
```

上面 URL 中，`grant_type`参数等于`client_credentials`表示采用凭证式，`client_id`和`client_secret`用来让 B 确认 A 的身份。

第二步，B 网站验证通过以后，直接返回令牌。

这种方式给出的令牌，是针对第三方应用的，而不是针对用户的，即有可能多个用户共享同一个令牌。

## 令牌的使用

A 网站拿到令牌以后，就可以向 B 网站的 API 请求数据了。

此时，每个发到 API 的请求，都必须带有令牌。具体做法是在请求的头信息，加上一个`Authorization`字段，令牌就放在这个字段里面。

 ```
 curl -H "Authorization: Bearer ACCESS_TOKEN" \
 "https://api.b.com"
 ```

上面命令中，`ACCESS_TOKEN`就是拿到的令牌。

## 更新令牌

令牌的有效期到了，如果让用户重新走一遍上面的流程，再申请一个新的令牌，很可能体验不好，而且也没有必要。OAuth 2.0 允许用户自动更新令牌。

具体方法是，B 网站颁发令牌的时候，一次性颁发两个令牌，一个用于获取数据，另一个用于获取新的令牌（refresh token 字段）。令牌到期前，用户使用 refresh token 发一个请求，去更新令牌。

```
https://b.com/oauth/token?
  grant_type=refresh_token&
  client_id=CLIENT_ID&
  client_secret=CLIENT_SECRET&
  refresh_token=REFRESH_TOKEN
```

上面 URL 中，`grant_type`参数为`refresh_token`表示要求更新令牌，`client_id`参数和`client_secret`参数用于确认身份，`refresh_token`参数就是用于更新令牌的令牌。

B 网站验证通过以后，就会颁发新的令牌。

## 第三方登录Github

所谓第三方登录，实质就是 OAuth 授权。用户想要登录 A 网站，A 网站让用户提供第三方网站的数据，证明自己的身份。获取第三方网站的身份数据，就需要 OAuth 授权。

比如，A 网站允许 GitHub 登录，背后就是下面的流程：

1. A 网站让用户跳转到 GitHub。
2. GitHub 要求用户登录，然后询问"A 网站要求获得 xx 权限，你是否同意？"
3. 用户同意，GitHub 就会重定向回 A 网站，同时发回一个授权码。
4. A 网站使用授权码，向 GitHub 请求令牌。
5. GitHub 返回令牌.
6. A 网站使用令牌，向 GitHub 请求用户数据。

### 注册 OAuth 应用

现在在 Github 上[注册](https://github.com/settings/applications/new)一个 OAuth 应用。

![github注册oauth应用](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220322/0db45fb787184c9e8321202da1758937.png?imageView2/0/interlace/1/q/50|imageslim ' ')

| 字段                         | 描述                                |
|----------------------------|-----------------------------------|
| Application name           | 应用名称                              |
| Homepage URL               | 首页URL，如`https://www.xiaobinqt.cn` |
| Authorization callback URL | 用户在 Github 登录成功后重定向回的 URL         |

注册成功后会生成 `Client ID` 和 `Client Secret`，这两个是用来请求令牌的。

![生成的Client信息](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220322/0c69a51ee31842b5979dce762e7dfede.png?imageView2/0/interlace/1/q/50|imageslim ' ')

### 获取用户信息

前端界面 oauth.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<a href="https://github.com/login/oauth/authorize?client_id={{.ClientId}}&redirect_uri={{.RedirectUrl}}">
    Github 第三方授权登录</a>
</body>
</html>

```

go 代码通过OAuth获取用户信息

```go
package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"html/template"
	"io/ioutil"
	"log"
	"net/http"
	"os"
)

var (
	clientSecret = flag.String("cs", "", "github oauth client secret")
	clientID     = flag.String("ci", "", "github oauth client id")
)

type Conf struct {
	ClientId     string
	ClientSecret string
	RedirectUrl  string
}

type Token struct {
	AccessToken string `json:"access_token"`
}

// 认证并获取用户信息
func OAuth(w http.ResponseWriter, r *http.Request) {
	var (
		err error
	)

	// 获取 code
	code := r.URL.Query().Get("code")

	// 通过 code, 获取 token
	var tokenAuthUrl = GetTokenAuthURL(code)
	var token *Token
	if token, err = GetToken(tokenAuthUrl); err != nil {
		fmt.Println(err)
		return
	}

	// 通过token，获取用户信息
	var userInfo map[string]interface{}
	if userInfo, err = GetUserInfo(token); err != nil {
		fmt.Println("获取用户信息失败，错误信息为:", err)
		return
	}

	//  将用户信息返回前端
	var userInfoBytes []byte
	if userInfoBytes, err = json.Marshal(userInfo); err != nil {
		fmt.Println("在将用户信息(map)转为用户信息([]byte)时发生错误，错误信息为:", err)
		return
	}
	w.Header().Set("Content-Type", "application/json")
	if _, err = w.Write(userInfoBytes); err != nil {
		fmt.Println("在将用户信息([]byte)返回前端时发生错误，错误信息为:", err)
		return
	}

}

// 通过code获取token认证url
func GetTokenAuthURL(code string) string {
	return fmt.Sprintf(
		"https://github.com/login/oauth/access_token?client_id=%s&client_secret=%s&code=%s",
		*clientID, *clientSecret, code,
	)
}

// 获取 token
func GetToken(url string) (*Token, error) {
	// 形成请求
	var req *http.Request
	var err error
	if req, err = http.NewRequest(http.MethodGet, url, nil); err != nil {
		return nil, err
	}
	req.Header.Set("accept", "application/json")

	// 发送请求并获得响应
	var (
		httpClient = http.Client{}
		res        *http.Response
		respBody   = make([]byte, 0)
		token      Token
	)

	if res, err = httpClient.Do(req); err != nil {
		return nil, err
	}

	respBody, err = ioutil.ReadAll(res.Body)
	if err != nil {
		return nil, err
	}

	log.Printf("token: %s", string(respBody))

	// 将响应体解析为 token，并返回
	err = json.Unmarshal(respBody, &token)
	if err != nil {
		return nil, err
	}
	return &token, nil
}

// 获取用户信息
func GetUserInfo(token *Token) (map[string]interface{}, error) {
	// 形成请求
	var userInfoUrl = "https://api.github.com/user" // github用户信息获取接口
	var req *http.Request
	var err error
	if req, err = http.NewRequest(http.MethodGet, userInfoUrl, nil); err != nil {
		return nil, err
	}
	req.Header.Set("accept", "application/json")
	req.Header.Set("Authorization", fmt.Sprintf("token %s", token.AccessToken))

	// 发送请求并获取响应
	var client = http.Client{}
	var res *http.Response
	if res, err = client.Do(req); err != nil {
		return nil, err
	}

	// 将响应的数据写入 userInfo 中，并返回
	var userInfo = make(map[string]interface{})
	if err = json.NewDecoder(res.Body).Decode(&userInfo); err != nil {
		return nil, err
	}
	return userInfo, nil
}

func Html(w http.ResponseWriter, r *http.Request) {
	// 解析指定文件生成模板对象
	var (
		temp *template.Template
		err  error
	)

	dir, _ := os.Getwd()

	if temp, err = template.ParseFiles(dir + "/oauth.html"); err != nil {
		fmt.Println("读取文件失败，错误信息为:", err)
		return
	}

	// 利用给定数据渲染模板(html页面)，并将结果写入w，返回给前端
	if err = temp.Execute(w, Conf{
		ClientId:     *clientID,
		ClientSecret: *clientSecret,
		RedirectUrl:  "http://127.0.0.1:9000/oauth/callback",
	}); err != nil {
		fmt.Println("读取渲染html页面失败，错误信息为:", err)
		return
	}
}

func UserInfo(w http.ResponseWriter, r *http.Request) {
	token := r.URL.Query().Get("token")
	log.Printf("UserInfo token: %s", token)
	var (
		err      error
		userInfo map[string]interface{}
	)
	if userInfo, err = GetUserInfo(&Token{AccessToken: token}); err != nil {
		fmt.Println("获取用户信息失败，错误信息为:", err)
		return
	}

	//  将用户信息返回前端
	var userInfoBytes []byte
	if userInfoBytes, err = json.Marshal(userInfo); err != nil {
		fmt.Println("在将用户信息(map)转为用户信息([]byte)时发生错误，错误信息为:", err)
		return
	}
	w.Header().Set("Content-Type", "application/json")
	if _, err = w.Write(userInfoBytes); err != nil {
		fmt.Println("在将用户信息([]byte)返回前端时发生错误，错误信息为:", err)
		return
	}
}

func main() {
	flag.Parse()
	log.Printf("clientSecrets: %s,clientID: %s", *clientSecret, *clientID)

	if *clientSecret == "" || *clientID == "" {
		log.Fatal("clientSecrets or clientID is required")
	}

	http.HandleFunc("/", Html)
	http.HandleFunc("/oauth/callback", OAuth)
	http.HandleFunc("/getUserInfo", UserInfo)
	if err := http.ListenAndServe(":9000", nil); err != nil {
		fmt.Println("监听失败，错误信息为:", err)
		return
	}

}


```

执行脚本：

```shell
 go run main.go -ci=$CLIENT_ID -cs=$CLIENT_SECRET
```

github 返回的token格式：

```json
{
  "access_token": "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",
  "token_type": "bearer",
  "scope": ""
}
```

### 效果

![前端界面](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220322/bfadd1f3ff8e43409b50985f99bc23ea.png?imageView2/0/interlace/1/q/50|imageslim '前端界面')

![授权页面](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220322/9bd65bc08fdc4c899d4b0def1ecdc2da.png?imageView2/0/interlace/1/q/50|imageslim '授权页面')

![github返回的用户信息](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220322/895795367370407592caa400eba1b3a0.png?imageView2/0/interlace/1/q/50|imageslim 'github返回的用户信息')

{{< admonition type=info title="源码" >}}
以上示例源码代码在：[https://github.com/xiaobinqt/go.src/tree/master/dev/github.oauth](https://github.com/xiaobinqt/go.src/tree/master/dev/github.oauth)
{{< /admonition >}}

## 参考

+ [Building OAuth Apps](https://docs.github.com/en/developers/apps/building-oauth-apps/creating-an-oauth-app)
+ [OAuth 2.0 的一个简单解释](http://www.ruanyifeng.com/blog/2019/04/oauth_design.html)
+ [Go语言实现第三方登录Github (通过OAuth2.0)](https://blog.csdn.net/qq_19018277/article/details/104935403)
+ [basics of authentication](https://docs.github.com/en/rest/guides/basics-of-authentication)
+ [[简易图解]『 OAuth2.0』 猴子都能懂的图解](https://learnku.com/articles/20031)
+ [[简易图解]『 OAuth2.0』 『进阶』 授权模式总结](https://learnku.com/articles/20082)

