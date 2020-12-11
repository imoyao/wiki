---
title: Redis 缓存和 MySQL 数据一致性方案详解

tags: 
  - 面试
  - 技术
  - 高并发
categories: 
  - 💻 工作
  - 数据库
  - redis
date: 2020-10-20 12:27:56
permalink: /pages/c64397/
---

## 需求

在高并发的业务场景下，数据库大多数情况都是用户并发访问最薄弱的环节。所以，就需要使用 redis 做一个缓冲操作，让请求先访问到 redis，而不是直接访问 MySQL 等数据库。

![](https://oscimg.oschina.net/oscnet/6101702c48dd9e9b410c23c4fe15c70d8eb.jpg)

这个业务场景，主要是解决读数据从 Redis 缓存，一般都是按照下图的流程来进行业务操作。

![](https://oscimg.oschina.net/oscnet/fa60658310f220abb9042070915d186b883.jpg)

读取缓存步骤一般没有什么问题，但是一旦涉及到数据更新：数据库和缓存更新，就容易出现**缓存(Redis)和数据库（MySQL）间的数据一致性问题**。

不管是先写 MySQL 数据库，再删除 Redis 缓存；还是先删除缓存，再写库，都有可能出现数据不一致的情况。举一个例子：

1.如果删除了缓存 Redis，还没有来得及写库 MySQL，另一个线程就来读取，发现缓存为空，则去数据库中读取数据写入缓存，此时缓存中为脏数据。

2.如果先写了库，在删除缓存前，写库的线程宕机了，没有删除掉缓存，则也会出现数据不一致情况。

因为写和读是并发的，没法保证顺序,就会出现缓存和数据库的数据不一致的问题。

如来解决？这里给出两个解决方案，先易后难，结合业务和技术代价选择使用。

## 缓存和数据库一致性解决方案


### 采用延时双删策略

在写库前后都进行 redis.del(key)操作，并且设定合理的超时时间。

- 伪代码

```java
public void write(String key,Object data){
 redis.delKey(key);
 db.updateData(data);
 Thread.sleep(500);
 redis.delKey(key);
 }
```

- 具体步骤
1. 先删除缓存
2. 再写数据库
3. 休眠一定时间
4. 再次删除缓存

- 那么，这个休眠时间怎么确定的，具体该休眠多久呢？

需要评估自己的项目的读数据业务逻辑的耗时。这么做的目的，就是确保读请求结束，写请求可以删除读请求造成的缓存脏数据。

当然这种策略还要考虑 redis 和数据库主从同步的耗时。最后的写数据的休眠时间，则在读数据业务逻辑的耗时基础上加几百 ms 即可。比如：休眠 1 秒。

- 设置缓存过期时间

从理论上来说，给缓存设置过期时间，是保证最终一致性的解决方案。所有的写操作以数据库为准，只要到达缓存过期时间，则后面的读请求自然会从数据库中读取新值然后回填进缓存。

### 弊端

结合双删策略+缓存超时设置，这样最差的情况就是在超时时间内数据存在不一致，而且又增加了写请求的耗时。

## 异步更新缓存(基于订阅 binlog 的同步机制)

### 整体思路

MySQL binlog 增量订阅消费+消息队列+增量数据更新到 redis

1. **读 Redis**：热数据基本都在 Redis

2. **写 MySQL**：增删改都是操作 MySQL

3. **更新 Redis 数据**：MySQL 的数据操作 binlog 来更新到 Redis

### Redis 更新

数据操作主要分为两大块：

*   一个是全量(将全部数据一次写入到 redis)
*   一个是增量（实时更新）
 这里说的是增量，指的是 mysql 的 update、insert、delete 变更数据之后，读取 binlog 并分析，利用消息队列，推送更新各台的 redis 缓存数据。

这样一旦 MySQL 中产生了新的写入、更新、删除等操作，就可以把 binlog 相关的消息推送至 Redis，Redis 再根据 binlog 中的记录，对 Redis 进行更新。

其实这种机制，很类似 MySQL 的主从备份机制，因为 MySQL 的主备也是通过 binlog 来实现的数据一致性。

这里可以结合使用 canal(阿里的一款开源框架)，通过该框架可以对 MySQL 的 binlog 进行订阅，而 canal 正是模仿了 mysql 的 slave 数据库的备份请求，使得 Redis 的数据更新达到了相同的效果。

当然，这里的消息推送工具你也可以采用别的第三方：kafka、rabbitMQ 等来实现推送更新 Redis。

以上就是 Redis 和 MySQL 数据一致性详解，相关的 MySQL 数据库主从同步一致性可以参考：[MySQL 数据库主从同步的 3 种一致性方案实现，及优劣比较](https://youzhixueyuan.com/database-master-slave-synchronization.html)

## 相关链接
[高并发架构系列：Redis 缓存和 MySQL 数据一致性方案详解 - 从程序员到架构师需要掌握的技术、知识、实战等干货，都在这里了~ - OSCHINA - 中文开源技术交流社区](https://my.oschina.net/jiagouzhan/blog/2990423?p=1)
[如何保持 mysql 和 redis 中数据的一致性？ - 知乎](https://www.zhihu.com/question/319817091)