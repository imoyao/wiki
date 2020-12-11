---
title: 监视器（mon）相关

categories: 
  - 💻 工作
  - 存储
  - CEPH
  - Ceph 运维
date: 2020-12-11 12:49:17
permalink: /pages/1481d9/
tags: 
  - 
---
# 1.说明
## 1.1 介绍
一个 Ceph 集群需要多个 Monitor 组成的小集群，它们通过 Paxos 同步数据，用来保存 OSD 的元数据。

# 2. 常用操作
## 2.1 查看 mon 状态
```plain
$ ceph mon stat
e1: 3 mons at {ceph-xx-osd00=10.69.0.1:6789/0,ceph-xx-osd01=10.69.0.2:6789/0,ceph-xx-osd02=10.69.0.3:6789/0}, election epoch 52, leader 0 ceph-xx-osd01, quorum 0,1,2 ceph-xx-osd01,ceph-xx-osd00,ceph-xx-osd02
```
## 2.2 查看 mon 的选举状态
```plain
$ ceph quorum_status
{"election_epoch":52,"quorum":[0,1,2],"quorum_names":["ceph-xx-osd01","ceph-xx-osd00","ceph-xx-osd02"],"quorum_leader_name":"ceph-xx-osd01","monmap":{"epoch":1,"fsid":"97219550-d917-4154-b745-32bac14f99f2","modified":"2017-08-31 16:14:09.434281","created":"2017-08-31 16:14:09.434281","features":{"persistent":["kraken","luminous"],"optional":[]},"mons":[{"rank":0,"name":"ceph-xx-osd01","addr":"10.69.0.2:6789/0","public_addr":"10.69.0.2:6789/0"},{"rank":1,"name":"ceph-xx-osd00","addr":"10.69.0.3:6789/0","public_addr":"10.69.0.3:6789/0"},{"rank":2,"name":"ceph-xx-osd02","addr":"10.69.0.3:6789/0","public_addr":"10.69.0.3:6789/0"}]}}
```
## 2.3 查看 mon 的映射信息
```plain
$ ceph mon dump
dumped monmap epoch 1
epoch 1
fsid 97219550-d917-4154-b745-32bac14f99f2
last_changed 2017-08-31 16:14:09.434281
created 2017-08-31 16:14:09.434281
0: 10.69.0.2:6789/0 mon.ceph-xx-osd01
1: 10.69.0.3:6789/0 mon.ceph-xx-osd00
2: 10.69.0.1:6789/0 mon.ceph-xx-osd02
```
## 2.4 删除一个 mon 节点
```plain
$ ceph mon remove ceph-xx-osd01
removing mon.ceph-xx-osd01 at 10.69.0.2:6789/0, there will be 2 monitors

$ ceph mon dump
dumped monmap epoch 2
epoch 2
fsid 97219550-d917-4154-b745-32bac14f99f2
last_changed 2017-11-23 17:06:35.075538
created 2017-08-31 16:14:09.434281
0: 10.69.0.3:6789/0 mon.ceph-xx-osd00
1: 10.69.0.1:6789/0 mon.ceph-xx-osd02
```

## 2.5 添加一个 mon 节点
```plain
$ ceph mon add  ceph-xx-osd01 10.69.0.2:6789
adding mon.ceph-xx-osd01 at 10.69.0.2:6789/0


$ ceph mon dump
dumped monmap epoch 3
epoch 3
fsid 97219550-d917-4154-b745-32bac14f99f2
last_changed 2017-11-23 17:07:39.789494
created 2017-08-31 16:14:09.434281
0: 10.69.0.2:6789/0 mon.ceph-xx-osd01
1: 10.69.0.4:6789/0 mon.ceph-xx-osd00
2: 10.69.0.3:6789/0 mon.ceph-xx-osd02
```

## 2.6 获取 mon map
```plain
$ ceph mon getmap -o 1.txt
got monmap epoch 3


$ monmaptool --print 1.txt
monmaptool: monmap file 1.txt
epoch 3
fsid 97219550-d917-4154-b745-32bac14f99f2
last_changed 2017-11-23 17:07:39.789494
created 2017-08-31 16:14:09.434281
0: 10.69.0.2:6789/0 mon.ceph-xx-osd01
1: 10.69.0.4:6789/0 mon.ceph-xx-osd00
2: 10.69.0.3:6789/0 mon.ceph-xx-osd02
```

## 2.7 注入新节点到 mon map
```plain
$ ceph mon getmap -o 1.txt
got monmap epoch 3


$ monmaptool --print 1.txt
monmaptool: monmap file 1.txt
epoch 3
fsid 97219550-d917-4154-b745-32bac14f99f2
last_changed 2017-11-23 17:07:39.789494
created 2017-08-31 16:14:09.434281
0: 10.69.0.2:6789/0 mon.ceph-xx-osd01
1: 10.69.0.4:6789/0 mon.ceph-xx-osd00
2: 10.69.0.3:6789/0 mon.ceph-xx-osd02

$ ceph-mon -i node4 -inject-monmap 1.txt
```
## 2.8 查看 mon 的 admin socket
```plain
$  ceph-conf --name mon.ceph-xx-osd00 --show-config-value admin_socket
/var/run/ceph/ceph-mon.ceph-xx-osd00.asok
```

## 2.9 查看 mon 的详细状态
```plain
$  ceph daemon mon.ceph-xx-osd00  mon_status
```

## 2.10 停止单机的 mon
```plain
#登陆对应mon的机器，停止mon进程
systemctl stop ceph-mon.target

#检查Mon的状态
ceph mon stat
```

