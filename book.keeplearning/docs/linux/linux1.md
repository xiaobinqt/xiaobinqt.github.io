---
weight: 1

bookFlatSection: true

bookCollapseSection: false

bookToc: true

title: "Linux（一）"
---

# Linux（一）

## 常用操作以及概念

### 快捷键

+ Tab：命令和文件名补全；
+ Ctrl+C：中断正在运行的程序；
+ Ctrl+D：结束键盘输入（End Of File，EOF）

### 求助

#### 1. --help

指令的基本用法与选项介绍。

#### 2. man

man 是 manual 的缩写，将指令的具体信息显示出来。

当执行`man date`时，有 DATE(1) 出现，其中的数字代表指令的类型，常用的数字及其类型如下：

| 代号  | 	类型                         | 
|-----|-----------------------------|
| 1	  | 用户在 shell 环境中可以操作的指令或者可执行文件 |
| 5	  | 配置文件                        |
| 8	  | 系统管理员可以使用的管理指令              |

#### 3. info

info 与 man 类似，但是 info 将文档分成一个个页面，每个页面可以跳转。

#### 4. doc

/usr/share/doc 存放着软件的一整套说明文件。

### 关机

#### 1. who

在关机前需要先使用 who 命令查看有没有其它用户在线。

#### 2. sync

为了加快对磁盘文件的读写速度，位于内存中的文件数据不会立即同步到磁盘，因此关机之前需要先进行 sync 同步操作。

#### 3. shutdown

```
## shutdown [-krhc] 时间 [信息]
-k ： 不会关机，只是发送警告信息，通知所有在线的用户
-r ： 将系统的服务停掉后就重新启动
-h ： 将系统的服务停掉后就立即关机
-c ： 取消已经在进行的 shutdown
```

### PATH

可以在环境变量 PATH 中声明可执行文件的路径，路径之间用 : 分隔。

```
/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/home/dmtsai/.local/bin:/home/dmtsai/bin
```

### sudo

sudo 允许一般用户使用 root 可执行的命令，不过只有在 /etc/sudoers 配置文件中添加的用户才能使用该指令。

### 包管理工具

RPM 和 DPKG 为最常见的两类软件包管理工具：

+ RPM 全称为 Redhat Package Manager，最早由 Red Hat 公司制定实施，随后被 GNU 开源操作系统接受并成为许多 Linux 系统的既定软件标准。YUM 基于 RPM，具有依赖管理和软件升级功能。
+ 与 RPM 竞争的是基于 Debian 操作系统的 DEB 软件包管理工具 DPKG，全称为 Debian Package，功能方面与 RPM 相似。

### 发行版

Linux 发行版是 Linux 内核及各种应用软件的集成版本。

| 基于的包管理工具	 | 商业发行版	   | 社区发行版           |
|-----------|----------|-----------------|
| RPM	      | Red Hat	 | Fedora / CentOS |
| DPKG	     | Ubuntu	  | Debian          |

### VIM 三个模式

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20221223/922f08bad9444c9b9933b218edb2ce3a.png)

+ 一般指令模式（Command mode）：VIM 的默认模式，可以用于移动游标查看内容；
+ 编辑模式（Insert mode）：按下`i`等按键之后进入，可以对文本进行编辑；
+ 指令列模式（Bottom-line mode）：按下`:`按键之后进入，用于保存退出等操作。

在指令列模式下，有以下命令用于离开或者保存文件。

| 命令    | 	作用                                   |
|-------|---------------------------------------|
| :w	   | 	写入磁盘                                 |
| :w!   | 		当文件为只读时，强制写入磁盘。到底能不能写入，与用户对该文件的权限有关 |
| :q	   | 	离开                                   |
| :q!   | 		强制离开不保存                             |	
| :wq	  | 	写入磁盘后离开                              |	
| :wq!	 | 	强制写入磁盘后离开                            |	

### GNU

GNU 计划，译为革奴计划，它的目标是创建一套完全自由的操作系统，称为 GNU，其内容软件完全以 GPL 方式发布。其中 GPL 全称为 GNU 通用公共许可协议（GNU General Public License），包含了以下内容：

+ 以任何目的运行此程序的自由；
+ 再复制的自由；
+ 改进此程序，并公开发布改进的自由。

### 开源协议

+ [Choose an open source license(opens new window)](https://choosealicense.com/)
+ [如何选择开源许可证？](http://www.ruanyifeng.com/blog/2011/05/how_to_choose_free_software_licenses.html)

## 磁盘

### 磁盘接口

#### 1. IDE

IDE（ATA）全称 Advanced Technology Attachment，接口速度最大为 133MB/s，因为并口线的抗干扰性太差，且排线占用空间较大，不利电脑内部散热，已逐渐被 SATA 所取代。

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20221223/0c949e06d9ba4da5845537b484a64384.png)

#### 2. SATA

SATA 全称 Serial ATA，也就是使用串口的 ATA 接口，抗干扰性强，且对数据线的长度要求比 ATA 低很多，支持热插拔等功能。SATA-II 的接口速度为 300MB/s，而 SATA-III 标准可达到 600MB/s 的传输速度。SATA 的数据线也比 ATA 的细得多，有利于机箱内的空气流通，整理线材也比较方便。

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20221223/a33b90d030ea4e66836a411ef116b9ad.png)

#### 3. SCSI

SCSI 全称是 Small Computer System Interface（小型机系统接口），SCSI 硬盘广为工作站以及个人电脑以及服务器所使用，因此会使用较为先进的技术，如碟片转速 15000rpm 的高转速，且传输时 CPU 占用率较低，但是单价也比相同容量的 ATA 及 SATA 硬盘更加昂贵。

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20221223/6c1853ebc100480e8aace7ece58f17e0.png)

### 磁盘的文件名

Linux 中每个硬件都被当做一个文件，包括磁盘。磁盘以磁盘接口类型进行命名，常见磁盘的文件名如下：

+ IDE 磁盘：/dev/hd[a-d]
+ SATA/SCSI/SAS 磁盘：/dev/sd[a-p]

其中文件名后面的序号的确定与系统检测到磁盘的顺序有关，而与磁盘所插入的插槽位置无关。

## 分区

### 分区表

磁盘分区表主要有两种格式，一种是限制较多的 MBR 分区表，一种是较新且限制较少的 GPT 分区表。

#### 1. MBR

MBR 中，第一个扇区最重要，里面有主要开机记录（Master boot record, MBR）及分区表（partition table），其中主要开机记录占 446 bytes，分区表占 64 bytes。

分区表只有 64 bytes，最多只能存储 4 个分区，这 4 个分区为主分区（Primary）和扩展分区（Extended）。其中扩展分区只有一个，它使用其它扇区来记录额外的分区表，因此通过扩展分区可以分出更多分区，这些分区称为逻辑分区。

Linux 也把分区当成文件，分区文件的命名方式为：磁盘文件名 + 编号，例如 /dev/sda1。注意，逻辑分区的编号从 5 开始。

#### 2. GPT

扇区是磁盘的最小存储单位，旧磁盘的扇区大小通常为 512 bytes，而最新的磁盘支持 4 k。GPT 为了兼容所有磁盘，在定义扇区上使用逻辑区块地址（Logical Block Address, LBA），LBA 默认大小为 512 bytes。

GPT 第 1 个区块记录了主要开机记录（MBR），紧接着是 33 个区块记录分区信息，并把最后的 33 个区块用于对分区信息进行备份。这 33 个区块第一个为 GPT 表头纪录，这个部份纪录了分区表本身的位置与大小和备份分区的位置，同时放置了分区表的校验码 (CRC32)，操作系统可以根据这个校验码来判断 GPT 是否正确。若有错误，可以使用备份分区进行恢复。

GPT 没有扩展分区概念，都是主分区，每个 LBA 可以分 4 个分区，因此总共可以分 4 * 32 = 128 个分区。

MBR 不支持 2.2 TB 以上的硬盘，GPT 则最多支持到 2^33 TB = 8 ZB。

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20221223/19aaac15173b43e4af24eb7d0689ba52.png)

### 开机检测程序

#### 1. BIOS

BIOS（Basic Input/Output System，基本输入输出系统），它是一个固件（嵌入在硬件中的软件），BIOS 程序存放在断电后内容不会丢失的只读内存中。

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20221223/91193eb72c704b8882e37424d6d70c6f.png)

BIOS 是开机的时候计算机执行的第一个程序，这个程序知道可以开机的磁盘，并读取磁盘第一个扇区的主要开机记录（MBR），由主要开机记录（MBR）执行其中的开机管理程序，这个开机管理程序会加载操作系统的核心文件。

主要开机记录（MBR）中的开机管理程序提供以下功能：选单、载入核心文件以及转交其它开机管理程序。转交这个功能可以用来实现多重引导，只需要将另一个操作系统的开机管理程序安装在其它分区的启动扇区上，在启动开机管理程序时，就可以通过选单选择启动当前的操作系统或者转交给其它开机管理程序从而启动另一个操作系统。

下图中，第一扇区的主要开机记录（MBR）中的开机管理程序提供了两个选单：M1、M2，M1 指向了 Windows 操作系统，而 M2 指向其它分区的启动扇区，里面包含了另外一个开机管理程序，提供了一个指向 Linux 的选单。

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20221223/d26e47410ef54d779c44bea562a09c5b.png)

安装多重引导，最好先安装 Windows 再安装 Linux。因为安装 Windows 时会覆盖掉主要开机记录（MBR），而 Linux 可以选择将开机管理程序安装在主要开机记录（MBR）或者其它分区的启动扇区，并且可以设置开机管理程序的选单。

#### 2. UEFI

BIOS 不可以读取 GPT 分区表，而 UEFI 可以。

## 文件系统

### 分区与文件系统

对分区进行格式化是为了在分区上建立文件系统。一个分区通常只能格式化为一个文件系统，但是磁盘阵列等技术可以将一个分区格式化为多个文件系统。

### 组成

最主要的几个组成部分如下：

+ inode：一个文件占用一个 inode，记录文件的属性，同时记录此文件的内容所在的 block 编号；
+ block：记录文件的内容，文件太大时，会占用多个 block。

除此之外还包括：

+ superblock：记录文件系统的整体信息，包括 inode 和 block 的总量、使用量、剩余量，以及文件系统的格式与相关信息等；
+ block bitmap：记录 block 是否被使用的位图。

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20221223/160be039582242049c3f53c15d4d5258.png)

### 文件读取

对于 Ext2 文件系统，当要读取一个文件的内容时，先在 inode 中查找文件内容所在的所有 block，然后把所有 block 的内容读出来。

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20221223/92608f9da3a74fb1b4d99a2c68e7d046.png)

而对于 FAT 文件系统，它没有 inode，每个 block 中存储着下一个 block 的编号。

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20221223/cdc5220c4fbc4781af440217a4fc0135.png)

### 磁盘碎片

指一个文件内容所在的 block 过于分散，导致磁盘磁头移动距离过大，从而降低磁盘读写性能。

### block

在 Ext2 文件系统中所支持的 block 大小有 1K，2K 及 4K 三种，不同的大小限制了单个文件和文件系统的最大大小。

| 大小     | 	1KB  | 	2KB   | 	4KB  |
|--------|-------|--------|-------|
| 最大单一文件 | 	16GB | 	256GB | 	2TB  |
| 最大文件系统 | 	2TB	 | 8TB    | 	16TB |

一个 block 只能被一个文件所使用，未使用的部分直接浪费了。因此如果需要存储大量的小文件，那么最好选用比较小的 block。

### inode

inode 具体包含以下信息：

+ 权限 (read/write/excute)；
+ 拥有者与群组 (owner/group)；
+ 容量；
+ 建立或状态改变的时间 (ctime)；
+ 最近读取时间 (atime)；
+ 最近修改时间 (mtime)；
+ 定义文件特性的旗标 (flag)，如 SetUID...；
+ 该文件真正内容的指向 (pointer)。

inode 具有以下特点：

+ 每个 inode 大小均固定为 128 bytes (新的 ext4 与 xfs 可设定到 256 bytes)；
+ 每个文件都仅会占用一个 inode。

inode 中记录了文件内容所在的 block 编号，但是每个 block 非常小，一个大文件随便都需要几十万的 block。而一个 inode 大小有限，无法直接引用这么多 block 编号。因此引入了间接、双间接、三间接引用。间接引用让 inode 记录的引用 block 块记录引用信息。

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20221223/88c9cbcae9a343bb9bdb2b6ee3b0f1e2.png)

### 目录

建立一个目录时，会分配一个 inode 与至少一个 block。block 记录的内容是目录下所有文件的 inode 编号以及文件名。

可以看到文件的 inode 本身不记录文件名，文件名记录在目录中，因此新增文件、删除文件、更改文件名这些操作与目录的写权限有关。

### 日志

如果突然断电，那么文件系统会发生错误，例如断电前只修改了 block bitmap，而还没有将数据真正写入 block 中。

ext3/ext4 文件系统引入了日志功能，可以利用日志来修复文件系统。

### 挂载

挂载利用目录作为文件系统的进入点，也就是说，进入目录之后就可以读取文件系统的数据。

### 目录配置

为了使不同 Linux 发行版本的目录结构保持一致性，Filesystem Hierarchy Standard (FHS) 规定了 Linux 的目录结构。最基础的三个目录如下：

+ / (root, 根目录)
+ /usr (unix software resource)：所有系统默认软件都会安装到这个目录；
+ /var (variable)：存放系统或程序运行过程中的数据文件。

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20221223/2219bc86741241ec8ccbfe7c6e500036.png)





