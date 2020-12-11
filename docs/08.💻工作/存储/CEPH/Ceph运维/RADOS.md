---
title: RADOS 相关

categories: 
  - 💻 工作
  - 存储
  - CEPH
  - Ceph 运维
date: 2020-12-11 12:49:18
permalink: /pages/15695e/
tags: 
  - 
---
# 1.说明
## 1.1 介绍
RADOS 全称 Reliable Autonomic Distributed Object Store，是 Ceph 集群的精华，用户实现数据分配、Failover 等集群操作。

# 2. 常用操作
## 2.1 查看集群多少个 pool
```plain
# rados lspools
rbd
test_data
test_metadata
test
benmark_test
.rgw.root
default.rgw.control
default.rgw.meta
default.rgw.log
default.rgw.buckets.index
web-services
test_pool
cephfs_data
cephfs_metadata
test_lihang
```

## 2.2 查看集群 pool 容量情况
```$ rados df
# rados df
POOL_NAME    USED OBJECTS CLONES COPIES MISSING_ON_PRIMARY UNFOUND DEGRADED RD_OPS      RD WR_OPS      WR 
test      324 MiB      95      0    285                  0       0        0    957 4.2 MiB  29966 586 MiB 

total_objects    95
total_used       45 GiB
total_avail      497 GiB
total_space      543 GiB
```

## 2.3 创建 pool
```plain
$ rados mkpool test_lihang1
successfully created pool test_lihang1
```

## 2.4 查看 pool 中 object 对象
```plain
$ rados ls -p test_data | more
10000026de5.00000000
1000005f1f3.00000000
100000664db.00000000
1000007461f.00000000
10000021bdf.00000000
1000005ef12.00000000
10000000fc8.00000000
1000002afd7.00000000
100000143b0.00000000
1000000179d.00000000
10000001b2f.00000000
10000073faa.00000000
10000072576.00000000
1000002a9f0.00000000
```

## 2.5 创建一个对象 object
```plain
$ rados create test-object -p test_data
 
$ rados -p test_data ls
```

## 2.6 删除一个对象 object
```plain
$ rados rm test-object -p test_data
```
