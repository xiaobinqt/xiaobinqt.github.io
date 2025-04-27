---
weight: 7

bookFlatSection: true

bookCollapseSection: false

bookToc: true

title: "Chrome"
---

# Chrome

## 允许复制页面内容

有些网站设置了不允许复制内容，大部分时候可以使用 [User JavaScript and CSS](https://chromewebstore.google.com/detail/user-javascript-and-css/nbhcbdghjpllgmfilhnhkllmkecfmpld) 这个插件来解决。

![](https://cdn.xiaobinqt.cn//xiaobinqt.io/20250427/0729233f562541fbb0220958ca7cd0cc.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15)

js 内容

```js
// 注入 CSS
let style = document.createElement('style');
style.textContent = `
    * {
        pointer-events: all !important;
        user-select: text !important;
        -webkit-user-select: text !important;
        -moz-user-select: text !important;
        -ms-user-select: text !important;
    }
`;
document.head.appendChild(style);

// 解除 JS 事件限制
document.onselectstart = null;
document.oncontextmenu = null;
document.oncopy = null;
```


css 内容：

```css
* {
    pointer-events: all !important;
    user-select: text !important;
    -webkit-user-select: text !important; /* 兼容 Safari */
    -moz-user-select: text !important; /* 兼容 Firefox */
    -ms-user-select: text !important; /* 兼容 IE/Edge */
}
```
