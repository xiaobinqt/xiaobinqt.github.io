---
title: "Gitalk 初始化 issue"
subtitle: ""

init_date: "2022-04-01T21:37:02+08:00"

date: 2022-04-01

lastmod: 2022-04-01

draft: false

author: "xiaobinqt"
description: "Gitalk 初始化 issue,Gitalk,自动化,init issue,python 脚本自动初始 gitalk issue,hugo 主题,hugo theme"

featuredImage: ""

reproduce: false

tags: ["gitalk","python","hugo"]
categories: ["hugo"]
lightgallery: true

toc:
auto: false

math:
enable: true
---


在用 Gitalk 作为个人博客评论系统时，发现有个恶心的点是，每篇文章必须手动初始化一个 issue 或是登录 github 后，把文章一个一个点开界面去初始化 issue，不然就会出现以下的提示

![no issus](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220401/e360635c7d7b4e5b931306af6c0455cd.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'no issus')

个人觉得这件事情非常麻烦，**Gitalk 使用 labels 来映射 issuse**，可以看下我用的主题 Gitalk 在初始化评论时发出的网络请求

![创建 issue 的请求](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220401/be1fd41847d1449c8287f4a7820a35e1.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '创建 issue 的请求')

labels 第一个参数是 Gitalk，第二个参数是文章的发布时间，呃，感觉改成文章的 path 会更好，但是 **github label 的最大长度是 50 个字符**，所以把 path md5 会更好。我看了下源码修改成了 URL
path 的 md5 格式

`themes/LoveIt/layouts/partials/comment.html`

![comment id](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220404/94a28c0aa1fd4f44a034b1dce2087af4.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'comment id')

初始工作做完，就可以写脚本了。

## 分析

我们要做的事其实就是给每篇新文章初始化一个 issue，可以用 github Actions 来做这件事。

![初始化 issue 大致逻辑](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220402/fcdfd734b67b4e4283637061f717788b.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '初始化 issue 大致逻辑')

这里有几个稍微麻烦的地方，以下是我的实现方案，**仅仅是提供一个思路**。

### 获取所有文章信息

怎么获取所有的文章:question:，我用的 [LoveIt](https://github.com/dillonzq/LoveIt) 主题在 build 时在 public 目录里会有一个 index.json
文件，里面包含了所有的文章的信息。

![public index.json](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220402/e224ac9d408e4dea972caecabecec8ba.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'public index.json')

其他的主题可以使用 sitemap.xml 来获取所有的文章信息，hugo 在 build 时会生成 sitemap.xml 文件。

![sitemap.xml](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220402/f59bb44ee8924b639a949bb494a40b9c.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'sitemap.xml')

### issue 如何初始化

![issue内容](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220404/3f28b1b6486e44cfbeeef571bfded6f2.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'issue内容')

如上截图:point_up_2:是我创建的 issue 内容。body 是文章的 URL，title 是文章标题，labels 有 Gitalk 和文章的 URL path 的 md5
两个。那么问题就简单了，我们只需要给每篇文章初始化一个这样的 issue 就可以了。

固定文章的 URL 为唯一标识，组成两个 map ，map 键就是文章的 URL。一个 map 是 github 已存在的 issue 暂定为 `issue_map`，一个 map 是我们所有文章的 map 暂定为 `posts_map`
，URL 在 `posts_map`
中存在但是 `issue_map` 不存在的就是**新增**
。URL 在 `posts_map` 和 `issue_map` 中都存在但是 `posts_map` 中的标题跟 `issue_map` 中的标题不相同可能就是文章标题被修改了。

对于新的 URL 我的做法是承认它是新文章，或是旧文章的 URL 被修改了那只能去 github 手动修改 issue body 为新的 URL。

## python 脚本实现

```python
import hashlib
import json
import sys
import time

import requests

site_url = "https://xiaobinqt.github.io"

if len(sys.argv) != 4:
    print("Usage:")
    print(sys.argv[0], "token username repo_name")
    sys.exit(1)

# issue 的 body 就是文章的 URL

token = sys.argv[1]
username = sys.argv[2]
repo_name = sys.argv[3]
issue_map = dict()  ## [issue_body] = {"issue_number": issue_number, "issue_title": issue_title}
posts_map = dict()  # [post_url] = {"post_uri":uri,"post_date":date,"post_title":title}


def get_all_gitalk_issues(token, username, repo_name):
    for i in range(1, 150):  # 15000 个 issue 基本够用了,不够可以再加
        _, ret = get_issues_page(i)
        time.sleep(5)
        if ret == -1:
            break


## 删除的文章不管....
## 文章 title 修改了的文章该怎么处理？ 标题可能修改,但是 uri 不变,issue 的 body 是文章地址,只要文章地址不变，就可以直接 update issue title
## uri 如果也变了，相当于是文件的重命名了，这时只能去手动 update issue title 了?.....
def update_issue(issue_number, title):
    if title == "":
        return

    url = 'https://api.github.com/repos/%s/%s/issues/%d' % (username, repo_name, issue_number)
    print("update_issue url: %s" % url)
    data = {
        'title': title,
    }
    print("create_issue req json: %s" % json.dumps(data))
    r = requests.patch(url, data=json.dumps(data), headers={
        "Authorization": "token %s" % token,
    }, verify=False)

    if r.status_code == 200:
        print("update_issue success")
    else:
        print("update_issue fail, status_code: %d,title: %s,issue_number: %d" %
              (r.status_code, title, issue_number))


# 获取所有 label 为 gitalk 的 issue
def get_issues_page(page=1):
    url = 'https://api.github.com/repos/%s/%s/issues?labels=Gitalk&per_page=100&page=%d' % (username, repo_name, page)
    print("get_issues url: %s" % url)
    r = requests.get(url, headers={
        "Authorization": "token %s" % token,
        "Accept": "application/vnd.github.v3+json"
    })

    if r.status_code != 200:
        print("get_issues_page fail, status_code: %d" % r.status_code)
        sys.exit(2)

    if r.json() == []:
        return (issue_map, -1)

    for issue in r.json():
        if issue['body'] not in issue_map and issue["body"] != "":
            issue_map[issue['body']] = {
                "issue_number": issue['number'],
                "issue_title": issue['title']
            }

    return (issue_map, 0)


# 通过 public/index.json 获取所有的文章
def get_post_titles():
    with open(file='public/index.json', mode='r', encoding='utf-8') as f:
        file_data = f.read()
        if file_data == "" or file_data == [] or file_data == {}:
            return posts_map

        file_data = json.loads(file_data)
        for data in file_data:
            key = "%s%s" % (site_url, data['uri'])
            if key not in posts_map:
                posts_map[key] = {
                    "post_uri": data['uri'],
                    "post_date": data['date'],
                    "post_title": data['title']
                }

    return posts_map


def create_issue(title="", uri="", date=""):
    if title == "":
        return

    url = 'https://api.github.com/repos/%s/%s/issues' % (username, repo_name)
    print("create_issue title: %s uri: %s date: %s" % (title, uri, date))
    m = hashlib.md5()
    m.update(uri.encode('utf-8'))
    urlmd5 = m.hexdigest()
    data = {
        'title': title,
        'body': '%s%s' % (site_url, uri),
        'labels': [
            'Gitalk',
            urlmd5
        ]
    }
    print("create_issue req json: %s" % json.dumps(data))
    r = requests.post(url, data=json.dumps(data), headers={
        "Authorization": "token %s" % token,
    })

    if r.status_code == 201:
        print("create_issue success")
    else:
        print("create_issue fail, status_code: %d,title: %s,req url: %s \n" % (r.status_code, title, url))


# 创建 gitalk 创建 issue,如果 issue 已经存在，则不创建
def init_gitalk():
    for post_url, item in posts_map.items():
        ## 标题被修改了
        if post_url in issue_map and item['post_title'] != issue_map[post_url]['issue_title']:
            update_issue(issue_map[post_url]["issue_number"], item['post_title'])
        elif post_url not in issue_map:  # 新增的文章
            print("title: [%s] , body [%s] issue 不存在,创建..." % (item["post_title"], post_url))
            create_issue(item["post_title"], item["post_uri"], item["post_date"])
            # 延迟 5 秒，防止 github api 请求过于频繁： https://docs.github.com/en/rest/guides/best-practices-for-integrators#dealing-with-secondary-rate-limits
            time.sleep(5)


if __name__ == "__main__":
    # create_issue("禁止Google浏览器强制跳转https", "/stop_chrome_auto_redirect_2_https/", "2022-03-29")
    # get_all_gitalk_issues(token, username, repo_name)
    # print(issue_titles_map)

    ## 执行....
    get_all_gitalk_issues(token, username, repo_name)
    get_post_titles()
    init_gitalk()

```

在 github Actions 中执行：

![github actions build](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220404/0cfea81fd2804aeca5099c364779dda8.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'github actions build')

完整的 Action
文件可以参考 [https://github.com/xiaobinqt/xiaobinqt.github.io/blob/main/.github/workflows/ci.yml](https://github.com/xiaobinqt/xiaobinqt.github.io/blob/main/.github/workflows/ci.yml)

## 参考

+ [自动初始化 Gitalk 和 Gitment 评论](https://draveness.me/git-comments-initialize/)
+ [利用 Github Action 自动初始化 Gitalk 评论之Python篇](https://www.lshell.com/post/use-github-action-and-python-to-automatically-initialize-gitalk-comments/)
