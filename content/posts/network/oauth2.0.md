---
title: "OAuth2.0的理解与应用"

date: 2022-03-22T11:38:59+08:00

lastmod: 2022-03-22T11:38:59+08:00

draft: false

reproduce: true

author: "xiaobinqt"

description: ""
resources:

- name: ""
  src: ""

tags: ["web"]
categories: ["web"]
lightgallery: true

toc:
auto: false

math:
enable: true

---

## 什么是 OAuth2.0

**OAuth 的核心就是向第三方应用颁发令牌**，比如网站A想用Github的信息，那么对于Github来说，网站A就是第三方应用。

第三方应用申请令牌之前，都必须先到系统备案，比如申请Github的令牌，得先到[github备案登记](https://github.com/settings/applications/new)，
说明自己的身份，然后会拿到两个身份识别码：客户端 ID（client ID）和客户端密钥（client secret）。这是为了防止令牌被滥用，没有备案过的第三方应用，是不会拿到令牌的。

关于 OAuth2.0 是什么可以参考一下文章：

+ [OAuth 2.0 的一个简单解释](http://www.ruanyifeng.com/blog/2019/04/oauth_design.html)
+ [[简易图解]『 OAuth2.0』 『进阶』 授权模式总结](https://learnku.com/articles/20082)

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

| 字段 | 描述                                |
| ---- |-----------------------------------|
| Application name | 应用名称                              |
| Homepage URL | 首页URL，如`https://www.xiaobinqt.cn` |
| Authorization callback URL | 用户在 Github 登录成功后重定向回的 URL         |

注册成功后会生成 `Client ID` 和 `Client Secret`，这两个是用来请求令牌的。

![生成的Client信息](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220322/0c69a51ee31842b5979dce762e7dfede.png?imageView2/0/interlace/1/q/50|imageslim ' ')

### 通过 OAuth 获取用户信息

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

github 返回的token格式：

```json
{
  "access_token":"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",
  "token_type":"bearer",
  "scope":""
}
```

## 效果

![前端界面](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220322/bfadd1f3ff8e43409b50985f99bc23ea.png?imageView2/0/interlace/1/q/50|imageslim '前端界面')

![授权页面](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220322/9bd65bc08fdc4c899d4b0def1ecdc2da.png?imageView2/0/interlace/1/q/50|imageslim '授权页面')

![github返回的用户信息](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220322/895795367370407592caa400eba1b3a0.png?imageView2/0/interlace/1/q/50|imageslim 'github返回的用户信息')


## 源码

[源码地址](https://github.com/xiaobinqt/go.src/tree/master/dev/github.oauth)

## 参考

+ [Building OAuth Apps](https://docs.github.com/en/developers/apps/building-oauth-apps/creating-an-oauth-app)
+ [OAuth 2.0 的一个简单解释](http://www.ruanyifeng.com/blog/2019/04/oauth_design.html)
+ [Go语言实现第三方登录Github (通过OAuth2.0)](https://blog.csdn.net/qq_19018277/article/details/104935403)
+ [basics of authentication](https://docs.github.com/en/rest/guides/basics-of-authentication)
+ [[简易图解]『 OAuth2.0』 『进阶』 授权模式总结](https://learnku.com/articles/20082)

