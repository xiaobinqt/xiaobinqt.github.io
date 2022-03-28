# hugo algolia Unreachable hosts


最近在使用 hugo algolia 时，在 github actions 同步索引到 algolia 时总是出现这样的错误：

![action error list](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220328/e0ad0f8731fc4d96becdf511a6be22f8.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'action error list')

![Unreachable hosts](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220328/0c3a871de45c4e15b25434cecb76fc16.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'Unreachable hosts')

我用的 action
插件是[Algolia Index Uploader](https://github.com/marketplace/actions/algolia-index-uploader)，找了半天发现是参数 `algolia_index_id`
写的有问题：

![algolia_index_id 填的值](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220328/0ed8a58ed9f1463694010a159d14ba85.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'algolia_index_id 填的值')

上传成功后可以去 [algolia 官网](https://www.algolia.com/)查看效果：

`Settings -> Applications -> 进入到应用 -> Search -> Browse`

![上传索引效果](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220328/18b9576e62ec41e69b4ddcab80eefaec.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '上传索引效果')

## 参考

+ [Algolia Hosts unreachable](https://stackoverflow.com/questions/45883334/algolia-hosts-unreachable)
