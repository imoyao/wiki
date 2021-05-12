---
title: RBD Snapshot 快照灾备方案

tags: 
  - ceph
categories: 
  - 💻 工作
  - 存储
  - CEPH
  - 方案
date: 2020-05-23 11:02:28
permalink: /pages/ca33bc/
---

## Snapshot

### 介绍

Cluster A & B 仍然是独立的 Ceph 集群，通过 RBD 的 snapshot 机制，在 Cluster A 端，针对 image 定期通过 rbd 创建 image 的 snap，

然后通过`rbd export-diff`, `rbd import-diff`命令来完成 image 备份到 Cluster B。

### 原理

 异步备份，基于 RBD 的`snapshot`机制

### 命令和步骤

把 Cluster A 的 pool rbd 下面 image testimage 异步备份到 Cluster B 的 pool rbd 下的相同 image 上；

1.  在 Cluster A/B 上创建 rbd/testimage
    `rbd create -p rbd --size 10240 testimage`

2.  在准备备份 image 前，暂停 Cluster A 端对 testimage 的 IO 操作，然后创建个 snapshot
    `rbd snap create <snap-name>`

3.  导出 Cluster A 端的 testimage 数据，不指定 from-snap
    `rbd export-diff <image-name> <path>`

4.  copy 上一步中导出的文件到 Cluster B，并导入数据到 testimage
    `rbd import-diff <path> <image-name>`

后续需周期性的暂停 Cluster A 端的 testimage 的 IO，然后创建 snapshot，通过 `rbd export-diff <image-name> [--from-snap <snap-name>] <path>`命令导出 incremental diff，

之后把差异数据文件 copy 到 Cluster B 上，然后通过命令`rbd import-diff <path> <image-name>`导入。

【注】：也可不暂停 Cluster A 端的 IO，直接 take snapshot；这样并不会引起 image 的数据不一致，只是有可能会使`rbd export-diff`时导出的数据在 take snapshot 之后

### 优缺点

* 优点：
1.  当前 Ceph 版本就支持 rbd snapshot 的功能
2.  命令简介方便，通过定制执行脚本就能实现 rbd 块设备的跨区备份

* 缺点：
1.  每次同步前都需要在源端 take snapshot
2.  持续的 snapshots 可能导致 image 的读写性能下降
3.  还要考虑后续删除不用的 snapshots
4.  snapshot 只能保证 IO 的一致性，并不能保证使用 rbd 块设备上的系统一致性；

可以每次暂停 image 的 IO，sync IO 数据来保证 rbd 块设备上的系统一致性，但需要虚拟机支持 qemu-guest-agent

### 参考资料
[ceph 块存储跨机房灾备调研 | ictfox blog](http://www.yangguanjun.com/2017/02/22/rbd-data-replication/)
[https://ceph.com/dev-notes/incremental-snapshots-with-rbd/](https://ceph.com/dev-notes/incremental-snapshots-with-rbd/)
[https://www.rapide.nl/blog/item/ceph_-_rbd_replication.html](https://www.rapide.nl/blog/item/ceph_-_rbd_replication.html)
[http://wiki.libvirt.org/page/Qemu_guest_agent](http://wiki.libvirt.org/page/Qemu_guest_agent)
[http://www.zphj1987.com/2016/06/22/rbd](http://www.zphj1987.com/2016/06/22/rbd%E7%9A%84%E5%A2%9E%E9%87%8F%E5%A4%87%E4%BB%BD%E5%92%8C%E6%81%A2%E5%A4%8D/)
[http://ju.outofmemory.cn/entry/243899](http://ju.outofmemory.cn/entry/243899)

## CEPH BackUp

### 介绍
teralytics 是一家国外的大数据公司，这个是他们开源的 ceph 的备份的工具。
这个软件基于 python 的实现，可以说作者的实现逻辑是很清晰的，并且提供了配置文件的方式，基本上是各个细节都考虑的比较到位，很容易上手，可以直接拿来使用，或者集成到自己的平台中去，是一个很好的软件。

软件包含以下功能：
- 支持存储池和多 image 的只对
- 支持自定义备份目标路径
- 配置文件支持
- 支持备份窗口设置
- 支持压缩选项
- 支持增量和全量备份的配置

### 原理
异步备份，基于 RBD 的 snapshot 机制。

### 命令和步骤

#### 全量备份配置
上面的配置文件已经写好了，直接执行备份命令就可以了
```plain
cephbackup
Starting backup for pool rbd
Full ceph backup
Images to backup:
 rbd/zp
Backup folder: /tmp/
Compression: True
Check mode: False
Taking full backup of images: zp
rbd image 'zp':
 size 40960 MB in 10240 objects
 order 22 (4096 kB objects)
 block_name_prefix: rbd_data.25496b8b4567
 format: 2
 features: layering
 flags:
Exporting image zp to /tmp/rbd/zp/zp_UTC20170119T092933.full
Compress mode activated
# rbd export rbd/zp /tmp/rbd/zp/zp_UTC20170119T092933.full
Exporting image: 100% complete...done.
# tar Scvfz /tmp/rbd/zp/zp_UTC20170119T092933.full.tar.gz /tmp/rbd/zp/zp_UTC20170119T092933.full
tar: Removing leading `/' from member names
```
压缩的如果开了，正好文件也是稀疏文件的话，需要等很久，压缩的效果很好，dd 生成的文件可以压缩到很小

检查备份生成的文件
```plain
ll /tmp/rbd/zp/zp_UTC20170119T092933.full*
-rw-r--r-- 1 root root 42949672960 Jan 19 17:29 /tmp/rbd/zp/zp_UTC20170119T092933.full
-rw-r--r-- 1 root root 0 Jan 19 17:29 /tmp/rbd/zp/zp_UTC20170119T092933.full.tar.gz
```

#### 全量备份的还原
```plain
rbd import /tmp/rbd/zp/zp_UTC20170119T092933.full zpbk
```
检查数据，没有问题

#### 增量备份配置
写下增量配置的文件，修改下备份模式的选项
```plain
[rbd]
window size = 7
window unit = day
destination directory = /tmp/
images = zp
compress = yes
ceph config = /etc/ceph/ceph.conf
backup mode = incremental
check mode = no
```
执行多次进行增量备份以后是这样的
```plain
[root@lab8106 ~]#ll /tmp/rbd/zpbk/
total 146452
-rw-r--r-- 1 root root 42949672960 Jan 19 18:04 zpbk@UTC20170119T100339.full
-rw-r--r-- 1 root root 66150 Jan 19 18:05 zpbk@UTC20170119T100546.diff_from_UTC20170119T100339
-rw-r--r-- 1 root root 68 Jan 19 18:05 zpbk@UTC20170119T100550.diff_from_UTC20170119T100546
-rw-r--r-- 1 root root 68 Jan 19 18:06 zpbk@UTC20170119T100606.diff_from_UTC20170119T100550
-rw-r--r-- 1 root root 68 Jan 19 18:06 zpbk@UTC20170119T100638.diff_from_UTC20170119T100606
```
#### 增量备份的还原
分成多个步骤进行
```plain
1、进行全量的恢复
# rbd import config@UTC20161130T170848.full dest_image
2、重新创建基础快照
# rbd snap create dest_image@UTC20161130T170848
3、还原增量的快照(多次执行)
# rbd import-diff config@UTC20161130T170929.diff_from_UTC20161130T170848 dest_image
```
本测试用例还原步骤就是
```plain
rbd import zpbk@UTC20170119T100339.full zpnew
rbd snap create zpnew@UTC20170119T100339
rbd import-diff zpbk@UTC20170119T100546.diff_from_UTC20170119T100339 zpnew
rbd import-diff zpbk@UTC20170119T100550.diff_from_UTC20170119T100546 zpnew
rbd import-diff zpbk@UTC20170119T100606.diff_from_UTC20170119T100550 zpnew
rbd import-diff zpbk@UTC20170119T100638.diff_from_UTC20170119T100606 zpnew
```
检查数据，没有问题

##  RBD Mirroring

###  介绍

Ceph 新的 rbd mirror 功能支持配置两个 Ceph Cluster 之间的 rbd 同步

###  原理

利用 Journal 日志进行异步备份，Ceph 自身带有的 rbd mirror 功能

###  命令和步骤

详见：rbd-mirror

###  优缺点

* 优点：
1.  Ceph 新的功能，不需要额外开发
2.  同步的粒度比较小，为一个块设备的 transaction
3.  保证了 Crash consistency
4.  可配置 pool 的备份，也可单独指定 image 备份

* 缺点：
1.  需要升级线上 Ceph 到 Jewel 10.2.2 版本以上
2.  Image Journal 日志性能影响较为严重

## 结论

### 方案对比

方案 |	详细说明 |	优点 |	缺点 |
---|---|---|---|
Snapshot | 主站点备份时为存储块打快照，将快照的差异部分发送到备站点重新生成新快照 | 1.当前 Ceph 版本就支持 rbd snapshot 的功能 <br> 2. 命令简介方便，通过定制执行脚本就能实现 rbd 块设备的跨区备份 <br> 3. 不需要对集群操作升级降级操作<br>4. 风险较低，简单，易实现 |1. 快照对原块的性能有很大影响，尤其是随机 IO <br>2. 快照间的差异部分是在备份时计算出来的，因此很耗时，即使两个快照间没有差异也要花上很长一段时间来扫描差异部分<br> 3. 定期备份存在差异数据丢失
Ceph-backup|	官方社区基于快照的方式，进行包装了下	| 同上	|同上 |
RBD Mirroring| 主要是客户端多写一份日志，然后异步同步到备集群进行实时备份 | 1. Ceph 新的功能，不需要额外开发<br>2. 同步的粒度比较小，为一个块设备的 transaction<br>3. 保证了 Crash consistency <br>4. 可配置 pool 的备份，也可单独指定 image 备份<br>5. 实时备份保证数据的一致性 |1. 需要升级线上 Ceph 到 Jewel 10.2.2 版本以上<br>2. Image Journal 日志性能影响较为严重

### 总结

结合业内的各大公司的灾备方案，以及社区相关的技术文档。个人建议用快照的方式， 简单、便捷、风险较低、易实现。

并且国内云厂商也普遍都是利用快照的方式实现灾备方案，然后加上自己的策略进行包装。

rbd-mirror 功能还是比较新 并且官方的文档也有一些措施进行优化，但是效果不佳。

官方也把这块列为 todolist，期待下个版本进行优化。
