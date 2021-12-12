---
title: 分布式存储 Cephfs 读取优化方案

tags: 
  - ceph
categories: 
  - 💻 工作
  - 存储
  - CEPH
  - 方案
date: 2020-05-23 11:02:28
permalink: /pages/c0519a/
---
## 1.背景说明
继上次分享的  [Ceph 介绍及原理架构分享](https://www.jianshu.com/p/cc3ece850433) 和 [分布式存储 Ceph 之 PG 状态详解](https://www.jianshu.com/p/36c2d5682d87) ，这次分享点干货。
用户需要从 cephfs 存储系统中检索一个大文件指定关键字的一行信息， 并且对延迟和性能要求比较高。

## 2. 原始方案
## 2.1 流程图

![image.png](https://upload-images.jianshu.io/upload_images/2099201-152dc1a964a7f60f.png)

##  2.2 说明
  - 假如用户拉取的文件大小是 16M, 文件按照 4M 切分，散落到四个数据片上
  - 用户首先请求 cephfs 拉取文件信息
  -  cephfs 会根据 crush 算法找计算文件散落到那几个数据片上
  - cephfs 会拉取文件所属的数据片然后聚合起来
  - cephfs 文件拉取后返回给用户
  - 用户拉取完整个文件，开始做过滤关键字操作

##  2.3 实战
```plain
//检索2.7G文件为例
$ ll -lh nginx/logs/access.log.2018102911
-rw-rw-r-- 1 root root 2.7G Oct 29 12:07 nginx/logs/access.log.2018102911

//grep 模拟花费12s
$ time grep "xxxyyyzzzqqq" nginx/logs/access.log.2018102911

real	0m12.355s
user	0m0.302s
sys	0m0.823s
```

## 2.4 优缺点
**优点**
- 简单方便
- 开发成本低

**缺点**
- 用户端检索延迟大，影响用户体验
- 客户端集群网卡带宽波动较大，带宽有限，每次都需要把大日志文件拉取到客户端
- 对 ceph 集群负载也有波动影响

##  2.5 总结
用户拉取文件，必须先通过 cephfs 拉取文件到本地，然后根据关键字检索这行数据。如果用户检索量比较大的时候，并且文件大小都不统一，拉取文件越大网络延迟越高，并且在大文件中过滤关键字效率非常低，严重影响用户的体验。

# 3. 优化方案
## 3.1 流程图
![image.png](https://upload-images.jianshu.io/upload_images/2099201-8830428557d4f17b.png)

##  3.2 说明
- 用户发起请求输入文件名和 key 关键字到达索引层
- 索引层根据 key 找到对应的 offset 信息，然后传给 dss-readline
- dss-readline 根据 cephfs cursh 算法找到对应的 object 信息和 offset 信息
- 根据 dss-readline 用户输入的 offset 找到对应的 object 块信息
- dss-readline 直接获取需要块的 offset 该行的信息

##  3.3 实战
```shell
//查找2.8G文件offset对应的信息
$ ll  nginx/logs/access.log.2018110216 -lh
-rw-rw-r-- 1 root root 2.8G Nov  2 17:08 nginx/logs/access.log.2018110216

//sed的方式模拟，花费12s
$ time sed -n "1024p" nginx/logs/access.log.2018110216

real	0m12.042s
user	0m1.191s
sys	0m0.929s

//dss_readfile 自研工具, 输入参数:poolname, filename, offset 可以看出来花费91ms
//usage: dss_readfile <poolname> <filename> <offset>
time ./dss_readfile data nginx/logs/access.log.2018110216 1024

real	0m0.091s
user	0m0.042s
sys	0m0.011s
```

## 3.4 优缺点
**缺点**
- 需要额外开发成本

**优点**
- 提升用户体验，从以前检索单个 2.8G 文件耗时 10s 左右， 优化后控制在 100ms 左右
- 客户端网络网卡带宽可用率得到提升
- 减少对 ceph 集群的冲击影响


## 3.5 总结
**思路：**
由于文件信息是放到服务端，进行切片存储到数据节点。
我们能不能只拉取我需要的块信息，不用全量拉取到本地，答案是肯定的。

- 根据文件信息查找所有的 object、offset 信息
- 根据 offset 找到需要检索的 object 信息
- 找到对应的 object，读取该 object 对应的 offset 位置的信息（一行数据可能会拆分多个 object)

**优点：**
- 提升用户体验，从以前检索单个 2.8G 文件耗时 10s 左右， 优化后控制在 100ms 左右
- 客户端网络网卡带宽可用率得到提升
- 减少对 ceph 集群的冲击影响

# 4. 深入分析
## 4.1 文件对应 object 信息
### 4.1.1 Jewel 版本
```shell
//Ceph Jewel版本里，有个cephfs的工具，可以获取file的location信息
//根据offset查找object信息
$ cephfs /mnt/kernel_log_push.log show_location -l 4194304
WARNING: This tool is deprecated.  Use the layout.* xattrs to query and modify layouts.
location.file_offset:  4194304
location.object_offset:0
location.object_no:    1
location.object_size:  4194304
location.object_name:  10002b63282.00000001
location.block_offset: 0
location.block_size:   4194304
location.osd:          67

//file object map 信息
$ cephfs /mnt/kernel_log_push.log map
WARNING: This tool is deprecated.  Use the layout.* xattrs to query and modify layouts.
    FILE OFFSET                    OBJECT        OFFSET        LENGTH  OSD
              0      10002b63282.00000000             0       4194304  61
        4194304      10002b63282.00000001             0       4194304  67
        8388608      10002b63282.00000002             0       4194304  70
       12582912      10002b63282.00000003             0       4194304  68
```
### 4.1.2 源码跟踪
**ceph jewel 版本，cephfs 代码**
    [https://github.com/ceph/ceph/blob/v10.2.9/src/cephfs.cc#L117](https://github.com/ceph/ceph/blob/v10.2.9/src/cephfs.cc#L117)

```c/c++
    struct ceph_ioctl_layout layout;
    memset(&layout, 0, sizeof(layout));
    //获取layout信息
    err = ioctl(fd, CEPH_IOC_GET_LAYOUT, (unsigned long)&layout);
    if (err) {
      cerr << "Error getting layout: " << cpp_strerror(errno) << endl;
      return 1;
    }

    printf("%15s  %24s  %12s  %12s  %s\n",
	   "FILE OFFSET", "OBJECT", "OFFSET", "LENGTH", "OSD");
    for (long long off = 0; off < st.st_size; off += layout.stripe_unit) {
      struct ceph_ioctl_dataloc location;
      location.file_offset = off;
      //获取location 信息
      err = ioctl(fd, CEPH_IOC_GET_DATALOC, (unsigned long)&location);
      if (err) {
	cerr << "Error getting location: " << cpp_strerror(errno) << endl;
	return 1;
      }
      printf("%15lld  %24s  %12lld  %12lld  %d\n",
	     off, location.object_name, (long long)location.object_offset,
	     (long long)location.block_size, (int)location.osd);
    }
```
**CEPH_IOC_GET_DATALOC 代码**

```c/c++
//定义/src/client/ioctl.h
//https://github.com/ceph/ceph/blob/d038e1da7a6c9b31ba4463b8ebedb9908981a55e/src/client/ioctl.h#L46
#define CEPH_IOC_GET_DATALOC _IOWR(CEPH_IOCTL_MAGIC, 3,	\
				   struct ceph_ioctl_dataloc)

//fuse 代码跟踪, 发现只支持layout
//https://github.com/ceph/ceph/blob/d038e1da7a6c9b31ba4463b8ebedb9908981a55e/src/client/fuse_ll.cc#L631
static void fuse_ll_ioctl(fuse_req_t req, fuse_ino_t ino, int cmd, void *arg, struct fuse_file_info *fi,
			  unsigned flags, const void *in_buf, size_t in_bufsz, size_t out_bufsz)
{
  CephFuse::Handle *cfuse = fuse_ll_req_prepare(req);

  if (flags & FUSE_IOCTL_COMPAT) {
    fuse_reply_err(req, ENOSYS);
    return;
  }

  switch (static_cast<unsigned>(cmd)) {
    case CEPH_IOC_GET_LAYOUT: {
      file_layout_t layout;
      struct ceph_ioctl_layout l;
      Fh *fh = (Fh*)fi->fh;
      cfuse->client->ll_file_layout(fh, &layout);
      l.stripe_unit = layout.stripe_unit;
      l.stripe_count = layout.stripe_count;
      l.object_size = layout.object_size;
      l.data_pool = layout.pool_id;
      fuse_reply_ioctl(req, 0, &l, sizeof(struct ceph_ioctl_layout));
    }
    break;
    default:
      fuse_reply_err(req, EINVAL);
  }
}

//kernel cephfs代码, 支持layout, 支持dataloc
// /usr/src/debug/kernel-3.10.0-693.17.1.el7/linux-3.10.0-693.17.1.el7.x86_64/fs/ceph/ioctl.c
long ceph_ioctl(struct file *file, unsigned int cmd, unsigned long arg)
{
        dout("ioctl file %p cmd %u arg %lu\n", file, cmd, arg);
        switch (cmd) {
        case CEPH_IOC_GET_LAYOUT:
                return ceph_ioctl_get_layout(file, (void __user *)arg);

        case CEPH_IOC_SET_LAYOUT:
                return ceph_ioctl_set_layout(file, (void __user *)arg);

        case CEPH_IOC_SET_LAYOUT_POLICY:
                return ceph_ioctl_set_layout_policy(file, (void __user *)arg);

        case CEPH_IOC_GET_DATALOC:
                return ceph_ioctl_get_dataloc(file, (void __user *)arg);

        case CEPH_IOC_LAZYIO:
                return ceph_ioctl_lazyio(file);

        case CEPH_IOC_SYNCIO:
                return ceph_ioctl_syncio(file);
        }

        return -ENOTTY;
}

static long ceph_ioctl_get_dataloc(struct file *file, void __user *arg)
{
        ...
        r = ceph_calc_file_object_mapping(&ci->i_layout, dl.file_offset, len,
                                          &dl.object_no, &dl.object_offset,
                                          &olen);
        if (r < 0) {
                up_read(&osdc->lock);
                return -EIO;
        }
        dl.file_offset -= dl.object_offset;
        dl.object_size = ceph_file_layout_object_size(ci->i_layout);
        dl.block_size = ceph_file_layout_su(ci->i_layout);

        /* block_offset = object_offset % block_size */
        tmp = dl.object_offset;
        dl.block_offset = do_div(tmp, dl.block_size);

        snprintf(dl.object_name, sizeof(dl.object_name), "%llx.%08llx",
                 ceph_ino(inode), dl.object_no);

     ...
```

### 4.1.2 Luminous 版本
Luminous 版本里，没有 src/cephfs.cc 文件, 发现 test_ioctls.c 其实有相关的测试代码。
https://github.com/ceph/ceph/blob/master/src/client/test_ioctls.c
/src/client/test_ioctls.c

```c/c++
int main(int argc, char **argv)
{
	...
	fd = open(fn, O_CREAT|O_RDWR, 0644);
	if (fd < 0) {
		perror("couldn't open file");
		return 1;
	}

	/* get layout */
        err = ioctl(fd, CEPH_IOC_GET_LAYOUT, (unsigned long)&l);
        if (err < 0) {
                perror("ioctl IOC_GET_LAYOUT error");
                return 1;
        }
        printf("layout:\n stripe_unit %lld\n stripe_count %lld\n object_size %lld\n data_pool %lld\n",
               (long long)l.stripe_unit, (long long)l.stripe_count, (long long)l.object_size, (long long)l.data_pool);

	/* dataloc */
	dl.file_offset = atoll(argv[2]);
	err = ioctl(fd, CEPH_IOC_GET_DATALOC, (unsigned long)&dl);
	if (err < 0) {
		perror("ioctl IOC_GET_DATALOC error");
		return 1;
	}

	printf("dataloc:\n");
	printf(" file_offset %lld (of object start)\n", (long long)dl.file_offset);
	printf(" object '%s'\n object_offset %lld\n object_size %lld object_no %lld\n",
	       dl.object_name, (long long)dl.object_offset, (long long)dl.object_size, (long long)dl.object_no);
	printf(" block_offset %lld\n block_size %lld\n",
	       (long long)dl.block_offset, (long long)dl.block_size);
    ...
```

### 4.2 总结
- 目前只有 kernel 版本支持 CEPH_IOC_GET_DATALOC
- 根据文件以及 offset 可以获取对应的 object 信息。 目前只支持内核 kernel 版本。


## 4.3 获取这个对象 offset 对应行的信息
**问题点：**
 - 一行数据可能会拆分为两个对象
 - 一行数据结尾符是否存在\n
 - 一行数据超大等问题

**解决方案：**
 - 用户给的 offset 属于这一行的开头， 只需要读取当前读取数据是否存在\n。
    a. 如果存在\n 证明该行，属于完整的行。
    b. 否则不存在\n 证明该行，被拆分为两个对象，读取当前 offset 对应的 object 信息以及下一个对象的信息，直到遇到\n 结束，然后合并两个对象读取的数据为完整的行。
- 超大行或者不存在结尾符\n 自动截取 1024 字节数。

## 4.4 通过 librados 库，读取 object 的信息

```c/c++
 /* Declare the cluster handle and required arguments. */
    int                                 err;
    char                                cluster_name[] = "ceph";
    char                                user_name[] = "client.admin";
    uint64_t                            flags = 0;
    rados_t                             cluster;
    rados_ioctx_t                       io;
    rados_completion_t                  comp;



    /* Initialize the cluster handle with the "ceph" cluster name and the "client.admin" user */
    err = rados_create2(&cluster, cluster_name, user_name, flags);
    if (err < 0) {
            fprintf(stderr, "error: couldn't create the cluster handle poolname=[%s] object_name=[%s] offset=[%d] error=[%s]\n",
			poolname, object_name, offset, strerror(-err));
            return 1;
    }

    /* Read a Ceph configuration file to configure the cluster handle. */
    err = rados_conf_read_file(cluster, "/etc/ceph/ceph.conf");
    if (err < 0) {
            fprintf(stderr, "error: cannot read config file poolname=[%s] object_name=[%s] offset=[%d] error=[%s]\n",
			poolname, object_name, offset,  strerror(-err));
            return 1;
    }

    /* Connect to the cluster */
    err = rados_connect(cluster);
    if (err < 0) {
            fprintf(stderr, "error: cannot connect to cluster poolname=[%s] object_name=[%s] offset=[%d] error=[%s]\n",
			poolname, object_name, offset,  strerror(-err));
            return 1;
    }

    //create io
    err = rados_ioctx_create(cluster, poolname, &io);
    if (err < 0) {
            fprintf(stderr, "error: cannot open rados pool poolname=[%s] object_name=[%s] offset=[%d] error=[%s]\n",
			poolname, object_name, offset, strerror(-err));
            rados_shutdown(cluster);
            return 1;
    }

    /*
     * Read data from the cluster asynchronously.
     * First, set up asynchronous I/O completion.
     */
    err = rados_aio_create_completion(NULL, NULL, NULL, &comp);
    if (err < 0) {
            fprintf(stderr, "error: could not create aio completion poolname=[%s] object_name=[%s] offset=[%d] error=[%s]\n",
			poolname, object_name, offset, strerror(-err));
            rados_ioctx_destroy(io);
            rados_shutdown(cluster);
            return 1;
    }

    /* Next, read data using rados_aio_read. */
    err = rados_aio_read(io, object_name, comp, line, line_size, offset);
    if (err < 0) {
            fprintf(stderr, "error: cannot read object poolname=[%s] object_name=[%s] offset=[%d] error=[%s]\n",
			poolname, object_name, offset, strerror(-err));
            rados_ioctx_destroy(io);
            rados_shutdown(cluster);
            return 1;
    }
    /* Wait for the operation to complete */
    rados_aio_wait_for_complete(comp);
    /* Release the asynchronous I/O complete handle to avoid memory leaks. */
    rados_aio_release(comp);

    rados_ioctx_destroy(io);
    rados_shutdown(cluster);
```

## 4.5 项目工具

**1. 源码地址**
 - https://github.com/lidaohang/cephfs_readline

![image.png](https://upload-images.jianshu.io/upload_images/2099201-b933bf9eeb1a6bad.png)

**2. dss_readfile 工具**
 - 根据存储池、文件信息、offset 获取对应的信息

```shell
//usage: dss_readfile <poolname> <filename> <offset>
./dss_readfile data nginx/logs/access.log.2018110216 1024

```
**3. ngx_cephfs_readline**
 - 为了提升性能以及用户体验，基于 ceph module + librados 开发，充分利用 nginx 优秀的高并发性能。

```json
//接口

http://127.0.0.1 :8088/v1/dss-cephfs/readfile


//请求body
{
    "poolname":"data",
    "filename":"/mnt/business.log.2018101708",
    "offset":1024
}

//响应body
{
    "code":1,
    "cost": 50,
    "data":"[INFO][2018-10-17T08:59:49.018+0800] xxxxxx"
}
```


## 参考资料
 - https://github.com/ceph/ceph
 - https://github.com/lidaohang/cephfs_readline (分布式存储 Cephfs 读取优化方案)
 - https://github.com/lidaohang/ceph_study (学习记录)
