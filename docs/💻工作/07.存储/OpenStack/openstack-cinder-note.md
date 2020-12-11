---
title: OpenStack 开发记录
tags: 
  - OpenStack
  - devstack
  - cinder
  - TODO
categories: 
  - 💻 工作
  - 存储
  - OpenStack
date: 2019-12-27 14:32:54
cover: null
permalink: /pages/6686bb/
---
{%note warning%}
**注意**：这是一条**仅**用于个人经验的基于 devstack 的开发记录，除“推荐阅读”章节以外，不针对大众有参考价值。
{% endnote%}

## 服务管理

```bash
systemctl restart  devstack@c-vol.service
```

## 查看日志

```bash
journalctl -f -u devstack@n-cpu.service
# vol 日志
journalctl -u devstack@c-vol.service

```

## drivers 路径
```plain
/opt/stack/cinder/cinder/volume/drivers/
```
## 认证

###  激活认证
在控制节点上，获得 admin 凭证来获取只有管理员能执行的命令的访问权限：
```bash
source /opt/stack/openrc.sh
```
### 查看 cinder 配置状态
看状态之前必须先执行上面一条命令给权限；

```bash
cinder service-list
```

### openstack 界面登录和 ssh 后台登录
```plain
IP：10.10.15.139    浏览器访问用户名admin,密码openstack;  ssh用户名qzz,密码qiu199212
```

## fc 和 ipsan 输出后，后台用 lsblk 可以看到

## 修改 cinder.conf 配置

```bash
default_volume_type = estorip-1
enabled_backends = estorip-1


[Estor]
volume_driver = cinder.volume.drivers.estor.estor_iscsi.EstorIscsiDriver
san_ip=10.10.15.180
san_login = superuser
san_password = P@ssw0rd
volume_group = StorPool11
volume_backend_name = estorip
use_multipath_for_image_xfer = True
```
## 使用 DRBD 作为 OpenStack 存储后端
[How to Setup LINSTOR in OpenStack » LINBIT](https://www.linbit.com/how-to-setup-linstor-in-openstack/)
## 推荐阅读

一些深入理解时可能有用的链接
- [OpenStack Docs: Drivers](https://docs.openstack.org/cinder/latest/contributor/drivers.html)
- [Cinder/how-to-contribute-a-driver - OpenStack](https://wiki.openstack.org/wiki/Cinder/how-to-contribute-a-driver)
- [OpenStack Docs: 概况](https://docs.openstack.org/liberty/zh_CN/install-guide-rdo/overview.html)
- [OpenStack 源码分析-Cinder 创建卷流程 | Yikun](http://yikun.github.io/2016/02/14/OpenStack%E6%BA%90%E7%A0%81%E5%88%86%E6%9E%90-Cinder%E5%88%9B%E5%BB%BA%E5%8D%B7%E6%B5%81%E7%A8%8B/)
- [Cinder 云盘创建与挂载流程](https://runsisi.com/2019-07-08/openstack-cinder)
- [Cinder 命令总结](https://blog.csdn.net/qq806692341/article/details/52397440)
- [cinder create volume 的流程(1) - 一切都是当下 - 博客园](https://www.cnblogs.com/potato-chip/p/10305835.html)
- [Openstack Cinder 中建立 volume 过程的源码解析（1）_网络_溜溜小哥-CSDN 博客](https://blog.csdn.net/gaoxingnengjisuan/article/details/22518045)
- [Openstack Cinder 中建立 volume 过程的源码解析（9）_后端_溜溜小哥-CSDN 博客](https://blog.csdn.net/gaoxingnengjisuan/article/details/23794279)
- [Cinder 组件解析 - luohaixian - 博客园](https://www.cnblogs.com/luohaixian/p/8134967.html)
- [探索 OpenStack 之（11）：cinder-api Service 启动过程分析 以及 WSGI / Paste deploy / Router 等介绍 - SammyLiu - 博客园](https://www.cnblogs.com/sammyliu/p/4272611.html)
- [cinder 块存储 后端采用 lvm、nfs 安装配置 - 子隐 - 博客园](https://www.cnblogs.com/elvi/p/7735881.html)
- [系统运维|30 个 Openstack 经典面试问题和解答](https://linux.cn/article-10328-1.html)