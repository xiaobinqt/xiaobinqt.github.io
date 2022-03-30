# 禁止Google浏览器强制跳转https


这几天在使用 google 浏览器打开公司的一个网站时，发现总是自动跳转到 https，以至于出现下面这个页面：

![ERR_SSL_PROTOCOL_ERROR](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220330/3bc5e2df037f497fb589a7927540f8f5.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'ERR_SSL_PROTOCOL_ERROR')

有时候浏览器太智能了也不是一件好事:rofl:。

## 解决方法

用 Google 浏览器打开[chrome://net-internals/#hsts](chrome://net-internals/#hsts) 这个页面，在最下面的 **Delete domain security policies**
填上需要禁止跳转的网站，然后点击**Delete**。

![Delete domain security policies](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220330/1dfabae20c7d4e3fb31303c1f99334fa.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'Delete domain security policies')

这里有个需要**注意**的地方是，如果我们的网址是 `http://g.xiaobinqt.cn:8000`，那么`Domain` 的值填的是 `xiaobinqt.cn`。

## 参考

+ [How to Stop Chrome from Automatically Redirecting to https](https://howchoo.com/chrome/stop-chrome-from-automatically-redirecting-https)

