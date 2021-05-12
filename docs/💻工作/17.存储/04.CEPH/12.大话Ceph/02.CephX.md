---
title: CephX 那点事儿

tags: 
  - ceph
categories: 
  - 💻 工作
  - 存储
  - CEPH
  - 大话 Ceph
date: 2020-05-23 11:02:28
permalink: /pages/15e2eb/
---

## 引言

这篇文章主要介绍了 Ceph 中的一个重要系统 – CephX 认证系统。简要介绍了 CephX 的命名格式。并介绍了从集群启动到用户连接集群这一系列流程中 CephX 所起的作用。最后通过实验操作讲解如何在集群所有秘钥丢失的情况下将其完整恢复，以及在实际生产环境中使用 CephX 的一些注意事项。



CephX 理解起来很简单，就是整个 Ceph 系统的**用户名/密码**，而这个用户不单单指我们平时在终端敲 `ceph -s` 而生成的 **client**，在这套认证系统中，还有一个特殊的用户群体，那就是 **MON/OSD/MDS**，也就是说，Monitor， OSD， MDS 也都需要一对账号密码来登陆 Ceph 系统。

### CephX 的命名规则

而**用户名/密码**遵循着一定的命名规则：

- **用户名**

用户名总体遵循 <**TYPE . ID**> 的命名规则，这里的`TYPE`有三种： `mon`,`osd`,`client`。而 `ID` 根据不同的类型的用户而有所不同：

- `mon` ： `ID` 为**空**。
- `osd` ： `ID` 为 OSD 的 **ID**。
- `client` ： `ID` 为该客户端的名称，比如 `admin`,`cinder`,`nova`。
- **密码**
- 密码通常为包含 40 个字符的字符串，形如：`AQBh1XlZAAAAABAAcVaBh1p8w4Q3oaGoPW0R8w==`。

### 默认用户

想要和一个 Ceph 集群进行交互，我们通常需要知道最少四条信息，并且是缺一不可的:

- 集群的 fsid。
- 集群的 Monitor 的 IP 地址，必须先连上 MON 之后才能获取集群信息。
- 一个用于登陆的 **用户名**。
- 登陆用户对应的 **密码**。

其实，很多同学会发现，在我们日常和 Ceph 集群交互时，并不需要指定这些参数，就可以执行 `ceph -s` 得到集群的状态。实际上，我们已经使用了 Ceph 提供的几个默认参数，而 `ceph -s` 加上默认参数后的全称是：

```plain
ceph -s --conf /etc/ceph/ceph.conf --name client.admin --keyring /etc/ceph/ceph.client.admin.keyring
```

从上面的指令可以看出，Ceph 使用的默认用户为 **client.admin**，而这个用户的秘钥文件通常是保存在 `/etc/ceph/ceph.client.admin.keyring` 路径下。如果这里，我们从`/etc/ceph`目录下删除这个秘钥文件，再次执行 `ceph -s`，就会得到下面这个最最常见的错误：

```plain
2017-07-28 15:56:03.271139 7f142579c700 -1 auth: unable to find a keyring on /etc/ceph/ceph.client.admin.keyring,/etc/ceph/ceph.keyring,/etc/ceph/keyring,/etc/ceph/keyring.bin: (2) No such file or directory
2017-07-28 15:56:03.271145 7f142579c700 -1 monclient(hunting): ERROR: missing keyring, cannot use cephx for authentication
2017-07-28 15:56:03.271146 7f142579c700  0 librados: client.admin initialization error (2) No such file or directory
Error connecting to cluster: ObjectNotFoundceph.conf
ceph.mon.keyring
ceph-deploy-ceph.log
```

从报错信息我们可以看出一点，因为我们使用了默认用户 `client.admin`，Ceph 就会以下四个默认路径去寻找 `client.admin` 这个用户的密码：

- `/etc/ceph/ceph.client.admin.keyring` ： 实际上命名格式为： `/etc/ceph/<$cluster>.<$type>.<$id>.keyring`。
- `/etc/ceph/ceph.keyring` ：命名格式为 ：`/etc/ceph/<$cluster>.keyring`。
- `/etc/ceph/keyring`。
- `/etc/ceph/keyring.bin`。

如果不存在这四个文件，或者在这四个文件里面均没有保存用户 `client.admin` 的秘钥，那么就会报错：**ERROR: missing keyring**。也就是说，用户`client.admin` 登陆 Ceph 系统失败！

## 谁才是 CephX 中的鼻祖

### 隐藏 Boss 之 mon

> 一段对话：
> client.admin : 当然是我！用我的账户密码登陆 Ceph 后可以执行任何指令!
> mon. : 哦。
> client.admin : 你谁？我这有所有账户密码(悄悄得查了下 ceph auth list)，怎么没看到你？
> mon. : 嗯。
> client.admin : 哎呀，哪个二货把我的秘钥文件删了，我不能连接集群了！
> mon. : 让一让，我来帮你把秘钥找回来。
> client.admin : 你？确定？
> mon. : 嗯。

一直以为自己权限很大的`client.admin`，忽然因为丢失了保存密码的秘钥文件而不能访问集群了。而从未露面的 `mon.` 却号称能够找回 `client.admin` 的秘钥，难道说 `mon.` 才是真正的鼻祖？！

现在我们回到故事最初的起点，也就是集群搭建之初，我们使用 `ceph-deploy new NodeA NodeB NodeC`后，生成了三个文件：

```plain
ceph.conf
ceph.mon.keyring
ceph-deploy-ceph.log
```

除了`ceph.conf` ，还默认生成了一个 `ceph.mon.keyring` 文件，不出意外的话，这个文件几乎是不会在后面的集群交互中使用的，因为在 `ceph-deploy mon create-initial` 之后，会生成`client.admin`用户，而后面的交互一般都会使用这个用户了。但是集群生成的第一个用户却是 **<mon.>** ，对应的秘钥文件保存在部署目录下的 `ceph.mon.keyring`。

查看 ceph-deloy 的 LOG，可以看到在步骤 `ceph-deploy mon create-initial` 时，有一段日志记录如下：

```plain
[2017-07-28 16:49:53,468][centos7][INFO  ] Running command: /usr/bin/ceph --connect-timeout=25 --cluster=ceph --admin-daemon=/var/run/ceph/ceph-mon.centos7.asok mon_status
[2017-07-28 16:49:53,557][centos7][INFO  ] Running command: /usr/bin/ceph --connect-timeout=25 --cluster=ceph --name mon. --keyring=/var/lib/ceph/mon/ceph-centos7/keyring auth get client.admin
[2017-07-28 16:49:53,761][centos7][INFO  ] Running command: /usr/bin/ceph --connect-timeout=25 --cluster=ceph --name mon. --keyring=/var/lib/ceph/mon/ceph-centos7/keyring auth get client.bootstrap-mds
[2017-07-28 16:49:54,046][centos7][INFO  ] Running command: /usr/bin/ceph --connect-timeout=25 --cluster=ceph --name mon. --keyring=/var/lib/ceph/mon/ceph-centos7/keyring auth get client.bootstrap-mgr
[2017-07-28 16:49:54,255][centos7][INFO  ] Running command: /usr/bin/ceph --connect-timeout=25 --cluster=ceph --name mon. --keyring=/var/lib/ceph/mon/ceph-centos7/keyring auth get-or-create client.bootstrap-mgr mon allow profile bootstrap-mgr
[2017-07-28 16:49:54,452][centos7][INFO  ] Running command: /usr/bin/ceph --connect-timeout=25 --cluster=ceph --name mon. --keyring=/var/lib/ceph/mon/ceph-centos7/keyring auth get client.bootstrap-osd
[2017-07-28 16:49:54,658][centos7][INFO  ] Running command: /usr/bin/ceph --connect-timeout=25 --cluster=ceph --name mon. --keyring=/var/lib/ceph/mon/ceph-centos7/keyring auth get client.bootstrap-rgw
```

实际上，这些秘钥文件都是通过用户 `mon.` 创建的，包括 `client.admin` 用户及其秘钥。所以在整个 CephX 的历史中，`mon.` 才是第一个生成的用户，而其他的用户均由 `mon.` 用户生成或者依次向下生成。

用一张图来表明秘钥的生成关系：

![如图](https://github.com/junfsir/jNote/raw/master/images/ceph-keyring.jpg)

通过这张图，我们可以很容易理解 `bootstrap` 的几个用户的用处了，就是用于引导生成对应类用户的用户，比如`bootstrap-osd` 用于引导生成所有 `osd.N` 用户。

### CephX 使用场景

聊完了各个用户的生成时间，我们来看看这些用户是在什么时候使用了它们的账户和密码的！

#### MON

在整个集群启动的时候，首先是 Monitor 启动，再然后是 OSD 启动。在 Monitor 启动的时候，Monitor 会携带自己的秘钥文件启动进程，也就是说，Monitor 启动的时候，是不需要向任何进程进行秘钥认证的，通俗点讲，Monitor 的秘钥哪怕被修改过了，也不会影响 Monitor 的启动，这里通过一个小实验来具体说明：

```plain
[root@blog cluster]# cat /var/lib/ceph/mon/ceph-blog/keyring
[mon.]
key = AQAr1H1ZAAAAABAAWItgjm4dOKPJx+FX9lVk4Q==
caps mon = "allow *"
[root@blog cluster]# ceph auth get mon.
exported keyring for mon.
[mon.]
key = AQAr1H1ZAAAAABAAWItgjm4dOKPJx+FX9lVk4Q==
caps mon = "allow *"
[root@blog cluster]# vim /var/lib/ceph/mon/ceph-blog/keyring
##### 将秘钥文件内容的一部分A改成了B，再重启Monitor
[root@blog cluster]# cat /var/lib/ceph/mon/ceph-blog/keyring
[mon.]
key = AQAr1H1ZBBBBBBAAWItgjm4dOKPJx+FX9lVk4Q==
caps mon = "allow *"
[root@blog cluster]# systemctl restart ceph-mon.target
[root@blog cluster]# ceph auth get mon.
exported keyring for mon.
[mon.]
key = AQAr1H1ZBBBBBBAAWItgjm4dOKPJx+FX9lVk4Q==
caps mon = "allow *"
```

Monitor 的数据库里面，记录着除了 `mon.` 以外的所有用户密码，在 Monitor 启动之后，才真正开启了认证这个步骤，之后的所有用户想要连接到集群，必须先要通过 fsid 和 MON IP 连上 Ceph 集群，通过了认证之后，就可以正常访问集群了，下面继续介绍下 OSD 的启动认证过程。

#### OSD

OSD 在启动的时候，首先要 `log_to_monitors`，也就是拿着自己的账户密码去登陆集群，这个账户密码在 Monitor 的数据库里有记录，所以如果互相匹配，那么 OSD 就可以正常启动，否则，就会报下面的错：

```plain
2017-08-01 16:54:51.515541 7f21ea978800 -1 osd.0 30 log_to_monitors {default=true}
2017-08-01 16:54:51.991263 7f21ea978800  1 journal close /var/lib/ceph/osd/ceph-0/journal
2017-08-01 16:54:51.999674 7f21ea978800 -1 ^[[0;31m ** ERROR: osd init failed: (1) Operation not permitted^[[0m
2017-08-01 16:54:52.006620 7f21ea978800 -1 common/HeartbeatMap.cc: In function 'ceph::HeartbeatMap::~HeartbeatMap()' thread 7f21ea978800 time 2017-08-01 16:54:52.001569
common/HeartbeatMap.cc: 44: FAILED assert(m_workers.empty())
```

日志里面的 `Operation not permitted` 也就是认证不通过的意思，说明这个 osd.0 携带的秘钥文件和 Monitor 所记录的内容不一致，导致了 OSD 的启动失败。这时候，需要比对下 osd.0 的秘钥内容和 Monitor 的是否一致：

```plain
[root@blog ~]# cat /var/lib/ceph/osd/ceph-0/keyring
[osd.0]
key = AQA81H5Zh05jDxAAkvaHBs07K9HYF1uGSPh+rA==
[root@blog ~]# ceph auth get osd.0
exported keyring for osd.0
[osd.0]
key = AQBH1H5Z6pBvDhAAul364EZsRjDy/NqTQh07Yw==
caps mon = "allow profile osd"
caps osd = "allow *"
```

的确，内容不一样，这时候用 `ceph auth get osd.0` 得到的 key 值替换秘钥文件`keyring`的 key 部分即可正常启动 OSD。

#### Client

通常我们执行 `ceph -s` 时，就相当于开启了一个客户端，连接到 Ceph 集群，而这个客户端默认是使用 `client.admin` 的账户密码登陆连接集群的，所以平时执行的 `ceph -s` 相当于执行了 `ceph -s --name client.admin --keyring /etc/ceph/ceph.client.admin.keyring` 。需要注意的是，每次我们在命令行执行 Ceph 的指令，都相当于开启一个客户端，和集群交互，再关闭客户端。

现在举一个很常见的报错，这在刚接触 Ceph 时，很容易遇到：

```plain
[root@blog ~]# ceph -s
2017-08-03 02:22:27.352516 7fbd157b7700  0 librados: client.admin authentication error (1) Operation not permitted
Error connecting to cluster: PermissionError
```

报错信息很好理解，操作不被允许，也就是认证未通过，由于这里我们使用的是默认的 `client.admin` 用户和它的秘钥，说明秘钥内容和 Ceph 集群记录的不一致，也就是说 `/etc/ceph/ceph.client.admin.keyring` 内容很可能是之前集群留下的，或者是记录了错误的秘钥，这时，只需要使用 `mon.` 用户来执行 `ceph auth list`就可以查看到正确的秘钥内容：

```plain
[root@blog ~]# ceph auth get client.admin --name mon. --keyring /var/lib/ceph/mon/ceph-blog/keyring
exported keyring for client.admin
[client.admin]
key = AQD7F4JZIs9DJxAAZms/NQQQ1YhUpCHRtjygJA==
caps mds = "allow *"
caps mon = "allow *"
caps osd = "allow *"
```

## 细说 caps

仔细查看 `ceph auth list` 的输出，除了用户名和对应的秘钥内容外，还有一个个以 `caps` 开头的内容，这就是 CephX 中对各个用户的权限的细分，比如：读、写、执行等:

```plain
caps mds = "allow *"
caps mon = "allow *"
caps osd = "allow *"
```

而针对不同的应用(mds/mon/osd)，同样的读权限或者写权限的作用是不同的，下面依次对这三个应用的 `r/w/x` 权限进行分析。

### MON

#### r 权限

那么问题来了，想要执行 `ceph -s` 的最低权限是什么呢？ 那就是 `caps mon ="allow r"`，也就是 MON 的 **r** 权限。那么这个读权限到底读了什么呢？首先要强调的一点，这里读的数据都是从 MON 来的，和 OSD 无关。

MON 作为集群的状态维护者，其数据库(`/var/lib/ceph/mon/ceph-$hostname/store.db`)内保存着集群这一系列状态图(Cluster Map)，这些 Map 包含但不限于：

- CRUSH Map
- OSD Map
- MON Map
- MDS Map
- PG Map

而这里的读权限，就是读取这些 Map 的权限，但是这些 Map 的真实内容读取出来没有多大意义，所以以比较友好的指令输出形式展示出来，而这些指令包含但不限于：

```plain
ceph -s
ceph osd crush dump
ceph osd tree
ceph pg dump
ceph osd dump
```

只要有了 MON 的 **r** 权限，那么就可以从集群读取所有 MON 维护的 Map 的数据，宏观来看，就是可以读取集群的状态信息(但是不能修改)。

这里简单介绍下验证流程，我们通过生成一个只包含 MON 的 **r** 权限的秘钥，来访问集群：

```plain
ceph auth get-or-create client.mon_r mon 'allow r' >> /root/key
ceph --name client.mon_r --keyring /root/key -s     ## OK
ceph --name client.mon_r --keyring /root/key osd dump     ## OK
ceph --name client.mon_r --keyring /root/key pg dump     ## OK
ceph --name client.mon_r --keyring /root/key osd out 0     ## Error EACCES: access denied
ceph --name client.mon_r --keyring /root/key osd set noout    ## Error EACCES: access denied
```

#### w 权限

**w** 权限比较有趣，必须配合 **r** 权限才能有效力，否则，单独 **w** 权限执行指令时，是会一直 `access denied`的。所以我们在测试 **w** 权限时，需要附加上 **r** 权限才行：

```plain
ceph auth get-or-create client.mon_rw mon 'allow rw' >> /root/key
```

这时，假象集群的各个 Map 摆在你的面前，你可以清晰得读取每个 OSD 的状态，每个 PG 的状态，但是，如果赋予了你 **w** 权限之后，你就可以对这些实体进行操作，比如踢掉一个 OSD (`ceph osd rm`)，修复一个 PG (`ceph pg repair`)，修改 CRUSH 结构 (`ceph osd setcrushmap`)，删除一个 MON (`ceph mon rm`），而这些操作，如果在仅有 **r** 权限时，是不能执行的（`access denied`）。

由于这里可以执行的指令实在太多了，我仅仅对 **r**, **w**权限做一个简单的总结：

- r : 读取集群各个组件(MON/OSD/MDS/CRUSH/PG)的状态，但是不能修改。
- rw : 读取并可以修改集群的各个组件的状态，可以执行对组件的各个**动作指令**。

> 注意：
> 目前讨论的组件读写权限，均不包含集群对象的读写权限的，也就是说，你单单有了 MON 的 rw 权限，是不能从集群读写对象的。

#### x 权限

MON 的 **x** 权限也比较有趣，因为这个权限仅仅和 `auth` 相关。也就是说，如果你想要执行 `ceph auth list`，`ceph auth get` 之类的所有和 `auth` 相关的指令，那么拥有了 **x** 权限就能执行了。但是和 **w** 权限类似，也需要 **r** 权限组合在一起才能有效力：

```plain
ceph auth get-or-create client.mon_rx mon 'allow rx' >> /root/key
ceph --name client.mon_rw --keyring /root/key auth list
```

#### * 权限

一句话说明 ： `* = rwx`

> Tips
> 可以通过将多个用户秘钥写入同一个文件中，比如上面的 `/root/key` 中，就包含了:
>
> ```plain
> [root@blog ~]# cat /root/key
> [client.mon_r]
> key=AQBtLIJZScuLARAAPQS9ahvU1oZh1Ha/fYhUhQ==
> [client.mon_w]
>  	 key = AQD5LYJZJO2/AxAAWgbuPPUNJ0ugxsqdDD3+sw==
> ```

> 在指令指定 `--name`后，Ceph 就会到 `--keyring` 后面的文件中找寻对应的用户名 section 下的秘钥。

#### profile osd 权限

官方的解释是：给用户以一个 **OSD 的身份** 连接到 其他 OSD/MON 的权限。给 OSD 授予这个权限，使得 OSD 能够处理副本心跳和状态汇报。暂时没找到比较通俗的理解~

### OSD

相比于 MON 的各个权限，OSD 的 rw 比较简单理解一下，**r** 权限就是读取对象的权限， **w** 权限就是写对象的权限，**x** 权限比较有趣，可以调用任何 `class-read/class-write`的权限，这里引用 **Ceph CookBook** 上的一段话来介绍 `class-read/class-write`：

> Ceph can be extended by creating shared object classes called Ceph Classes. Ceph can load .so classes stored in the OSD class dir.For a class ,you can create new object methods that have the ability to call native methods in Ceph object store ,for example , the objects that you have defined in your class can call native Ceph methods such as read and write.

举个例子，你可以实现一些自定义的方法，通过调用这些方法，可以读写具有某一类特征的对象，比如都是以`rbd_data`开头的对象。目前只有调用 librados 层才能使用自定义 class 方法，而上层 RBD，RGW 之类的是不能使用的。

***** 权限除了包含了 rwx，还包含了`ceph tell osd.*` 这类 admin 指令的权限。

官网的这个页面(http://docs.ceph.com/docs/kraken/man/8/ceph-authtool/)比较好的介绍了几个实例，这里简单介绍下一个比较长的指令的意义：

```plain
osd = "allow class-read object_prefix rbd_children, allow pool templates r class-read, allow pool vms rwx"
```

第一个权限：`object_prefix` 是一个类方法，而这个方法的作用是给予所有以`rbd_children`为名开头的对象的`class-read`也就是读权限。只能读，不能写。

第二个权限：给予池 `templates`的读权限，可以执行 class-read 方法的权限。也就是说，客户除了可以读这个池的对象外，还能自己实现形如`obejct_prefix`这种系统自带的类方法来读取对象，比如读取具备某一类特征的对象。

第三个权限：给予池 `vms` 的读写以及执行 class-read/class-write 方法的权限。

## 丢失所有秘钥的恢复流程

讲了这么多理论知识，某个二货运维同学不耐烦了，一口气把所有的秘钥全部删除了，这些秘钥包含：

- MON ： /var/lib/ceph/mon/ceph-`hostname`/keyring
- OSD ： /var/lib/ceph/osd/ceph-0/keyring
- Client ：/etc/ceph/ceph.client.admin.keyring

总之，所有包含秘钥内容的文件都被删除了，并且连同`/etc/ceph/`目录都删的干干净净。这时候能否将所有的秘钥文件恢复出来吗？答案是：可以！

在管理秘钥方面，Ceph 做了一个比较有趣的设定：所有除了 `mon.` 用户的账户密码都保存在 MON 的数据库 leveldb 中，但是 `mon.` 用户的信息并没有保存在数据库里，而是在 MON 启动时读取 MON 目录下的 `keyring` 文件得到的。所以，我们甚至可以随便伪造一个`keyring`，放置到 MON 目录下去。然后同步到各个 MON 节点，然后重启三个 MON。 这时候，MON 就拿着人造的`keyring`启动生效了。有了 `mon.`用户的账户密码，我们很容易的可以使用 `ceph auth list --name mon. --keyring /var/lib/ceph/mon/ceph-$hostname/keyring` 指令来得到所有的秘钥内容！

等等，如果真的删干净了`/etc/ceph/`目录的话， 上面的这个指令是不能执行的，因为没有`/etc/ceph/ceph.conf`去指定集群，这时候，我们可以从任意一个 OSD 目录下的 `/var/lib/ceph/osd/ceph-0/ceph_fsid` 得到集群的 fsid，MON 的 IP 信息也很容易恢复。简单得重构了 `ceph.conf`后，使用`mon.` 的用户密码就可以得到正确的 `ceph auth list`的信息啦~。

再等等，现在的`ceph.conf`内容太精简了，比删除之前少了很多东东，这些东东还能恢复吗？答案是，能！

找寻任何一个未重启的 OSD，执行 `ceph daemon osd.0 config diff`，这样，就可以看到这个 OSD 启动加载的配置项和默认的配置项的不一样的地方，通过仔细比对很容易恢复成删除之前的配置文件样~。

> 疑问:
> 相信这里就会有同学有疑问了，为什么不直接把 `ceph.conf` 里面的 `cephx` 改为 `none` 后直接重启集群呢，首先这样做的成本较高，因为要重启 OSD(必须重启 OSD，否则 OSD 会在 MON 重启一段时间内全部自杀)。所以上面的方法只重启了 MON，影响范围小。

## CephX 实际使用中的注意事项

### zabbix 使用

在部署 zabbix-agent 后，server 通过拉取 agent 的指令输出得到返回值，但是却会报：

```plain
zabbix_get -s 1.2.3.4 -k ceph.ops
ZBX_NOTSUPPORTED: Unsupported item key
```

前往 agent 节点执行脚本，却能得到正常的输出。

这里查看 zabbix_agent 的 LOG 发现，日志里面总是报 ：

```plain
librados: client.admin authentication error (1) Operation not permitted
```

原来是,zabbix_agent 对 `/etc/ceph/ceph.client.admin.keyring` 没有读权限，将秘钥 `chmod a+r`之后，就能正常读取数据了。

所以，在我们的日常使用中，一定要注意 `/etc/ceph/ceph.client.admin.keyring` 的读权限，很多不是运行在 root 用户上的应用读取不到秘钥内容后，就会连接不上集群，造成比较奇怪的现象。

### cephx -> none

在关闭 CephX 功能时，要遵循一定的顺序：

- 关闭： 重启 MON -> 重启 OSD
- 开启： 重启 MON -> 重启 OSD

如果关闭 CephX 后未重启 OSD，过一段时间，OSD 会随机挂掉。

### keyring 的分布

通常我们可以在 MON 节点执行 `ceph -s`，但是到了 OSD 节点，就会因为缺失 `client.admin` 的秘钥文件而无法执行 `ceph -s`。

MON 的秘钥保存路径为： `/var/lib/ceph/mon/ceph-$hostname/keyring`。
OSD 的秘钥保存路径为： `/var/lib/ceph/osd/ceph-$osd_id/keyring`。
client.admin 的秘钥保存路径为： `/etc/ceph/ceph.client.admin.keyring`。

实际上，我们甚至可以在 OSD 节点(没有 client.admin.keyring)，通过执行：

```plain
ceph -s --name osd.0 --keyring /var/lib/ceph/osd/ceph-0/keyring
```

来读取集群的状态。

### 配置只能访问一个 RBD 的用户权限

具体介绍可以参考这篇文章(https://blog-fromsomedude.rhcloud.com/2016/04/26/Allowing-a-RBD-client-to-map-only-one-RBD/)

这里主要说下秘钥的创建指令的意义：

```plain
ceph auth get-or-create client.myclient
mon
'allow r'
osd
'allow rwx object_prefix rbd_data.103d2ae8944a;
allow rwx object_prefix rbd_header.103d2ae8944a;
allow rx object_prefix rbd_id.myimage'
-o /etc/ceph/ceph.client.myclient.keyring
```

这里通过 `object_prefix` 前缀方法，赋予了用户对和某个 RBD 所有相关的对象的读写权限，是一个比较有实用价值的应用。

## 总结

本文介绍了 CephX 在 Ceph 系统中的生成过程以及互相之间的依赖生成关系。详细讲述了各个权限在不同应用中的作用和使用场景。最后通过秘钥丢失的例子来将理论应用到实际生产环境中，使大家对 CephX 的使用游刃有余。

## 参考链接
[大话 Ceph -- CephX 那点事儿](http://xuxiaopang.com/2017/08/23/easy-ceph-CephX/)