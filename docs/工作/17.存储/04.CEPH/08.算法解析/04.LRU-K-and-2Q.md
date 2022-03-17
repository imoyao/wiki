---
title: LRU-K 和 2Q 缓存算法介绍

tags: 
  - ceph
categories: 
  - 💻 工作
  - 存储
  - CEPH
  - 算法解析
date: 2020-05-23 11:02:28
permalink: /pages/eab28f/
---
## LRU-K 算法

### 算法思想

　　LRU-K 中的 K 代表最近使用的次数，因此 LRU 可以认为是 LRU-1。LRU-K 的主要目的是为了解决 LRU 算法“缓存污染”的问题，其核心思想是将“最近使用过 1 次”的判断标准扩展为“最近使用过 K 次”。

### 工作原理

　　相比 LRU，LRU-K 需要多维护一个队列，用于记录所有缓存数据被访问的历史。只有当数据的访问次数达到 K 次的时候，才将数据放入缓存。当需要淘汰数据时，LRU-K 会淘汰第 K 次访问时间距当前时间最大的数据。详细实现如下

![472792-20161120232440279-600049881.png](https://upload-images.jianshu.io/upload_images/2099201-a41c570dcac9fcad.png)

　　(1). 数据第一次被访问，加入到访问历史列表；

　　(2). 如果数据在访问历史列表里后没有达到 K 次访问，则按照一定规则（FIFO，LRU）淘汰；

　　(3). 当访问历史队列中的数据访问次数达到 K 次后，将数据索引从历史队列删除，将数据移到缓存队列中，并缓存此数据，缓存队列重新按照时间排序；

　　(4). 缓存数据队列中被再次访问后，重新排序；

　　(5). 需要淘汰数据时，淘汰缓存队列中排在末尾的数据，即：淘汰“倒数第 K 次访问离现在最久”的数据。

　　LRU-K 具有 LRU 的优点，同时能够避免 LRU 的缺点，实际应用中 LRU-2 是综合各种因素后最优的选择，LRU-3 或者更大的 K 值命中率会高，但适应性差，需要大量的数据访问才能将历史访问记录清除掉。

## Two queues（2Q）

### 算法思想

　　该算法类似于 LRU-2，不同点在于 2Q 将 LRU-2 算法中的访问历史队列（注意这不是缓存数据的）改为一个 FIFO 缓存队列，即：2Q 算法有两个缓存队列，一个是 FIFO 队列，一个是 LRU 队列。

### 工作原理

　　当数据第一次访问时，2Q 算法将数据缓存在 FIFO 队列里面，当数据第二次被访问时，则将数据从 FIFO 队列移到 LRU 队列里面，两个队列各自按照自己的方法淘汰数据。详细实现如下：

![image](http://upload-images.jianshu.io/upload_images/2099201-c7cd9fd3e6dd1a83.png)

　　(1). 新访问的数据插入到 FIFO 队列；

　　(2). 如果数据在 FIFO 队列中一直没有被再次访问，则最终按照 FIFO 规则淘汰；

　　(3). 如果数据在 FIFO 队列中被再次访问，则将数据移到 LRU 队列头部；

　　(4). 如果数据在 LRU 队列再次被访问，则将数据移到 LRU 队列头部；

　　(5). LRU 队列淘汰末尾的数据。


## 参考资料
 - [The LRU-K Page Replacement Algorithm For Database Disk Buffering](http://www.cs.cmu.edu/~christos/courses/721-resources/p297-o_neil.pdf)
 - [2Q: A Low Overhead High Performance Buffer Management Replacement Algorithm ](http://www.vldb.org/conf/1994/P439.PDF)
