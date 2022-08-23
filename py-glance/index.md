# python 学习笔记


<!-- author： xiaobinqt -->
<!-- email： xiaobinqt@163.com -->
<!-- https://xiaobinqt.github.io -->
<!-- https://www.xiaobinqt.cn -->

## 安装 pip

### 安装 pip3

环境为 `armv7l`

```shell
apt-get install python3-pip
```

![安装 pip3](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220506/0c0124fe0fc94492a6784befd8c02b76.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '安装 pip3')

![安装成功](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220506/e371015510e3492d9f2668c333b6316d.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '安装成功')

### 安装 pip

对于 python2 来说可以安装 pip：

```shell
apt install python-pip
```

## conda 和 pip 的区别

+ pip 仅仅是包管理工具，而 conda 不仅仅是包管理工具，conda 的功能比 pip 更多。

+ pip 仅限于 python 包的安装更新卸载，conda 包括且不限于 Python、C、R 等语言。

+ pip 能安装 pypi 里的一切 python 包。而 conda 可安装的 python 包数量相比 pip 要少很多。

+ pip 不支持创建 python 虚拟环境，得安装了 virtualenv 包才可以，而 conda 支持创建 python 虚拟环境。

+ `pip install -r requirements.txt`更加流畅，而 `conda install -r`时一旦未找到某个包，便会中断。

## 镜像

### 国内镜像源

+ `https://pypi.douban.com/simple/` 豆瓣
+ `https://mirrors.aliyun.com/pypi/simple/` 阿里
+ `https://pypi.hustunique.com/simple/` 华中理工大学
+ `https://pypi.sdutlinux.org/simple/` 山东理工大学
+ `https://pypi.mirrors.ustc.edu.cn/simple/` 中国科学技术大学
+ `https://pypi.tuna.tsinghua.edu.cn/simple` 清华

### 使用镜像安装

可以参考这篇文章[https://www.runoob.com/w3cnote/pip-cn-mirror.html](https://www.runoob.com/w3cnote/pip-cn-mirror.html)

## 更新 pip3

```shell
pip3 install --upgrade pip
```

或者

```shell
python3 -m pip install --upgrade pip
```

## 参考

+ [python conda安装与使用教程](https://blog.csdn.net/linxinfa/article/details/108914011)





