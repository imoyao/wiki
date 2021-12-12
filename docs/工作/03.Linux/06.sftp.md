---
title: 给 SFTP 创建新用户、默认打开和限制在某个目录

tags: SFTP
categories: 
  - 💻 工作
  - Linux
date: 2020-05-26 12:27:56
permalink: /pages/0b0e21/
---

## 背景

给外包的工作人员提供我司服务器的**某一目录**的访问（包括读写）权限，方便他们部署代码文件。

之所以是某一目录的访问，是因为 SFTP 的用户登录后，默认是能看到整个系统的文件目录，这样很不安全。限制用户只能在自己的 home 目录下活动，这里需要使用到 chroot，openssh 4.8p1 以后都支持 chroot。可以输入`ssh -V`来查看 openssh 的版本，如果低于 4.8p1，需要自行升级安装。

题外话：如果是针对 ftp 的用户权限管理，推荐使用 vsftpd，可通过 yum 直接安装。

## 基本流程

### 创建用户组
```bash
groupadd sftp   # 本例中使用sftp作为组名
```
### 创建新用户
创建一个 sftp 用户，名为 mysftp
```bash
useradd -g sftp -s /bin/false mysftp
```
设置用户密码
```bash
passwd mysftp
```
- useradd 和 adduser 的区别
参见[linux - What's the difference between "adduser" and "useradd"? - Super User](https://superuser.com/questions/547966/whats-the-difference-between-adduser-and-useradd)

>useradd is native binary compiled with the system. But, adduser is a perl script which uses useradd binary in back-end.
>
> adduser is more user friendly and interactive than its back-end useradd. There's no difference in features provided.

### 禁止该用户登录 SSH

因为我们只想该用户使用 SFTP，并不需要该用户能登录 SSH，威胁安全。

```plain
usermod -s /bin/false mysftp
```

将`mysftp`的 shell 改成 /bin/false。

#### 4、修改该用户的家目录

```plain
usermod -d /data/wwwroot/user1/ mysftp
```

这样每次用户访问服务器都会默认打开`/data/www/user1/`，但还是可以跳出这个访问其它目录，需要进行下面一步的操作。

#### 5、设置 sshd\_config

打开`sshd_config`文件

```plain
vi /etc/ssh/sshd_config
```

找到 `Subsystem sftp /usr/libexec/openssh/sftp-server` 这一行，修改成：

```plain
Subsystem sftp internal-sftp    # 指定sftp服务使用系统自带的internal-sftp
Match Group sftp    # 这行用来匹配sftp组的用户，如果要匹配多个组，多个组之间用逗号分割
Match user mysftp   # 当然，也可以匹配用户，多个用户名之间也是用逗号分割，但我们这里按组匹配更灵活和方便
ForceCommand internal-sftp
ChrootDirectory /data/www/user1/
```
`ChrootDirectory /data/sftp/%u`用 chroot 将用户的根目录指定到/data/sftp/%u，%u 代表用户名，这样用户就只能在/data/sftp/%u 下活动，chroot 的含义，可以参考这里：[理解 chroot](https://www.ibm.com/developerworks/cn/linux/l-cn-chroot/)
将上面的 `mysftp` 和 `/data/www/user1/` 替换成你需要的。
```plain
AllowTcpForwarding no
X11Forwarding no
```
这两行，如果不希望该用户能使用端口转发的话就加上，否则删掉；

多个用户请重复配置这三行：  
```plain
Match user xxxx  
ForceCommand internal-sftp  
ChrootDirectory /data/www/user2/
```
这样可以为不同的用户设置不同的限制目录。

### 重新启动 sshd 服务

```bash
/etc/init.d/sshd restart
```

现在用 SFTP 软件使用`mysftp`用户登录，就可以发现目录已经被限定、锁死在`/data/wwwroot/user1/`了。

## 设定 Chroot 目录权限
```bash
# chown root:sftp /data/wwwroot/user1
# chmod 755 /data/wwwroot/user1/
```

### 遇到的问题

#### 1、修改`sshd_config`文件后重启 sshd，报错：Directive 'UseDNS' is not allowed within a Match block

语法错误，原因未知，只需要把两段配置的位置互调就不报错了。

修改前：

```plain
Subsystem sftp internal-sftp
UsePAM yes
Match user mysftp
ForceCommand internal-sftp
ChrootDirectory /data/wwwroot/user1/

UseDNS no
AddressFamily inet
PermitRootLogin yes
SyslogFacility AUTHPRIV
PasswordAuthentication yes
```

修改后：

```plain
UseDNS no
AddressFamily inet
PermitRootLogin yes
SyslogFacility AUTHPRIV
PasswordAuthentication yes

Subsystem sftp internal-sftp
UsePAM yes
Match user mysftp
ForceCommand internal-sftp
ChrootDirectory /data/wwwroot/user1/
```

### 新用户通过 sftp 访问时，权限不全，只能读不能写

我试着用 root 账号去把该用户的家目录权限改成 777，但是会出现该用户 sftp 登陆不了的情况。（报错：Server unexpectedly closed network connection）

给新用户的家目录的权限设定有两个要点：
1. 由 ChrootDirectory 指定的目录开始一直往上到系统根目录为止的目录拥有者都只能是 root
2. 由 ChrootDirectory 指定的目录开始一直往上到系统根目录为止都不可以具有群组写入权限（最大权限 755）

如果违反了上面的两条要求，那么就会出现新用户访问不了 sftp  的情况。

**所以`/data/www/user1/`及上级的所有目录属主一定要是 root，并且组权限和公共权限不能有写入权限，如果一定需要有写入权限，那们可以在`/data/www/user1/`下建立 777 权限的 upload 文件夹**。

```plain
mkdir /data/wwwroot/user1/upload
chown -R mysftp:root /data/wwwroot/user1/upload
```

这样`mysftp`用户就可以在`/data/wwwroot/user1/upload`里随意读写文件了。

## 参考链接
[如何将 SFTP 用户限制在某个目录下？](http://www.jbxue.com/LINUXjishu/22628.html)
[centos 下配置 sftp 且限制用户访问目录](https://segmentfault.com/a/1190000000441260)
[CentOS 的 ssh sftp 配置及权限设置[转载-验证可用] - wooya - 博客园](https://www.cnblogs.com/wooya/p/9392142.html)

## umask 计算
[umask Calculator - WintelGuy.com](https://wintelguy.com/umask-calc.pl)

## 计算规则

[Linux umask 与文件默认权限 - 诺晨 - OSCHINA](https://my.oschina.net/nk2011/blog/811273?utm_source=debugrun&utm_medium=referral)

[Linux umask 详解：令新建文件和目录拥有默认权限_操作系统_zyy1659949090 的博客-CSDN 博客](https://blog.csdn.net/zyy1659949090/article/details/88122535)
[linux - How to use os.umask() in Python - StackOverflow](https://stackoverflow.com/questions/10291131/how-to-use-os-umask-in-python)