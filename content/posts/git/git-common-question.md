---
title: "Git 常见问题"
subtitle: ""

init_date: "2022-07-12T14:09:39+08:00"

date: 2020-07-12

lastmod: 2022-07-12

draft: false

author: "xiaobinqt"
description: "xiaobinqt,"

featuredImage: ""

featuredImagePreview: ""

reproduce: false

translate: false

tags: ["git"]
categories: ["开发者手册"]
lightgallery: true

toc: true

math:
enable: true
---

<!-- author： xiaobinqt -->
<!-- email： xiaobinqt@163.com -->
<!-- https://xiaobinqt.github.io -->
<!-- https://www.xiaobinqt.cn -->

## unable to auto-detect email address

这个问题网上固定的解决方案是全局设置用户名和邮箱：

```bash
git config --global user.email "you@example.com"
git config --global user.name "Your Name"
```

其实这个问题也可以**在提交时单独设置**：

```shell
git -c "user.name=Your Name" -c "user.email=Your email" commit "Your commit message"
```

## 指定私钥文件

```shell
GIT_SSH_COMMAND='ssh  -i "/data/flexcloud/vscode/.ssh/id_rsa"' git push origin master
```

## are you sure you want to continue connecting

![are you sure](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220712/73049793ae584d35b6812cc0ec0f318b.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15)

如何想要忽略这个提示，可以在终端中输入:point_down:

```shell
GIT_SSH_COMMAND='ssh -o "UserKnownHostsFile=/dev/null" -o "StrictHostKeyChecking=no"' git push origin master
```

## 参考

+ [Override configured user for a single git commit](https://stackoverflow.com/questions/19840921/override-configured-user-for-a-single-git-commit)


