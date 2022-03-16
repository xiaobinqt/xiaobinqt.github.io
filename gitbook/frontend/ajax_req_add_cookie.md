# ajax 在请求时携带 cookie 信息

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
