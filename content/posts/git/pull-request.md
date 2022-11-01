---
title: "github pull request"
subtitle: "how to use github pull request"

date: 2021-04-29

lastmod: 2022-04-12

draft: false 

author: "xiaobinqt"
description: "xiaobinqt,github PR,PR,pull request,如何使用 PR, Can’t automatically merge "
resources:

- name: ""
  src: ""

tags: ["git"]
categories: ["开发者手册"]
lightgallery: true

toc:
  auto: false

math:
  enable: true
---

[//]: # (xiaobinqt.github.io)

## 总览

之前在 CSDN 上写过一篇关于 RP 的笔记 [github fork PR 的简单使用](https://blog.csdn.net/xiaobinqt/article/details/116277126)
，那篇文章写的比较随意且不是用命令行操作的，大部分操作都是基于 IDE，所以想着重新整理下那篇文章，同时也复习下 git 常用命令。

![pull request](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220413/cc120b7593074d3d8b2ff9adf3e13c64.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'pull request')


## 模拟场景

公司有个项目为 [xiao1996cc/git-dev](https://github.com/xiao1996cc/git-dev)
，有两个开发者，分别为 [xiaobinqt](https://github.com/xiaobinqt)
和 [lovenarcissus](https://github.com/lovenarcissus) 对这个项目进行开发，开发的新功能都会提交 PR 请求合并。

## fork

两个开发者分别把项目 fork 项目到自己的账号下，以 [xiaobinqt](https://github.com/xiaobinqt) 为例：

![forking](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220412/8a9dc338417745369e88b4b3df91a014.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'forking')

![fork 成功后](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220412/f16363d22f0d4826acaba334bc5232af.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'fork 成功后')

[xiaobinqt](https://github.com/xiaobinqt) 现在已经 fork 了 [xiao1996cc/git-dev](https://github.com/xiao1996cc/git-dev)
项目到自己的账号下 [xiaobinqt/git-dev](https://github.com/xiaobinqt/git-dev) 。

## xiaobinqt 开发新功能

> 每次开发新功能之前一定要先 `fetch` 下远程仓库。

### clone 

[xiaobinqt](https://github.com/xiaobinqt) fork 完成后，clone 项目到本地。

![clone](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220412/80f2eb7573af438683313396c4f63ca6.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'clone')

### 添加远程仓库

添加远程仓库 [xiao1996cc/git-dev](https://github.com/xiao1996cc/git-dev)

```git
git remote add upstream git@github.com:xiao1996cc/git-dev.git
```

![添加远程仓库](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220412/c34854f3e49048eba90bcc34cc309c0a.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '添加远程仓库')

fetch 远程仓库

```git
git fetch upstream
```

![fetch 远程仓库](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220412/3d0660ed67064b22a3689a54966248a4.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'fetch 远程仓库')

### 新建分支并开发

基于 upstream/main 创建新分支 dev_xiaobinqt

```git
git checkout -b dev_xiaobinqt upstream/main
```

![创建 dev_xiaobinqt 分支](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220412/cb13278fb56c4a048cd816462159673a.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '创建 dev_xiaobinqt 分支')


新建新文件 xiaobinqt.txt 并提交

![新建文件并提交](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220412/d35eca199f72453f9ed972e75de3a91b.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '新建文件并提交')

push 成功后再 github 项目下可以看到成功提示

![push 成功提示](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220412/c14f7b141e2e4b61885c90894a5b0e2d.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'push 成功提示')


### 新建 PR

![new pull request](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220412/14eee66c4908418ca52fc44d04739bab.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'new pull request')

选择要合并的分支并创建 pull request，这里我们将 `xiabinqt/git-dev` 下面的 `dev_xiaobinqt` 分支里的代码合并到 `xiao1996cc/git-dev` 下的 `main` 分支。

![创建 pull request](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220412/1baa99b602894dbb92024f578aadaaaf.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '创建 pull request')

![创建 pull request 成功](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220412/e2e612f093d94ac7a3989b01578351f6.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '创建 pull request 成功')

### 合并 PR

`xiao1996cc/git-dev` 项目下的 PR 只有**管理**这个项目的用户才有权限处理。管理员看到的界面是如下这样的：

![管理者看到的 PR 界面](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220412/f3005f3c551c429eae96deb6c53e78dd.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '管理者看到的 PR 界面')

处理完的 PR 状态会变成 Merged

![Merge PR](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220412/b983d0f5d73a4a8e8a01a457df8fa584.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'Merge PR')

至此 xiaobinqt 开发的一个功能已经成功提交到远程 upstream 仓库，也就是 `xiao1996cc/git-dev` 仓库，虽然只新建了一个文件，但是一个完整的 pull request 流程。


## lovenarcissus 开发新功能

对于 `lovenarcissus` 开发者来说，也是先 fork 项目再 clone 项目到本地。

可以看到 `lovenarcissus` fork 后的项目是有 xiaobinqt.txt 这个文件的，同时也验证了 xiaobinqt 开发者成功向远程仓库提交了代码。这里默认已经 clone 到了本地仓库。

![lovenarcissus fork](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220412/91c9b6dd2c614ff28d7d73751bbe59b8.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'lovenarcissus fork')



[//]: # (![clone]&#40;https://cdn.xiaobinqt.cn/xiaobinqt.io/20220412/c2c5a3604af04886b4053e7475df75b5.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'clone'&#41;)

### 添加远程仓库

![添加远程仓库](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220412/4ca1d947307d4ec58848a23eb5bc73fc.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '添加远程仓库')

fetch 远程仓库代码

![git fetch upsteam](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220412/2f039b5452514811a89853710843a6a0.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'git fetch upsteam')

### 新建分支并开发

基于 `upstream/main` 创建新分支 `dev_lovenarcissus` 开发分支

```git
git checkout -b dev_lovenarcissus upstream/main
```

![新建开发分支](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220412/64abb29d6e604f84b732c055a9359372.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '新建开发分支')

新建 lovenarcissus.txt 文件并修改 xiaobinqt.txt 文件

![开发代码](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220412/7af1393f145b4837b651c45c6c67167b.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '开发代码')

提交代码

![提交代码](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220412/d748706fc84d4874bb3f548b9b770deb.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '提交代码')

### 新建 PR

![新建 pull request](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220412/ae6ab7174cc74c58b02216267b2bfb06.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '新建 pull request')

### 合并 PR

![Merge pull request](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220412/617fd9602dec47e39f6e69ce57138bee.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'Merge pull request')

## 模拟并解决冲突

### 出现冲突

现在开发者 xiaobinqt 和开发者 lovenarcissus 都提了代码到远程仓库 `xiao1996cc/git-dev`，仓库里文件如下：

![远程代码仓库](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220412/ab47d38c6f544048a2e39a8f5c90314b.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '远程代码仓库')

现在开发者 xiaobinqt 需要开发一个新的功能，新增一个 xiaobinqt2.txt 文件，并且修改 xiaobinqt.txt 文件，但是这时 xiaobinqt 并没有 fetch 合并远程仓库的代码，xiaobinqt 本地仓库文件如下：

![文件列表](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220412/cd94ad34b4e4464598c6ec6726baec10.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '文件列表')

直接新建 xiaobinqt2.txt 文件，并且修改 xiaobinqt.txt 文件

![新建并修改文件](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220412/1faab506c99d4ca2ba4781fed2ae64bd.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '新建并修改文件')

push 代码到远程仓库，并创建 pull request 

![push 代码](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220412/dc48fe23f17d424a93bd817868996c3c.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'push 代码')

可以看到在创建 pull request 时出现了冲突，提示 **Can’t automatically merge** ，

![PR 出现冲突](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220412/d3a54feea2844ffe82712751186a651a.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'PR 出现冲突')


### 解决冲突

出现冲突的原因是本地代码跟 origin 仓库的代码是一样的，但是 origin 仓库跟 upstream 仓库代码不一致。我们需要先 fetch 下 upstream 仓库的代码跟本地代码合并后再 push 到 origin 仓库，再从 origin 仓库提 pull request 到 upsteam 仓库。

由:point_down:图可知，在 merge upstream/main 分支时出现了冲突 `Automatic merge failed; fix conflicts and then commit the result.`

![merge conflicts](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220413/40dd7bedf7c041d1859fb76c0cc3a2b7.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'merge conflicts')

vim 打开冲突文件 xiaobinqt.txt 解决冲突

![冲突文件内容](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220413/be7281a78f814a13b97c50fb8a643bbd.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '冲突文件内容')

解决冲突后的文件 :point_down:

![解决冲突后的文件](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220413/e5f0185bb84548a98ad33d1a23d7f5c2.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '解决冲突后的文件')

以下:point_down:是解决这次冲突的具体步骤：

![解决冲突具体步骤](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220413/f54a92110ac345c68c327ed16f6aea47.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '解决冲突具体步骤')

### 重提 PR

这时对于 xiaobinqt 开发者来说，冲突已经解决，可以重新提 pull request :point_down:，可以看到现在的状态是 **Able to merge.**。

![重提 PR](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220413/df8451a7d11f4799a3ed00a36ffe37bb.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '重提 PR')

创建新的 pull request 成功

![创建新的 PR 成功](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220413/c061dcc8dc51406b8ec77431273ea5cd.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '创建新的 PR 成功')

