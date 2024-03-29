---
title: "工作中问题总结"
subtitle: "my work is Ctrl+c and Ctrl+v"

init_date: "2022-12-15T13:43:14+08:00"

date: 2021-12-20

lastmod: 2022-12-15

draft: false

author: "xiaobinqt"
description: "xiaobinqt,"

featuredImage: ""

featuredImagePreview: "https://cdn.xiaobinqt.cn/xiaobinqt.io/20221215/e705681f5f744f9dab1b2a3f5a5c2b71.png"

reproduce: false

translate: false

tags: [ "面试" ]
categories: [ "开发者手册" ]
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

## 缘起

那天面试一家公司，面试的人问我工作内容，我说大部分时间就是写业务。好吧，我承认我是个菜鸡。然后他问，找个你工作中遇到的问题和解决的过程来谈一谈。我想了下说，大部分问题 google 下都能解决，没有什么特别复杂的，大部分问题前人都有解决方法，有些问题可能是之前没有接触过，所以花的时间比较长。

我当时心里有一万匹草泥马走过。现在我™就给你们这些大爷总结下，我这个菜鸡工作中遇到的问题，并且如何解决这些问题的，我谢谢你们:innocent::innocent:。

![CV工程师](https://cdn.xiaobinqt.cn/xiaobinqt.io/20221215/3c16037e9aac4bfe9dc0400fa2c3ee01.png 'CV工程师')

## go-bindata改成embed

公司有个老项目用的是 [go-bindata](https://github.com/go-bindata/go-bindata) 将前端打包到二进制里的。go-bindata 太老了，它的出现出现是由于 Go 之前版本官方不支持资源嵌入，但是 Go1.16 之后，官方推出了`embed`解决了资源嵌入问题，个人觉得至此之后，类似 go-bindata 社区维护的资源嵌入工具会慢慢退出历史舞台。

关于`embed`的使用可以参看

+ [Go embed 简明教程](https://colobu.com/2021/01/17/go-embed-tutorial/)
+ [Go 1.16新特性-embed包及其使用](https://zhuanlan.zhihu.com/p/351931501)

这是我的使用:point_down:

```go
package main

import (
	"crypto/md5"
	"embed"
	"fmt"
	"io/fs"
	"io/ioutil"
	"net/http"
	"strings"
	"time"

	"github.com/gin-gonic/gin"
)

var webFs embed.FS

func SetWebFs(fs embed.FS) {
	webFs = fs
}

func GetWebFs() embed.FS {
	return webFs
}

func GetWebFileSystem(p ...string) fs.FS {
	path := "dist"
	if len(p) != 0 && p[0] != "" {
		path = p[0]
	}
	fsys, _ := fs.Sub(GetWebFs(), path)
	return fsys
}

func ReturnMsg(msg string) gin.H {
	return gin.H{
		"msg": msg,
	}
}

func NoRouteBypass(ctx *gin.Context) {
	path := ctx.Request.URL.Path
	// flexcloud 前端
	_, err := GetWebFileSystem().Open(strings.TrimPrefix(path, "/"))
	if err != nil { // 显示首页
		f, err := GetWebFileSystem().Open("index.html")
		if err != nil {
			ctx.AbortWithStatusJSON(http.StatusNotFound, ReturnMsg(err.Error()))
			return
		}
		defer f.Close()
		content, err := ioutil.ReadAll(f)
		if err != nil {
			ctx.AbortWithStatusJSON(http.StatusNotFound, ReturnMsg(err.Error()))
			return
		}
		ctx.Data(http.StatusOK, "text/html", content)
		return
	}

	ctx.Header("Cache-Control", "max-age=31536000")
	etag := fmt.Sprintf("%x", md5.Sum([]byte(time.Now().String())))
	ctx.Header("ETag", etag)
	http.FileServer(http.FS(GetWebFileSystem())).ServeHTTP(ctx.Writer, ctx.Request)
}

```

## 热更新自动重置开发机

公司有个项目，中心控制器会控制所有用户的开发机，控制器可以给开发机下发指令，比如打开 ide 等。每个开发机上都安装了我们的 fca 软件，fca 会主动连接控制器。现在有个问题是，fca 软件前期更新的比较频繁，但是又不想每次更新都去告诉用户，让用户手动重置下开发机，以便更新下 fca 软件，如果每次都这样实在是太智障了:nauseated_face:。

我们找了个在 Go 中优雅热升级的软件 [tableflip](https://github.com/cloudflare/tableflip)，具体使用可以参考这篇文章 [Go 使用 tableflip 實現應用的優雅熱升級](https://www.readfog.com/a/1640457272592273408)。

我们起了一个服务，类似 `http://127.0.0.1:8011/fca/sha256sums` 可以获取到所有的 fca 版本，第一行就是最新的版本 `head -n 1 sha256sum.txt | awk '{print $1","$2}'`。每隔 5 分钟去获取下最新的 fca 信息与本地的运行的 fca 版本 `printf $(sha256sum /usr/bin/fca)` 进行对比，不一致则去下载新的 fca 惊醒替换并重启 `systemctl reload flexcloud-fca`。

但是这样操作其实也是有一些问题的，我们也都记录了。

![issue](https://cdn.xiaobinqt.cn/xiaobinqt.io/20221215/02303102490a4852acd49cdf959ad903.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 ' ')

## 模板更新后自动重置开发机

我们项目的客户开发机是通过模板 clone 的，但是当模板有更新，比如新内置了一些功能，对于基于旧模板的用户开发机来说是没有这些新功能的，所以就需要重置开发机。但是如果模板更新的比较频繁，每次通知用户手动重置开发机显的不够高端，所以我们做了一个自动重置开发机的功能。

每天凌晨`2:15 - 5:15`服务获取所有需要重置开发机的**不在线用户
**，自动重置开发机。超时 5:15 如果没有重置完，停止任务。对于那些在线用户我们会在`/api/profile`接口里添加一个字段，提示用户是否需要重置开发机。有个问题是，如果半夜自动更新出错，可能会导致第二天用户登录时，开发机在重置状态，因为登录时一旦开发机不可用，会自动去重置开发机，这种情况其实也可以接受。

我们的 fca 软件会每隔一分钟向中心控制器上报一下镜像 ID `/usr/bin/docker images --digests | sort | awk '{ if (NR>1) print $3 }' | xargs | sed 's/ //g'`，如果开发机的镜像 ID 跟模板的镜像 ID 不一致说明模板更新了，需要重置开发机。

```go
package agent

import (
	"fmt"
	"net/http"
	"os/exec"
	"strings"
	"time"

	"flexcloud/proxy/agent/controller"
	"github.com/pkg/errors"
	"github.com/sirupsen/logrus"
)

var (
	reportImageIDCmdStr = `/usr/bin/docker images --digests | sort | awk '{ if (NR>1) print $3 }' | xargs | sed 's/ //g'`
)

// 一分钟上报一个 imageID 给控制
func reportImageID() {
	var (
		err       error
		cmdOutput = make([]byte, 0)
	)

	for {
		cmdOutput, err = exec.Command("/bin/sh", "-c", reportImageIDCmdStr).CombinedOutput()
		if err != nil {
			err = errors.Wrapf(err, "reportImageID exec.Command err")
			logrus.Error(err.Error())
			time.Sleep(1 * time.Minute)
			continue
		}

		imageID := strings.ReplaceAll(string(cmdOutput), "\n", "")
		logrus.Debugf("reportImageID imageID: %s ", imageID)
		resp, err := controller.HTTPRequestWithJsonPayload(http.MethodPost,
			fmt.Sprintf("/edges/%s?image_id=%s", Edge_ID, imageID), nil, 10*time.Second)
		if err != nil {
			logrus.Errorf("Failed to report edge reportImageID info to controller: %s", err.Error())
			time.Sleep(1 * time.Minute)
			continue
		}

		if resp.StatusCode != http.StatusOK {
			logrus.Errorf("Failed to report edge reportImageID info to controller: %s", err.Error())
			time.Sleep(1 * time.Minute)
			continue
		}

		time.Sleep(1 * time.Minute)
	}
}

```

获取某个镜像的 sha256sum 的值，可以参考 [How to obtain docker image digest from tag](https://stackoverflow.com/questions/56178911/how-to-obtain-docker-image-digest-from-tag)

```shell
curl -s -L -H "Accept: application/vnd.docker.distribution.manifest.v2+json,application/vnd.docker.distribution.manifest.list.v2+json" -H "Authorization: Bearer $(curl -s "https://auth.docker.io/token?service=registry.docker.io&scope=repository:zsm1703/flexcloud:1.0-dep:pull" | jq -r .token)" https://index.docker.io/v2/zsm1703/flexcloud/manifests/1.0-dep | sha256sum
```

![sha256sum](https://cdn.xiaobinqt.cn/xiaobinqt.io/20221215/e60cf71214184c71ab219bdbb095fe52.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'sha256sum')

在更新模板时，我们会把 imageID 写入到一个文件中，有个文件服务类似`http://127.0.0.1:8012/SHA256SUMS` ，可以获取最新的模板 ID。

```shell
#!/bin/bash

readonly TARGET_ARCH="ARM"
readonly IMAGE_NAMESPACE="XXXXXXX"
readonly IMGAE_NAME_FLEXCLOUD="flexcloud"
readonly IMAGE_NAME_FLEXCLOUD_CODE="flexcloud-code"
readonly IMAGE_TAG_FLEXCLOUD="1.0"
readonly IMAGE_TAG_FLEXCLOUD_CODE="1.0"

main() {
  find ./ -maxdepth 1 -type f -executable -exec file {} \; | grep "$TARGET_ARCH" | awk '{print $1}' | sed 's/.$//' >/tmp/t1
  cat /tmp/t1 | xargs -I {} stat -c '%Y %N' {} | sort -r | awk '{print $2}' | sed s/\'//g >/tmp/t2
  cat /tmp/t2 | xargs -I {} sha256sum {} | sed 's/.\///' >SHA256SUMS
  digests1=$(get_digests "${IMAGE_NAMESPACE}" "${IMGAE_NAME_FLEXCLOUD}" "${IMAGE_TAG_FLEXCLOUD}")
  digests2=$(get_digests "${IMAGE_NAMESPACE}" "${IMAGE_NAME_FLEXCLOUD_CODE}" "${IMAGE_TAG_FLEXCLOUD_CODE}")
  sed -i "1 s/$/\t$digests1$digests2/" ./SHA256SUMS
  rm -f /tmp/t1 /tmp/t2
}

get_digests() {
  _tmp=$(curl -v -L -I \
    -H "Accept: application/vnd.docker.distribution.manifest.v2+json,application/vnd.docker.distribution.manifest.list.v2+json" \
    -H "Authorization: Bearer $(curl -s "https://auth.docker.io/token?service=registry.docker.io&scope=repository:$1/$2:pull" | jq -r .token)" \
    https://index.docker.io/v2/"$1"/"$2"/manifests/"$3" | tr -d '\r' | grep ^docker-content-digest | awk '{print $2}')
  echo "$_tmp"
}

main

```

## ide刷新token

项目中，客户的开发机可以打开在线 vscode 或是 nodered 进行编辑，但是在这 2 个新 tab 中没有 JS 去定时去刷新 token，当停在这 2 个页面操作一段时候后，token 可能会过期时，而此时是不会去主动刷新 token 的，这样会导致在 ide 中操作时间过长时，回到主站中，导致 token 失效回到登录页。

我们的做法是，在 proxy 反向代理时，重写首页请求的 response Body，在 Body 中注入一段 JS 代码，让它去实时刷新 token :point_down:

```
const JsScript = `

<script>

(function ($) {
    $('document').ready(function () {
        if (window.sessionStorage.getItem('token')) {
            setInterval(() => {
                if (window.localStorage.getItem("online") === "0") {
                    window.localStorage.setItem('token', '')
                    window.localStorage.setItem('refresh_token', '')
                    window.sessionStorage.setItem('token', '')
                    window.sessionStorage.setItem('refresh_token', '')
                    location.href = '/login'
                }

                if (window.sessionStorage.getItem('token') && (window.localStorage.getItem('expire_at') < (Math.round(new Date() / 1000) + 30))) {
                    $.ajax({
                        url: "/api/refreshToken", type: 'get', headers: {
                            'X-Token': window.localStorage.getItem('refresh_token'),
                        }, success: function (data) {
                            window.localStorage.setItem('token', data.token)
                            window.localStorage.setItem('refresh_token', data.refresh_token)
                            window.sessionStorage.setItem('token', data.token)
                            window.sessionStorage.setItem('refresh_token', data.refresh_token)
                            window.localStorage.setItem('expire_at', data.expire_at)
                            window.localStorage.setItem('refresh_expire_at', data.refresh_expire_at)
                            console.log("update token success to ", data.expire_at)
                        }, error: function (data) {
                            if (data.status !== 200) {
                                window.localStorage.setItem('token', '')
                                window.localStorage.setItem('refresh_token', '')
                                window.sessionStorage.setItem('token', '')
                                window.sessionStorage.setItem('refresh_token', '')
                                location.href = '/login'
                            }
                        }
                    })
                } else {
                    // console.log("expire_at", window.localStorage.getItem('expire_at'), "current_at", Math.round(new Date() / 1000))
                }
            }, 5000)

        } else {
            console.log('token empty', window.localStorage.getItem('token'), window.sessionStorage.getItem('token'))
            window.localStorage.setItem('token', '')
            window.localStorage.setItem('refresh_token', '')
            window.sessionStorage.setItem('token', '')
            window.sessionStorage.setItem('refresh_token', '')
            location.href = '/login'
        }

    })
})(jQuery)

</script>
`

var NodeRedJSScript = fmt.Sprintf(`
%s
</body>
`, JsScript)

var VsCodeScript = fmt.Sprintf(`
<script src="jquery/jquery-1.12.4.min.js"></script>

%s
</html>
`, JsScript)

```

在代理 node-red 是可以直接替换

```
cproxy := &httputil.ReverseProxy{
    Director: director,
    ModifyResponse: func(r *http.Response) (err error) {
        b, err := ioutil.ReadAll(r.Body)
        if err != nil {
            err = errors.Wrapf(err, "node red reverse proxy read body err")
            logrus.Error(err.Error())
            return err
        }

        body := string(b)
        body = strings.ReplaceAll(body, "</body>", NodeRedJSScript)
        buf := bytes.NewBufferString(body)
        r.Body = ioutil.NopCloser(buf)
        r.Header["Content-Length"] = []string{fmt.Sprint(buf.Len())}
        return nil
    },
}
```

vscode 是 gzip 过的，需要先解析下:point_down:

```
cproxy := &httputil.ReverseProxy{
		Director: director,
		ModifyResponse: func(r *http.Response) (err error) {
			upgrade := ctx.Request.Header.Get("Upgrade")
			if upgrade == "websocket" {
				return nil
			}

			bodyReader, err := gzip.NewReader(r.Body)
			if err != nil && err == io.EOF {
				logrus.Warnf("gzip.NewReader err:%s", err.Error())
				return nil
			}

			if err != nil && err != io.EOF {
				err = errors.Wrapf(err, "OpenVsCode gzip.NewReader err")
				logrus.Error(err.Error())
				return err
			}

			b, err := ioutil.ReadAll(bodyReader)
			if err != nil {
				err = errors.Wrapf(err, "OpenVsCode ioutil.ReadAll err")
				logrus.Error(err.Error())
				return err
			}

			body := string(b)
			body = strings.ReplaceAll(body, "</html>", VsCodeScript)

			var bx bytes.Buffer
			gz := gzip.NewWriter(&bx)
			gz.Write([]byte(body))
			gz.Close()
			buf := bytes.NewBuffer(bx.Bytes())
			r.Body = ioutil.NopCloser(buf)
			r.Header["Content-Length"] = []string{fmt.Sprint(buf.Len())}
			return nil
		},
	}
```

![效果图](https://cdn.xiaobinqt.cn/xiaobinqt.io/20221215/fa81da4d899247ed8004a1e776510f3c.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '效果图')

## 节点包预览功能

客户想要预览开发者上传到 npm 内部仓库里的节点包，前端没有线程的组件，我们就做成了一下处理。先把 npm 包下载到服务器，然后去遍历目录生成目录树，过滤掉特定后缀的文件和特别大的文件不读取，其他的文件内容读取 base64 格式返给前端，前端再反 base64 去展示。

根据文件夹路径，遍历生成目录树:point_down:

```go
package dir

import (
	"os"

	"github.com/pkg/errors"
	uuid "github.com/satori/go.uuid"
)

type Tree struct {
	Title    string `json:"title"`
	Children []Tree `json:"children"`
	ID       string `json:"id"`
}

func DirTreeJSON(dstPath string) (tree Tree, err error) {
	dstF, err := os.Open(dstPath)
	if err != nil {
		err = errors.Wrapf(err, "打开目录失败，目录：%s", dstPath)
		return tree, err
	}

	defer dstF.Close()
	fileInfo, err := dstF.Stat()
	if err != nil {
		err = errors.Wrapf(err, "DirTreeJSON dstF.stat err")
		return tree, err
	}

	if fileInfo.IsDir() == false { //如果是文件
		tree.Title = fileInfo.Name()
		tree.ID = uuid.NewV4().String()
		return tree, nil

	} else { //如果是文件夹
		dir, err := dstF.Readdir(0) //获取文件夹下各个文件或文件夹的fileInfo
		if err != nil {
			err = errors.Wrapf(err, "DirTreeJSON dstF.Readdir err")
			return tree, err
		}

		for _, fileInfo = range dir {
			x, err := DirTreeJSON(dstPath + "/" + fileInfo.Name())
			if err != nil {
				err = errors.Wrapf(err, "range DirTreeJSON err")
				return tree, err
			}
			x.Title = fileInfo.Name()
			tree.ID = uuid.NewV4().String()
			tree.Children = append(tree.Children, x)
		}

		return tree, nil
	}
}

```

想着可以通过 tgz 包获取各个文件的相对路径和文件大小（KB）:point_down:

```shell
tar tvf ResLoad_phsA-1.0.0.tgz | awk 'BEGIN {print "{"} {print " \""$6"\": "$3","} END {print "}"}' | sed -zr 's/,([^,]*$)/\1/'
```

将文件内容转成 base64

```shell
tar xf ResLoad_phsA-1.0.0.tgz package/ResLoad_phsA.html -O | base64

```

![结果展示](https://cdn.xiaobinqt.cn/xiaobinqt.io/20221215/7b4f2f9e70694f0d8bdc454a75164dbe.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '结果展示')

JS 中 base64 转换可以使用

```js
var base64Chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".split("")

function byteCode(codes) {
    var codeStr = '', binStr;
    for (var i = 0; i < codes.length; i += 2) {
        binStr = parseInt(codes.slice(i, i + 2), 16).toString(2);
        if (binStr.length < 8) {
            binStr = ('0000000' + binStr).slice(-8);
        }
        codeStr += binStr;
    }
    return codeStr
}

function base64encode(str) {
    var bb = byteCode(charToUtf8(str)), i, b6 = [], x, base64 = '', n;
    for (i = 0; i < bb.length; i += 6) {
        b6.push(bb.slice(i, i + 6));
    }
    for (x in b6) {
        if (Number(x) + 1 == b6.length) {
            b6[x] = (b6[x] + '00000').slice(0, 6)
        }
        base64 += base64Chars[parseInt(b6[x], 2)]
    }
    if (bb.length % 24 != 0) {
        n = (24 - bb.length % 24) / 8;
        if (n == 1) base64 += '=';
        else if (n == 2) base64 += '==';
    }
    return base64;
}

function base64decode(str) {
    var bc = str.replace(/=/g, '').split(""), y, z, c, b, bs = '';
    for (y in bc) {
        c = '';
        for (z in base64Chars) {
            if (bc[y] == base64Chars[z]) {
                c = z;
                break;
            }
        }
        if (c == '') return '编码有误';
        b = Number(c).toString(2);
        if (b.length < 6) {
            b = ('00000' + b).slice(-6)
        }
        bs += b
    }
    var j = Math.floor(bs.length / 8), i, ha = '', hb;
    for (i = 0; i < j; i++) {
        hb = parseInt(bs.slice(i * 8, i * 8 + 8), 2).toString(16);
        if (hb.length < 2) hb = ('00' + hb).slice(-2);
        ha += '%' + hb;
    }
    return decodeURIComponent(ha)
}

function charToUtf8(text) {
    var index = 0, output = '';
    while (index < text.length) {
        var character = text.charAt(index), charCode = text.charCodeAt(index);
        if (charCode >= 0xD800 && charCode <= 0xDBFF) {
            output += encodeURI(character + text.charAt(++index)).replace(/%/g, '');
        } else {
            if (charCode > 127)
                output += encodeURI(character).replace(/%/g, '');
            else {
                var asc = charCode.toString(16).toUpperCase();
                if (asc.length < 2) asc = '0' + asc;
                output += asc;
            }
        }
        ++index
    }
    return output;
}

export {base64encode, base64decode}
```

## 节点项目代码加密

客户想让 npm 节点项目的源码不可读，想在 npm 包公开的时候加密一下。所以是不是可以考虑节点项目，有一个`src`源代码目录，所有的源代码包括 js，python，c 代码都在 `src` 目录下。

对于 js 文件，现在也只有一个 js 可以文件，使用 [javascript-obfuscator](https://github.com/javascript-obfuscator/javascript-obfuscator) 方式混淆，把混淆后的文件放到项目根目录。

对于 python 文件，使用 compile 进行编译，把整个`src`目录下的 py 文件都编译成一个单个的 pyc 文件。把编译后的文件放到项目根目录。

```
python -m compileall -f ./src/python
```

对于 c 文件，把编译后的 build 文件夹也上传到 npm 仓库，这样在安装的时候，是不是就不用编译了。

这样，源码就跟编译后的文件彻底分开了，对于公开是不需要公开源文件的，可以直接把`src`目录删除。

## 数据传输加密

**前端**

```js
var CryptoJS = require("crypto-js");
//msg 需要被对称加密的明文
//key aes 对称加密的密钥  必须是16长度,为了和后端交互 key字符串必须是16进制字符串,否在给golang进行string -> []byte带来困难
function aseEncrypt(msg, key) {
    key = PaddingLeft(key, 16);//保证key的长度为16byte,进行'0'补位
    key = CryptoJS.enc.Utf8.parse(key);
    // 加密结果返回的是CipherParams object类型
    // key 和 iv 使用同一个值
    var encrypted = CryptoJS.AES.encrypt(msg, key, {
        iv: key, mode: CryptoJS.mode.CBC,// CBC算法
        padding: CryptoJS.pad.Pkcs7 //使用pkcs7 进行padding 后端需要注意
    });
    // ciphertext是密文,toString()内传编码格式,比如Base64,这里用了16进制
    // 如果密文要放在 url的参数中 建议进行 base64-url-encoding 和 hex encoding, 不建议使用base64 encoding
    return encrypted.ciphertext.toString(CryptoJS.enc.Hex)  //后端必须进行相反操作

}

// 确保key的长度,使用 0 字符来补位
// length 建议 16 24 32
function PaddingLeft(key, length) {
    let pkey = key.toString();
    let l = pkey.length;
    if (l < length) {
        pkey = new Array(length - l + 1).join('0') + pkey;
    } else if (l > length) {
        pkey = pkey.slice(length);
    }
    return pkey;
}


let xpass = aseEncrypt("先帝创业未半而中道崩殂，今天下三分，益州疲弊，此诚危急存亡之秋也。然侍卫之臣不懈于内，忠志之士忘身于外者，盖追先帝之殊遇，欲报之于陛下也。诚宜开张圣听，以光先帝遗德，恢弘志士之气，不宜妄自菲薄，引喻失义，以塞忠谏之路也。宫中府中，俱为一体，陟罚臧否，不宜异同。若有作奸犯科及为忠善者，宜付有司论其刑赏，以昭陛下平明之理，不宜偏私，使内外异法也。侍中、侍郎郭攸之、费祎、董允等，此皆良实，志虑忠纯，是以先帝简拔以遗陛下。愚以为宫中之事，事无大小，悉以咨之，然后施行，必能裨补阙漏，有所广益。将军向宠，性行淑均，晓畅军事，试用于昔日，先帝称之曰能，是以众议举宠为督。愚以为营中之事，悉以咨之，必能使行阵和睦，优劣得所。亲贤臣，远小人，此先汉所以兴隆也；亲小人，远贤臣，此后汉所以倾颓也。先帝在时，每与臣论此事，未尝不叹息痛恨于桓、灵也。侍中、尚书、长史、参军，此悉贞良死节之臣，愿陛下亲之信之，则汉室之隆，可计日而待也。臣本布衣，躬耕于南阳，苟全性命于乱世，不求闻达于诸侯。先帝不以臣卑鄙，猥自枉屈，三顾臣于草庐之中，咨臣以当世之事，由是感激，遂许先帝以驱驰。后值倾覆，受任于败军之际，奉命于危难之间，尔来二十有一年矣。先帝知臣谨慎，故临崩寄臣以大事也。受命以来，夙夜忧叹，恐托付不效，以伤先帝之明，故五月渡泸，深入不毛。今南方已定，兵甲已足，当奖率三军，北定中原，庶竭驽钝，攘除奸凶，兴复汉室，还于旧都。此臣所以报先帝而忠陛下之职分也。至于斟酌损益，进尽忠言，则攸之、祎、允之任也。愿陛下托臣以讨贼兴复之效，不效，则治臣之罪，以告先帝之灵。若无兴德之言，则责攸之、祎、允等之慢，以彰其咎；陛下亦宜自谋，以咨诹善道，察纳雅言，深追先帝遗诏，臣不胜受恩感激。今当远离，临表涕零，不知所言。先帝创业未半而中道崩殂，今天下三分，益州疲弊，此诚危急存亡之秋也。然侍卫之臣不懈于内，忠志之士忘身于外者，盖追先帝之殊遇，欲报之于陛下也。诚宜开张圣听，以光先帝遗德，恢弘志士之气，不宜妄自菲薄，引喻失义，以塞忠谏之路也。宫中府中，俱为一体，陟罚臧否，不宜异同。若有作奸犯科及为忠善者，宜付有司论其刑赏，以昭陛下平明之理，不宜偏私，使内外异法也。侍中、侍郎郭攸之、费祎、董允等，此皆良实，志虑忠纯，是以先帝简拔以遗陛下。愚以为宫中之事，事无大小，悉以咨之，然后施行，必能裨补阙漏，有所广益。将军向宠，性行淑均，晓畅军事，试用于昔日，先帝称之曰能，是以众议举宠为督。愚以为营中之事，悉以咨之，必能使行阵和睦，优劣得所。亲贤臣，远小人，此先汉所以兴隆也；亲小人，远贤臣，此后汉所以倾颓也。先帝在时，每与臣论此事，未尝不叹息痛恨于桓、灵也。侍中、尚书、长史、参军，此悉贞良死节之臣，愿陛下亲之信之，则汉室之隆，可计日而待也。臣本布衣，躬耕于南阳，苟全性命于乱世，不求闻达于诸侯。先帝不以臣卑鄙，猥自枉屈，三顾臣于草庐之中，咨臣以当世之事，由是感激，遂许先帝以驱驰。后值倾覆，受任于败军之际，奉命于危难之间，尔来二十有一年矣。先帝知臣谨慎，故临崩寄臣以大事也。受命以来，夙夜忧叹，恐托付不效，以伤先帝之明，故五月渡泸，深入不毛。今南方已定，兵甲已足，当奖率三军，北定中原，庶竭驽钝，攘除奸凶，兴复汉室，还于旧都。此臣所以报先帝而忠陛下之职分也。至于斟酌损益，进尽忠言，则攸之、祎、允之任也。愿陛下托臣以讨贼兴复之效，不效，则治臣之罪，以告先帝之灵。若无兴德之言，则责攸之、祎、允等之慢，以彰其咎；陛下亦宜自谋，以咨诹善道，察纳雅言，深追先帝遗诏，臣不胜受恩感激。今当远离，临表涕零，不知所言。先帝创业未半而中道崩殂，今天下三分，益州疲弊，此诚危急存亡之秋也。然侍卫之臣不懈于内，忠志之士忘身于外者，盖追先帝之殊遇，欲报之于陛下也。诚宜开张圣听，以光先帝遗德，恢弘志士之气，不宜妄自菲薄，引喻失义，以塞忠谏之路也。宫中府中，俱为一体，陟罚臧否，不宜异同。若有作奸犯科及为忠善者，宜付有司论其刑赏，以昭陛下平明之理，不宜偏私，使内外异法也。侍中、侍郎郭攸之、费祎、董允等，此皆良实，志虑忠纯，是以先帝简拔以遗陛下。愚以为宫中之事，事无大小，悉以咨之，然后施行，必能裨补阙漏，有所广益。将军向宠，性行淑均，晓畅军事，试用于昔日，先帝称之曰能，是以众议举宠为督。愚以为营中之事，悉以咨之，必能使行阵和睦，优劣得所。亲贤臣，远小人，此先汉所以兴隆也；亲小人，远贤臣，此后汉所以倾颓也。先帝在时，每与臣论此事，未尝不叹息痛恨于桓、灵也。侍中、尚书、长史、参军，此悉贞良死节之臣，愿陛下亲之信之，则汉室之隆，可计日而待也。臣本布衣，躬耕于南阳，苟全性命于乱世，不求闻达于诸侯。先帝不以臣卑鄙，猥自枉屈，三顾臣于草庐之中，咨臣以当世之事，由是感激，遂许先帝以驱驰。后值倾覆，受任于败军之际，奉命于危难之间，尔来二十有一年矣。先帝知臣谨慎，故临崩寄臣以大事也。受命以来，夙夜忧叹，恐托付不效，以伤先帝之明，故五月渡泸，深入不毛。今南方已定，兵甲已足，当奖率三军，北定中原，庶竭驽钝，攘除奸凶，兴复汉室，还于旧都。此臣所以报先帝而忠陛下之职分也。至于斟酌损益，进尽忠言，则攸之、祎、允之任也。愿陛下托臣以讨贼兴复之效，不效，则治臣之罪，以告先帝之灵。若无兴德之言，则责攸之、祎、允等之慢，以彰其咎；陛下亦宜自谋，以咨诹善道，察纳雅言，深追先帝遗诏，臣不胜受恩感激。今当远离，临表涕零，不知所言。先帝创业未半而中道崩殂，今天下三分，益州疲弊，此诚危急存亡之秋也。然侍卫之臣不懈于内，忠志之士忘身于外者，盖追先帝之殊遇，欲报之于陛下也。诚宜开张圣听，以光先帝遗德，恢弘志士之气，不宜妄自菲薄，引喻失义，以塞忠谏之路也。宫中府中，俱为一体，陟罚臧否，不宜异同。若有作奸犯科及为忠善者，宜付有司论其刑赏，以昭陛下平明之理，不宜偏私，使内外异法也。侍中、侍郎郭攸之、费祎、董允等，此皆良实，志虑忠纯，是以先帝简拔以遗陛下。愚以为宫中之事，事无大小，悉以咨之，然后施行，必能裨补阙漏，有所广益。将军向宠，性行淑均，晓畅军事，试用于昔日，先帝称之曰能，是以众议举宠为督。愚以为营中之事，悉以咨之，必能使行阵和睦，优劣得所。亲贤臣，远小人，此先汉所以兴隆也；亲小人，远贤臣，此后汉所以倾颓也。先帝在时，每与臣论此事，未尝不叹息痛恨于桓、灵也。侍中、尚书、长史、参军，此悉贞良死节之臣，愿陛下亲之信之，则汉室之隆，可计日而待也。臣本布衣，躬耕于南阳，苟全性命于乱世，不求闻达于诸侯。先帝不以臣卑鄙，猥自枉屈，三顾臣于草庐之中，咨臣以当世之事，由是感激，遂许先帝以驱驰。后值倾覆，受任于败军之际，奉命于危难之间，尔来二十有一年矣。先帝知臣谨慎，故临崩寄臣以大事也。受命以来，夙夜忧叹，恐托付不效，以伤先帝之明，故五月渡泸，深入不毛。今南方已定，兵甲已足，当奖率三军，北定中原，庶竭驽钝，攘除奸凶，兴复汉室，还于旧都。此臣所以报先帝而忠陛下之职分也。至于斟酌损益，进尽忠言，则攸之、祎、允之任也。愿陛下托臣以讨贼兴复之效，不效，则治臣之罪，以告先帝之灵。若无兴德之言，则责攸之、祎、允等之慢，以彰其咎；陛下亦宜自谋，以咨诹善道，察纳雅言，深追先帝遗诏，臣不胜受恩感激。今当远离，临表涕零，不知所言。先帝创业未半而中道崩殂，今天下三分，益州疲弊，此诚危急存亡之秋也。然侍卫之臣不懈于内，忠志之士忘身于外者，盖追先帝之殊遇，欲报之于陛下也。诚宜开张圣听，以光先帝遗德，恢弘志士之气，不宜妄自菲薄，引喻失义，以塞忠谏之路也。宫中府中，俱为一体，陟罚臧否，不宜异同。若有作奸犯科及为忠善者，宜付有司论其刑赏，以昭陛下平明之理，不宜偏私，使内外异法也。侍中、侍郎郭攸之、费祎、董允等，此皆良实，志虑忠纯，是以先帝简拔以遗陛下。愚以为宫中之事，事无大小，悉以咨之，然后施行，必能裨补阙漏，有所广益。将军向宠，性行淑均，晓畅军事，试用于昔日，先帝称之曰能，是以众议举宠为督。愚以为营中之事，悉以咨之，必能使行阵和睦，优劣得所。亲贤臣，远小人，此先汉所以兴隆也；亲小人，远贤臣，此后汉所以倾颓也。先帝在时，每与臣论此事，未尝不叹息痛恨于桓、灵也。侍中、尚书、长史、参军，此悉贞良死节之臣，愿陛下亲之信之，则汉室之隆，可计日而待也。臣本布衣，躬耕于南阳，苟全性命于乱世，不求闻达于诸侯。先帝不以臣卑鄙，猥自枉屈，三顾臣于草庐之中，咨臣以当世之事，由是感激，遂许先帝以驱驰。后值倾覆，受任于败军之际，奉命于危难之间，尔来二十有一年矣。先帝知臣谨慎，故临崩寄臣以大事也。受命以来，夙夜忧叹，恐托付不效，以伤先帝之明，故五月渡泸，深入不毛。今南方已定，兵甲已足，当奖率三军，北定中原，庶竭驽钝，攘除奸凶，兴复汉室，还于旧都。此臣所以报先帝而忠陛下之职分也。至于斟酌损益，进尽忠言，则攸之、祎、允之任也。愿陛下托臣以讨贼兴复之效，不效，则治臣之罪，以告先帝之灵。若无兴德之言，则责攸之、祎、允等之慢，以彰其咎；陛下亦宜自谋，以咨诹善道，察纳雅言，深追先帝遗诏，臣不胜受恩感激。今当远离，临表涕零，不知所言。1111111111111111111", "12345678abcdefgh")
console.log(xpass)

```

**后端**

```go

package main

import (
	"bytes"
	"crypto/aes"
	"crypto/cipher"
	"encoding/hex"
	"fmt"
)

// Decrypt Golang解密
// ciphertext  important important 上面js的生成的密文进行了 hex.encoding 在这之前必须要进行 hex.Decoding
// 上面js代码最后返回的是16进制
// 所以收到的数据hexText还需要用hex.DecodeString(hexText)转一下,这里略了
func Decrypt(ciphertext, key []byte) ([]byte, error) {
	pkey := PaddingLeft(key, '0', 16) //和js的key补码方法一致

	block, err := aes.NewCipher(pkey) //选择加密算法
	if err != nil {
		return nil, fmt.Errorf("key 长度必须 16/24/32长度: %s", err)
	}
	blockModel := cipher.NewCBCDecrypter(block, pkey) //和前端代码对应:   mode: CryptoJS.mode.CBC,// CBC算法
	plantText := make([]byte, len(ciphertext))
	blockModel.CryptBlocks(plantText, ciphertext)
	plantText = PKCS7UnPadding(plantText) //和前端代码对应:  padding: CryptoJS.pad.Pkcs7
	return plantText, nil
}

func PKCS7UnPadding(plantText []byte) []byte {
	length := len(plantText)
	unpadding := int(plantText[length-1])
	return plantText[:(length - unpadding)]
}

//这个方案必须和js的方法是一样的
func PaddingLeft(ori []byte, pad byte, length int) []byte {
	if len(ori) >= length {
		return ori[:length]
	}
	pads := bytes.Repeat([]byte{pad}, length-len(ori))
	return append(pads, ori...)
}

func main() {
	xpass := "bd53c9418578251a1d585e867be1795ac9281ec9d93cbc892e7771f6c40b59f8e9b0dc4dab73d3409174e56005561e7aafbc552c9b1f5676bd1ab4db712d863cf11c62d1943ecdcb43cb75bb6bb3c825d23211ad34647683bae2d6d32c165ae0d096d3557ef9e5a299c7391b30bc13d6f7159a8aa29e95c324dce26a88986f273d382b407ff5b40d97fa9f75ab8f89366de71871fe2cb1b328cf78b966353306cb1ca1f394096d5e17abf5ec2a16d5fd188836b1f4dfb7754ecef5450e98c4e884539ef20a4b58981f0b372e1209743db9a26bf35e170fef1735e7015cfa318a2319a9cf9cd21f38ff62ff97ca5de8c89cf9c65035d6b4664fbb72ee44f44fe8dcb9898572e49e3f8a77a7ad0abefada99cf856bf92074b0247d9676a3ad6c9f443423594241f57a59761369efade5e70929f1222276a6841989214246c7771e26d9716eaa6834e7a302194ef9031d29d292abbbd4a7ef733d0d72c827b49fcecfa7b82e504556de127203e38a6a3f43f0f641fd122494e6e60cd2e08e089b49e9caa849953ed9895d7559bdefa128d6df3b0d3d0ea5a445c86122552587a0063e7496d62d06186a70abe7aa4fd93e61a87b40877a37a2f07adcc54c5a27e7f87275c427aefa11693e34c3f48e898cfaa19441ecb8993458ec66108d0a9f131230e0a801bae4ad2d20f9f0f1386d759ba70ac2a3a71430fa405c473a6906b90cc8bb02804dacc0a562610292268d5cd8864d1034e35ca986183d117d4c477c8a4349f9c7dc203de4a30e1812a5e4d7a1b2b2b268f8a3998d2050fbcba4e282a90442786489ca120fbdd2a3b08fc70af914624d3a650f569246b9a13430bf9be853a89b117538ee1419fba79488efc63661cad87776eaef31a6535290cd1ad8f3bae547547e9e5de03f136b2169e3bca1b88a717d8d0b39497a877440714374a9e21356c7363f6e0ae4d6342447d3c4eae3c172c08823ffc18d9c5ad418536b78e6ba8d8994b3df62b8e50b6af32d8d9e35fb090c39e060afd6f5e888b7a7b18b050833548f4e8a01d34102f8eb912afd48899c4d0800510dce7593c5180ab7c6989dc2b2ace03b513e58fd8a1f48d7aee3da7b254881d05cf57a9f26b8bffb37d2c03518ef8efe91ec47402f03e58d9bc229a32d251b0eab2d0f6d9a2b41f82737158bcccc30b3b099542b792316bfe5070084c58dfc97605cb2b8336589efb629378a0b6a523a2b8a398ec05a279c2f39d4b0aee3851eafa0a0718ae44669bbf96474baad7ce516a18aa7d6885a6af4164a63a7f7495fa54efa9d451609882f08496632aa8fdb6532ba9cb7810f63cc90f49a85735605c41f8bf7aa59d61e192c72d5935c8f8331c4d4cdcc4928af0faa52c46173fc83eb5fc82415afdaad90ac58355ec8d769a393f72fa505858bafd7f2055d0ce18c26bec4075bc6246427a0094ef862c46ecff78fdc2a30defed8a2115bf1d83151b2a9c9d746403baca8ee08f46df336c205f5de1c951f292999dea12370571421cf1588006e19ec448e32a34a112b8a8f3f1bb30e71fbb18b7ecec1dd303c42a4ed6306f0d07cfd60c37152286a5de7d3699691b67031d1d762fe966780960f4408057fb0f9786fea9834d844ed2959b29c0b1e17b32ede0f310d243c7db366969bdcc998e23d8e6b3c2650e897f2c4c7b03cea4ccad0ff7215810f0f7ad57cca6032e3cad7508191e2e6e77f0efa4d1498e77fa157f341c96b0eb1e2537bff29ce4136cb222dd43ee0bbe1a0967815c9b3cac035cb59f673cfbfc52cf84e2cea07796bcf62fbccaea153ce86863823c408e84cb09cb0da9d8e9d2d93b0a2db8d3b83a8953854c7363c6002829b2e6db32afb425d90949b34de2bfc50a377e958f707dfd38b16a780dfca453a612d0a6da5d4373973291760d31fd9028dcbc252016767fb75bfd745be5e409be4d4130ab4845469cd68606966e8e1b02db6d76592d2dd4f8887405b6a5ce462bca1ebd47706d3a0621cc8ba9ede4df5d25d4cce7f8f6f47a71251f9b07d3579376f3a62b71babf25eaead82638be9a2fe949d607d045ebc793b74a10d4d146fa93c98b11b6f8223b359a79f40858241208bd17e48decfc87882b0702985a10de3c7d853257f032895ec840a0e95165b92852b98efccd4972a808863cb33b23447cf339f3f5581af5d31b2dc72d9f5a5a10b3ef2907d13fb8f71a62509c571a3c3a6e2164c6b11499adcfd3a0e01ab55d6bd9e90656478ebe9229b8509e3adf27ce2ee7da7ce36c6224c2da66caec22cdcd4c1d42f755e54bac7e91c6454388019eb3547e19073585933aa94044517bd13cb7ab57f8b6acdbdb3dec79322a6d3f7620e4e833ed28cbfb4390dc4b319daf4dc8af41cf4114b7fdc32933341e6416f84bf9aa8823d06a1773ea3eb9f80c93f30a77e28a8031b108cfb0ab6754098f5d479577e5a7c7db8270673a41ef9efb8d56d6f9682f25dfe7bcffa9d363e2e2baaad9b48727e195c7f8eaca0efdc2023c3d62ae97cd39961df9bcd6dd4787694a53b6646e0bba30c0bf26ffcefb3eba2e117493322449a4e54f9c9873ba7e221b3b8e2d6a0f93e762224c3b81efc3bb206551dec43a1005651ed52b84c4a6d009b7571cd1abf56ace83d9f9ba36c258002a2cc7b67328696edc130b51c201e6dcc457b19ee57c5f8103cfe07c78e03e4a84572054aae71dd5c785769e823dcef96fd37c8438c31b48077b271561d52e2844f432e7fa6782feca562009b514f797c2ae7319c6c11be0d04c45bc412eea5b0c718489efae9d0210dd8ec14853010fde59af59fe65f9c4f2df2db262cbc002877eb696a4012ea485fb015197d93d52277dad52d8b5ee7d8ae8841b2f328bca87e9a9f164412e332aabaa38549ba22320f6e9f446d1719fbacde1150bbea95f2ffa6fc8e8fa02bb9f7a5f7c66942b2314746ff3720c8d969bd31ce34b8e1a1ff8e5e924d7e1be0acc7c2dc7f2d9c6d1d424e49f651546785864270ceca7c85e5c7abc566485df8292826804f3f411edb80e4d44a0f51083c14e7b478ef05821f1bb35d135e852f35f7d4b94e5c515d417854c019dd5fc0e28dc91cf28175f71a9f34e9ff830275fcb02e865707c4b161ce6804cf0394b66b7ee57f214eb7bce841019688a5302da05a1436603e0f814e7ab174abebe218b1839b6486e24fa9b83b1f11b76defbfe5ee03efa28c09a47accb10df18a68a699b81d3cbc3ec5200ac7f229ec0c126f9e3a8a1653a090ef4059ecb980e7ed876f5d8f6bf830766b4d6c45f0d2a0e08ca703a17f027624b9bfc8679185dd893793b40f85ecdc3eac285c49be2d63a3484f6202c389c82dfdd290a0079bb8718426d7a6d14ae5cccd4f2491cb3a378eab3afbe9aa267037d7b8127a46cb5479e8b7bf0c98542ec3cbf6697c9cc048898cad8844d7d80697f748cb7e06de2c3c984151d87db54301176b4d59a6dcf7a89b48d1c848fdde187d02b1573e61225d9686c3229c22365677eb7ef8c5f7fb41f823fa47c55e3f752f21bfe558731c42b91510c7d2f52a35966ca23ca4666f84ddf38719f036e79c01fc524c2af5fa70c5d336fefe42d85ef926fee1714c2cc2c2d87c45d7cc9f16a90a2cc1b70a3e0717fc012146e7d5f925a641893bd132d8fcc768748489536b69be94596308123b6479fda17197ce4b98d8ec95aa83def540835dabd3540ed2709a472cf28cead4bb4892bf89412ee30c1f903cb15f81530fce9c0e9ccad51c26d317d1c9939c2009330172777b394d9b214d2830e01ec9fd8b883ce081550f374a265d41e88166e03faeafc26e4456246e3634da0b382aa13038d30bfe0b66dc67704281ce7d0d841c91904fbd8e0728e3a662df2b955739cadf0d74642439f997b7e8a993176f781f79bc5bc951102097e51a828b2786fa816145e5fc22bf890e5e517855f67269b5a51dec8351c2fd00eba2d422f96e366f40097890671d48373598fc95cc585da286faf2a854ddc0c457d1bca508e4be318b65a5b211762e28bc31f1e61a9ab8d2a1d2a2f591d0725ab811c15a974e06380f15bba2d39fb9020fa07ea49d9dd440994dfddd7cd87130e7855083fe0c23c6f0414a714333aa790a1f472acffbb6608f2ec3e039a7251d83a572eae3842ce405ee00104f37ad0ac9e99c302565e2b259d40bef89534a9edd6cb095671718018a113b160f4daa213c8b65e470a5b166dd91847e3516325c8d27ef4c1d1267a2f43c46e428026237574eea0c740a4a250f0266c97637012091b33d39317c7ecbd3d4269982f1f72bb2ee33dd892f7ff63b133f7ca46533ab898c85494e5e26ff7f9679a45efd4cf8a23aba29b6ddbbc724a2f3cc44cb998c45f312feb5a71acc8f0ad134d64b92438839472a3466e3b957acfe6647bd9779e9e2bd9f09c189521788f7b4cafaca433912dee2c9b4bfde3644f790f3148fad086a983bce713cece1c58c4e3df307d42b77794594db1d1d1d4c0133d20e4adb7d05eab1607f9a452f0c8ecefceb73bfe68767f07d7d7f444e913fb7bbee182d1ef7cc026789609781ab5a6ada4391bd9296cc634edf76614e8230a7fe2aca0591bff071d86ebf78261415365c15ac1332ac63eb5a224b9c25426c15b807357f8a84f635007f8b004049343480758cca5f808f0fb8f98ba83e4694adf2da15047f81b5349972bcb5566df15200d8445e24422e78b36bec18e0eb49a433cbc12110002e0010e53b7a16bba7e2eaf7ba61f05d67cd84b46649d02f772ff686d251e904f64d072e82a9a4bc33c90ec1b19c00b8dbf1e245c46db6b4dcd1b827c1ffe1745d206dd0257993a504a43570b4ee362549aebd3c7b48368f6748634a18a4e61f1d2f878dd77db3401fe2fbbf8e4cac8862323abedc6a9be4a6475f54c2fea603f7d4ba58473cfafa4cba3975264c39f1d8625074b8bb2486f34440d6ad37088d584bf0ba874d8ef29c199e3f8b1de238a8054704a8d1d073418da349511457c9b47ee3fef6251e154702fcae0ea9a6e45089c1ca24b7db79973c3f4f41360ddaa4da50a905b330a162b6f54193c5f20732ac4b0a2f2162a7239bf7f590750621f0669c60acc8aa68f03b99c99d09942e2cb10fb84c49a25ecb0b17762e126fc353bcfb7cb9aa63072cf012f07728f7a2fadc9dd701f6311d11eb3dba03da8cdd1d245dd24622fa927318f1678e26e11f411c30853a79af8b0d9e7c2250e32ad211a536aab8cbba293be695f12cc09de4a48890632e8fbd398b784205cefcb04ebda47ba3c6234b0f8ba2f5275ab7a1d8ef537064ecf9e316b0584ec93fb566773c55f7454baa73bfce7ee9a91a2bda8535bb284c9fc8fabdcb8ff686da6fc8367a57087e390b2a011df19ba265beb56f9825bb1dd635b1c28c17776cdda4e4bdc1444677b3d8efe335c6152fa9afe48fb825c04cf30aff79571dbcf73456250101a2018b0d7d875091cea15d7e82dcfbd2e74c6bde23a01440ec0a2173643f377eb7a3f30718b86e752c9dea5803870711cd5e2102e96bff0a52e4cf087d6435879dbeb4e216d8a7fa36443231ad342bd8a5ef29ff4e5f171b627b5d3f8feb2b7f24bd24cf14cba6aa50bb6a7099a57b8dc7bcbdcf10ecd6335caf7cfd31f50a67d2f3982f3a4e6cc47f06d3c7013e769a662c305ecd9c6f8e3eb88bbcd2db0bbb513d6dff323f82f92f0d9c60d7e5239a944437ae9870f37daefe66a3ce7a295a363d9b9bd86c8b17b141612030197a3a3d91330038ac60c107ebc23092cb417ae00c26d92c0285fe443b6eeb5629e68ad0623596b022112267de428e40d6b716d0d90c93f2bfc133f4b8daa5f5240c72c59d4036b9a458dfb00c9984cffa0fe62609da4369fbdd0d842574ff353c7b6ad7deba2cca0d9dc5567ab783234c0279e67708b8a361cbd41067919c2489095e48303efcaf500daf573fb0d98194d10c9776c5b2e21d861b8fbeb47bccf5eee034b394e4dfd8db9033e6262268f7930edbb4660c2e9dd930385a0d77973672f51266ec7409fc2b818c37aee3c73d62b5498692502cf817ec5a50ea747c441c531788b125f3d4663a1f87f2c70beffd0d0e2f25eee2f63e69d2d6a0b8a9bb527a965823a7534eb1d45920f152b7f0e183cf30e940ad4843e50410bf917da397b5acb6d20ea783b1c4c862314cd9afe592e9628fda2e09fd86ad80961da043c7af6b5fcb8e5fae68ed8916cfd906792286b740631668aad4524c0ef2b3db990db48f658602bded44013445f72133b118a5b970fe23d512e18c35eb870e1bcfac55b2d56cac26c8d56b425a7520a00c6b83ea2aa9c81bab9ccd9538bb9e457166071b81ebb0e5606aa3dc48b25abb0a7c190328d1d5fa090f8a288b3753e16592c739e44e5f24bb2effdd6b308d7f434d2b5c4de88049a29cc8a5b6adcfec6ccf943d4d7460e3609b15d0a10492e4fe7e94e2587e5e321581073025e5472c1f63bd916bc584d22050784173fefa182e2375002cb760ae32a390f29612727feaf99e22f5e49ecc7c2d089c291946df4a1a21b7f360ab9cf733289948b2018828342bb8e351b5a6f214e730f4a21f4a851d3269ea2d61ba19a4e257d3adf5cfc075852e5208d6e15b312ccdc0114da3a703668c9afca59afe0822f1d61a53cdbdf88bd0e10f7227ce19d585509b4342b83dfc6a857323cc5a30d6c68e86343df7daa051af55ac684da6816ce72823e31d78d3e2f436b9707bd93fb79228c6c934456661b710d319a33e6b8398f3e728a11055cfae4c3139ee3088f3dc0fff0394178ec9e755e1d00a1a30bda66372a85c59d856c23073a3d1bbc676a22f1782cf70f3f457e15f641ea0d397f3cefb316cb075ba89c86bb4859beed7a6ea142aa7d6ad480a393dee8a5b8b07a8e548c3e7cef49160f913cf866900172ba65a502f8db7035a6da24007a03014f08ed6d68fbacd3df6287412a0e532eba03d371381c6c697a2ca34b18e3824c6880ce7d69b1932405cf3eea1037dd471e98d46c2ea2a97de3e2023a2438b4275a1409486f6e84c5301246364b24211fd12bc90f4bbc59bca41442ebb693d9927300ee30b7c074872faf42282d515098991b8bd67c0709a781624231457e6623795802f0b6a560127e1537a9f5d1807fb6e9971b268baa0d7d57a137ad71e37e639afec67f1fec50d00990dcac02774c0e8d867d5b46a9c39142a7f4afa318931c30a3f182d37b03fcc87acec5c612e14771ee1b23e4aefbe37d5f07f29d6e4296a2223d46f019a5a28def6b144dfdeb5f742e9bd62019be9f7fc2455712ac6f9aa6482759ae60566c0fb9d1053796400640dca24a387497e635fe2c537e34a57204e20c6522c64a39d8cb0e27820d29fce1ee5e0cd0044fa7efd375a5217eaf61aa10d0381f7fb1cdd8a05e96196267f09a5432021fffb98256f94582f2417bd0c0e2ce70b2477b2e7c4fb6f172c18b85c6c6eceff3c8432b5d386c76ee1f8c43526183541e8164309b0e800394b0c863db353584c2794a4c0cfc2b1d8c5321260552efc5d0e9e92a1d31272a782a62551fb1950d9f4c5f1eb302e22956c4d8e2aa9865135793d43bc9d7dfb33b011321c58bf93dfb60de6b6074dd6b92cf40d2872c63aaf7e9f5d1d8604a487e7c9ab7b1fff41b1db04fc92bf9fb02d136b27373152555c86c689a3cb87a99809a01caecfcd3e22a859a6e7148ddcacbe74b46704806cdd3921b39202c972b2c1fa5b3c028c7aa800f0dc3d950d8a5b5888db8df3a52a20ffaa60ad7032a81c5007295002051f891b40e9930f3cb1a0791e28c9e6df9fce0d52118a153849df6deb9418758ba295eadd772f5186c2267d2a55fd0706681c51121c7bb7ab7aff1f155cf055b42781023cebd08ad1aa58fc4940fc2adca068d842f69a7f8138103fb9ac0d3c3efd52f50223857e81ebf397df281b6a88195302e67e9fc82e51b2144985b633d8a854ff836244d38300a29c3a3b3546d53c3f4fae83d17ecf221688f909336113d210f3fe55bc2ef20c0f3e4dd8b8f76b4d3e9cc017dbdb774acaca7f4e058eada72f122a834e38c0847890ccd3010ef391ab1b9dad4d324c113efd6ae9eeba0667c7bfebb1b2c1b1f71e234f8ce1481c87dcbf75507078dd6a8c15647f79372670457ec285fad1063e135595fbb9435ab2023dab01305625da39fac44c4ae4f83b7007ef989f09e6c160284e13e209530107edad6e693836a91a410eb65798781fe6e14b56eecac40c09c9b0522bb87f4f56a35aadfaa1010ae8b369c600f3fdd7d5066c65c2a2815bfd4cdbf639bd9ae8566c26954ff16683c73c4c402a49eb5880a36765048ae6dd564b8f5f124a42b67c1af4b7695ececaea95b57fe07b97f21eaf0351c85f12c757d00fd3f9332c89f43c14c5d605a96fe57763b24d93710500e09bebe33504046d0b41d2a9f3f0013cdf48aa104a5bdd23e0c61b36fb7fe57e2e02701ef1ec98ae28d5516358f008e3f86ae962896539f86143f33098002c857225105ec86f6e7331c8665f1704a65f6c82e61d1407bac7c7a10c3482e8ade5ba8fb5555cc37b6d00ca62beb8b92e0fd3fc28940e69602665d3ea6c5d1fa3168fc6a7b605dc75af1bba8dc1b3d284c27f893d6c73f6e8d4e9e17006784a315a08ad255fd37b85d9a2044fe5f0c659623da0022d765f263055d866131f2e7faf6870037fd7a5852fa035fc42c90aef6ddc5e7c32f9a01a900f353c9b49ee615ab66d94568752cd83231503cb81b1688ed49cd2d8dee7395d8099aab6be0773985dadbe290c75bac57bd13e1cfecbf9d4f5300a1c7f28ad608e622a673bac1579ae5ac92678edbce5e15a92c4eba7b85f2036e34f5b75f37ab1f2e9e60b37b384fb9656215badd19e61371d410b549e2b3b11c877796e4713ff8aaa2f358766634d30d3c919bcec502bbd03880662af9dbba2f15a397f8f701b84cdc8542edf8ba65d76bc4f619989939d48b63d8e2d811e5480d1ee4e758d439b333774a027725880e6cf5889faa73b2995cb74fbf4fd00e6d7f1d35c14adfead3fa9be3683f89a7002ff1d78b6db3703afcc72afe196b50aff8eae10ba9d37c7e7021324b42a9f852a0edb24c71787573b875c60780fc0ed1ec1efcdcc645afcf3a60e90104c15f4c0597f7edcb2e958075fadf9b6863e6d160d8e77cce89c0b07656f31174d67854698243a9d4d15d080f0a51414d148632a3842385e612bbcdb4158d657f6beaa8a38a016308ce48be8417e7dbb5a9786c6d149bdc80658bb58577d8dfa9cbda993dc283278183f4428984616ea7e48c2a5036b33aa53d8851fc0715f9c4a82c780b5d8e5b18d2156aea1d1b507cfec5adae68c69f87bdd167765e6400aeef8728b206d46740dda531ffdf2c73c40b656c9d8403750a9fb5723397b4e800c601e4f210f3a32e683f45b1b017441e694e05677241f0b8a50938c6a92f5f7c7df929ab7727f2a7d00834a1a9f7d4f1b06a6fa6a38ffbc0ba88f6eb7f2b93e43a4572b4e23d7cf7bd94c467ae8502ac7928e6610dae529626ea99e85ab22d252f10be33a70470b4ffdf624ff6a0bd3a8c6704f84ab2c398dac698231b2aad54c6c36f1cc61f73c9f85027a558b23b5006fa311e5698ceef2375586bfbf5591d7ff563b91904697f7456d8a9653f97bdb13388774bee667346144e30c8d38f3988eecb55981cb2d582ada50343b1bd2242883468ee9fe3fb1420790040c351d4f0566765a6e8a16852d6c1233b50d82faf4e6150750c5ac96192891cae159af24e15a930008adfdccecec255923cb474e52b301a85422c5c2b014dba6426274098c3cdcef762e4eab1843ad45810d363e2f20c82a498bc031dd28492bde02a95d0f272fc367c2fba6d2464a698fa8eb26d74bfd59743ba0db770449cd50902794fd3f6b6090ae49033edfbe0790976c7a51a7da6bb3f8388a0ccea4256839b681b2e7054f40cd8a7fe4fd939993d86fe7bed00b9643e614a8379e75e71b486aec5cba53f0ae504755a6448b42603794f3bfb73b4e6fcc5a5df1aa0ceead48de5ad65508edf5bd573ad1390c42b64d326147d08eb592579c43236b77128176126317d2b038ed06295bef9387bdf7168028b26fadede24e8b40b0c4b771eb615da8c787784932ab2cabfeda05e2d6225fcde57cd80c8913c483bcb326f00d4400a97ae6c366333482f8745934fd37861ced14fd2374538b35ac96332407ea453a0797c69898c33cf473d66ffd06967ff9eefee94e8971a47b4f65976e73c57da2cd29a99dac5f64f3960b264a9529b113b01809dac89b0775dcc19d41847b2a6320d40ed82bd822436029df1a2c776263c75f1b4c188d3952d45f603af0701e0013962ef741df37d2ac81d8c5cf2a02162c5574458a0c99392453d747ff6d29c14515850c1cedc483ba037f3aa418d4eca736ab6d00700496c653f936e4a4684fac0c2446430a5bc7b6e7b91d108e9f3b06a4a53646ce146d5736210d1a69a3c6c2ce302dbbfcdb8adb332bcc4f1bccc5a655ab4d4e3ccf7248e2eeb46d12bbebfb7aec4ff2486e9a947333681799307c062386b0a8ea985f35cf151a264e4befd1f5ad85718d132da3dbeb92a5687f261b97807d5b8581617c0e3fe371614c8ea1047cd8ada6c1a9e74f3d94f6940e034d65d5301a6ff4200a15f70a52e4b13c34fe9e81823d2107852d9d4f045e8c724e50230c2f5fc6bf5f052becc9d6fee738ea70be041baf6067bb0c91553868021e2c70fa31807aa18c3513eb7d07398849190abaaef4f0f8e32de6356740778ccfde0633ff06e2ea777a92efbcc4f1d03985c21e485a8c0fc819f4cf49353f76e1e3251a8b66bbc819375d48e02e1441b9c0f0939acfe8ac22c2b9d0b2ad6bb7b7030d30e483358427b4a39fa8b4afcabe62b7d85131e8593db409747b5240e33c942d5c2e689fec5e2dcd659e003da8280e1ab2c27200f10a0b9af671206297a387cbd6a9c900733cbfb33e8cd69cd96a6f7a5956af31400f8d25b34b73228826383655d66891717e4e5f8658948558f5ee7bfe19d43d10f90a92d689f82aa564b6a011a0dd42bf219f505a66b04dce5a306f49eab28e01783568830bf6f45ef1c84f19c55e1d54e25a005fd032fcb49663eea77de6fa7ce572d92b3f551575cc4b6d3aa970dbddf54f5642d4a58a3e2e4380222bf4a64edbc228688ba1576caed699f1b414dc2242ae116e766512d333b00a72e1bc4fc9eaa28f342babcc42de4f2eb2830ae58e9f1aa3a23bfd83cc2ffaa6a2a3bb2bfda6fd9ca93940427550114a0e1f35b25ce494df1bed777ef977c08505080aa3b0073bb2fc292e27ce318adc538aad8272f4bd3315e6ed19e7d114f82337bb361ec5c3f9ab5741805c06e43cc334f43b94a836c79d1a3235923f873253bf7087ce3d7bc74233265301c4c3fb78ec8be2543a133cdd551e8693d9657aa2c158ee1fa9bd85714e1e948280ef753593beebaee344b3514c34380bc6c3ecd38ed465f2f691530d9348b9d812c2062c43745ce71b2aa1fe12d7808d542715a593ffc07d409d378c3a57b13b9fbe74e965cd0a7b924b717ed5bc1572f54171e1ffb8e39c11611c34545b691cafb2166724ff6d4947f61fca3055df44e6f8282713fbfdefb6b54b1f2cdc16f778ffa6d1b33cfbfde0f0f1dab353ff69a3fc75ebd4d757d725ed2fc58a1d1cacb40e95ec96e582a4376b39457821306cf5bfeb6ca1ccc5f532c14d9170f55014c854869c21cbf48fab1981e949a6649c7eae079f19d7698a208dee8c5b8cc936cba9309a2616ad15c01544e8d4e67b34f6a3218e70fb6d74dc5e0a0fcbcbdd5a95385d2988953279dfd3739be7932ab87010c3bb466f0a7580904be9e002d84cd78fb49db3c1561f4292e0dc1c22ed705b4cdccbe1f12ad41e6479acc78977e406c9573203ee591f6667fb95339373fc68ff2a5f0dd23ea2b2fe42244e410415683ddb7ca28da879ff5ce12557bea5c634977cafeb36ad9fda0012433ece065b62abb99422b791dc99fbe5127dffa404784d541d5d0abefc5f69bfcf8319df037743d29b35a8968d14807cb7b016309294032bf6725f04cb04b8b322d73d1ec55a8300061365ef294bdd4bbfd014608053cc5a5b640cf7616b43091fd8ff4b000fe4b55213c739fe28120d8af7108561c5fe07bed98c9b467c21d857db2be8c409a4f32ed58510dd0140349012723ee656631845c9494a63fec3657a9938bf3fbd4e80ca77d76abe13bd170ddefd69159f089e46a36cc1b67df7a39958149fc73513996eae146249ad2735958e1790e3bcf946371c8ece2d1972c515d82781483f9f30c00349e762007fb977201096cc51f6caa7eae0815fc37e8b978b591d19489f6e2f12aa896597e2d00f36729f9358152a625ce13c7d8f49dad5b589c8d7a4afc5370f9ca87b0eda2c80d438dca4b2f2826b2872e70f8fead665bed03ee4be9f9bf0ffa08f235c01d9f87fb4e965424c6da3000609e584e3c83c855b6b9ba4f2f49c1a5643e93e7ffd9d89378df7a9e91259d6c09b4de641d1584f7c9c752a15097324a879672a00d55f09aed4fac0ad3b06786f784b04b8f96feed900728e7dcc45f0c92263229be33c4466766ac2112b792b81a002797a472af68638fb33361324d448ee375bd423e86a4e4f4de26368d6ad20cee9d8e5996d3c5a6550e52dff68517f504cde212f4c90a8ece915f33c482634b58cbc65d440d7663de72441ce792b60b66ce4a4f59f64afa712b4b99c873afca735d499a9062fce94a5f12d56d43e57af7c61f5ca2b775855bd5ebe037f8316e52daeda734d09b61997decab65dc2dae3b008c7b388963027afa7f926125090fbd31caee9368c88e4e2cf4aecbe1c496bdeca9599c1ab3c1699738fc2b6f59558eaf7017a2444c01cdb514cf28a42254c998ac3056ace4a6f79e20405ad303d4f2d01cda061d5c869463f4dd07333a9e973fd2205829aafd6c490b9f917d9c7082dd0991bc5808ffea7e8eb1173909b16acf98cfe8ce77779c84637ef72025a30a8618790e83d0f582b6b4e606c14fe527c4632d8831bf1dd183fdfa3e61fd01d9f0c965c90653a8b24517f2ecdb1e532de9955426240b849bf97b4591cd4ae1bd85c73e2e93caf3a6b07305c45a267810e1192424c737e33b46a122071d79c21f121f571fae182d12fe2cde7c60bbe3c3569afef04b7818a31974b95c2c85d599fa4747c6d0b41fbb5dbb1075ca05719eb7039bc85fb4deaf1b255af8e001c8d10902315ea9330e95b4e231e299daa9b5973a0db846d38bc2ad60a7f2f023923519ffacef27dcb6967cc1d68ba4af7a99923a00efe5dbf444433d3953d75924d00b2d12df1d3c10449dae5d471d9c1f09451886a24d7f5ee87cd43a7628e9725ce9578d011dde71c7c7fb952366bc6c72b1a334a736f1ed6726420a839219ff9f014a6eada8baef14a322b7f11bacd81742736224620f96513d0a695f60b48a8137f216e7fcd3f45be25e5b85cd64dd024e9d43daeca30c0f30eabf6da1965f29f9a88455bb44b80e3a9f9bced8d72e5482c517e555fe789a8ec04ce8566c519d9d4d52c6025377fcbb9fb866a44cb8fd369515ad76c03692e949b55b174f2e61c0c2f029cc1d4e333a8c46cab1a5c8f555648d19838863a04bb4140c06d13f891769ce04f2696aa78226f62ce77d05f62fd406b7723dd3b95a26188aea2f392b5e4c244fb4f46375748e5420ca46949e4c884187bc798d7621d23081e0d66b654dad39082bb15a8c0619d524fe75901bd186b307745ec01eb635aa29f6d19624348ee55a0846f471acdd30cfcf23a51fd2b467a9c45070ec1a391b985400b7260e6b3e4e0f1c1e21b3ac22178ec4156970aa51c406724033951e810a9c575238906929447c652a079c5e9fa203d2e3b983e555131b779c0dedceb2fda2071a12d822938c81b165d6d0256576235471bb7e2190a948f464619e9cd89655be4f6539c4adf9624dadcc60c88e2b2a724bc4268aaff03aa44a602b2258ed6a70af699caac1c929ef2b368a29d6b8b266db141896cadc3cdc672ef712c95630ff05fbd78413addf52dc936d225b3089f374130bf2ac1a72598298d52e07cac04182ee764d55d1c9b81b2b3bbd2dbfe13640619dac4f3f3ead545b051fc0f390182a81abb365e3b08347b2434c4e2a07f9d158971f2e18a74c4993b3793c5822651f2987f5a6903c92b39e5361041635a1006c23791549d80fb885b963969e5eea36b13c7f47f92ba280bd88ca6ee42e024f6a5295fc6de07e4b617f41312e2ccb55a1f6cdadb7cd56309f963d0326dc49944a14b8c6837f80f7935d7e1e22c0e71e9ba48aab6045226c16d95ba9652fd77047deb60e1a2198e13a163ce120fea8a15ca364b0b93fea529f539300304edbbabebb0f324e9840dcbecc99687fb203359a413f5209fd7a2d449dc6f4d14da23b70e9fc5f9c484d73ac5ce73251186b578cde5967dc45b4d3d7492a7ef4c717a5ea0a73cbf980bc38799e86817673c5f1381d09eecf6e64cf89a1f35697f786e3ed0acbd0570b8aec056fcbfc6123a0b44b6454eb040487d13ef1b7a78c12d615b69b45ec8f5c6daa63bfd9bb49a2c38834965d6c31918b7cd546985c32e83cdd6c78d69365a295a7955c68b71df56da3df6e946b1a9d880aab8d7887919f240d8c6508c6f2ecfbe554ce3e698fc36fe17388d597e9b68b308a6862e9604c9d4abf51beaff382c04152d987de7c97b6e60f22a8c6acfda5e610097ef5d913cc40bc72a9588b49fb5f246944c588bd9c5e33c77b20b8472f2a21cfed86d861bbe79cac5482e19d30831441952aa18065590c50ca91a5185909896cdcd74b407a5123e0d3e57baf5b0ca90dff6ff62575bcdd092d04cceb5b2a1df4d6c758bd8c6d3e5c5b17794a4725eb5c48e4a92c46fd8a2a4794ec838038a9ef1d01370913e9d9094287db5d9b78d922c9722dab1049f71ac0fb87e4520eb95d2e2d54c314338bf25fe620a66a4dcb7f4511e026cab89155da5f7d2361715820dbc44ca84b4b7fc74fdfd3c9df21a1982a2151d719278e33ed2d3e8077730e75bbefd05c4fd96ccf57719e9409153f7f80d3478283c75735f559bb386bb9129bb9aec396adf171e7f580e59d6989fb6bcc58cd002e5e1c54e825bce9f146556d5086bb2955db0b61b4265bbfcd8a3120d4dc08491fd044f144e849c7e8acdc5221d8edb1b62fb07b47ac0ce6189592356754a344a8a4562091d013ec2913d45a9f2fd4546927d848c856576d269ee1f8b408d295c91111db7a1329dc528f10c8ad3a657124752e63429c77a6629b441cf68160f4437216c45d8abc0f180266524087475e363926a2252b00e156c32a8a3a5f1db386c3e60821efb3f56eabaca79c674555b8ead0c3d56ca323213dab78cc9e17e5d5edff13bbf3e93db5f15bb57a5ccfcc67775485f79811bdd79b3073845c1b8f9bd4db5428b07a2f41d565f9bbed8c5241216aaaf8f1fda7564fa24a7707174b39ebe564561377c3030a4d1b5198e1a4c5fb52b2d09542e19d97f0249f7c1ed9f48a22c0861e4bd62f210a2533ae10af3265e28d07564996205a71a593833f69fbc1cbb63859b66443088fa3e51bf62ee6822db7006d5cd5e0e8717c608d41bc8580b49175b3241a04212a5bb79929fa8122cc72ea46d88ed58eca3e942f4f73bc8cf4264bb6e2fad066cc5f2bcbc6054c92930811928"
	bs, err := hex.DecodeString(xpass)
	if err != nil {
		fmt.Printf("DecryptJs() error = %v", err)
		return
	}
	//ABCDEF1234123412 使对称加密的密钥
	got, err := Decrypt(bs, []byte("12345678abcdefgh"))
	if err != nil {
		fmt.Printf("DecryptJs() error = %v", err)
		return
	}
	fmt.Println(string(got))
}

```

## 参考

+ [AES对称 Crypto-JS 加密和Go解密](https://mojotv.cn/go/crypto-js-with-golang)
+ [python 代码编译、打包](https://www.jianshu.com/p/099089535e0e)
