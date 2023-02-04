# Failed to start LSB: Bring up/down networking 问题解决


<!-- author： xiaobinqt -->
<!-- email： xiaobinqt@163.com -->
<!-- https://xiaobinqt.github.io -->
<!-- https://www.xiaobinqt.cn -->

刚在虚拟机上执行

```shell
service network restart

```

时报了以下错误:point_down:

```
2月 04 11:09:16 192.168.48.151 postfix/pickup[19414]: fatal: unable to use my own hostname
2月 04 11:09:17 192.168.48.151 postfix/master[7179]: warning: process /usr/libexec/postfix/pickup pid 19414 exit status 1
2月 04 11:09:17 192.168.48.151 postfix/master[7179]: warning: /usr/libexec/postfix/pickup: bad command startup -- throttling
2月 04 11:10:17 192.168.48.151 postfix/pickup[19416]: warning: valid_hostname: numeric hostname: 192.168.48.151
2月 04 11:10:17 192.168.48.151 postfix/pickup[19416]: fatal: unable to use my own hostname
2月 04 11:10:18 192.168.48.151 postfix/master[7179]: warning: process /usr/libexec/postfix/pickup pid 19416 exit status 1
2月 04 11:10:18 192.168.48.151 postfix/master[7179]: warning: /usr/libexec/postfix/pickup: bad command startup -- throttling
2月 04 11:11:18 192.168.48.151 postfix/pickup[19441]: warning: valid_hostname: numeric hostname: 192.168.48.151
2月 04 11:11:18 192.168.48.151 postfix/pickup[19441]: fatal: unable to use my own hostname
2月 04 11:11:19 192.168.48.151 postfix/master[7179]: warning: process /usr/libexec/postfix/pickup pid 19441 exit status 1
2月 04 11:11:19 192.168.48.151 postfix/master[7179]: warning: /usr/libexec/postfix/pickup: bad command startup -- throttling
2月 04 11:12:19 192.168.48.151 postfix/pickup[19442]: warning: valid_hostname: numeric hostname: 192.168.48.151
2月 04 11:12:19 192.168.48.151 postfix/pickup[19442]: fatal: unable to use my own hostname
2月 04 11:12:20 192.168.48.151 postfix/master[7179]: warning: process /usr/libexec/postfix/pickup pid 19442 exit status 1
2月 04 11:12:20 192.168.48.151 postfix/master[7179]: warning: /usr/libexec/postfix/pickup: bad command startup -- throttling
2月 04 11:13:20 192.168.48.151 postfix/pickup[19443]: warning: valid_hostname: numeric hostname: 192.168.48.151
2月 04 11:13:20 192.168.48.151 postfix/pickup[19443]: fatal: unable to use my own hostname
2月 04 11:13:21 192.168.48.151 postfix/master[7179]: warning: process /usr/libexec/postfix/pickup pid 19443 exit status 1
2月 04 11:13:21 192.168.48.151 postfix/master[7179]: warning: /usr/libexec/postfix/pickup: bad command startup -- throttling
2月 04 11:13:32 192.168.48.151 polkitd[6082]: Registered Authentication Agent for unix-process:19457:2442477 (system bus name :1.95 [/usr/bin/pkttyagent --notify-fd 5 --fallback], object path /org/freedesktop/
2月 04 11:13:32 192.168.48.151 systemd[1]: Starting LSB: Bring up/down networking...
-- Subject: Unit network.service has begun start-up
-- Defined-By: systemd
-- Support: http://lists.freedesktop.org/mailman/listinfo/systemd-devel
--
-- Unit network.service has begun starting up.
2月 04 11:13:33 192.168.48.151 network[19463]: 正在打开环回接口： [  确定  ]
2月 04 11:13:33 192.168.48.151 NetworkManager[6504]: <info>  [1675480413.4150] audit: op="connection-activate" uuid="8740e83d-258d-4030-a9d6-8433e9cfccbb" name="ens33" result="fail" reason="No suitable device
2月 04 11:13:33 192.168.48.151 network[19463]: 正在打开接口 ens33： 错误：激活连接失败：No suitable device found for this connection.
2月 04 11:13:33 192.168.48.151 network[19463]: [失败]
2月 04 11:13:33 192.168.48.151 network[19463]: RTNETLINK answers: File exists
2月 04 11:13:33 192.168.48.151 network[19463]: RTNETLINK answers: File exists
2月 04 11:13:33 192.168.48.151 network[19463]: RTNETLINK answers: File exists
2月 04 11:13:33 192.168.48.151 network[19463]: RTNETLINK answers: File exists
2月 04 11:13:33 192.168.48.151 network[19463]: RTNETLINK answers: File exists
2月 04 11:13:33 192.168.48.151 network[19463]: RTNETLINK answers: File exists
2月 04 11:13:33 192.168.48.151 network[19463]: RTNETLINK answers: File exists
2月 04 11:13:33 192.168.48.151 network[19463]: RTNETLINK answers: File exists
2月 04 11:13:33 192.168.48.151 network[19463]: RTNETLINK answers: File exists
2月 04 11:13:33 192.168.48.151 systemd[1]: network.service: control process exited, code=exited status=1
2月 04 11:13:33 192.168.48.151 systemd[1]: Failed to start LSB: Bring up/down networking.
-- Subject: Unit network.service has failed
```

![systemctl status network.service](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230204/6d13f35511864b5691d6e6eed02a0748.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'systemctl status network.service')

我虚拟机的型号是 CentOS Linux release 7.6.1810 (Core)

![release](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230204/cf61f62164b2461a9d2547006973faa7.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 'release')

由于我把网卡从 ensXX 格式改成了 ethX 格式，但是我**没有**把配置文件从 ifcfg-ens33 改成 ifcfg-eth0，先备份旧的文件，然后重命名为 eth0 格式的配置文件。

![备份并重命名](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230204/7a09a119f02d4dafa76380e87516a70a.png?imageView2/0/q/75|watermark/2/text/eGlhb2JpbnF0/font/dmlqYXlh/fontsize/1000/fill/IzVDNUI1Qg==/dissolve/52/gravity/SouthEast/dx/15/dy/15 '备份并重命名')

将 ifcfg-eth0 配置文件中的 NAME 和 DEVICE 值改为 eth0。

![修改配置值](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230204/a137db46bcdf4fcb94ae18cfc8bd233f.png '修改配置值')




