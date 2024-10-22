# python virtualenvwrapper 使用


<!-- author： xiaobinqt -->
<!-- email： xiaobinqt@163.com -->
<!-- https://xiaobinqt.github.io -->
<!-- https://www.xiaobinqt.cn -->


Virtualenvwrapper 是一个用于管理 Python 虚拟环境的工具，它为创建、切换和删除虚拟环境提供了一组方便的命令，并通过简化管理多个虚拟环境的过程来提高开发效率。

## windows

### 安装

可以使用 pip 安装 Virtualenvwrapper：

```shell
pip install virtualenvwrapper-win

```

安装完成后，需要设置一些环境变量。创建一个名为`WORKON_HOME`的环境变量，用于指定虚拟环境的存储位置。例如，可以将其设置为`D:\python\venv`。

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230526/7e68bb0eecb1482b88a6ab962986487a.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'WORKON_HOME')

在安装并配置好 Virtualenvwrapper 后，打开一个**新的**命令行窗口，以便新的环境变量生效。

### 创建虚拟环境

使用 mkvirtualenv 命令创建一个新的虚拟环境。例如，要创建一个名为 go.src 的虚拟环境，可以运行以下命令：

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230526/9b1e834a1bff4c54b551bedd9b49e384.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'mkvirtualenv')

### 设置虚拟环境存储位置

修改系统环境变量，增加一个名为`WORKON_HOME`的变量。

![WORKON_HOME](https://cdn.xiaobinqt.cn/xiaobinqt.io/20241022/2cac06d1965b4b2096947589c2f14b37.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'WORKON_HOME')

### 查看所有虚拟环境

要列出所有可用的虚拟环境，可以使用 workon 命令，不带任何参数运行它：

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230526/cce01cbdc5254cee8b9115e2bd2cb30d.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'workon')

### 激活虚拟环境

创建虚拟环境后，可以使用 workon 命令来激活该环境。例如，要激活名为 go.src 的虚拟环境，可以运行以下命令：

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230526/1109c7cf3de9479081bbf3aeafdf4c61.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '激活虚拟环境')

### 删除虚拟环境

如果要删除不再需要的虚拟环境，可以使用 rmvirtualenv 命令，后跟要删除的虚拟环境的名称。例如，要删除名为 myenv 的虚拟环境，可以运行以下命令：

```shell
rmvirtualenv myenv

```

### 退出虚拟环境

可以使用 deactivate 命令退出虚拟环境：

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230526/3a979dd3e94942f1aaeaa2a2d54a967e.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '退出虚拟环境')

## mac 使用

这是我的 mac 型号

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20240720/35469fe5f0374e4eae05c947d23117d6.png 'mac 型号')

通过 brew 安装的的 python 版本是 3.12.4。

其实可以直接使用 python3 的 venv 模块来创建一个虚拟环境。假设需要创建一个名为 myenv 的虚拟环境：

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20240720/19e8da1758524258a1c8cd133e9513d2.png '创建虚拟环境')

激活虚拟环境后，你可以在这个环境中自由安装 Python 包而不会影响系统的 Python 安装：

```shell
source ~/myenv/bin/activate
```

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20240720/5bce893b9764480a9e9d97c0b5139cd6.png '激活虚拟环境')

在激活的虚拟环境中，可以运行 pip 安装包：

```shell
pip install --upgrade pip
```

现在可以在虚拟环境中安装需要的任何包。退出虚拟环境可以直接使用 deactivate 命令。

## pycharm 配置

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230526/856d78b8073b47dc9d57874624a7ea6b.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15)

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230526/4093998f664f4d47ad95d563cbfab817.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15)

## 参考

- [mkvirtualenv命令改变虚拟环境存储位置](https://blog.csdn.net/qq_41649001/article/details/106454327)









