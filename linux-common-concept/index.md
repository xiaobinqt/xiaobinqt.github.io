# Linux 常用命令备忘


<!-- author： xiaobinqt -->
<!-- email： xiaobinqt@163.com -->
<!-- https://xiaobinqt.github.io -->
<!-- https://www.xiaobinqt.cn -->

## linux 和 unix 的区别

[Linux和Unix之间的区别是什么？](https://baijiahao.baidu.com/s?id=1725517662598994230&wfr=spider&for=pc)

## musl 和 glibc 的区别

musl 和 glibc 都是 Linux 的标准库，区别是 musl 是一个 mini 版本，或是叫做基于 glibc 的库，而 glibc 是一个完整版本。

## ubuntu

### 获取系统代号

```shell
lsb_release -cs
```

![获取系统代号](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220507/6fbea271a68b46a994188ae23a6eb291.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '获取系统代号')

### 内核版本信息

```shell
uname -a
# 或者
cat /proc/version
```

![内核版本信息](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220507/5649c120ada14e0193593b847d46d652.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '内核版本信息')

## lsb_release

[LSB]^(Linux Standard Base) 是 Linux 标准库的缩写， `lsb_release` 命令 用来与具体 Linux 发行版相关的 Linux 标准库信息。

CentOS 最小化安装时默认没有这个命令，需要安装 lsb_release 使用命令，:point_down:以下是常见系统的安装 lsb_release 命令。

### Ubuntu, Debian

```shell
sudo apt-get update && sudo apt-get install lsb-core
```

### CentOS

```shell
sudo yum update && sudo yum install redhat-lsb-core
```

### Fedora

```shell
sudo dnf update && sudo dnf install redhat-lsb-core
```

### 参数

![lsb_release 参数](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220507/287b2dcba4694769b879bcc0e19e8d68.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'lsb_release 参数')

+ `-v`：显示与你 Linux 发行版相对应的 Linux 版本库描述信息。Linux 版本库模块描述使用冒号 `:` 分分隔

+ `-i`：显示该 Linux 系统的发行商

+ `-d`：显示 Linux 发行版描述信息

+ `-r`：显示当前 Linux 发行版版本号

+ `-c`：显示当前 Linux 发行版[代号]^(codename)

+ `-a`：显示全部信息，包括 LSB、版本号、代号、版本描述信息

## linux 常用命令

以下命令都是笔者在工作中用到过的，因为不是专业的 shell 工程师，所以遍通过笔记记录下来防止忘记。

### cut

`cut` 命令从文件的每一行剪切字节、字符和字段并将这些字节、字符和字段写至标准输出。

+ `-d` ：自定义分隔符，默认为制表符。
+ `-f` ：与`-d`一起使用，指定显示哪个区域。

![cut -d -f](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220718/a050c61a3f2b410da7641f8972811dbb.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'cut -d -f')

### grep

```shell
grep -v name # 表示查看除了含有name之外的行内容
```

![grep -v](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220718/a7c681db9d6b461f8bbce757a75b9eec.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'grep -v')

### curl

```shell
curl -o /dev/null -s -w %{http_code}  https://www.baidu.com
```

+ `-o` ：输出文件，默认为标准输出。
+ `-s` ：屏蔽掉输出，不显示任何内容。
+ `-w` ：输出http状态码。

### 数组操作

```shell
#!/bin/bash

let a=0
for i in $(seq 1 10);do
  array[a]=$i
  let a++
done

echo "一个添加多个元素：e f g"
array+=(e f g)

echo "数组所有元素 ${array[*]}"
# shellcheck disable=SC2145
echo "数组所有下标: ${!array[@]}"
echo "数组长度为：${#array[*]}"
echo "数组第一个元素为：${array[0]}"

echo "删除数组第二个元素"
# shellcheck disable=SC2184
unset array[1]
echo "再次数组所有元素 ${array[*]}"

```

![数组操作](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220718/45e1e48fc0ce4d1ca29cb4593a79257b.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '数组操作')

### sed

#### `-e`多重编辑

```shell
tail /etc/services | sed -e '1,2d' -e 's/blp5/test/'
```

+ `1,2d`：删除第一行和第二行

+ `s/blp5/test/`：将`blp5`替换为`test`

可以用`;`分隔多个命令:point_down:效果一样：

```shell
tail /etc/services | sed  '1,2d;s/blp5/test/'
```

![sed多行编辑](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220719/ba6358760d314a4aa69c9fd10e5ad836.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'sed多行编辑')

#### 读取下一行

`n` 读取下一行到模式空间

```shell
seq 6 | sed -n 'n;p'
```

sed 先读取第一行 1，执行 n 命令，获取下一行 2，此时模式空间是 2，执行 p 命令，打印模式空间。现在模式空间是 2， sed 再读取 3，执行 n 命令，获取下一行 4，此时模式空间为 4，执行 p 命令，以此类推。

![打印偶数](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220719/22639dc6e1b048a280f0af7beb2c1fd3.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '打印偶数')

## 参考

+ [curl -w,–write-out参数详解](https://blog.csdn.net/workdsz/article/details/78489101)
















