---
title: Ceph bluestore 和 ceph-volume

tags: 
  - ceph
categories: 
  - 💻 工作
  - 存储
  - CEPH
  - 知识拓展
date: 2020-05-23 11:02:28
permalink: /pages/1dc76b/
---
# [Ceph bluestore 和 ceph-volume](https://xcodest.me/ceph-bluestore-and-ceph-volume.html)

## bluestore & rocksdb & ceph-volume

ceph 的组件多采用插件的机制，包括后端存储，KV 数据库，磁盘管理等。各组件之间可以灵活的组合。

基于后端存储包括 filestore, kvstore，memstore 和新的 bluestore。 Ceph Luminous 引用了 bluestore 的存储类型，不依赖文件系统，直接管理物理磁盘，相比 filestore, 在 io 写入的时候路径更短，也避免了二次写入的问题，性能会更加好。

KV 存储主要包括 LevelDB, MemDB 和新的 RocksDB。 RocksDB 是 Facebook 基于 LevelDB 开发的 key-value 数据，并对闪存(flash)有更友好的优化。

磁盘管理之前只有个 ceph-disk, 现在新引入了 ceph-volume。基于 lvm 来管理磁盘，并会逐渐废弃掉 ceph-disk。

![ceph-bluestore.png](https://xcodest.me/images/2018/ceph-bluestore.png)

基中比较有意思的是 RocksDB 的实现，RocksDB 原本只基于文件系统的。但是得益于它本身的灵活性，bluestore 实现了一套 RocksDB 的 Env 接口，还在 BlueStore 上面实现了一套 BlueFS 的接口与 BluestoreEnv 对接。使得 RocksDB 可以存储在 BlueStore 上面。

## wal & db 的大小问题

在 ceph bluestore 的情况下，wal 是 RocksDB 的 write-ahead log, 相当于之前的 journal 数据，db 是 RocksDB 的 metadata 信息。在磁盘选择原则是 block.wal > block.db > block。当然所有的数据也可以放到同一块盘上。

默认情况下， wal 和 db 的大小分别是 512 MB 和 1GB, 包括 Sage Weil 的 PPT 里面也是这样标明的[1](https://xcodest.me/ceph-bluestore-and-ceph-volume.html#fn-1)。现在没有一个太好的理论值，它和 ceph 里面的每个 OSD 里面的对象个数有关系。更多讨论可以参看[2](https://xcodest.me/ceph-bluestore-and-ceph-volume.html#fn-2)。 现在社区推荐的是 block size * 4% 的值。也就是说如果你的 block 盘大小是 1TB，那 block.db 的大小最少是 40GB。[4](https://xcodest.me/ceph-bluestore-and-ceph-volume.html#fn-4)[5](https://xcodest.me/ceph-bluestore-and-ceph-volume.html#fn-5)

值得注意的是，如果所有的数据都在单块盘上，那是没有必要指定 wal & db 的大小的。如果 wal & db 是在不同的盘上，由于 wal/db 一般都会分的比较小，是有满的可能性的。如果满了，这些数据会迁移到下一个快的盘上(wal - db - main)。所以最少不会因为数据满了，而造成无法写入[3](https://xcodest.me/ceph-bluestore-and-ceph-volume.html#fn-3)。

## 使用 bluestore 时的 osd 分区

如果是使用的 ceph-disk 管理磁盘，他会建立一个 100MB 的分区，来存放 keyring / whoami 这些信息，这和之前的逻辑是一样的。

如果是使用 ceph-volume 管理磁盘，`/var/lib/ceph/osd/ceph-0` 分区会从 tmpfs 挂载过来(也就是内存)

```plain
$ mount | grep osd
tmpfs on /var/lib/ceph/osd/ceph-0 type tmpfs (rw,relatime,seclabel)
$ ls -Alh /var/lib/ceph/osd/ceph-0
lrwxrwxrwx. 1 ceph ceph 19 Apr  7 21:36 block -> /dev/ceph-pool/osd0
lrwxrwxrwx. 1 root root 22 Apr  7 21:36 block.db -> /dev/ceph-pool/osd0.db
lrwxrwxrwx. 1 root root 23 Apr  7 21:36 block.wal -> /dev/ceph-pool/osd0.wal
-rw-------. 1 ceph ceph 37 Apr  7 21:36 ceph_fsid
-rw-------. 1 ceph ceph 37 Apr  7 21:36 fsid
-rw-------. 1 ceph ceph 55 Apr  7 21:36 keyring
-rw-------. 1 ceph ceph  6 Apr  7 21:36 ready
-rw-------. 1 ceph ceph 10 Apr  7 21:36 type
-rw-------. 1 ceph ceph  2 Apr  7 21:36 whoami
```

至于目录中的这些文件则是从 bluestore 盘一开始的 `BDEV_LABEL_BLOCK_SIZE=4096` 位置读取过来的。通过 以下命令，可以把所有的 label 打印出来

```plain
$ ceph-bluestore-tool  show-label --path /var/lib/ceph/osd/ceph-0
{
    "/var/lib/ceph/osd/ceph-0/block": {
        "osd_uuid": "c349b2ba-690f-4a36-b6f6-2cc0d0839f29",
        "size": 2147483648,
        "btime": "2018-04-04 10:22:25.216117",
        "description": "main",
        "bluefs": "1",
        "ceph_fsid": "14941be9-c327-4a17-8b86-be50ee2f962e",
        "kv_backend": "rocksdb",
        "magic": "ceph osd volume v026",
        "mkfs_done": "yes",
        "osd_key": "AQDgNsRaVtsRIBAA6pmOf7y2GBufyE83nHwVvg==",
        "ready": "ready",
        "whoami": "0"
    }
}
```

相关代码参看

- [ceph-volume activate](https://github.com/ceph/ceph/blob/d65b8844d16d71df01b57f368badc100db505506/src/ceph-volume/ceph_volume/devices/lvm/activate.py#L144)
- [ceph-bluestore-tool prime-osd-dir](https://github.com/ceph/ceph/blob/d65b8844d16d71df01b57f368badc100db505506/src/os/bluestore/bluestore_tool.cc#L316-L396)

使用 ceph-volume， 不管 store 使用的是 filestore 还是 bluestore, 都会把一些 tag 存在 lvm 上面， 可以使用以下命令查看(做了格式化处理)

```plain
$lvs -o lv_tags /dev/mapper/ceph--pool-osd
LV Tags
ceph.block_device=/dev/ceph-pool/osd
ceph.block_uuid=dRW0FO-KiVS-vBjB-PE42-RnSd-mL04-FRQmAz
ceph.cephx_lockbox_secret=
ceph.cluster_fsid=14941be9-c327-4a17-8b86-be50ee2f962e
ceph.cluster_name=ceph
ceph.crush_device_class=None
ceph.encrypted=0
ceph.osd_fsid=c349b2ba-690f-4a36-b6f6-2cc0d0839f29
ceph.osd_id=0
ceph.type=block
```

## osd 的盘是如何挂载的

ceph 依赖 systemd 来管理挂载，不需要配置 `/etc/fstab` 文件。在初始化 osd 的时候, ceph 会 enable 一个 ceph-volume@x.service 服务，其中 x 的格式如 `{lvm|simple}-{osd id}-{osd uuid}`, 这个服务会在系统的`local-fs.target` 组里面，当系统挂载本地盘的时候，会自动挂载上。

这个 ceph-volume@.service 定义如下

```plain
$systemctl cat ceph-volume@lvm-0-b7b4fa98-d36e-430b-9789-a432a078292c
# /usr/lib/systemd/system/ceph-volume@.service
[Unit]
Description=Ceph Volume activation: %i
After=local-fs.target
Wants=local-fs.target

[Service]
Type=oneshot
KillMode=none
Environment=CEPH_VOLUME_TIMEOUT=10000
ExecStart=/bin/sh -c 'timeout $CEPH_VOLUME_TIMEOUT /usr/sbin/ceph-volume-systemd %i'
TimeoutSec=0
[Install]
WantedBy=multi-user.target
```

可以看到， 他是把参数传递给了 `ceph-volume-systemd` 命令， 而这个命令又把参数解析后，传给了 `ceph-volume` 命令，最后的执行的命令是

```plain
ceph-volume lvm trigger {osd id} {osd uuid]
```

> 需要`ceph-volume-systemd` 这个命令的原因应该是 systemd 只能传一个参数

这个 `trigger` 会调用 `ceph-volume lvm activate` 命令，去准备相对应挂载及里面的数据初始化。

最后， `ceph-volume lvm activate` 会调用 `ceph-bluestore-tool pirme-osd-dir` 命令来初始化里面的数据。

## 其它

### ceph osd purge

ceph Limunous 新加了一个 `ceph osd purge` 命令，很好用，可以一个命令，把某个 osd 相关的信息都清除掉。包括

- osd
- crush rule
- auth key

### ceph-disk lvm

ceph-disk 应试不支持 lvm 的， 参见 http://tracker.ceph.com/issues/5461

不过 kolla 是否支持，可以验证下， 因为 kolla 的脚本里面不依赖 ceph-disk

------

1. https://www.slideshare.net/sageweil1/bluestore-a-new-storage-backend-for-ceph-one-year-in [↩](https://xcodest.me/ceph-bluestore-and-ceph-volume.html#fnref-1)
2. http://lists.ceph.com/pipermail/ceph-users-ceph.com/2017-September/020822.html [↩](https://xcodest.me/ceph-bluestore-and-ceph-volume.html#fnref-2)
3. http://lists.ceph.com/pipermail/ceph-users-ceph.com/2017-September/021037.html [↩](https://xcodest.me/ceph-bluestore-and-ceph-volume.html#fnref-3)
4. http://docs.ceph.com/docs/master/rados/configuration/bluestore-config-ref/#sizing [↩](https://xcodest.me/ceph-bluestore-and-ceph-volume.html#fnref-4)
5. http://lists.ceph.com/pipermail/ceph-users-ceph.com/2018-September/029643.html [↩](https://xcodest.me/ceph-bluestore-and-ceph-volume.html#fnref-5)
6. [ceph 存储引擎 bluestore 解析](http://www.sysnote.org/2016/08/19/ceph-bluestore/) [↩](https://xcodest.me/ceph-bluestore-and-ceph-volume.html#fnref-6)
7. https://ceph.com/community/new-luminous-bluestore/ [↩](https://xcodest.me/ceph-bluestore-and-ceph-volume.html#fnref-7)
8. [ceph bluestore 基本原理](http://liyichao.github.io/posts/ceph-bluestore-基本原理.html) [↩](https://xcodest.me/ceph-bluestore-and-ceph-volume.html#fnref-8)