---
title: "Go 实现下载文件的断点续传"
subtitle: ""

init_date: "2022-05-19T17:23:47+08:00"

date: 2022-01-21

lastmod: 2022-05-19

draft: false

author: "xiaobinqt"
description: "xiaobinqt,实现下载文件的断点续传,断点续传,go 实现下载文件的断点续传"

featuredImage: ""

featuredImagePreview: ""

reproduce: false

translate: false

tags: ["golang","断点续传"]
categories: ["golang"]
lightgallery: true

toc: true

math:
    enable: true
---

<!-- author： xiaobinqt -->
<!-- email： xiaobinqt@163.com -->
<!-- https://xiaobinqt.github.io -->
<!-- https://www.xiaobinqt.cn -->

## 断点续传

断点继传就是下载的文件可以在你下载了一半的时候暂停，下一次下载的时候可以从你暂停的地方继续下载，不用从头开始下载。

## 服务端

### martini 实现

[martini](https://github.com/go-martini/martini) 框架实现:point_down:

```go
package main

import (
	"bufio"
	"crypto/md5"
	"encoding/hex"
	"fmt"
	"io"
	"net/http"
	"os"
	"strconv"
	"strings"

	"github.com/go-martini/martini"
	"github.com/pkg/errors"
)

// 大文件
var path = "/mnt/d/code-server-3.11.0-linux-amd64.tar.gz"

func download(w http.ResponseWriter, r *http.Request) {
	filename := "download"

	file, err := os.Open(path)
	if err != nil {
		err = errors.Wrapf(err, "download openfile err")
		w.WriteHeader(500)
		w.Write([]byte(err.Error()))
		return
	}
	defer file.Close()

	info, err := file.Stat()
	if err != nil {
		err = errors.Wrapf(err, "download stat err")
		w.WriteHeader(500)
		w.Write([]byte(err.Error()))
		return
	}
	md5sum, err := MD5sum(file)
	if err != nil {
		err = errors.Wrapf(err, "download md5sum err")
		w.WriteHeader(500)
		w.Write([]byte(err.Error()))
		return
	}

	fmt.Println("md5sum = ", md5sum)

	w.Header().Add("Accept-Ranges", "bytes")
	w.Header().Add("Content-Disposition", "attachment; filename="+filename)
	w.Header().Add("Content-Md5", md5sum)
	var start, end int64
	if r := r.Header.Get("Range"); r != "" {
		if strings.Contains(r, "bytes=") && strings.Contains(r, "-") {
			fmt.Sscanf(r, "bytes=%d-%d", &start, &end)

			if end == 0 {
				end = info.Size() - 1
			}

			// start 从 0 开始,所以 end = info.Size() 也是有问题的，end 最大是 `info.Size() - 1`
			if start > end || start < 0 || end < 0 || end >= info.Size() {
				w.WriteHeader(http.StatusRequestedRangeNotSatisfiable)
				w.Write([]byte("参数错误...."))
				return
			}

			w.Header().Add("Content-Length", strconv.FormatInt(end-start+1, 10))
			w.Header().Add("Content-Range", fmt.Sprintf("bytes %d-%d/%d", start, end, info.Size()))
			w.Header().Set("Content-Type", "application/octet-stream")
			w.WriteHeader(http.StatusPartialContent)

		} else {
			w.WriteHeader(400)
			w.Write([]byte("header Range"))
			return
		}
	} else {
		w.Header().Add("Content-Length", strconv.FormatInt(info.Size(), 10))
		w.Header().Set("Content-Type", "application/octet-stream")
		start = 0
		end = info.Size() - 1
	}

	_, err = file.Seek(start, 0)
	if err != nil {
		err = errors.Wrapf(err, "file seek err")
		w.WriteHeader(500)
		w.Write([]byte(err.Error()))
		return
	}

	n := 2048
	buf := make([]byte, n)
	for {
		if end-start+1 < int64(n) {
			n = int(end - start + 1)
		}
		_, err = file.Read(buf[:n])
		if err != nil {
			if err != io.EOF {
				err = errors.Wrapf(err, "io.Eof err")
				w.WriteHeader(500)
				w.Write([]byte(err.Error()))
				return
			}
			return
		}

		_, err = w.Write(buf[:n])
		if err != nil {
			err = errors.Wrapf(err, "Writer.Write err")
			w.WriteHeader(500)
			w.Write([]byte(err.Error()))
			return
		}

		start += int64(n)
		if start >= end+1 {
			return
		}
	}
}

func MD5sum(file *os.File) (string, error) {
	hash := md5.New()
	for buf, reader := make([]byte, 65536), bufio.NewReader(file); ; {
		n, err := reader.Read(buf)
		if err != nil {
			if err == io.EOF {
				break
			}
			return "", err
		}
		hash.Write(buf[:n])
	}
	return hex.EncodeToString(hash.Sum(nil)), nil
}

func main() {
	route := martini.Classic()
	route.Get("/download", download)

	route.RunOnAddr(":8080")
}

```

## 客户端下载

```go
package main

import (
	"bufio"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"os"
	"os/exec"
	"strconv"

	"github.com/pkg/errors"
	"github.com/sirupsen/logrus"
)

func DownloadDownloadArtifact(downloadPath, surl string) (err error) {
	dfn := downloadPath
	var (
		file *os.File
		size int64
		headerMd5sum,
		downloadMd5sum string
	)

	file, err = os.OpenFile(dfn, os.O_RDWR|os.O_CREATE, 0644)
	defer file.Close()
	if err != nil {
		err = errors.Wrapf(err, "download openfile err")
		return err
	}
	stat, _ := file.Stat()
	size = stat.Size()
	sk, err := file.Seek(size, 0)
	if err != nil {
		err = errors.Wrapf(err, "seek err")
		return err
	}

	if sk != size {
		err = fmt.Errorf("seek length not equal file size,seek=%d,size=%d", sk, size)
		logrus.Error(err.Error())
		return err
	}

	request := http.Request{}
	request.Method = http.MethodGet
	if size != 0 {
		header := http.Header{}
		header.Set("Range", "bytes="+strconv.FormatInt(size, 10)+"-")
		request.Header = header
	}
	parse, _ := url.Parse(surl)
	request.URL = parse
	resp, err := http.DefaultClient.Do(&request)
	//resp, err := http.DefaultClient.Do(&request)
	defer resp.Body.Close()
	if err != nil {
		err = errors.Wrapf(err, "client do err")
		logrus.Error(err.Error())
		return err
	}

	headerMd5sum = resp.Header.Get("Content-Md5")
	if headerMd5sum == "" {
		return fmt.Errorf("resp header md5sum empty")
	}

	body := resp.Body
	writer := bufio.NewWriter(file)
	bs := make([]byte, 1024*1024)
	for {
		var read int
		read, err = body.Read(bs)
		if err != nil {
			if err != io.EOF {
				err = errors.Wrapf(err, "body read not io eof")
				logrus.Error(err.Error())
				return err
			}

			if err == io.EOF && resp.StatusCode != http.StatusOK {
				err = nil
				return
			}

			if read != 0 {
				_, err = writer.Write(bs[:read])
				if err != nil {
					err = errors.Wrapf(err, "writer write err")
					return err
				}
			}

			err = nil
			break
		}
		_, err = writer.Write(bs[:read])
		if err != nil {
			err = errors.Wrapf(err, "writer write err")
			return err
		}
	}

	if err != nil {
		return err
	}

	err = writer.Flush()
	if err != nil {
		err = errors.Wrapf(err, "writer.Flush err")
		return err
	}

	// 比对 md5 是否一致
	downloadMd5sum, err = md5sum(downloadPath)
	if err != nil {
		err = errors.Wrapf(err, "get download md5dum err")
		logrus.Error(err.Error())
		// md5 不一致直接删除
		os.Remove(downloadPath)
		return err
	}
	logrus.Debugf("downloadMd5sum: %s,headerMd5sum:%s ", downloadMd5sum, headerMd5sum)

	if downloadMd5sum == headerMd5sum {
		return nil
	}

	// 错误了删除 tar 包
	os.Remove(downloadPath)
	return fmt.Errorf("download md5sum not equal header md5dum")
}

func md5sum(downloadPath string) (string, error) {
	cmdStr := fmt.Sprintf("printf $(md5sum %s)", downloadPath)
	cmdOutput, err := exec.Command("/bin/sh", "-c", cmdStr).CombinedOutput()
	logrus.Debugf("md5sum: %s ", cmdStr)
	if err != nil {
		err = errors.Wrapf(err, "md5sum [%s] exec.Command err", cmdStr)
		logrus.Error(err.Error())
		return "", err
	}
	return string(cmdOutput), nil
}

func main() {
	err := DownloadDownloadArtifact("/mnt/d/tmp/xxx.111.test", "http://127.0.0.1:8080/download")
	if err != nil {
		fmt.Println("download err", err.Error())
		return
	}
	fmt.Println("success..........")
}

```

