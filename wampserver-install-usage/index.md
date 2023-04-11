# wampserver 的安装和使用


<!-- author： xiaobinqt -->
<!-- email： xiaobinqt@163.com -->
<!-- https://xiaobinqt.github.io -->
<!-- https://www.xiaobinqt.cn -->


本地开发 php 环境推荐使用 wampserver，下载地址为 [WampServer download | SourceForge.net](https://sourceforge.net/projects/wampserver/)

当然国产的 phpStudy 也可以，个人喜好问题。

## 下载

安装 wampserver 之前我们需要先安装 Visual C++ Redistributable for Visual Studio，这是 visual 2015
的下载地址 [Visual C++ Redistributable for Visual Studio 2015 from Official Microsoft Download Center](https://www.microsoft.com/en-us/download/details.aspx?id=48145)
，根据自己的版本下载对应的版本。

![Visual Studio](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230411/1e2f0f30d30b4f918136fc3b6ea9583d.png 'Visual Studio')

visual c++ redistributable for visual studio 2012 在很多时候已经不能用了。

我安装的是 64 位的 wampserver，所以下载对应的 visual C++：

![visual C++ 图 1](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230411/cd4d8a8ff6214663b4ba2b70df7957e2.png 'visual C++ 图 1')

![visual C++ 图 2](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230411/05a4f7bfbb0e40be9e94573cb93ccc1e.png 'visual C++ 图 2')

之后安装 wampserver

![安装 wampserver](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230411/bf7b661cfa4e47179bc03c3649d3e423.png '安装 wampserver')

在安装过程中会让你选择默认的浏览器和编辑器。

## 配置

如果有需要可以修改 wampserver 的根目录

1. 打开 wampserver 的安装目录，在打开里面的 script 文件夹，用记事本打开里面的 `config.inc.php`
   ,找到 `$wwwDir = $c_installDir.'/www'` 改成希望的目录就行了。
   比如改成 `D:\website`，对应的代码就是 `$wwwDir = 'D:/website'`；然后关闭 wampserver。

> （注意，windows下表示路径的 `\`在这里必须改为 `/`）

![wwwDir](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230411/f8dba744064643a7946d8c3e92366c24.png 'wwwDir')

2. 打开 Apach 下面的 `httpd.conf` 文件，路径示例

![httpd.conf](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230411/a45e7c965a8348ec9f355eeeceea918a.png 'httpd.conf')

寻找 DocumentRoot，把后面的值改成我们实际网站需要的路径，再寻找 `<Directory "c:/wamp/www/">` 修改成相同的路径

![DocumentRoot](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230411/fc931693d16e4dce98d1ae6babdd4937.png 'DocumentRoot')

配置虚拟主机 VirtualHost 示例

```shell
<VirtualHost *>
    ServerAdmin root@localhost
    DocumentRoot "D:\projects\pc-mes\src\public"
    ServerName pc-mes.local
    ErrorLog "d:\wamp64\www\pc-mes.localhost-error.log"
    CustomLog "d:\wamp64\www\pc-mes.localhost.log" common
</VirtualHost>
```

访问示例

![访问示例](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230411/16f1c29cdfea48dbaa297f972b81b723.png '访问示例')









