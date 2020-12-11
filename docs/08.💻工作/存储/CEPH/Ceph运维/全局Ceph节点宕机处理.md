---
title: 全局 Ceph 节点宕机处理
categories: 
  - 💻 工作
  - 存储
  - CEPH
  - Ceph 运维
date: 2020-12-11 12:49:18
permalink: /pages/4a419f/
tags: 
  - 
---
# 4. 全局 Ceph 节点宕机处理

----------

在极端情况下，如数据中心断电，造成 Ceph 存储集群全局宕机，可以按照本节所示流程进行 Ceph 集群上电恢复操作。

### 4.1 手动上电执行步骤

1. 如为 Ceph 集群上电，monitor server 应最先上电；集群上电前确认使用 Ceph 之前端作业服务已停止。

2. 使用 IPMI 或于设备前手动进行上电。

3. 确认 NTP 服务及系统时间已同步，命令如下：

   `# ps-ef | grep ntp`

   `# date`

   `# ntpq -p`

4. 登入上电之 ceph server 确认 ceph service 已正常运行，命令如下：

   `# ps -ef | grep ceph`

5. 登入集群 monitor server 查看状态，OSD 全都 up 集群仍为 `noout flag(s) set`

   `# ceph -s`

   `# ceph osd tree`

6. 登入 monitor server 解除 `stopping w/out rebalancing`，命令如下：

   `# ceph osd unset noout`

   `# ceph -w`

   使用 `ceph-w` 可查看集群运作输出，同步完毕后集群 health 应为`HEALTH_OK` 状态。

### 4.2 恢复后检查步骤

1. 确认设备上电状态，以 IPMI 或 于设备前确认电源为开启上电状态。
2. `ping ceph monitor server`，检查 monitor server 可以 ping 通。
3. 系统时间和校时服务器时间同步。
4. `ceph -s`  状态为`HEALTH_OK`
5. `ceph osd tree` OSD 状态皆为`UP`

### 4.3 恢复使用指令及其说明

1. `ceph -s` ： 确认 ceph cluster status
2. `ceph -w` ： 查看集群运作输出
3. `ceph osd tree` ： 查看 ceph cluster 上 osd 排列及状态
4. `start ceph-all` ： 启动 所有 ceph service
5. `start ceph-osd-all` ： 启动 所有 osd service
6. `start ceph-mon-all` ： 启动 所有 mon service
7. `start ceph-osd id={id}` ： 启动指定 osd id service
8. `start ceph-mon id={hostname}` ： 启动指定 ceph monitor host
9. `ceph osd set noout` ： ceph stopping w/out rebalancing
10. `ceph osd unset noout` ： 解除 ceph stopping w/out rebalancing







