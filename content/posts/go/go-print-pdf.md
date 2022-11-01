---
title: "Go 利用 chromedp 生成 pdf"
subtitle: ""

init_date: "2022-04-16T00:39:00+08:00"

date: 2021-05-11

lastmod: 2022-04-16

draft: false

author: "xiaobinqt"
description: "xiaobinqt,golang 打印pdf,go 打印 pdf,chromedp 使用"

featuredImage: ""

featuredImagePreview: "https://cdn.xiaobinqt.cn/xiaobinqt.io/20220823/a229b28988f94958a2293925a53e7f7b.png"

reproduce: false

tags: ["golang","pdf"]
categories: ["golang"]
lightgallery: true

toc:
    auto: false

math:
    enable: true
---

<!-- author： xiaobinqt -->
<!-- email： xiaobinqt@163.com -->
<!-- https://xiaobinqt.github.io -->
<!-- https://www.xiaobinqt.cn -->

## chromedp

Package [chromedp](https://github.com/chromedp/chromedp) is a faster, simpler way to drive browsers supporting
the Chrome DevTools Protocol in Go without external dependencies.

可以查看官方的[示例](https://github.com/chromedp/examples)。

以下示例用的版本为 `github.com/chromedp/chromedp v0.8.4`。

## 示例

### 打印在线页面

:point_down: 有时需要打印一个在线页面成 pdf，比如把`https://www.baidu.com/`这个页面打印成 pdf，如下

```go
package main

import (
	"bufio"
	"bytes"
	"context"
	"fmt"
	"net/http"

	"github.com/chromedp/cdproto/page"
	"github.com/chromedp/chromedp"
	"github.com/gin-gonic/gin"
	"github.com/pkg/errors"
)

func dp(c *gin.Context) {
	var (
		err error
		buf = make([]byte, 0)
	)

	ctx, cancel := chromedp.NewContext(context.Background())
	defer cancel()
	err = chromedp.Run(ctx, chromedp.Tasks{
		chromedp.Navigate("https://www.baidu.com/"),
		chromedp.ActionFunc(func(ctx context.Context) error {
			buf, _, err = page.PrintToPDF().
				WithPrintBackground(true).
				Do(ctx)
			return err
		}),
	})

	if err != nil {
		err = errors.Wrapf(err, "chromedp Run failed")
		c.JSON(http.StatusInternalServerError, gin.H{
			"msg": err.Error(),
		})
		return
	}

	buffer := &bytes.Buffer{}
	buffer.WriteString("\xEF\xBB\xBF") // 防止中文乱码
	writer := bufio.NewWriter(buffer)

	_, err = writer.Write(buf)
	if err != nil {
		err = errors.Wrapf(err, "bufio Write err")
		c.JSON(http.StatusInternalServerError, gin.H{
			"msg": err.Error(),
		})
		return
	}

	_ = writer.Flush()
	fileName := fmt.Sprintf("1111.pdf")

	c.Header("Content-Type", "text/pdf")
	c.Header("Content-Disposition", "attachment;filename="+fileName)

	_, _ = c.Writer.Write(buffer.Bytes())
	return
}

func main() {
	route := gin.New()
	route.GET("/dp", dp)

	route.Run(":8080")
}
```

### 打印本地文件

有时需要将一个本地的 html 文件渲染后，提供下载链接，下载成一个 pdf 格式的文件。

```go
package main

import (
	"bufio"
	"bytes"
	"context"
	"fmt"
	"html/template"
	"net/http"
	"net/http/httptest"
	"os"

	"github.com/chromedp/cdproto/page"
	"github.com/chromedp/chromedp"
	"github.com/gin-gonic/gin"
	"github.com/pkg/errors"
)

type Content struct {
	ChannelLogo     template.URL
	ProductLogo     template.URL
	Title           string
	Content         string
	UserName        string
	OrgName         string
	ChannelName     string
	Number          string
	Date            string
	BackgroundImage template.URL
}

func writeHTML(content Content) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "text/html")

		var (
			wd   string
			err  error
			tmpl *template.Template
		)

		wd, _ = os.Getwd()

		tmpl, err = template.ParseFiles(wd + "/tmp.html")
		if err != nil {
			err = errors.Wrapf(err, "template.ParseFiles err")
			_, _ = w.Write([]byte(err.Error()))
			return
		}

		buffer := &bytes.Buffer{}

		err = tmpl.Execute(buffer, content)
		if err != nil {
			err = errors.Wrapf(err, "tmpl.Execute err")
			_, _ = w.Write([]byte(err.Error()))
			return
		}

		_, _ = w.Write(buffer.Bytes())
	})
}

func dp(c *gin.Context) {
	var (
		err error
		buf = make([]byte, 0)
	)

	ctx, cancel := chromedp.NewContext(context.Background())
	defer cancel()

	mux := http.NewServeMux()
	mux.Handle("/pre", writeHTML(Content{
		ChannelLogo:     "",
		ProductLogo:     "",
		Title:           "我是title",
		Content:         "我是内容",
		UserName:        "1111",
		OrgName:         "2222",
		ChannelName:     "3333",
		Number:          "4444",
		Date:            "2006-01-02 15:04:05",
		BackgroundImage: "",
	}))
	ts := httptest.NewServer(mux)
	defer ts.Close()

	url := fmt.Sprintf("%s/pre", ts.URL)

	err = chromedp.Run(ctx, chromedp.Tasks{
		chromedp.Navigate(url),
		chromedp.WaitReady("body"),
		chromedp.ActionFunc(func(ctx context.Context) error {
			var err error
			buf, _, err = page.PrintToPDF().
				WithPrintBackground(true).
				WithPageRanges("1").
				Do(ctx)
			return err
		}),
	})

	if err != nil {
		err = errors.Wrapf(err, "chromedp Run failed")
		c.JSON(http.StatusInternalServerError, gin.H{
			"msg": err.Error(),
		})
		return
	}

	buffer := &bytes.Buffer{}
	buffer.WriteString("\xEF\xBB\xBF") // 防止中文乱码
	writer := bufio.NewWriter(buffer)

	_, err = writer.Write(buf)
	if err != nil {
		err = errors.Wrapf(err, "bufio Write err")
		c.JSON(http.StatusInternalServerError, gin.H{
			"msg": err.Error(),
		})
		return
	}

	_ = writer.Flush()
	fileName := fmt.Sprintf("1111.pdf")

	c.Header("Content-Type", "text/pdf")
	c.Header("Content-Disposition", "attachment;filename="+fileName)

	_, _ = c.Writer.Write(buffer.Bytes())
	return
}

func main() {
	route := gin.New()
	route.GET("/dp", dp)

	route.Run(":8080")
}

```

本地文件 tmp.html：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <style>
        .root {
            width: 210mm;
            height: 276mm;
            padding: 0;
            margin: 0 auto;
            background-color: white;
            /*background-image: url();*/
            /* background-size: 210mm 276mm; */
            position: relative;
            overflow: hidden;
        }

        .background-box {
            position: absolute;
            top: 0;
            left: 0;
            bottom: 0;
            right: 0;
            z-index: 0;
        }

        .background-box img {
            width: 210mm;
        }

        .container {
            position: absolute;
            top: 0;
            left: 0;
            bottom: 0;
            right: 0;
            z-index: 1;
            /*border: 1px solid #000;*/
        }

        .title {
            font-size: 38px;
            text-align: center;
            margin-top: 100px;
        }

        .content {
            margin-top: 50px;
            font-size: 22px;
            line-height: 2em;
            padding: 0 108px;
        }

        .content p {
            text-indent: 2em;
            white-space: normal;
            word-break: break-all;
        }

        p strong {
            font-weight: normal;
            text-indent: 0;
            padding: 2px 1em;
            border-bottom: 1px solid #000;
        }

        .logo-box {
            padding: 130px 100px 0 100px;
            display: flex;
            justify-content: space-between;
        }

        .logo-box img {
            max-width: 260px;
        }

        .signature {
            padding: 36px 100px 0 100px;
            font-size: 22px;
            display: flex;
            justify-content: space-between;
            text-align: center;
        }

        .signature p {
            line-height: 2em;
            width: 48%;
        }

        .footer {
            font-size: 14px;
            position: absolute;
            bottom: 36px;
            left: 100px;
            right: 100px;
            top: auto;
            line-height: 1.8em;
        }

        @media screen {
            .root {
                width: 210mm;
                height: 276mm;
                display: flex;
                flex-direction: column;
            }
        }

        @media print {
            .root {
                width: 210mm;
                height: 276mm;
                display: flex;
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
<div class="root">
    <div class="background-box">
        <img src="{{.BackgroundImage}}"
             alt="">
    </div>
    <div class="container">
        <div class="logo-box">
            <div><img
                    src="{{.ChannelLogo}}"
                    alt=""></div>
            <div><img
                    src="{{.ProductLogo}}"
                    alt=""></div>
        </div>
        <div class="title">{{.Title}}</div>
        <div class="content">
            {{.Content}}
        </div>
        <section class="signature">
            <p>{{.ChannelName}}<br/>{{.Date}}</p>
            <p>{{.OrgName}}<br/>{{.Date}}</p>
        </section>
        <section class="footer">
            <p>声明：</p>
            <p style="text-indent: 2em;">
                XXX不对{产品}升级引起的不兼容性负责，牛逼公司不对由XXX产品升级引起的不兼容性负责。此认证书仅适用于牛逼公司现有产品及XXX现有产品（如上所列）。</p>
            <p>证书编号：{{.Number}}</p>
        </section>
    </div>
</div>
</body>
</html>

```


