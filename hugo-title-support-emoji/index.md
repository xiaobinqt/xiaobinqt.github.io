# hugo主题标题支持emoji:smile:


## 解决方法

hugo 在渲染时默认是不支持标题中的emoji的（有的主题也许是支持的），可以通过修改主题源码来支持。

我用的主题是[LoveIt](https://github.com/dillonzq/LoveIt)，找到 simple.html 文件，路径为 `themes/LoveIt/layouts/posts/single.html`
修改标题的渲染方式为 `{{ .Title | emojify }}`，如下：

![修改主题的渲染方式](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220321/685a911f54f045568fa3791ee8c368a9.png?imageView2/0/interlace/1/q/50|imageslim ' ')

这样就可以支持 emoji 了。

![title support emoji](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220321/a19ba2a3551f48dd89d1ab497bdba623.png?imageView2/0/interlace/1/q/50|imageslim ' ')

此时列表中还不支持 emoji，同样的修改方式。

![list not support emoji](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220321/daf40dd155ae42df9e1d52c448057582.png?imageView2/0/interlace/1/q/50|imageslim ' ')

修改 `themes/LoveIt/layouts/_default/summary.html` 文件文件中的 title 的渲染方式为 `{{ .Title | emojify }}`。

## 参考

+ [Hugo should render emojis in page titles if enableEmoji = true](https://github.com/gohugoio/hugo/issues/7171)
