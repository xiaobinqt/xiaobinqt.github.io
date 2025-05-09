---
weight: 5

bookFlatSection: true

bookCollapseSection: false

bookToc: true

title: "Mac"
---

# Mac

## 工具

- [iTerm2安装配置使用指南——保姆级](https://zhuanlan.zhihu.com/p/550022490)
- [奇技淫巧玄妙无穷| M1 mac os(苹果/AppleSilicon)系统的基本操作和设置](https://segmentfault.com/a/1190000039782096)
- [录屏后没声音？这应该是 Mac（苹果电脑） 内录声音最优雅的解决方案了](https://www.youtube.com/watch?v=-aTCbnc-0Dk&ab_channel=Mac%E4%BA%91%E8%AF%BE%E5%A0%82)
- [苹果Mac录屏没声音怎么办？安装LoopBack解决Mac内录电脑系统声音](https://zhuanlan.zhihu.com/p/121026374)

## 常用功能

### 强制退出软件

同时按下以下三个按键：Option（或 Alt）、Command、Esc (Escape)1。或者，从屏幕角落的苹果菜单  中选取“强制退出”。

[如何在 Mac 上强制退出 App](https://support.apple.com/zh-cn/102586)

### 查看隐藏文件

方法一：使用快捷键

在 Finder 中按下：

⌘ Command + ⇧ Shift + .（英文句号）

再次按一次会隐藏它们，相当于开关。

方法二：使用终端命令永久开启

1. 打开「终端 Terminal」
2. 输入以下命令并回车：

```bash
defaults write com.apple.finder AppleShowAllFiles -bool true
killall Finder
```

3. 若想关闭显示隐藏文件：

```bash
defaults write com.apple.finder AppleShowAllFiles -bool false
killall Finder
```

## 查看系统数据占用

最近遇到一个问题，突然磁盘满了，直接显示 no space left on device. 排查了半天也不知道是什么东西把磁盘写满了。

```bash
du -sh ./* ./.??* 2>/dev/null | sort -hr | head -n 10
```

这个命令按照从大到小排序并显示前 10 个最大的文件或目录。

`du` 是一个用于统计磁盘使用量的命令。

- `-s`：汇总（summarize），仅显示每个指定路径的总大小。
- `-h`：以人类可读的格式输出大小（例如 `1.2G`、`345M`、`12K` 等）。
- `./*`：匹配当前目录下的所有非隐藏文件和目录（通配符 `*` 匹配所有文件名，但不包括以 `.` 开头的隐藏文件）。
- `./.??*`：匹配当前目录下的隐藏文件和目录，但只包括以 `.` 开头且文件名长度至少为 3 字符的项（例如 `.git`、`.env`）。具体解释：
    - `.??*` 表示：
        - 第一个 `.`：匹配隐藏文件的开头点。
        - `??`：匹配任意两个字符（确保文件名至少有 2 个字符，避免匹配 `.` 和 `..`）。
        - `*`：匹配剩余的任意字符。
    - 这样可以避免匹配当前目录（`.`）和父目录（`..`），只包括真正的隐藏文件或目录。

`./* ./.??*` 结合在一起，覆盖了当前目录下几乎所有的文件和目录（包括隐藏文件，但排除 `.` 和 `..`）。

- `2>`：重定向标准错误（stderr，文件描述符 2）。
- `/dev/null`：一个特殊的“黑洞”设备文件，丢弃所有写入的数据。作用：忽略 `du` 命令可能产生的错误信息（例如权限不足导致无法访问某些目录）。这确保命令输出只包含有效结果，不会显示错误提示。

**`sort -hr`**，`sort` 命令对输入进行排序。

- **`-h`**：按人类可读的数字排序（human-numeric sort），能够正确比较 `1G`、`500M`、`10K` 等大小单位。
- **`-r`**：反向排序（reverse），使结果从大到小排序（默认是升序）。

`sort -hr` 将 `du` 的输出按照文件/目录大小从大到小排序。

**`head -n 10`**，`head` 命令提取输入的前几行。**`-n 10`**：仅显示前 10 行。这将限制输出，只显示最大的 10 个文件或目录。

```
find . -maxdepth 1 -type f -o -type d -not -name . -not -name .. | xargs du -sh 2>/dev/null | sort -hr | head -n 10
```

列出当前目录下（不包括子目录）文件和目录的大小，按大小从大到小排序，并显示前 10 个结果。

![](https://cdn.xiaobinqt.cn//xiaobinqt.io/20250420/a5eafe5bc5af4994a6cba67196d8afae.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15)

## brew

search 搜索

```
brew search mcrypt
```

## 安装 php

```
brew install shivammathur/php/php@8.2

```

### 安装扩展

- mcrypt

```
brew install shivammathur/extensions/mcrypt@7.2
```

## 安装 hugo

安装指定版本的

[https://github.com/gohugoio/hugo/releases](https://github.com/gohugoio/hugo/releases)

```
wget https://github.com/gohugoio/hugo/releases/download/v0.144.0/hugo_extended_0.144.0_darwin-universal.tar.gz

tar -zxvf hugo_extended_0.144.0_darwin-universal.tar.gz

mv hugo /usr/local/bin
```

安装最新版

```
brew install hugo
```

## 安装 nginx

在 macOS 上，Nginx 的错误日志（error log）默认路径可能因安装方式而异。下面是常见的几种情况：

### 🍎 常见路径（Homebrew 安装）

如果你是用 **Homebrew 安装的 Nginx**（大多数人都是这样装的），那么错误日志的位置通常是：

```
/opt/homebrew/var/log/nginx/error.log    # Apple Silicon (M1/M2/M3)
/usr/local/var/log/nginx/error.log       # Intel Mac
```

你可以用这个命令快速查看当前日志路径：

```bash
grep error_log /opt/homebrew/etc/nginx/nginx.conf
```

或者（Intel Mac）：

```bash
grep error_log /usr/local/etc/nginx/nginx.conf
```


### 🛠️ 自定义日志路径

你也可以在 `nginx.conf` 中找到这行配置：

```nginx
error_log  /path/to/log/error.log  warn;
```

这就是你当前设置的错误日志路径。你可以改成你想要的，比如：

```nginx
error_log  /var/log/nginx/my_error.log  error;
```

记得改完之后：

```bash
nginx -t         # 检查配置
sudo nginx -s reload  # linux 系统使用，重新加载配置
brew services restart nginx # mac 使用 brew 重启
```


### 📖 实时查看日志

你可以用 `tail -f` 实时查看错误日志：

```bash
tail -f /opt/homebrew/var/log/nginx/error.log
```

或者 Intel Mac：

```bash
tail -f /usr/local/var/log/nginx/error.log
```

## Beyond Compare 4 破解方式

在应用程序找到 Beyond Compare，然后右键，点击显示包内容，进入 Contents 目录，然后再进到 MacOs 目录。

![](https://cdn.xiaobinqt.cn//xiaobinqt.io/20250501/e97ba105ba2d47a19771d494a665a9bf.png)

重命名主应用程序 BCompare 更改为 BCompare.real

在这种目录中用终端打开

![](https://cdn.xiaobinqt.cn//xiaobinqt.io/20250501/9ee588af9b014a9b923dff18eff81173.png)

vim 新建 BCompare 文件，文件内容如下：

```shell
#!/bin/bash
rm "/Users/电脑名称/Library/Application Support/Beyond Compare/registry.dat"
"`dirname "$0"`"/BCompare.real $@
```

给与执行权限

```shell
chmod a+x BCompare.real
chmod a+x BCompare
```










