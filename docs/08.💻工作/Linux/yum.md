---
title: Yum 常见操作记录

tags: 
  - Linux
  - Yum
categories: 
  - 💻 工作
  - Linux
date: 2020-05-23 18:21:46
permalink: /pages/97ccbd/
---

## 配置
默认 yum 下载的包保存在`/var/cache/yum`，也可以在 /etc/yum.conf 指定：
```plain
cachedir=/var/cache/yum # 存放目录
keepcache=1 # 1为保存 0为不保存
metadata_expire=90m # 过期时间
```

## 只下载不安装包

1. 安装`yum-downloadonly`或 `yum-plugin-downloadonly` 软件包
```bash
yum install yum-plugin-downloadonly
```
说明：`yum-downloadonly`是 yum 的一个插件，使得 yum 可以从 RHN 或者 yum 的仓库只下载包而不安装。

2. 安装完成后，查看`/etc/yum/pluginconf.d/downloadonly.conf` 配置文件的内容，确认这个插件已经启用：
```bash
vim /etc/yum/pluginconf.d/downloadonly.conf
```
```plain
[main] 
enabled=1
```
举例，从 yum 源下载 lrzsz 软件包
```bash
yum install --downloadonly lrzsz
```
### 自定义下载路径
默认下载保存的位是`/var/cache/yum/{RepositoryName}/packages/`目录。可以使用 yum 的参数`–downloaddir`来指定自定义的路径。与
`–downloadonly` 参数一块使用。
```bash
yum install --downloadonly --downloaddir=/download {YUOR_PACKAGE_NAME}
```
**注意**：指令后面全是双短横线！
参见：[Yum 只下载不安装包_运维_mini_xiang 的博客-CSDN 博客](https://blog.csdn.net/mini_xiang/article/details/53070321)

## 卸载安装同时清除全部依赖

1. 查看包依赖
```bash
yum history list {YUOR_PACKAGE_NAME}
```
```plain
Loaded plugins: fastestmirror
ID     | Login user               | Date and time    | Action(s)      | Altered
-------------------------------------------------------------------------------
    16 | root <root>              | 2017-06-07 11:39 | Install        |  101  
history list
```
其中 Altered:101 是指依赖的包数
2. 完全卸载所有的信赖包
```bash
yum history undo 16     # 其中16为查询到的id
```

## 搭建本地离线 yum 仓库
1. 把 rpm 包及其相关依赖全部都下载到本地，保存好。
2. 手动在/etc/yum.repos.d/目录下配置本地仓库信息。
3. 使用 createrepo 命令生成 repodata 信息。
4. 使用 yum repoinfo 检查确认。
具体参见：[搭建本地离线 yum 仓库 - 阿胜 4K - 博客园](https://www.cnblogs.com/asheng2016/p/local-yum.html#%E9%85%8D%E7%BD%AE%E6%9C%AC%E5%9C%B0yum%E4%BB%93%E5%BA%93%E4%BF%A1%E6%81%AF)