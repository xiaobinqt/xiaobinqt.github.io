---
title: "github PR 简单使用"

date: 2021-04-29T23:28:36+08:00

lastmod: 2022-03-18T23:28:36+08:00

draft: false

author: "xiaobinqt"
description: ""
resources:

- name: ""
  src: ""

tags: ["git"]
categories: ["git"]
lightgallery: true

toc:
auto: false

math:
enable: true
---


入职新公司，就在 git 的使用上被各种虐。整理一篇文档，对这个问题梳理总结下。 之前用 git 都是直接新建分支，然后 PR review 后合到主分支，现在是先 fork 下，之前没用过 fork :cry:
，其实就是多了一步，从自己仓库的分支提 PR 。

## clone 代码

![fork](https://img-blog.csdnimg.cn/20210429211554301.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3hpYW9iaW5xdA==,size_16,color_FFFFFF,t_70 'fork')

fork 代码后 clone 到本地。

```shell
git clone git@github.com:xxxxx/dev-git.git
```

![clone](https://img-blog.csdnimg.cn/20210429211810760.png "clone")

我们可以用 `git remote -v ` 看下远程仓库情况：

![git remote -v](https://img-blog.csdnimg.cn/20210429211952265.png "git remote -v")

## 添加远程仓库

用  `git remote add` 添加远程仓库，这里的远程就是我 fork 的那个仓库。

```shell
 git remote add upstream git@github.xxxxx/dev-git.git
```

这里的 upstream 是远程仓库的别名，类似 origin 。

![add upstream](https://img-blog.csdnimg.cn/20210429212519676.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3hpYW9iaW5xdA==,size_16,color_FFFFFF,t_70 'git remote')

现在我们可以看到已经有 2 个远程仓库地址了，origin 是我自己的远程仓库，upstream 是别人的，也就是真实项目的远程仓库。

## PR

我们现在可以 upstream 远程仓库中提交一个 PR。先 fetch 一下 upstream 远程仓库的代码。确保我们的代码是最新的。

![fetch](https://img-blog.csdnimg.cn/20210429213832300.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3hpYW9iaW5xdA==,size_16,color_FFFFFF,t_70 ' ')

接下来就可以在 ide 上操作了。

![ide operate](https://img-blog.csdnimg.cn/20210429213954128.png ' ')

我们可以看到远程分支了 upstream/main 和 origin/main ，upstream 是真正的项目地址，origin 是 fork 到我们仓库的分支。 checkout 下 upstream/main ：

![ide operate](https://img-blog.csdnimg.cn/20210429214144804.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3hpYW9iaW5xdA==,size_16,color_FFFFFF,t_70 ' ')

![](https://img-blog.csdnimg.cn/20210429214206976.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3hpYW9iaW5xdA==,size_16,color_FFFFFF,t_70 ' ')

再拉下最新的代码

![ide operate](https://img-blog.csdnimg.cn/20210429214238679.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3hpYW9iaW5xdA==,size_16,color_FFFFFF,t_70 ' ')

再切回到我们的 origin/main 分支

从我们的分支 checkout 一个新的开发分支 dev

![origin main](https://img-blog.csdnimg.cn/20210429214429980.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3hpYW9iaW5xdA==,size_16,color_FFFFFF,t_70 ' ')

![dev branch](https://img-blog.csdnimg.cn/20210429214442427.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3hpYW9iaW5xdA==,size_16,color_FFFFFF,t_70 ' ')

rebase 下远程分支的代码

![](https://img-blog.csdnimg.cn/2021042921451443.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3hpYW9iaW5xdA==,size_16,color_FFFFFF,t_70 ' ')

我们简单修改一行，提下代码

![add](https://img-blog.csdnimg.cn/20210429214644990.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3hpYW9iaW5xdA==,size_16,color_FFFFFF,t_70 ' ')

push

![push1](https://img-blog.csdnimg.cn/20210429214713664.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3hpYW9iaW5xdA==,size_16,color_FFFFFF,t_70 ' ')

![push2](https://img-blog.csdnimg.cn/20210429214746471.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3hpYW9iaW5xdA==,size_16,color_FFFFFF,t_70 ' ')

push 完成后我们的仓库会出现提示

![](https://img-blog.csdnimg.cn/20210429215000526.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3hpYW9iaW5xdA==,size_16,color_FFFFFF,t_70 ' ')

现在我们就可以提一个 PR 了。

![](https://img-blog.csdnimg.cn/20210429215218625.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3hpYW9iaW5xdA==,size_16,color_FFFFFF,t_70 ' ')

成功提了一个 PR

![](https://img-blog.csdnimg.cn/20210429215305879.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3hpYW9iaW5xdA==,size_16,color_FFFFFF,t_70 ' ')

## 更新代码

![](https://img-blog.csdnimg.cn/20210429215730968.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3hpYW9iaW5xdA==,size_16,color_FFFFFF,t_70 ' ')

PR 合并之后我们需要更新下代码： checkout 到 upstream-main 分支，拉下代码

![](https://img-blog.csdnimg.cn/20210429215851367.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3hpYW9iaW5xdA==,size_16,color_FFFFFF,t_70 ' ')

再切到 origin/dev 分支 rebase 下 upstream-main

![](https://img-blog.csdnimg.cn/20210429220007359.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3hpYW9iaW5xdA==,size_16,color_FFFFFF,t_70 ' ')

![](https://img-blog.csdnimg.cn/20210429220038487.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3hpYW9iaW5xdA==,size_16,color_FFFFFF,t_70 ' ')

以上，一个闭环结束。


