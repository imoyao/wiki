---
title: ntpd 时钟同步服务

tags: 
  - Linux
  - NTP
categories: 
  - 💻 工作
  - Linux
date: 2020-06-02 18:21:46
permalink: /pages/42a5df/
---

- 为什么要使用 ntpd 而不是 ntpdate？
原因很简单，ntpd 是步进式的逐渐调整时间，而 ntpdate 是断点更新，比如现在服务器时间是 9.18 分，而标准时间是 9.28 分，ntpd 会在一段时间内逐渐的把时间校准到与标准时间相同，而 ntpdate 会立刻把时间调整到 9.28 分，如果你往数据库内写入内容或在其他对时间有严格要求的生产环境下，产生的后果会是很严重的。（注：当本地时间与标准时间相差 30 分钟以上时 ntpd 会停止工作）

## NTP 通信协议原理
首先主机启动 NTP。客户端会向 NTP 服务器发送调整时间的 message。
然后 NTP server 会送出当前的标准时间给 client；client 接受来自 server 的时间后，会根据这个信息来调整自己的时间。这样就实现了网络对时。
NTP 这个 deamon 采用了 UDP 123 端口。当我们要利用 Tim server 来进行实践的同步更新时，就需要使用 NTP 软件提供的 ntpdate 来连接端口 123。

### 相关的命令和配置文件
- /etc/ntp.conf: linux 各版本虽然目录不同，但文件名相同。可以用 which ntp.conf 或者 locate ntp.conf 来查找。这是 NTP 唯一的一个设置文件。
- /usr/share/zoneinfo/: 这个里面规定了这个主要时区的时间设置文件。
- /etc/sysconfig/clock: 这个文件是 linux 的主要时区设置文件，每次开机后 linux 会自动读取这个文件来设置系统所默认的显示时间，可以看看它里面到底设置了什么：
```bash
cat /etc/sysconfig/clock
```
```plain
# The ZONE parameter is only evaluated by system-config-date.
# The timezone of the system is defined by the contents of /etc/localtime.
ZONE="Asia/Shanghai"
UTC=true
ARC=false
```
- /etc/localtime: 本地端时间配置文件。
- /bin/date: 这个是时间的修改命令，除了输出时间，还可以修改时间。
- /sbin/hwclock: 因为 linux 系统上面 BIOS 时间与 linux 系统时间是分开的，所以使用 date 这个指令调整了时间之后，还需要使用 hwclock 才能将修改过的时间写入 BIOS 中。
- /usr/sbin/ntpd: 这是 NTP 的 daemon 文件，需要启动它才能提供 NTP 服务，这个命令会读取/etc/ntp.conf 里面的设置。
- /usr/sbin/ntpdate: 这是 client 用来连接 NTP Server 的主要执行文件，如果您不想启用 NTP，只想启用 NTP Client 功能的话，可以只应用此命令。
- /usr/sbin/ntptrace: 可以用来追踪某台时间服务器的时间对应关系。

## 安装与配置

### 设置时区
```plain
cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
```
### 安装 ntpd 服务
```bash
yum -y install ntp
```
### 配置 ntpd
```plain
vi /etc/ntp.conf
```
```plain
restrict default kod nomodify notrap nopeer noquery
# restrict -6 default kod nomodify notrap nopeer noquery  #针对ipv6设置
 
# 允许本地所有操作
restrict 127.0.0.1
#restrict -6 ::1
 
# 允许的局域网络段或单独ip
restrict 10.0.0.0 mask 255.0.0.0 nomodify motrap
restrict 192.168.0.0 mask 255.255.255.0 nomodify motrap
restrict 192.168.1.123 mask 255.255.255.255 nomodify motrap
 
# 使用上层的internet ntp服务器
server cn.pool.ntp.org prefer
server 0.asia.pool.ntp.org
server 3.asia.pool.ntp.org
server 0.centos.pool.ntp.org iburst
 
# 如果无法与上层ntp server通信以本地时间为标准时间
server   127.127.1.0    # local clock
fudge    127.127.1.0 stratum 10
 
# 计算本ntp server 与上层ntpserver的频率误差
driftfile /var/lib/ntp/drift
 
# Key file containing the keys and key identifiers used when operating
# with symmetric key cryptography.
keys /etc/ntp/keys
 
#日志文件
logfile /var/log/ntp.log
```

### 修改/etc/sysconfig/ntpd
```plain
# Drop root to id 'ntp:ntp' by default.
OPTIONS="-u ntp:ntp -p /var/run/ntpd.pid"
# Set to 'yes' to sync hw clock after successful ntpdate
SYNC_HWCLOCK=yes #make no into yes; BIOS的时间也会跟着修改
# Additional options for ntpdate
NTPDATE_OPTIONS=""
restrict [address] mask [netmask_ip] [parameter]
```
其中 parameter 的参数主要有：
ignore     ：    拒绝所有类型的 ntp 连接
nomodify   ：    客户端不能使用 ntpc 与 ntpq 两支程式来修改服务器的时间参数
noquery    ：    客户端不能使用 ntpq、ntpc 等指令来查询服务器时间，等于不提供 ntp 的网络校时
notrap     ：    不提供 trap 这个远程时间登录的功能
notrust    ：    拒绝没有认证的客户端
nopeer     ：    不与其他同一层的 ntp 服务器进行时间同步

## 验证与状态检查

### 运行 ntp
```bash
service ntpd start/stop/restart
```
### 查看 ntp 的端口,应该看到 123 端口
```bash
netstat -unlnp
```
### 查看 ntp 服务器有无和上层连通
```plain
ntpstat
 
synchronised to NTP server () at stratum 2
time correct to within 74 ms
polling server every 128 s
```
注意：此命令出现上述 synchronised 结果比较慢，我的用了大概 5 分钟。
### 查看 ntp 服务器与上层间的联系
```plain
ntptrace

ntptrace -n 127.0.0.1
 
127.0.0.1: stratum 3, offset -0.001095, synch distance 0.532610
116.193.83.174: timed out, nothing received
```
### 查看 ntp 服务器与上层 ntp 服务器的状态:ntpq
```bash
ntpq -p
```
```plain
# 其中:
# remote - 本机和上层ntp的ip或主机名，“+”表示优先，“*”表示次优先
# refid  - 参考上一层ntp主机地址
# st     - stratum阶层
# when   - 多少秒前曾经同步过时间
# poll   - 下次更新在多少秒后
# reach  - 已经向上层ntp服务器要求更新的次数
# delay  - 网络延迟
# offset - 时间补偿
# jitter - 系统时间与bios时间差
```
如果所有远程服务器的 jitter 值是 4000 并且 delay 和 reach 的值是 0，那么说明时间同步是有问题的。

可能的原因是防火墙阻断了与 server 之间的通讯，即 123 端口是否正常开放；

此外每次重启 NTP 服务器之后大约要 3－5 分钟客户端才能与 server 建立正常的通讯连接，否则你在客户端执行“ntpdate 服务器 ip”的时候将返回：
```plain
27 Jun 10:20:17 ntpdate[21920]: no server suitable for synchronization found
```

### 启动 NTPD
我采用了一个很笨的办法来手动启动 ntpd，而不是把 ntpd 加入服务，写一个简单的脚本
```plain
vi ntpstart.sh
ntpdate cn.pool.ntp.org
ntpdate cn.pool.ntp.org
service ntpd start
```
然后加入/etc/rc.local:
```plain
/{sh path}/ntpstart.sh
```
这是因为我有一台服务器启动后的时间总是与标准时间差别很大，每次启动后 ntpd 要花很多时间才能把时间校准，所以我是先在系统启动后 ntpdate 更新两次，然后再启动 ntpd 服务，在 freebsd 里好像有修改配置文件，让时间服务器在系统启动之前启动的，centos 还没仔细琢磨。

## 客户端配置

方法 1.使用 ntpdate 与上面配置的时间服务器定时同步，不推荐此方法
方法 2.安装 ntpd，指定时间 server 为上面配置的服务器地址，推荐
更详细的介绍参见台湾 鸟哥的 Linux 私房菜: http://linux.vbird.org/linux_server/0440ntp.php

## 附录
```plain
中国国家授时中心(陕西西安) 210.72.145.44
上海： 61.129.66.79 (t2.hshh.org) 61.129.42.44 (ntp.fudan.edu.cn) 202.120.2.101 (ntp.sjtu.edu.cn)
浙江 218.75.4.130 (t1.hshh.org)
内蒙古 218.21.130.42 (t1.hshh.org)
香港: 137.189.11.66 (clock.cuhk.edu.hk ) 137.189.11.128 (ntp.cuhk.edu.hk )
台湾: 220.130.158.52(time.stdtime.gov.tw) 220.130.158.72(Clock.stdtime.gov.tw)
220.130.158.51(tick.stdtime.gov.tw) 220.130.158.54(watch.stdtime.gov.tw)
asia.pool.ntp.org， 更多亚洲服务器请参考 http://www.pool.ntp.org/zone/asia
cn.pool.ntp.org, 更多中国服务器请参考 http://www.pool.ntp.org/zone/cn
tw.pool.ntp.org, 更多中国台湾服务器请参考 http://www.pool.ntp.org/zone/tw
hk.pool.ntp.org, 更多中国香港服务器请参考 http://www.pool.ntp.org/zone/hk
```
取消 ntpd 自动启动，在系统启动时，指定 ntpdate 远程标准时间服务器两次，然后 service ntpd start
好像也可以修改 rc.conf 或者加上一堆什么参数来实现，我偷懒用这个笨办法来保证时间的准确了

## 解决 ntp 的错误
解决 ntp 的错误 no server suitable for synchronization found

当用 ntpdate -d 来查询时会发现导致 no server suitable for synchronization found 的错误的信息有以下 2 个：

错误 1.Server dropped: Strata too high
在 ntp 客户端运行 ntpdate serverIP，出现 no server suitable for synchronization found 的错误。

在 ntp 客户端用 ntpdate –d serverIP 查看，发现有 Server dropped: strata too high 的错误，并且显示 stratum 16。而正常情况下 stratum 这个值得范围是 0~15。

这是因为 NTP server 还没有和其自身或者它的 server 同步上。

以下的定义是让 NTP Server 和其自身保持同步，如果在/ntp.conf 中定义的 server 都不可用时，将使用 local 时间作为 ntp 服务提供给 ntp 客户端。

server 127.127.1.0
fudge 127.127.1.0 stratum 8
在 ntp server 上重新启动 ntp 服务后，ntp server 自身或者与其 server 的同步的需要一个时间段，这个过程可能是 5 分钟，在这个时间之内在客户端运行 ntpdate 命令时会产生 no server suitable for synchronization found 的错误。

那么如何知道何时 ntp server 完成了和自身同步的过程呢？ 在 ntp server 上使用命令：
```plain
watch ntpq -p

出现画面：
Every 2.0s: ntpq -p                                                                                                             Thu Jul 10 02:28:32 2008
     remote           refid      st t when poll reach   delay   offset jitter
==============================================================================
 192.168.30.22   LOCAL(0)         8 u   22   64    1    2.113 179133.   0.001
 LOCAL(0)        LOCAL(0)        10 l   21   64    1    0.000   0.000  0.001
 ```
注意 LOCAL 的这个就是与自身同步的 ntp server。

注意 reach 这个值，在启动 ntp server 服务后，这个值就从 0 开始不断增加，当增加到 17 的时候，从 0 到 17 是 5 次的变更，每一次是 poll 的值的秒数，是 64 秒*5=320 秒的时间。

如果之后从 ntp 客户端同步 ntp server 还失败的话，用 ntpdate –d 来查询详细错误信息，再做判断。

错误 2.Server dropped: no data
从客户端执行 ntpdate –d 时有错误信息如下：
```plain
ntpdate -d 192.168.30.22

transmit(192.168.30.22)
transmit(192.168.30.22)
transmit(192.168.30.22)
transmit(192.168.30.22)
transmit(192.168.30.22)
192.168.30.22: Server dropped: no data
server 192.168.30.22, port 123
.....
28 Jul 17:42:24 ntpdate[14148]: no server suitable for synchronization found
```
出现这个问题的原因可能有两个：

1. 检查 ntp 的版本，如果你使用的是 ntp4.2（包括 4.2）之后的版本，在 restrict 的定义中使用了 notrust 的话，会导致以上错误。使用以下命令检查 ntp 的版本：ntpq -c version。下面是来自 ntp 官方网站的说明：

> The behavior of notrust changed between versions 4.1 and 4.2.
In 4.1 (and earlier) notrust meant "Don't trust this host/subnet for time".
In 4.2 (and later) notrust means "Ignore all NTP packets that are not cryptographically authenticated." This forces remote time servers to authenticate themselves to your (client) ntpd
解决:把 notrust 去掉。

2. 检查 ntp server 的防火墙。可能是 server 的防火墙屏蔽了 upd 123 端口。 可以用命令 service iptables stop 来关掉 iptables 服务后再尝试从 ntp 客户端的同步，如果成功，证明是防火墙的问题，需要更改 iptables 的设置。
## 参考来源
[鳥哥的 Linux 私房菜 -- NTP 時間伺服器](http://linux.vbird.org/linux_server/0440ntp.php)
[ntpd 时钟同步服务](http://xstarcd.github.io/wiki/sysadmin/ntpd.html)
[NTP 配置实践 | HelloDog](https://wsgzao.github.io/post/ntp/)
[03-NTP 配置-新华三集团-H3C](http://www.h3c.com/cn/d_201904/1173803_30005_0.htm)
