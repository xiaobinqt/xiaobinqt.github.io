---
title: "Github Actions replace env vars in file"
subtitle: ""

init_date: "2022-04-02T14:20:16+08:00"

date: 2022-04-02

lastmod: 2022-04-02

draft: false

author: "xiaobinqt"
description: "github actions replace env vars in file, 将配置文件中的变量替换为环境变量,github actions,github actions 替换配置文件"

featuredImage: ""

reproduce: false

tags: ["github-actions"]
categories: ["开发者工具"]
lightgallery: true

toc:
auto: false

math:
enable: true
---

Github Actions 是个好东西:grinning:，最近在使用的时候有个需求是，我项目不想把设置成私有的，但是有些配置又比较私密，比如 github 的 Personal access token，这种配置就不能暴露出来。
呃，这种需求前辈们估计也遇到过，[github actions marketplace](https://github.com/marketplace?type=actions)
是个好地方，我去里面搜了搜，果然有很多轮子，但是不知道能不能满足需求。

![marketplace](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220402/cf7d693259714fda8798eb7b9eaaff1c.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'marketplace')

[Replace env vars in file](https://github.com/marketplace/actions/replace-env-vars-in-file) 是我选中的一个轮子。

## 使用

![Replace env vars in file](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220402/436e6e8bd1b441da9f8861f5cb096ac0.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'Replace env vars in file')

[Replace env vars in file](https://github.com/marketplace/actions/replace-env-vars-in-file) 的文档就一句话，
`Replaces __TOKENS__ with environment variables in file.`
我刚开始还不太理解。

好吧，其实是**所有的环境变量都必须以`__`开头，然后以`__`结尾，这样才能被替换**。

我在项目中是这样使用的：

![配置文件](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220403/6633fcb2192f433f9be187f77fb26406.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '配置文件')

![action 中替换](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220403/df8850a8418643188140bf0fd9c1095d.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'action 中替换')


[//]: # (![action 中替换]&#40;https://cdn.xiaobinqt.cn/xiaobinqt.io/20220402/b9098ec71b84420a89bb53bbcecb29ea.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'action 中替换'&#41;)

[//]: # ()

[//]: # (![action 中替换]&#40;https://cdn.xiaobinqt.cn/xiaobinqt.io/20220402/76085f2e078a411da17bbce7dbea970a.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15&#41;)

[//]: # ()





