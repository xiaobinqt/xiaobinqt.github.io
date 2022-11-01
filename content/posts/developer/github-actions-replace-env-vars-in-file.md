---
title: "Github Actions replace env vars in file"
subtitle: ""

init_date: "2022-04-02T14:20:16+08:00"

date: 2022-04-02

lastmod: 2022-05-13

draft: false

author: "xiaobinqt"
description: "github actions replace env vars in file, 将配置文件中的变量替换为环境变量,github actions,github actions 替换配置文件"

featuredImage: ""

reproduce: false

tags: ["github-actions"]
categories: ["开发者手册"]
lightgallery: true

toc: true

math:
    enable: true
---

Github Actions 是个好东西:grinning:，最近在使用的时候有个需求是，我项目不想把设置成私有的，但是有些配置又比较私密，比如 github 的 Personal access token，这种配置就不能暴露出来。
呃，这种需求前辈们估计也遇到过，[github actions marketplace](https://github.com/marketplace?type=actions)
是个好地方，我去里面搜了搜，果然有很多轮子，但是不知道能不能满足需求。

![marketplace](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220402/cf7d693259714fda8798eb7b9eaaff1c.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'marketplace')

## replace-env-vars-in-file

[Replace env vars in file](https://github.com/marketplace/actions/replace-env-vars-in-file) 是我选中的一个轮子。

[//]: # (## 使用)

![Replace env vars in file](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220402/436e6e8bd1b441da9f8861f5cb096ac0.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'Replace env vars in file')

[Replace env vars in file](https://github.com/marketplace/actions/replace-env-vars-in-file) 的文档就一句话，
`Replaces __TOKENS__ with environment variables in file.`
我刚开始还不太理解。

好吧，其实是**所有的环境变量都必须以`__`开头，然后以`__`结尾，这样才能被替换**。

我在项目中是这样使用的：

![配置文件](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220421/78223a9a71cb4b39bf09daf1f36d3167.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '配置文件')

![action 中替换](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220421/4d886ce9639043da9bf7794908404277.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'action 中替换')

具体可以参看 [config.toml 配置文件](https://github.com/xiaobinqt/xiaobinqt.github.io/blob/23f0767e6b77f46c70edbf50e6822e5eebd85622/config.toml#L495)
，[workflows
工作流](https://github.com/xiaobinqt/xiaobinqt.github.io/blob/23f0767e6b77f46c70edbf50e6822e5eebd85622/.github/workflows/ci.yml#L18)

## simple-template-renderer

[simple-template-renderer](https://github.com/marketplace/actions/simple-template-renderer)
相比 [Replace env vars in file](https://github.com/marketplace/actions/replace-env-vars-in-file)
有个明显的优势，simple-template-renderer 支持 html 格式，replace-env-vars-in-file 不支持:cry:。

比如源文件中有

```yaml
icp = "${ICP}"
```

这个变量，需要把 `${ICP}` 替换成一个 html 的变量：

```shell
ICP: "<a href=https://beian.miit.gov.cn/ target=_blank>京ICP备16062974号-1</a>"
```

![simple-template-renderer](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220513/296318e8d2664cc3bb920f1c9406ed4a.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'simple-template-renderer')




