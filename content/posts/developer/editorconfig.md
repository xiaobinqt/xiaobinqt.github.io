---
title: "使用 EditorConfig 管理代码样式"
subtitle: ""

init_date: "2023-03-20T14:56:05+08:00"

date: 2019-09-26

lastmod: 2023-03-20

draft: false

author: "xiaobinqt"
description: "xiaobinqt,"

featuredImage: ""

featuredImagePreview: ""

reproduce: false

translate: false

tags: [""]
categories: [""]
lightgallery: true

series: []

series_weight:

toc: true

math: true
---

<!-- author： xiaobinqt -->
<!-- email： xiaobinqt@163.com -->
<!-- https://xiaobinqt.github.io -->
<!-- https://www.xiaobinqt.cn -->

windows 比较恶心的一点是，默认使用 CRLF 换行，比如苹果电脑就是类 Unix 系统，使用 LF 换行符。有时可能还会因为 windows 换行符的问题，编译的 shell 脚本传到服务器上显示运行错误。

EditorConfig 是用于统一不同 IDE 编码风格配置的一种配置文件，容易阅读，并且方便版本控制系统管理，只需要在项目中添加一个`.editorconfig` 文件即可。

下面是一个官网的例子，使用的配置文件是 ini 格式

```shell
# EditorConfig is awesome: https://EditorConfig.org

# top-most EditorConfig file
root = true

# unix格式换行符,并且在文件末尾插入新行
[*]
end_of_line = lf
insert_final_newline = true

# Matches multiple files with brace expansion notation
# Set default charset
[*.{js,py}]
charset = utf-8

# 4 space indentation
[*.py]
indent_style = space
indent_size = 4

# Tab indentation (no size specified)
[Makefile]
indent_style = tab

# Indentation override for all JS under lib directory
[lib/**.js]
indent_style = space
indent_size = 2

# Matches the exact files either package.json or .travis.yml
[{package.json,.travis.yml}]
indent_style = space
indent_size = 2

```

## 文件匹配

| 字符模式	          | 匹配内容                                                       |
|----------------|------------------------------------------------------------|
| `*`	           | 匹配任意字母组成的字符串,除了路径分隔符/                                      |
| `**`	          | 匹配任意字母组成的字符串                                               |
| `?`	           | 匹配任意单个字符                                                   |
| `[name]`	      | 匹配括号内的任意单个字符                                               |
| `[!name]`      | 	匹配除了括号内的字符                                                |
| `{s1,s2,s3}`	  | 匹配其中任何一个,用逗号隔开的 (Available since EditorConfig Core 0.11.0) |
| `{num1..num2}` | 	匹配两个数字之间的整数                                               |

## 支持的配置项

EditorConfig文件部分包含由等号（=）分隔的键值对。 除 root 外，所有键值对都必须位于生效的部分下。

| Key	                       | Supported values                                                             |
|----------------------------|------------------------------------------------------------------------------|
| `indent_style`	            | 使用 tab 还是 space                                                              |
| `indent_size`	             | 设置缩进宽度                                                                       |
| `tab_width`	               | 设置制表符宽度, 默认和 indent_size 值一样,通常不需要设定                                         |
| `end_of_line`	             | 设置换行符`lf`, `c`r, or `crlf`                                                   |
| `charset`	                 | 设置字符编码`latin1`, `utf-8`, `utf-8-bom`, `utf-16be`，`utf-16le`。不建议使用`utf-8-bom` |
| `trim_trailing_whitespace` | 	设置为 true 删除所有换行符前的空白字符 false 不删除                                            |
| `insert_final_newline`	    | 设置 true 保存的时候文件结尾会生成新行 false 不生成新行                                           |
| `root`	                    | 需要在开头指定，通常建议项目最顶层的配置文件设置该值。<br>设定为 true 以后搜索 editorconfig 到当前的文件就会停止         |

## 参考

+ [使用 EditorConfig 设置项目的偏好设置](https://blog.windrunner.me/pages/editorconfig)
+ [EditorConfig Specification](https://spec.editorconfig.org/)
+ [EditorConfig使用指南](https://www.jianshu.com/p/c49a9ecff04d)
+ [EditorConfig](https://editorconfig.org/)

