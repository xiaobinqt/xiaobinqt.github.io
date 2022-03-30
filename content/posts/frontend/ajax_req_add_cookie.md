---
title: "ajax 在请求时携带 cookie 信息"

date: 2022-03-01

lastmod: 2022-03-16

draft: false

author: "xiaobinqt"
description: ""
resources:

- name: ""
  src: ""

tags: ["web"]
categories: ["web"]
lightgallery: true

toc:
auto: false

math:
enable: true
---



最近有个需求在使用 $.ajax 时需要把 cookie 信息也带着，google 下发现可以这么写：

```javascript

$.ajax({
    url: "/nodered/nodes",
    headers: {
        Accept: "text/html",
    },
    xhrFields: {
        withCredentials: true // 携带 cookie 信息
    },
    success: function (data) {
        console.log(data)
        $("#red-ui-palette-container").html(data)
    },
    error: function (jqXHR) {
        console.log(jqXHR)
    }
});

```


