---
title: "VMware 安装 CentOS 7.x"
subtitle: ""

init_date: "2022-04-15T14:42:58+08:00"

date: 2021-03-08

lastmod: 2022-04-18

draft: false

author: "xiaobinqt"
description: "xiaobinqt,vmware,centos 7.9,静态 ip,vmware 安装,vmware 安装 CentOS 7.x,vmware 设置静态 ip,centos7,ifconfig command
not found,修改网卡为 eth0"

featuredImage: ""

reproduce: false

tags: ["CentOS 7.x","VMware"]
categories: ["开发者手册"]
lightgallery: true

toc: true

math:
enable: true
---

<!-- author： xiaobinqt -->
<!-- email： xiaobinqt@163.com -->
<!-- https://xiaobinqt.github.io -->
<!-- https://www.xiaobinqt.cn -->

## 下载镜像

在 CentOS 的官网 [https://wiki.centos.org/Download](https://wiki.centos.org/Download) 可以下载 CentOS 各个版本的镜像文件。

![CentOS Download](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220415/b74714e1b8a14d97898350923f9bdc9a.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'CentOS Download')

包括已经不在维护的各个版本：

![Archived Versions](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220415/ec976869da494f84bf74d765ed21b59c.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'Archived Versions')

也可以去阿里的镜像仓库去下载 [mirrors.aliyun.com/centos](https://mirrors.aliyun.com/centos/)。

## 安装 CentOS 7.9

下载完 [CentOS-7-x86_64-Minimal-2009](https://mirrors.aliyun.com/centos/7.9.2009/isos/x86_64/) 就可以安装了，这里用的是 Minimal
版本，安装完成后，系统中只有最基本的组件，方便学习。

![新建虚拟机](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220415/b3e26ed50cd849c4acb1fd03eda92705.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '新建虚拟机')

![典型配置](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220415/8a9a3656b1f14461847da9924c730acb.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '典型配置')

![选择 ios 文件](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220415/f31b7d2ae48548d9b9273829a75fc4d6.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '选择 ios 文件')

命名虚拟机并选择系统文件保存路径：

![命名虚拟机](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220415/ba19b8c62ee94986985291c00dd5a88c.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '命名虚拟机')

> 如果物理机支持大与 4GB 以上的单文件，可以选择“将虚拟磁盘存储为单个文件”

![指定磁盘容量](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220415/72fc8ae20afe4887809079325a562115.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '指定磁盘容量')

![自定义硬件](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220415/439029d3f584484582121b347112eaa0.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '自定义硬件')

由于服务器用不到声卡，USB 控制器，打印机这些设备，可以将这些设备移除：

![移除硬件](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220415/c13f3ed6b3d5458fbf9c9a676894eb43.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '移除硬件')

![移除后的硬件](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220415/15df2863d25b49d7a76ec9bdc6b617b9.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '移除后的硬件')

![完成](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220415/d5663f41d9ee4c25a9d842ee42d92d17.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '完成')

![开启虚拟机](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220415/476f763d3cbc41d4839429bca8b3175e.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '开启虚拟机')

![Install CentOS7](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220417/c9840008ce6144e5a91e17e33c03d3bf.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'Install CentOS7')

![安装中](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220417/a939c8c699a042aaa1b0cb6bdbd85b60.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '安装中')

![选择语言](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220417/a1e517684d1946fa9f560b4a848eaaff.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '选择语言')

点击 INSTALLATION DESTINATION

![INSTALLATION DESTINATION](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220417/f78e0f23022749eb88895182d245375f.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15)

INSTALLATION DESTINATION 默认值不用改，直接点 Done

![INSTALLATION DESTINATION Done](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220417/0f3fef4c733c499eb1f6690d1421280b.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'INSTALLATION DESTINATION Done')

![Begin Installation](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220417/a9563032d90c46f0aaf001b848b486b7.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'Begin Installation')

设置 ROOT 密码和创建用户

![设置 ROOT 密码和创建用户](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220417/3352639ce0dd4648b3dcebf1b2bc69dd.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '设置 ROOT 密码和创建用户')

![创建用户](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220417/066889c865c44947bde9387c1e5187a1.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '创建用户')

等待安装任务

![等待安装任务](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220417/d411484eb47847dfb51dd5c24ef58de8.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '等待安装任务')

![安装任务完成重启](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220417/154217e8813f421fbb8649a3816d1c79.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '安装任务完成重启')

重启完成登录

![root Login](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220417/3585320091a1411586204f12701ccd94.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'root Login')

## 网络配置

一般新装的**最小化**的 CentOS 7.x 系统是没有网络配置的，而安装命令就是联网下载软件，所以网络配置是必须的。

![ping](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220417/3a7a989e2f68499e853cc206c3eb9a13.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'ping')

CentOS 7.x 的默认网卡是 essxx，我们可以在配置文件 `/etc/syconfig/network-scripts` 中看到：

![network-scripts](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220417/b09768d8763041f0bcefe58d5dbea5c6.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'network-scripts')

可以先把 ifcfg-ensxx 这个文件**备份下**，然后修改 `onboot` 参数从 no 修改为 yes ，保存，重启机器。

![update onboot](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220417/62dffe2555ef424e8f0009b9c3bc7be8.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'update onboot')

重启完后就可以 ping 通网络了：

![ping 2](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220417/5db4c9b9390f4617b8ca1a3e900ffa3f.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'ping 2')

## ifconfig command not found

安装 net-tools 工具

```shell
yum install -y net-tools
```

![net-tools install](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220417/d77b3da7989f4020b5d9a7ee9574e719.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'net-tools install')

![ifconfig](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220417/3e3b4820d5ac4ce0b5883f0be3e547e1.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'ifconfig')

## 修改网卡为 eth0

CentOS 7.x 的网卡不是 eth0 而是 ensxx，这是 CentOS 7.x 的一致性网络设备命名导致的，可以使用以下方式，将网卡名称回到 eth0 格式。

![ensxx](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220417/031a5551677449d8a3e83f3dc02a3562.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'ensxx')

修改配置

```shell
vim /etc/default/grub
```

中添加

```bash
biosdevname=0 net.ifnames=0
```

![biosdevname=0 net.ifnames=0](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220417/ee2294ced6d54804ac88fe49edabd248.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'biosdevname=0 net.ifnames=0')

执行命令

```shell
grub2-mkconfig -o /boot/grub2/grub.cfg
```

![执行命令](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220417/15180738ff9745dda45fd7060d61efba.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '执行命令')

`reboot` 重启机器

![修改成功](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220417/05fde4e3946c43c88de3b9e063408e1b.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '
修改成功')

## 设置静态 IP

NAT 模式是 VMware 虚拟机默认使用的模式，其最大的优势就是虚拟机接入网络非常简单，只要物理机可以访问网络，虚拟机就可以访问网络。网络结构如下图：

![NAT模式](https://img-blog.csdnimg.cn/20200303215932129.png 'NAT模式')

所谓的静态 ip ，就是设置后固定不变的，因为在真实环境中，需要为所有的服务器配置静态 ip，从而确保通过一个 ip 地址只能找到一台服务器。

### 设置

在修改配置文件之前，为了防止配置出错，建议提前备份配置文件 `ifcfg-eth0`。

```shell
cp /etc/sysconfig/network-scripts/ifcfg-ens32 /etc/sysconfig/network-scripts/ifcfg-ens32.bak
```

我们需要把 `ifcfg-eth0` 配置文件中的 `BOOTPROTO` 的值设置为 `static`，将 `IPADDR`(IP 地址)的值设置为其所在的子网中正确的，无冲突的 ip 地址即可。

在 NAT 模式中，我们需要找到 4 个地址才能确定我们的无冲突的 ip 到底是哪些。

+ 子网 ip
+ VMnet8 虚拟网卡 ip
+ NAT 网关 ip
+ DHCP 地址池

接下来找这几个参数：

![图 1](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220418/8197b0164ca24015b522f4ba13b5f04a.png '图 1')

![图 2](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220418/fc5eb5ca96ca4bd29b796b8f32fbec1b.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '图 2')


[//]: # (![图 2]&#40;https://img-blog.csdnimg.cn/20200303221248639.png '图 2'&#41;)

点击【NAT设置】查看子网掩码和网关 IP。点击【DHCP 设置】查看起始 IP 地址和结束 IP 地址。

![图 3](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220418/bc1b37ed3e9c43e39c6988342b746b0d.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '图 3')


[//]: # (![图 3]&#40;https://img-blog.csdnimg.cn/20200303221204559.png '图 3'&#41;)

![图 4](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220418/59acd1549914426b9375c5850e8b5b36.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '图 4')

[//]: # (![图 4]&#40;https://img-blog.csdnimg.cn/20200303221358852.png '图 4'&#41;)

打开物理机的 cmd 输入 `ipconfig` 命令：

![图 5](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220418/655158e74b14445cb92005f842ed225e.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '图 5')


[//]: # (![图 5]&#40;https://img-blog.csdnimg.cn/20200303221513492.png '图 5'&#41;)

所以，除去这几个地址，`192.168.48.3` ~ `192.168.48.127` 范围内的 ip 都可以作为静态 ip 使用。

`vi ifcfg-eth0` 需要修改的地方为：

1. 将 `ONBOOT` 改为 `yes`
2. `BOOTPROTO` 由 `dhcp` 改为 `static`
3. 增加 `IPADDR`(ip 地址)
4. 增加 `NETMASK`(子网掩码)
5. 增加 `GATEWAY`(网关)
6. 增加 `DNS1`(首选域名服务器)

其中，网关不设置，虚拟机只能在局域网内访问，无法访问外部网络。DNS 不设置则无法解析域名。 **DNS 可以设置成跟网关一样的地址**。

![图 6](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220418/3e52c6df0d1c40678ad826e6a3d995c1.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '图 6')


[//]: # (![图 6]&#40;https://cdn.xiaobinqt.cn/xiaobinqt.io/20220418/eed9c7a6a3f54962ad900e35f0ab543e.png '图 6'&#41;)


[//]: # (![图 6]&#40;https://img-blog.csdnimg.cn/20200303223806494.png '图 6'&#41;)

设置完成后执行：`systemctl restart network ` 命令使配置生效。

![图 7](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220418/b5384ea25f6a4345b041f0d488c8ff6c.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '图 7')


[//]: # (![图 7]&#40;https://img-blog.csdnimg.cn/20200303224727752.png '图 7'&#41;)

[//]: # (生效后，可以通过以下命令查看当前使用的默认网关和 dns 服务器：)

[//]: # (![图 8]&#40;https://img-blog.csdnimg.cn/20200303224849317.png '图 8'&#41;)

### 访问测试

### 物理机测试

在物理机中 ping 虚拟机 ip 地址：

![图 8](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220418/32c855d6ab164f8293c14191716296e4.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '图 8')


[//]: # (![图 9]&#40;https://img-blog.csdnimg.cn/20200303225047693.png '图 9'&#41;)

物理机共向 ip 地址 `192.168.48.8` 发送了 4 次 ping 请求，4 次都是成功的，发送的数据包为 32 字节，TTL(生存时间值)为 64，其中 TTL 在发送时的默认值为 64，每经过一个路由则减 1
，此次显示最终结果为 64 说明中间没有经过路由。

### 虚拟机测试

![图 9](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220418/356ddc9263ac44619d2c003fbcc146f5.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '图 9')


[//]: # (![图 10]&#40;https://img-blog.csdnimg.cn/20200303225756338.png '图 10'&#41;)

### 说明

因为我把默认网卡从 ensxx 改成了 eth0 所以在修改静态 ip 是把配置文件也改成了 ifcfg-eth0

![图 10](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220418/a1e71dfe0e6948648eed5ac052fdd3e9.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '图 10')

[//]: # (![图 10]&#40;https://cdn.xiaobinqt.cn/xiaobinqt.io/20220418/b9a48b92ab7c4cd08020f824171c949b.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '图 10'&#41;)

## 参考

+ [How To Configure Static IP Address in CentOS 7 / RHEL 7](https://www.itzgeek.com/how-tos/linux/centos-how-tos/how-to-configure-static-ip-address-in-centos-7-rhel-7-fedora-26.html)


