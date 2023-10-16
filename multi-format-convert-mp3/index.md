# 各种音乐文件格式转 MP3


<!-- author： xiaobinqt -->
<!-- email： xiaobinqt@163.com -->
<!-- https://xiaobinqt.github.io -->
<!-- https://www.xiaobinqt.cn -->

## mgg

我的 qq 音乐桌面播放器版本是 1951，下载下来的音乐格式是 mgg 格式的。

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20231016/256c0eddcd2e4f76a4e0f6215dd9455d.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'qq music version')

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20231016/943f3b65ff8d4590b0796a8d9195435c.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'mgg')

如何将 mgg 格式转 mgg 格式转成 MP3 格式呢:question: mgg 文件暂时不支持直接转成 mp3，可以先把 mgg 文件转成 ogg 文件，再把 ogg 文件转成 mp3 文件。

1. 先用工具将 mgg 文件转成 ogg 文件，可以通过在线工具 [OpenYYY - https://openyyy.com/](https://openyyy.com/)

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20231016/4933322bfc504a7e82574c67472f533d.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '转 ogg')

2. 下载 ogg 文件，通过 ffmpeg 将 ogg 转成 mp3，命令为 `ffmpeg -i ogg文件 输出mp3文件`，下面的示例中，将老鼠爱大米的 ogg 转成了 mp3 文件：

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20231016/587e2afcba774a5cba89c2d302568ef4.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'ogg convert mp3')

转之后的 mp3 文件用播放器可以正常播放：

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20231016/004eaea8e54d47318ada684c393edf8c.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '正常播放')

**ffmpeg 的在线工具**可以使用 [https://ffmpeg-online.vercel.app/](https://ffmpeg-online.vercel.app/)

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20231016/388e4e1179d9419393db7cf133dcb450.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'ffmpeg 在线工具')

## 参考

+ [How can I convert audio from ogg to mp3?](https://askubuntu.com/questions/442997/how-can-i-convert-audio-from-ogg-to-mp3)
+ [How to Install FFmpeg on Ubuntu 22.04?](https://linuxhint.com/install-ffmpeg-ubuntu22-04/)

