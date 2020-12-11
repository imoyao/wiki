---
title: Ceph RBD 快照

tags: 
  - ceph
categories: 
  - 💻 工作
  - 存储
  - CEPH
  - 方案
date: 2020-05-23 11:02:28
permalink: /pages/1f8f5c/
---
# 一、说明
从主集群定期的导出最近两个快照之差，然后导入到备集群。

# 二、Ceph 生成差量文件的方式
## 2.1 导出某个 image 从创建到此刻的变化
### 2.1.1 导出快照
```plain
rbd export-diff test_pool/test_image testimage_now
```
#### 2.1.2 导入快照
```plain
rbd import-diff testimage_now test_pool/test_image
```
#### 2.1.3 流程图
![__image_____.png](https://upload-images.jianshu.io/upload_images/2099201-99e61d6804426e19.png)

## 2.2 导出 image 从创建到快照时刻的变化
### 2.2.1 创建快照
```plain
echo "v0.log" >> /mnt/ceph_lihang/v0.log
 
#create snap v1
rbd snap create test_pool/test_image@v1
echo "v1.log" >> /mnt/ceph_lihang/v1.log
 
#create snap v2
rbd snap create test_pool/test_image@v2
echo "v2.log" >> /mnt/ceph_lihang/v2.log
 
#create snap v3
rbd snap create test_pool/test_image@v3
echo "v3.log" >> /mnt/ceph_lihang/v3.log
 
#create snap v4
rbd snap create test_pool/test_image@v4
echo "v4.log" >> /mnt/ceph_lihang/v4.log
 
#create snap v5
rbd snap create test_pool/test_image@v5
echo "v5.log" >> /mnt/ceph_lihang/v5.log
```
### 2.2.2 导出快照
```plain
#export snap v1
rbd export-diff  test_pool/test_image@v1 testimage_v1
 
#export snap v2
rbd export-diff  test_pool/test_image@v2 testimage_v2
 
#export snap v3
rbd export-diff  test_pool/test_image@v3 testimage_v3
 
#export snap v4
rbd export-diff  test_pool/test_image@v4 testimage_v4
 
#export snap v5
rbd export-diff  test_pool/test_image@v5 testimage_v5
```
### 2.2.3 导入快照
```plain
#import snap v1
rbd import-diff testimage_v1 test_pool/test_image
 
#import snap v2
rbd import-diff testimage_v2 test_pool/test_image
 
#import snap v3
rbd import-diff testimage_v3 test_pool/test_image
 
#import snap v4
rbd import-diff testimage_v4 test_pool/test_image
 
#import snap v5
rbd import-diff testimage_v5 test_pool/test_image
```
### 2.2.4 流程图
![_______(____).png](https://upload-images.jianshu.io/upload_images/2099201-9f1412a4b99eeafe.png)

## 2.3 导出 image 两个快照之间的差异变化
### 2.3.1 创建快照
```plain
echo "v0.log" >> /mnt/ceph_lihang/v0.log
 
#create snap v1
rbd snap create test_pool/test_image@v1
echo "v1.log" >> /mnt/ceph_lihang/v1.log
 
#create snap v2
rbd snap create test_pool/test_image@v2
echo "v2.log" >> /mnt/ceph_lihang/v2.log
 
#create snap v3
rbd snap create test_pool/test_image@v3
echo "v3.log" >> /mnt/ceph_lihang/v3.log
 
#create snap v4
rbd snap create test_pool/test_image@v4
echo "v4.log" >> /mnt/ceph_lihang/v4.log
 
#create snap v5
rbd snap create test_pool/test_image@v5
echo "v5.log" >> /mnt/ceph_lihang/v5.log
```

### 2.3.2 导出快照
```plain
#首次导出 export v1
rbd export-diff  test_pool/test_image@v1 testimage_v1
 
#export (snap v1 - snap v2)
rbd export-diff  test_pool/test_image@v2 --from-snap v1 testimage_v1_v2
 
#export (snap v2 - snap v3)
rbd export-diff  test_pool/test_image@v3 --from-snap v2 testimage_v2_v3
 
#export (snap v3 - snap v4)
rbd export-diff  test_pool/test_image@v4 --from-snap v3 testimage_v3_v4
 
#export (snap v4 - snap v5)
rbd export-diff  test_pool/test_image@v5 --from-snap v4 testimage_v4_v5
```
### 2.3.3 导入快照
```plain
#import snap v1
rbd import-diff testimage_v1 test_pool/test_image
 
#import (snap v1 - snap v2)
rbd import-diff testimage_v1_v2 test_pool/test_image
 
#import (snap v2 - snap v3)
rbd import-diff testimage_v2_v3 test_pool/test_image
 
#import (snap v3 - snap v4)
rbd import-diff testimage_v3_v4 test_pool/test_image
 
#import (snap v4 - snap v5)
rbd import-diff testimage_v4_v5 test_pool/test_image
```
### 2.3.4 流程图
![_______(____) (1).png](https://upload-images.jianshu.io/upload_images/2099201-37c939912a17418f.png)

# 三、总结
最终选择方案三定期的备份增量文件，达到增量备份。

## 3.1 备份流程图
![image.png](https://upload-images.jianshu.io/upload_images/2099201-37a50e5ae3cf4e3a.png)

### 3.1.2 首次备份
  1.在主集群创建 Image 的快照
  2.导出主集群 Image 的全量快照
  3.将导出的全量快照文件传输到备集群
  4.备集群创建对应的 pool/image
  5.导入全量快照文件到备集群中
  6.完成备份
 

### 3.1.3 非首次备份
  1.在主集群查找最近的快照文件，并且确认备集群是否存在同名的快照
  2.在主集群创建 Image 的快照
  3.导出最近快照文件和刚创建快照文件的差量文件。(导出每次 diff，实现增量备份)
  4.将导出的差量快照文件传输到备集群
  5.导入全量快照文件到备集群中
  6.完成备份
 

## 3.2 总结
- 定期的每天导出增量的数据文件，在做恢复的时候，就从第一个快照导入，然后按顺序导入增量的快照即可。
- 定期做一个快照，导出完整的快照数据，以防中间的增量快照漏了。
- 定期清理快照
