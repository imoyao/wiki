---
title: RGW 监控埋点.md

tags: RGW
categories: 
  - 💻 工作
  - 存储
  - CEPH
  - Ceph 监控
date: 2020-05-23 11:02:28
permalink: /pages/5e41c5/
---
# 1. RADOS
## 1.1 RGW Client Metrics Table
- ceph --admin-daemon /var/run/ceph/ceph-client.rgw.ceph-xx-osd04.ys.asok perf dump 

监控类型 | 监控项 |  说明 | 级别 |
|---|---|---|---|
|AsyncMessenger | msgr_recv_messages | 网络接收消息 | |
|* | msgr_send_messages | 网络发送消息 | |
|* | msgr_recv_bytes | 网络接收字节 | |
|* | msgr_send_bytes | 网络发送字节 | |
|* | msgr_created_connections | 创建连接数 | |
|* | msgr_active_connections | 有效连接数 | |
|* | msgr_running_total_time | 线程运行的总时间 | |
|* | msgr_running_send_time | 消息发送的总时间 | |
|* | msgr_running_recv_time | 消息接收的总时间 | |
|* | msgr_running_fast_dispatch_time | 快速调度总时间 | |

## 1.2 CCT Metrics Table
监控类型 | 监控项 |  说明 | 级别 |
|---|---|---|---|
|cct | total_workers | 总 worker 数 | |
|* | unhealthy_workers | 不健康的 worker | |

## 1.3 RADOS Client Metrics Table
 - ceph --admin-daemon /var/run/ceph/ceph-client.rgw.ceph-xx-osd04.ys.asok perf dump

监控类型 | 监控项 |  说明 | 级别 |
|---|---|---|---|
|client.rgw.<rgw_node_name> | req | 请求数 | |
|* | failed_req | 错误的请求数 | |
|* | get | 获取数 |  |
|* | get_b | 获取的大小 | |
|* | get_initial_lat.avgcount | 获取延迟 平均数 | |
|* | get_initial_lat.sum | 获取延迟 总数 | |
|* | put | put | |
|* | put_b | put 大小 | |
|* | put_initial_lat | put 延迟 | |
|* | qlen | 队列长度 | |
|* | qactive | 活跃的请求队列 | |
|* | cache_hit | 命中缓存 | |
|* | cache_miss | 穿透缓存 | |
|* | keystone_token_cache_hit | 命中 keystone 秘钥缓存 | |
|* | keystone_token_cache_miss | 穿透 keystone 秘钥缓存 | |

## 1.4 Finisher-RadosClient Metrics Table
监控类型 | 监控项 |  说明 | 级别 |
---|---|---|---|
|finisher-radosclient | queue_len | 队列长度 |  |
|* | complete_latency.avgcount | 完成的请求延迟队列的平均数 |  |
|* | complete_latency.sum | 完成的请求延迟队列的总数 | |
|* | complete_latency.avgtime | 完成的请求延迟队列的平均时间 | |

## 1.5 Objecter Metrics Table
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


## 1.6 RADOS Gateway Throttle
监控类型 | 监控项 |  说明 | 级别 |
|---|---|---|---|
|perf dump throttle-*|val|当前可用的值||	 	 	 
|*|max|最大限制数||	 	 	 
|*|get|获取到的值||	 	 	 
|*|get_sum|获取到的总数	|| 	 	 
|*|get_or_fail_fail|获取或者错误值||	 	 	 
|*|get_or_fail_success|获取或者错误成功值||	 	 	 
|*|take|接受值||	 	 	 
|*|take_sum|接受总数||	 	 	 
|*|put	|推送值||	 	 	 
|*|put_sum|推送总数	 ||	 	 
|*|wait.avgcount|等待平均数量||	 	 	 
|*|wait.sum|等待总数||	



