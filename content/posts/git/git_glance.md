---
title: "git 使用文档"

date: 2022-03-23T17:40:29+08:00

lastmod: 2022-03-23T17:40:29+08:00

draft: false

featuredImage: "https://cdn.xiaobinqt.cn/xiaobinqt.io/20220324/c4b622f71a954f5492654749f5bb2aef.png?imageView2/0/interlace/1/q/50|imageslim"

author: "xiaobinqt"
description: "git使用，git，git基本操作，git clone,git push,git remote,.gitignore,git pull,git status,git add,git commit,git
log,git diff,git rebase,git merge,git stash,git rebase,git rebase --continue,git rebase --skip,git rebase --abort,git"

tags: ["git"]
categories: ["git"]
lightgallery: true

toc:
auto: false

math:
enable: true
---

## 基本概念

![基本概念](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220324/287032d97f2b4f7982abfcf4a28c802e.png?imageView2/0/interlace/1/q/50|imageslim '基本概念')

## .gitignore文件

```gitignore
# 此为注释 – 将被 Git 忽略
*.a       # 忽略所有 .a 结尾的文件
!lib.a    # 但 lib.a 除外
/TODO     # 仅仅忽略项目根目录下的 TODO 文件，不包括 subdir/TODO
build/    # 忽略 build/ 目录下的所有文件
doc/*.txt # 会忽略 doc/notes.txt 但不包括 doc/server/arch.txt
```

## git 常用命令

### git reset

当已经把代码从暂存区提交到版本库了，`git rest`命令可以恢复到暂存区的状态。

`git rest --hard HEAD $commit_id`，如果只会退上一个版本就是`HEAD^`，上上一个版本就是`HEAD^^`，当然往上100个版本写100个^比较容易数不过来，所以写成`HEAD~100`。

如果知道 commit id 的话，可以直接用 commit id，commit id 没必要写全，前6位基本就可以用，git会自动去找。

commit id 可以通过`git log`命令查看，格式化log可以使用`git log --pretty=oneline`

![git log --pretty=oneline](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220324/28ed39984d0f4556ab87d4f2f3766c94.png?imageView2/0/interlace/1/q/50|imageslim 'git log --pretty=oneline')

#### `--hard` 参数的作用

当文件被修改过，并且 add 到了暂存区，`git reset` 命令会把文件状态恢复到最初的状态，也就是从暂存区撤销掉，此时跟`git reset HEAD `命令一样。

如果文件从暂存区 commit 了，说明已经生成了最新的版本号了，此时回退，则需要回退到之前的一个版本，如果知道前一个版本的版本号，`git reset 版本号`这样就可以了，但是一般我们不会去记版本号， 可以执行`git log`
命令去查看，也可以使用` git reset HEAD^` 命令用于回退到上一个版本，会重新回到工作区，也就是 add 之前的状态。

如果使用了 `--hard` 参数会连工作区的状态内容也修改了。

以下是同样的 commit 之后，不加 `--hard` 参数和使用 `--hard` 参数的区别：

![不使用 --hard 参数](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220324/07fd3ad257cb40ee81a4a2ef835258d8.png?imageView2/0/interlace/1/q/50|imageslim '不使用 --hard 参数')

![使用 --hard 参数](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220324/84bb9684af7a4721aecaab77f6c8bf7a.png?imageView2/0/interlace/1/q/50|imageslim '使用 --hard 参数')

### git diff

| cmd                         | 说明           |
|-----------------------------|--------------|
| `git diff [file]`           | 显示暂存区和工作区的差异 |
| `git diff --cached [file]`/`git diff --staged [file]` | 显示暂存区和上一次提交(commit)的差异|

### git reflog

`git reflog` 用来记录你的每一次命令，可以查看你最近执行过的命令，可以用来回退到某一个时刻。所以为了好查记录，**`commit -m` 的提交说明文案尽量写清楚**。

![git reflog](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220324/71328dc599e24269bd001430cabd606e.png?imageView2/0/interlace/1/q/50|imageslim 'git reflog')

| cmd                            | 说明        |
|--------------------------------|-----------|
|  git reflog --date=local --all &#124; grep dev | 查看 dev 分支是基于哪个分支创建的|

{{< admonition type=tip title="Tips" open=true >}}

markdown 表格中使用 `|` 可以使用`&#124;`

{{< /admonition >}}

### git log

#### git log

不传入任何参数的默认情况下，`git log` 会按时间先后顺序列出所有的提交，最近的更新排在最上面，当记录太多时会出现分页，可以按空格键翻页，按 `q` 键退出。

![git log](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220324/91e168c43f4b486790fd8bd2f5f29349.png?imageView2/0/interlace/1/q/50|imageslim 'git log')

#### `git log --pretty=oneline`

将每个提交放在一行显示，在浏览大量的提交时非常有用。

![git log pretty oneline](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220324/a613f48add4f4750bd4d8772cba995d7.png?imageView2/0/interlace/1/q/50|imageslim 'git log --pretty=oneline')

#### `git log --graph --pretty=oneline `

`--abbrev-commit` 仅显示 SHA-1 校验和所有 40 个字符中的前几个字符。`--oneline` 是 `--pretty=oneline --abbrev-commit` 合用的简写。

所以 `git log --graph --pretty=oneline ` 可以也可以写为 `git log --graph --pretty=oneline --abbrev-commit`。

`--graph` 在日志旁以 ASCII 图形显示分支与合并历史。

![git graph](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220324/e28c6a5447a44e04b73b63cbb8358352.png?imageView2/0/interlace/1/q/50|imageslim 'git graph')

### git checkout

|cmd | 说明                                                                                                                                                                                  |
|--- |-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|`git checkout dev` | 切换到dev分支                                                                                                                                                                            |
|`git checkout -- file` | 可以丢弃工作区的修改， `git checkout -- readme.txt `意思是，把readme.txt文件在工作区的修改全部撤销。<br>这里有两种情况：<br>1. readme.txt自修改后还没有被放到暂存区，撤销修改就回到和版本库一模一样的状态。<br>2. readme.txt已经添加到暂存区后，又作了修改，撤销修改就回到添加到暂存区后的状态 |
|`git checkout -b yourbranchname origin/oldbranchname` | 在本地创建和远程分支对应的分支                                                                                                                                                                                    |

### git rm

git rm 有 2 个常用命令：

1. `git rm <file>`：同时从工作区和索引中删除文件。即**本地的文件也被删除**了，并把此次删除操作提交到了暂存区。

![git rm file](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220324/b22ecd44c7a94fc3974d5237fc3f048c.png?imageView2/0/interlace/1/q/50|imageslim 'git rm file')

2. `git rm --cached` ：从索引中删除文件。但是**本地文件还存在**，只是不希望这个文件被版本控制。

![git rm --cached](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220324/1134987486b345ef8f7157c8ac4636f6.png?imageView2/0/interlace/1/q/50|imageslim 'git rm --cached')

如果是文件夹需要加上 `-r` 参数，比如：

```git
git rm -r --cached 文件/文件夹名字
```

{{< admonition type=tip open=true title="Tips" >}}

先手动删除文件，然后使用`git rm <file>`和`git add<file>`效果是一样的。

{{< /admonition >}}

### git remote

| cmd                    | 说明                                                                                |
|------------------------|-----------------------------------------------------------------------------------|
| `git remote add 名字 地址` | 关联一个远程库时必须给远程库指定一个名字，如：`git remote add origin git@server-name:path/repo-name.git` |
|`git remote -v`| 查看远程库信息                                                                           |
|`git remote rm <name>`| 解除了本地和远程的绑定关系，如：`git remote rm origin`                                                                  |

### git push

把本地库的内容推送到远程，用`git push`命令，比如：

```git
git push -u origin master
```

实际上是把当前分支推送到远程的 master 分支上。

加上了`-u`参数，git不但会把本地的分支内容推送的远程的master分支，还会把本地的分支和远程的master分支关联起来，在以后的推送或者拉取时就可以简化命令，直接使用
`git push`。

### git branch

| cmd                 | 说明                                   |
|---------------------|--------------------------------------|
| `git brahcn -b 分支名` | 新建并切换到新分支，如新建并切换到dev分支：`git branch -b dev` |
| `git branch`        | 列出所有分支，当前分支前面会标一个`*`号 |
| `git branch -d 分支名` | 删除某个分支                               |
|`git branch -a` | 查看远程分支，远程分支会用红色表示出来（如果开了颜色支持的话）|
|`git branch -D <name>` | 强行删除一个没有被合并过的分支|
|`git branch --set-upstream branch-name origin/branch-name`|建立本地分支和远程分支的关联|

### git merge

`git merge`命令用于合并指定分支到当前分支。如：`git merge dev` 合并 dev 分支到当前分支。

### git switch

git 2.23+ 版本支持了 switch 命令用来切换分支，实际上，切换分支这个动作，用switch更好理解。

之前切换分支使用`git checkout <branch>`，而撤销修改则是`git checkout -- <file>`，同一个命令，有两种作用，确实有点令人迷惑。

| 操作      | version 2.23-       | version 2.23+       |
|---------|---------------------|---------------------|
| 切换分支    | `git branch dev`    | `git switch dev`    |
| 新建并切换分支 | `git branch -b dev` | `git switch -c dev` |

### git cherry-pick

在合并代码的时候，有两种情况：

1. 需要另一个分支的所有代码变动，那么就采用合并`git merge`。
2. 只需要部分代码变动（某几个提交），这时可以采用 `cherry pick`。

```git
git cherry-pick <commid_1> <commit_2>
```

### git stash

新增的文件，直接执行 `git stash` 是不会被存储的，需要先执行 `git add` 把文件加到版本控制里。

文件在版本控制里，并不等于就被stash起来了，git add 和 git stash 没有必然的关系，但是执行 **git stash 能正确存储的前提是文件必须在 git 版本控制中才行**。

可以多次stash，恢复的时候，先用git stash list查看，然后恢复指定的stash。

| cmd | 说明                                                                                                                                                            |
|---|---------------------------------------------------------------------------------------------------------------------------------------------------------------|
|`git stash save "save message"`  | 执行存储时，添加备注，方便查找，只有git stash 也要可以的，但查找时不方便识别                                                                                                                   |
| `git stash list`  | 查看stash了哪些存储                                                                                                                                                  |
| `git stash show` | 显示做了哪些改动，默认show第一个存储,如果要显示其他存贮，后面加 stash@{$num}，比如第二个 git stash show stash@{1}                                                                                |
| `git stash show -p` | 显示第一个存储的改动，如果想显示其他存存储，命令：`git stash show  stash@{$num}`  -p ，比如第二个：`git stash show  stash@{1} -p`                                                             |
| `git stash apply` | 应用某个存储，但不会把存储从存储列表中删除，默认使用第一个存储，即stash@{0}，如果要使用其他个，`git stash apply stash@{$num}` ， 比如第二个：`git stash apply stash@{1}`                                        |
|`git stash pop` | 命令恢复之前缓存的工作目录，将缓存堆栈中的对应stash删除，并将对应修改应用到当前的工作目录下，默认为第一个stash，即stash@{0}，如果要应用并删除其他stash，命令：`git stash pop stash@{$num}` ，比如应用并删除第二个：`git stash pop stash@{1}` |
| `git stash drop stash@{$num}` | 丢弃stash@{$num}存储，从列表中删除这个存储                                                                                                                                   |
|`git stash clear` | 删除所有缓存的stash                                                                                                                                                  |

## 分支管理

`HEAD`严格来说不是指向提交，而是指向某个分支，如master分支，master才是指向提交的，所以，HEAD指向的就是当前分支。

![head](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220324/a82292b2e5824a6298d3e53ac5819eb8.png?imageView2/0/interlace/1/q/50|imageslim 'head')

在合并分支时如果出现冲突，Git用`<<<<<<<`，`=======`，`>>>>>>>`标记出不同分支的内容。

![merge conflict](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220324/1071a4d1601f464080b4aedaa3acbe4e.png?imageView2/0/interlace/1/q/50|imageslim '合并分支有冲突')

### Fast forward

通常，合并分支时，如果可能，git会用Fast forward模式，但这种模式下，删除分支后，会丢掉分支信息。

可以使用`--no-ff`强制禁用Fast forward模式，git就会在merge时生成一个新的commit，这样，从分支历史上就可以看出分支信息。

![git merge --no-ff](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220324/38fbc059693942a69c7db82476275fed.png?imageView2/0/interlace/1/q/50|imageslim 'git merge --no-ff')

因为本次合并要创建一个新的commit，所以加上-m参数，把commit描述写进去。

![分支历史](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220324/ff5c6a084f18472ab52ecf5b62d754e3.png?imageView2/0/interlace/1/q/50|imageslim '分支历史')

## 标签Tag

tag 是基于某个分支下的某次 commit。如只执行 `git tag v1.0`，那么标签是打在该分支最新提交的 commit 上的。

创建的标签都只存储在本地，不会自动推送到远程，打错的标签可以在本地安全删除。如果标签已经推送到远程，得先删除本地标签，再删除远程标签。

| cmd | 说明                                  |
|---|-------------------------------------|
| `git tag -a v0.1 -m "version 0.1 released" 1094adb` | 基于某次 commit 打 tag，`-a`指定标签名，`-m`指定说明文字 |
| `git show <tagname>`| 显示 tag 的说明文字                        |
| `git tag`  | 可以查看所有标签                            | 
|`git tag -d v0.1`  | 删除标签                                |
|`git push origin <tagname>` | 推送某个标签到远程，如：`git push origin v1.0`                        | 
|`git push origin --tags` |一次性推送全部尚未推送到远程的本地标签 | 
|`git push origin :refs/tags/<tagname>` | 删除一个远程标签| 

## 参考

+ [git-fast-version-control](https://git-scm.com/book/zh/v2/%E8%B5%B7%E6%AD%A5-%E5%85%B3%E4%BA%8E%E7%89%88%E6%9C%AC%E6%8E%A7%E5%88%B6)
+ [Git教程](https://www.liaoxuefeng.com/wiki/896043488029600)
+ [Git Cheat Sheet](https://liaoxuefeng.gitee.io/resource.liaoxuefeng.com/git/git-cheat-sheet.pdf)
+ [git cherry-pick 教程](http://www.ruanyifeng.com/blog/2020/04/git-cherry-pick.html)
+ [git stash 用法总结和注意点](https://www.cnblogs.com/zndxall/archive/2018/09/04/9586088.html)
