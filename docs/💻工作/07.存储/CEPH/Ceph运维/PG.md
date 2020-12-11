---
title: 归置组（PG）相关

categories: 
  - 💻 工作
  - 存储
  - CEPH
  - Ceph 运维
date: 2020-12-11 12:49:18
permalink: /pages/910899/
tags: 
  - 
---
# 1.说明
## 1.1 介绍
PG 全称 Placement Grouops，是一个逻辑的概念，一个 PG 包含多个 OSD。引入 PG 这一层其实是为了更好的分配数据和定位数据。

# 2. 常用操作
## 2.1 查看 pg 组映射信息
```plain
$ ceph pg dump
```

## 2.2 查看一个 PG 的 map
```plain
$ ceph pg map 1.2f6
osdmap e7768 pg 1.2f6 (1.2f6) -> up [6,14,25] acting [6,14,25]  
#其中[6,14,25]代表存储在osd.6、osd.14、osd.25节点，osd.6代表主副本存储的位置
```

## 2.3 查看 PG 状态
```plain
$ ceph pg stat
5416 pgs: 5416 active+clean; 471 GB data, 1915 GB used, 154 TB / 156 TB avail
```

## 2.4 查看 pg 详细信息
```plain
$ ceph pg 1.2f6 query
```

## 2.5 查看 pg 中 stuck 状态
```plain
$ ceph pg dump_stuck unclean
ok
 
$ ceph pg dump_stuck inactive
ok
 
$ ceph pg dump_stuck stale
ok
```

## 2.6 显示集群所有 pg 统计
```plain
$ ceph pg dump --format plain
```

## 2.7 恢复一个丢失的 pg
```plain
$ ceph pg {pg-id} mark_unfound_lost revert
```

## 2.8 显示非正常状态的 pg
```plain
$ ceph pg dump_stuck inactive|unclean|stale
```




