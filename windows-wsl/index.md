# Windows 10 专业版使用 WSL


<!-- author： xiaobinqt -->
<!-- email： xiaobinqt@163.com -->
<!-- https://xiaobinqt.github.io -->
<!-- https://www.xiaobinqt.cn -->

## 什么是 wsl

Windows Subsystem for Linux（WSL）是一个在 Windows 10+ 上能够运行原生 Linux 二进制可执行文件的兼容层。

与 WSL1 相比，WSL 2 使用更新、更强大的虚拟化技术在轻量级实用工具虚拟机 (VM) 中运行 Linux 内核。

## 安装

我是 win10 专业版，其他版本的 win10 也类似，不过**推荐使用专业版**。

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230320/a15dfa3e82854382859261a104cd8f3c.png '电脑版本')

1. 进入 windows 终端
2. `wsl -l -o`查看可安装的发行版
3. 执行`wsl --set-default-version 2`将 WSL 默认版本调整为 WSL2
4. `wsl --install --d NAME`即可安装。如： `wsl --install --d ubuntu-20.04`可安装 ubuntu20.04
5. `wsl -l -v`可查看安装的发行版的 WSL 版本

注销（卸载）当前安装的 Linux 的 Windows 子系统可以使用：

```shell
wsl --unregister 名称
```

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230320/0808f63a623d4c44aa9971e854b7f2e5.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '卸载 wsl')

对于已安装的 wsl 版本，从 wsl1 切换到 wsl2 可以使用：

```shell
wsl --set-version 名称 2
```

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230222/38eff9e474cc40b0a43068cec25fe08a.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '切换 wsl2')

## no_proxy 设置

win10 的 no_proxy 可以直接添加系统环境变量：

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230705/64a916b5dc924109aef92251094661d3.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'win10 no_proxy')

WSL no_proxy 也可以通过添加环境变量方式：

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230705/f562263377664765a1d56204777d5168.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'wsl no_proxy')

## 参考

+ [WSL 的基本命令](https://learn.microsoft.com/zh-cn/windows/wsl/basic-commands)
+ [如何在 Windows 11 中安装 Windows Subsystem for Linux（WSL）](https://www.sysgeek.cn/windows-11-install-windows-subsystem-for-linux/)
+ [windows clash 设置代理](https://gist.github.com/libChan/3a804a46b532cc326a2ee55b27e8ac19)
+ [windows 的cmd设置代理方法](https://blog.csdn.net/SHERLOCKSALVATORE/article/details/123599042)
+ [Windows 10/11 安装 WSL2 的简单方法](https://www.jianshu.com/p/6e7488440db2)
+ [Win11卸载WSL，卸载Windows子系统](https://blog.csdn.net/admans/article/details/125071913)

