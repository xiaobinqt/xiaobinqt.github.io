# SSH error: permissions are too open


## 问题描述

我的 git 版本在 1.8.3.1 的时候提交 push 代码时一直报错

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230324/66823aa8269d4341837ac1a2ecd69735.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'git 版本')

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230324/934bd49f1f9449ed9a22606e0c19f64d.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'Permission denied (publickey)')

```shell
Permission denied (publickey).
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
```

排查了几个小时，一直没解决，之前也一直是这么用的，也没出现过问题。后来没办法，我尝试更新了下 git 版本到 2.39.2，发现错误提示不一样了:cry:

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230324/f4a5ce70fd7146d982ff72b70ec5098a.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'Permissions are too open')

```shell
Warning: Permanently added '192.168.40.233' (ECDSA) to the list of known hosts.
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@         WARNING: UNPROTECTED PRIVATE KEY FILE!          @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
Permissions 0755 for '/tmp/tmp.LGAlGyMvNs/id_rsa' are too open.
It is required that your private key files are NOT accessible by others.
This private key will be ignored.
Load key "/tmp/tmp.LGAlGyMvNs/id_rsa": bad permissions
Permission denied (publickey).
致命错误：无法读取远程仓库。

请确认您有正确的访问权限并且仓库存在。
```

我根据`Permissions 0755 for '/tmp/tmp.LGAlGyMvNs/id_rsa' are too open.` google 了下，原来是 isa 文件权限给的太高了，改成 400 或是 600 就可以了。

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230324/283ea804c9de4b1dbe456b4e8915182f.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '问题解决')

## 参考

+ [SSH error: permissions are too open](https://www.educative.io/answers/ssh-error-permissions-are-too-open)
+ [CentOS 7 升级 git 版本到 2.x](https://juejin.cn/post/7071910670056292389)











