---
title: TODO，其他暂时无法归类

tags: 
  - 存储
categories: 
  - 💻 工作
  - Linux
date: 2020-05-23 12:27:56
permalink: /pages/c5c060/
---

## 不重启扫描磁盘
```bash
echo '- - -' > /sys/class/scsi_host/host0/scan  # 有几个host就扫描几个，除非找到已加磁盘
```

## 指令查询
[jaywcjlove/linux-command: Linux 命令大全搜索工具，内容包含 Linux 命令手册、详解、学习、搜集。https://git.io/linux](https://github.com/jaywcjlove/linux-command)

## python3 编译成 pyc 文件
```shell
python3 -m compileall -b .
```
[python3 编译成 pyc 文件_kriszhang 的博客-CSDN 博客](https://blog.csdn.net/kriszhang/article/details/78773285)