---
title: "阿里云 SSL 免费证书使用"

date: 2019-06-07

lastmod: 2022-03-16

draft: false

author: "xiaobinqt"
description: "阿里云,SSL,免费证书使用,aliyun,ali,证书,TLS"
resources:

- name: ""
  src: ""

tags: ["SSL","aliyun"]
categories: ["开发者手册"]
lightgallery: true

toc:
auto: false

math:
enable: true
---

## 申请

证书[申请地址](https://common-buy.aliyun.com/?spm=5176.2020520163.cas.20.165a56a7xopCbo&commodityCode=cas#/buy)

![在这里插入图片描述](https://img-blog.csdnimg.cn/20190607203929789.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3hpYW9iaW5xdA==,size_16,color_FFFFFF,t_70 " ")

申请完成页面

![在这里插入图片描述](https://img-blog.csdnimg.cn/20190607204004466.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3hpYW9iaW5xdA==,size_16,color_FFFFFF,t_70 " ")

将主机记录解析

![在这里插入图片描述](https://img-blog.csdnimg.cn/20190607204129284.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3hpYW9iaW5xdA==,size_16,color_FFFFFF,t_70 " ")
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190607204157300.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3hpYW9iaW5xdA==,size_16,color_FFFFFF,t_70 " ")
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190607204230499.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3hpYW9iaW5xdA==,size_16,color_FFFFFF,t_70 " ")

将主机记录和记录值填写

![在这里插入图片描述](https://img-blog.csdnimg.cn/2019060720435450.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3hpYW9iaW5xdA==,size_16,color_FFFFFF,t_70 " ")

解析成功后下载证书

![在这里插入图片描述](https://img-blog.csdnimg.cn/20190607204727926.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3hpYW9iaW5xdA==,size_16,color_FFFFFF,t_70 " ")

我用的是 Apache ,所以下载的是 Apache

![在这里插入图片描述](https://img-blog.csdnimg.cn/20190607204822312.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3hpYW9iaW5xdA==,size_16,color_FFFFFF,t_70 " ")

## 上传证书

由于本人使用的是 apache ,以下配置是 apache 的通用配置,具体可参看官方
[文档](https://help.aliyun.com/knowledge_detail/95493.html?spm=5176.2020520163.cas.66.72aa56a7v9JUNG)

在 apache 的路径下新建一个 cert 目录,其实该目录建在哪里都可以,但是放在 apache 下方便管理。

![](https://img-blog.csdnimg.cn/20190607225644252.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3hpYW9iaW5xdA==,size_16,color_FFFFFF,t_70 " ")

在 cert 目录下可以建不同的文件夹放在不同域名或子域名的 ssl 文件。

![](https://img-blog.csdnimg.cn/20190607225749622.png " ")

把我们刚才下载的证书上传到服务器上

![](https://img-blog.csdnimg.cn/20190607231234686.png " ")

## 配置

这是基本的配置语句

```bash
# 添加 SSL 协议支持协议，去掉不安全的协议
SSLProtocol all -SSLv2 -SSLv3
# 修改加密套件如下
SSLCipherSuite HIGH:!RC4:!MD5:!aNULL:!eNULL:!NULL:!DH:!EDH:!EXP:+MEDIUM
SSLHonorCipherOrder on
# 证书公钥配置
SSLCertificateFile cert/a_public.crt
# 证书私钥配置
SSLCertificateKeyFile cert/a.key
# 证书链配置，如果该属性开头有 '#'字符，请删除掉
SSLCertificateChainFile cert/a_chain.crt
```

我们将默认的配置 copy 一份出来,取一个跟域名有关的文件名

```bash
cp /etc/apache2/sites-available/000-default.conf /etc/apache2/sites-available/www.xiaobinqt.cn.conf
```

具体配置可参考

```bash
<VirtualHost *:80>

      ServerName www.xiaobinqt.cn
      Redirect permanent / https://www.xiaobinqt.cn/
</VirtualHost>

<VirtualHost *:443>
     SSLEngine On
        # 添加 SSL 协议支持协议，去掉不安全的协议
SSLProtocol all -SSLv2 -SSLv3
# 修改加密套件如下
SSLCipherSuite HIGH:!RC4:!MD5:!aNULL:!eNULL:!NULL:!DH:!EDH:!EXP:+MEDIUM
SSLHonorCipherOrder on
# 证书公钥配置
SSLCertificateFile cert/xiaobinqt.cn/2324042_www.xiaobinqt.cn_public.crt
# 证书私钥配置
SSLCertificateKeyFile cert/xiaobinqt.cn/2324042_www.xiaobinqt.cn.key
# 证书链配置，如果该属性开头有 '#'字符，请删除掉
SSLCertificateChainFile cert/xiaobinqt.cn/2324042_www.xiaobinqt.cn_chain.crt
    # etc
ServerName www.xiaobinqt.cn
     ProxyPreserveHost On
     ProxyRequests Off
     ProxyPass / http://localhost:30007/
     ProxyPassReverse / http://localhost:30007/
</VirtualHost>
```

我用的是 docker 服务,如果你的只是项目文件夹可以参考这样配置

```bash
<VirtualHost *:80>
        # The ServerName directive sets the request scheme, hostname and port that
        # the server uses to identify itself. This is used when creating
        # redirection URLs. In the context of virtual hosts, the ServerName
        # specifies what hostname must appear in the request's Host: header to
        # match this virtual host. For the default virtual host (this file) this
        # value is not decisive as it is used as a last resort host regardless.
        # However, you must set it for any further virtual host explicitly.
        #ServerName www.example.com

        #ServerAdmin webmaster@localhost
        ServerName www.xiaobinqt.cn
        DocumentRoot /var/www/html
        Redirect permanent / https://www.xiaobinqt.cn/

        # Available loglevels: trace8, ..., trace1, debug, info, notice, warn,
        # error, crit, alert, emerg.
        # It is also possible to configure the loglevel for particular
        # modules, e.g.
        #LogLevel info ssl:warn

        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined

        # For most configuration files from conf-available/, which are
        # enabled or disabled at a global level, it is possible to
        # include a line for only one particular virtual host. For example the
        # following line enables the CGI configuration for this host only
        # after it has been globally disabled with "a2disconf".
        #Include conf-available/serve-cgi-bin.conf
</VirtualHost>

<VirtualHost *:443>
     SSLEngine On
        # 添加 SSL 协议支持协议，去掉不安全的协议
SSLProtocol all -SSLv2 -SSLv3
# 修改加密套件如下
SSLCipherSuite HIGH:!RC4:!MD5:!aNULL:!eNULL:!NULL:!DH:!EDH:!EXP:+MEDIUM
SSLHonorCipherOrder on
# 证书公钥配置
SSLCertificateFile cert/xiaobinqt.cn/public.pem
# 证书私钥配置
SSLCertificateKeyFile cert/xiaobinqt.cn/214792197160511.key
# 证书链配置，如果该属性开头有 '#'字符，请删除掉
SSLCertificateChainFile cert/xiaobinqt.cn/chain.pem
    # etc
     ServerName www.xiaobinqt.cn
</VirtualHost>
```

以上配置全部基于 apache ,如果你用的不是 apache ,以上配置可能不适合你. 关于 apache
服务的一些其他知识可以参考这篇[文章](https://www.linode.com/docs/web-servers/lamp/install-lamp-stack-on-ubuntu-16-04/),该文章可能需要翻~墙访问.
配置完成后重启服务,可以利用 curl 命令查看是否配置成功.

```bash
curl -I localhost:xxx
```

![](https://img-blog.csdnimg.cn/20190608192331596.png " ")

对于 ssl 是否配置成功可以通过浏览器查看.

![](https://img-blog.csdnimg.cn/20190608192741852.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3hpYW9iaW5xdA==,size_16,color_FFFFFF,t_70 " ")

可以看到这是我们最新申请的一年的 ssl 证书.

![](https://img-blog.csdnimg.cn/20190608192809335.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3hpYW9iaW5xdA==,size_16,color_FFFFFF,t_70 " ")
