---
title: CephFS 监控埋点

tags: CephFS
categories: 
  - 💻 工作
  - 存储
  - CEPH
  - Ceph 监控
date: 2020-05-23 11:02:28
permalink: /pages/3a7947/
---
# 1. perf dump
## 1.1. FS Client Metrics Table
- ceph daemon /var/run/ceph/ceph-client.admin.asok  perf dump 

监控类型 | 监控项 |  说明 | 级别 |
---|---|---|---|
AsyncMessenger* | msgr_recv_messages | 网络接收消息 | |
* | msgr_send_messages | 网络发送消息 | |
* | msgr_recv_bytes | 网络接收字节 | |
* | msgr_send_bytes | 网络发送字节 | |
* | msgr_created_connections | 创建连接数 | |
* | msgr_active_connections | 有效连接数 | |
* | msgr_running_total_time | 线程运行的总时间 | |
* | msgr_running_send_time | 消息发送的总时间 | |
* | msgr_running_recv_time | 消息接收的总时间 | |
* | msgr_running_fast_dispatch_time | 快速调度总时间 | |

## 1.2. FS Client Metrics Table
监控类型 | 监控项 |  说明 | 级别 |
---|---|---|---|
client | reply.avgcount | 在元数据请求上接收答复的等待时间队列的平均数 | |
* | reply.sum | 在元数据请求上接收答复的等待时间队列的总数 | |
* | reply.avgtime | 在元数据请求上接收答复的等待时间队列的平均时间 | |
* | lat.avgcount | 处理元数据请求的等待时间队列的平均数 | |
* | lat.sum | 处理元数据请求的等待时间队列的总数 | |
* | lat.avgtime | 处理元数据请求的等待时间队列的平均时间 | |
* | wrlat.avgcount | 文件数据写入操作的等待时间队列的平均数 | |
* | wrlat.sum | 文件数据写入操作的等待时间队列的总数 | |
* | wrlat.avgtime | 文件数据写入操作的等待时间队列的平均时间 | |

## 1.3. FS ObjectCacher-libcephfs Metrics Table
监控类型 | 监控项 |  说明 | 级别 |
---|---|---|---|
objectcacher-libcephfs | cache_ops_hit | 命中缓存 | |
* | cache_ops_miss | 穿透缓存 | |
* | cache_bytes_hit | 命中缓存大小 | |
* | cache_bytes_miss | 穿透缓存大小 | |
* | data_read | 读数据大小 | |
* | data_written | 写缓存数据大小 | |
* | data_flushed | 数据刷新 | |
* | data_overwritten_while_flushing | 刷新时数据重写 | |
* | write_ops_blocked | 肮脏限制延迟的写操作 | |
* | write_bytes_blocked | 写入脏数据的限制 | |
* | write_time_blocked | 由于脏数据限制而阻塞写入的时间 | |


## 1.4. objecter
| 监控类型   |      监控项      |  说明  |
|----------|:-------------:|:-------------:|
| perf dump objecter  |  op_active         				 	  | 主动操作数	    					|
|   				  |  op_laggy         					  | 消极操作数	    					|
|   				  |  op_send         					  | 发送操作数	    					|
|   				  |  op_send_bytes         				  | 发送操作 bytes	    					|
|   				  |  op_resend         				  	  | 重操作数    							|
|   				  |  op_reply         				  	  | 回复操作数	    					|
|   				  |  op         				  		  | 操作数	    						|
|   				  |  op_r         				  		  | 读操作数    							|
|   				  |  op_w         				  		  | 写操作数    							|
|   				  |  op_rmw         				  	  | 读写修改操作数    					|
|   				  |  op_pg         				  		  | PG 操作数    							|
|   				  |  osdop_stat         				  | 操作状态    							|
|   				  |  osdop_create         				  | 创建对象操作    						|
|   				  |  osdop_read         				  | 读操作    							|
|   				  |  osdop_write         				  | 写操作    							|
|   				  |  osdop_writefull         			  | 写满对象操作    						|
|   				  |  osdop_writesame         			  | 写相同的对象操作    					|
|   				  |  osdop_append         				  | 追加操作    							|
|   				  |  osdop_zero         				  | 设置对象 0 操作    						|
|   				  |  osdop_truncate         			  | 截断对象操作    						|
|   				  |  osdop_delete         				  | 删除对象操作    						|
|   				  |  osdop_mapext         				  | 映射范围操作    						|
|   				  |  osdop_sparse_read         			  | 稀少读操作    						|
|   				  |  osdop_clonerange         			  | 克隆范围操作    						|
|   				  |  osdop_getxattr         			  | 获取 xattr 操作    						|
|   				  |  osdop_setxattr         			  | 设置 xattr 操作    						|
|   				  |  osdop_cmpxattr         			  | 比较 xattr 操作    						|
|   				  |  osdop_rmxattr         			  	  | 移除 xattr 操作    						|
|   				  |  osdop_resetxattrs         			  | 重置 xattr 操作    						|
|   				  |  osdop_tmap_up         			  	  | tmap 更新操作    						|
|   				  |  osdop_tmap_put         			  | tmap 推送操作    						|
|   				  |  osdop_tmap_get         			  | tmap 获取操作    						|
|   				  |  osdop_call         			  	  | 调用执行操作    						|
|   				  |  osdop_watch         			  	  | 监控对象操作    						|
|   				  |  osdop_notify         			  	  | 对象操作通知    						|
|   				  |  osdop_src_cmpxattr         		  | 多个操作扩展属性    					|
|   				  |  osdop_pgls         		  		  | pg 对象操作   							|
|   				  |  osdop_pgls_filter         		  	  | pg 过滤对象操作    					|
|   				  |  osdop_other         		  		  | 其他操作    							|
|   				  |  linger_active         		  		  | 主动延迟操作    						|
|   				  |  linger_send         		  		  | 延迟发送操作    						|
|   				  |  linger_resend         		  		  | 延迟重新发送    						|
|   				  |  linger_ping         		  		  | 延迟 ping 操作    						|
|   				  |  poolop_active         		  		  | 主动池操作    						|
|   				  |  poolop_send         		  		  | 发送池操作   							|
|   				  |  poolop_resend         		  		  | 重新发送池操作	   							|
|   				  |  poolstat_active         		  	  | 主动获取池子统计操作   							|
|   				  |  poolstat_send         		  		  | 发送池子统计操作   							|
|   				  |  poolstat_resend         		  	  | 重新发送池子统计操作   							|
|   				  |  statfs_active         		  		  | fs 状态操作   							|
|   				  |  statfs_send         		  		  | 发送 fs 状态   							|
|   				  |  statfs_resend         		  		  | 重新发送 fs 状态   							|
|   				  |  command_active         		  	  | 活动的命令   							|
|   				  |  command_send         		  		  | 发送指令  							|
|   				  |  command_resend         		  	  | 重新发送指令  							|
|   				  |  map_epoch         		  	  		  | OSD map epoch  							|
|   				  |  map_full         		  	  		  | 接收满的 OSD map  							|
|   				  |  map_inc         		  	  		  | 接收到增量 OSD map  							|
|   				  |  osd_sessions         		  	  	  | osd 会话  							|
|   				  |  osd_session_open         		  	  	  | 打开 osd 会话  							|
|   				  |  osd_session_close         		  	  	  | 关闭 osd 会话  							|
|   				  |  osd_laggy         		  	  	  	 | 缓慢的 osd 会话  							|
|   				  |  omap_wr         		  	  	  	 | osd map 读写操作  							|
|   				  |  omap_rd         		  	  	  	 | osd map 读操作  							|
|   				  |  omap_del         		  	  	  	 | osd map 删除操作  							|


## 1.5. throttle
监控类型 | 监控项 |  说明 | 级别 |
---|---|---|---|
perf dump throttle-*|val|当前可用的值||	 	 	 
*|max|最大限制数||	 	 	 
*|get|获取到的值||	 	 	 
*|get_sum|获取到的总数	|| 	 	 
*|get_or_fail_fail|获取或者错误值||	 	 	 
*|get_or_fail_success|获取或者错误成功值||	 	 	 
*|take|接受值||	 	 	 
*|take_sum|接受总数||	 	 	 
*|put	|推送值||	 	 	 
*|put_sum|推送总数	 ||	 	 
*|wait.avgcount|等待平均数量||	 	 	 
*|wait.sum|等待总数||	

# 2. status
ceph daemon /var/run/ceph/ceph-client.admin.asok status

|监控类型 | 监控项 |  说明 | 级别 |
|---|---|---|---|
|status | osd_epoch_barrier |||
| | osd_epoch | osd epoch 编号 ||
| | mds_epoch | mds epoch 编号 ||
| | inode_count | 文件句柄数量 ||
| | addr_str | 客户端地址 ||
| | inst_str | 客户端 inst 信息 ||
| | id | 编号 ||
| | dentry_pinned_count | 文件夹数量 ||
| | dentry_count | 所有文件数量(包含文件夹) ||
| | metadata.ceph_sha1 | ceph sha1||
| | metadata.ceph_version | ceph 版本号||
| | metadata.entity_id | 账号 id 信息||
| | metadata.hostname | 机器名||
| | metadata.mount_point | 挂载目录||
| | metadata.pid| 进程 pid||
| | metadata. root | 挂载父节点||