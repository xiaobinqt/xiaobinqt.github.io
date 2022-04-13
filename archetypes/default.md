---
title: "{{ replace .Name "-" " " | title }}"
subtitle: ""

init_date: "{{ .Date }}"

date: {{ .Date | time.Format "2006-01-02" }}

lastmod: {{ .Date | time.Format "2006-01-02" }}

draft: false

author: "xiaobinqt"
description: ""

featuredImage: ""

reproduce: false

tags: [""]
categories: [""]
lightgallery: true

toc:
auto: false

math:
enable: true
---

[//]: # (https://xiaobinqt.github.io)

[//]: # (https://www.xiaobinqt.cn)





