---
title: CRUSH 那点事儿

tags: 
  - ceph
categories: 
  - 💻 工作
  - 存储
  - CEPH
  - 大话 Ceph
date: 2020-05-23 11:02:28
permalink: /pages/6083ca/
---

## 引言

> 那么问题来了，把一份数据存到一群 Server 中分几步？

Ceph 的答案是：两步。

1. 计算 PG
2. 计算 OSD



首先，要明确 Ceph 的一个规定：在 Ceph 中，一切皆对象。

不论是视频，文本，照片等一切格式的数据，Ceph 统一将其看作是对象，因为追其根源，所有的数据都是二进制数据保存于磁盘上，所以每一份二进制数据都看成一个对象，不以它们的格式来区分他们。

那么用什么来区分两个对象呢？**对象名**。也就是说，每个不同的对象都有不一样的对象名。于是，开篇的问题就变成了：

> 把一个对象存到一群 Server 中分几步？

这里的一群 Server，由 Ceph 组织成一个集群，这个集群由若干的磁盘组成，也就是由若干的 OSD 组成。于是，继续简化问题：

> 把一个对象存到一堆 OSD 中分几步?

## Ceph 中的逻辑层

Ceph 为了保存一个对象，对上构建了一个逻辑层，也就是池(pool)，用于保存对象，这个池的翻译很好的解释了 pool 的特征，如果把 pool 比喻成一个中国象棋棋盘，那么保存一个对象的过程就类似于把一粒芝麻放置到棋盘上。

Pool 再一次进行了细分，即将一个 pool 划分为若干的 PG(归置组 Placement Group)，这类似于棋盘上的方格，所有的方格构成了整个棋盘，也就是说所有的 PG 构成了一个 pool。

现在需要解决的问题是，对象怎么知道要保存到哪个 PG 上，假定这里我们的 pool 名叫 rbd，共有 256 个 PG，给每个 PG 编个号分别叫做`0x0, 0x1, ...0xF, 0x10, 0x11... 0xFE, 0xFF`。

要解决这个问题，我们先看看我们拥有什么，1，不同的对象名。2，不同的 PG 编号。这里就可以引入 Ceph 的计算方法了 : HASH。

对于对象名分别为`bar`和`foo`的两个对象，对他们的对象名进行计算即:

- HASH(‘bar’) = 0x3E0A4162
- HASH(‘foo’) = 0x7FE391A0
- HASH(‘bar’) = 0x3E0A4162

对对象名进行 HASH 后，得到了一串十六进制输出值，也就是说通过 HASH 我们将一个对象名转化成了一串数字，那么上面的第一行和第三行是一样的有什么意义？ 意义就是对于一个同样的对象名，计算出来的结果永远都是一样的，但是 HASH 算法的确将对象名计算得出了一个随机数。

有了这个输出，我们使用小学就会的方法：求余数！用随机数除以 PG 的总数 256，得到的余数一定会落在[0x0, 0xFF]之间，也就是这 256 个 PG 中的某一个：

- 0x3E0A4162 % 0xFF ===> 0x62
- 0x7FE391A0 % 0xFF ===> 0xA0

于是乎，对象`bar`保存到编号为`0x62`的 PG 中，对象`foo`保存到编号为`0xA0`的 PG 中。对象`bar`永远都会保存到 PG 0x62 中！ 对象`foo`永远都会保存到 PG 0xA0 中！

现在又来了一亿个对象，他们也想知道自己会保存到哪个 PG 中，Ceph 说：“自己算”。于是这一亿个对象，各自对自己对象名进行 HASH，得到输出后除以 PG 总数得到的余数就是要保存的 PG。

求余的好处就是对象数量规模越大，每个 PG 分布的对象数量就越平均。

所以每个对象自有名字开始，他们要保存到的 PG 就已经确定了。

那么爱思考的小明同学就会提出一个问题，难道不管对象的高矮胖瘦都是一样的使用这种方法计算 PG 吗，答案是，YES! 也就是说 Ceph 不区分对象的真实大小内容以及任何形式的格式，只认对象名。毕竟当对象数达到百万级时，对象的分布从宏观上来看还是平均的。

这里给出更 Ceph 一点的说明，实际上在 Ceph 中，存在着多个 pool，每个 pool 里面存在着若干的 PG，如果两个 pool 里面的 PG 编号相同，Ceph 怎么区分呢? 于是乎，Ceph 对每个 pool 进行了编号，比如刚刚的 rbd 池，给予编号 0，再建一个 pool 就给予编号 1，那么在 Ceph 里，PG 的实际编号是由`pool_id+.+PG_id`组成的，也就是说，刚刚的`bar`对象会保存在`0.62`这个 PG 里，`foo`这个对象会保存在`0.A0`这个 PG 里。其他池里的 PG 名称可能为`1.12f, 2.aa1,10.aa1`等。

## Ceph 中的物理层

理解了刚刚的逻辑层，我们再看一下 Ceph 里的物理层，对下，也就是我们若干的服务器上的磁盘，通常，Ceph 将一个磁盘看作一个 OSD(实际上，OSD 是管理一个磁盘的程序)，于是物理层由若干的 OSD 组成，我们的最终目标是将对象保存到磁盘上，在逻辑层里，对象是保存到 PG 里面的，那么现在的任务就是`打通PG和OSD之间的隧道`。PG 相当于一堆余数相同的对象的组合，PG 把这一部分对象打了个包，现在我们需要把很多的包平均的安放在各个 OSD 上，这就是 CRUSH 算法所要做的事情：`CRUSH计算PG->OSD的映射关系`。

加上刚刚的对象映射到 PG 的方法，我们将开篇的两步表示成如下的两个计算公式：

- 池 ID + HASH(‘对象名’) % pg_num ===> PG_ID
- CRUSH(PG_ID) ===> OSD

## 使用 HASH 代替 CRUSH

在讨论 CRUSH 算法之前，我们来做一点思考，可以发现，上面两个计算公式有点类似，为何我们不把

- `CRUSH(PG_ID) ===> OSD`
  改为
- `HASH(PG_ID) %OSD_num ===> OSD`

我可以如下几个由此假设带来的副作用：

- 如果挂掉一个 OSD，`OSD_num-1`，于是所有的`PG % OSD_num`的余数都会变化，也就是说这个 PG 保存的磁盘发生了变化，对这最简单的解释就是，这个 PG 上的数据要从一个磁盘全部迁移到另一个磁盘上去，一个优秀的存储架构应当在磁盘损坏时使得数据迁移量降到最低，CRUSH 可以做到。
- 如果保存多个副本，我们希望得到多个 OSD 结果的输出，HASH 只能获得一个，但是 CRUSH 可以获得任意多个。
- 如果增加 OSD 的数量，OSD_num 增大了，同样会导致 PG 在 OSD 之间的胡乱迁移，但是 CRUSH 可以保证数据向新增机器均匀的扩散。

所以 HASH 只适用于一对一的映射关系计算，并且两个映射组合(对象名和 PG 总数)不能变化，因此这里的假设不适用于 PG->OSD 的映射计算。因此，这里开始引入 CRUSH 算法。

## 引入 CRUSH 算法

千呼万唤始出来，终于开始讲 CRUSH 算法了，如果直接讲 Sage 的博士论文或者`crush.c`的代码的话，可能会十分苦涩难懂，所以我决定尝试大话一把 CRUSH，希望能让没有接触过 CRUSH 的同学也能对其有所理解。

首先来看我们要做什么：

- 把已有的 PG_ID 映射到 OSD 上，有了映射关系就可以把一个 PG 保存到一个磁盘上。
- 如果我们想保存三个副本，可以把一个 PG 映射到三个不同的 OSD 上，这三个 OSD 上保存着一模一样的 PG 内容。

再来看我们有了什么：

- 互不相同的 PG_ID。
- 如果给 OSD 也编个号，那么就有了互不相同的 OSD_ID。
- 每个 OSD 最大的不同的就是它们的容量，即 4T 还是 800G 的容量，我们将每个 OSD 的容量又称为 OSD 的权重(weight)，规定 4T 权重为 4，800G 为 0.8，也就是以 T 为单位的值。

现在问题转化为：如何将 PG_ID 映射到有各自权重的 OSD 上。这里我直接使用 CRUSH 里面采取的`Straw`算法，翻译过来就是抽签，说白了就是挑个最长的签，这里的签指的是 OSD 的权重。

那么问题就来了，总不至于每次都挑容量最大的 OSD 吧，这不分分钟都把数据存满那个最大的 OSD 了吗？是的，所以在挑之前先把这些 OSD`搓一搓`，这里直接介绍 CRUSH 的方法，如下图(可忽视代码直接看文字)：

[![Alt text](http://www.xuxiaopang.com/images/1478244507156.png)](http://www.xuxiaopang.com/images/1478244507156.png)

- CRUSH_HASH( PG_ID, OSD_ID, r ) ===> draw
- ( draw &0xffff ) * osd_weight ===> osd_straw
- pick up high_osd_straw

第一行，我们姑且把 r 当做一个常数，第一行实际上就做了搓一搓的事情:将 PG_ID, OSD_ID 和 r 一起当做 CRUSH_HASH 的输入，求出一个十六进制输出，这和 HASH(对象名)完全类似，只是多了两个输入。所以需要强调的是，对于相同的三个输入，计算得出的`draw`的值是一定相同的。

这个`draw`到底有啥用？其实，CRUSH 希望得到一个随机数，也就是这里的`draw`，然后拿这个随机数去乘以 OSD 的权重，这样把随机数和 OSD 的权重搓在一起，就得到了每个 OSD 的实际签长，而且每个签都不一样长(极大概率)，就很容易从中挑一个最长的。

说白了，CRUSH 希望`随机`挑一个 OSD 出来，但是还要满足权重越大的 OSD 被挑中的概率越大，为了达到随机的目的，它在挑之前让每个 OSD 都拿着自己的权重乘以一个随机数，再取乘积最大的那个。那么这里我们再定个小目标：挑个一亿次！从宏观来看，同样是乘以一个随机数，在样本容量足够大之后，这个随机数对挑中的结果不再有影响，起决定性影响的是 OSD 的权重，也就是说，OSD 的权重越大，宏观来看被挑中的概率越大。

这里再说明下 CRUSH 造出来的随机数`draw`，前文可知，对于常量输入，一定会得到一样的输出，所以这并不是真正的随机，所以说，CRUSH 是一个`伪随机`算法。下图是`CRUSH_HASH`的代码段，我喜欢叫它搅拌搅拌再搅拌得出一个随机数:

[![Alt text](http://www.xuxiaopang.com/images/1478244378743.png)](http://www.xuxiaopang.com/images/1478244378743.png)

如果看到这里你已经被搅晕了，那让我再简单梳理下 PG 选择一个 OSD 时做的事情：

- 给出一个 PG_ID，作为 CRUSH_HASH 的输入。
- CRUSH_HASH(PG_ID, OSD_ID, r) 得出一个随机数(重点是随机数，不是 HASH)。
- 对于所有的 OSD 用他们的权重乘以每个 OSD_ID 对应的随机数，得到乘积。
- 选出乘积最大的 OSD。
- 这个 PG 就会保存到这个 OSD 上。

现在趁热打铁，解决一个 PG 映射到多个 OSD 的问题，还记得那个常量`r`吗？我们把`r+1`，再求一遍随机数，再去乘以每个 OSD 的权重，再去选出乘积最大的 OSD，如果和之前的 OSD 编号不一样，那么就选中它，如果和之前的 OSD 编号一样的话，那么再把`r+2`，再次选一次，直到选出我们需要的三个不一样编号的 OSD 为止！


当然实际选择过程还要稍微复杂一点，我这里只是用最简单的方法来解释 CRUSH 在选择 OSD 的时候所做的事情。

下面我们来举个例子，假定我们有 6 个 OSD，需要从中选出三个副本：

| osd_id | weight | CRUSH_HASH | (CRUSH_HASH & 0xffff)* weight |
| :----: | :----: | :--------: | :---------------------------: |
| osd.0  |   4    | 0xC35E90CB |            0x2432C            |
| osd.1  |   4    | 0xA67DE680 |          **0x39A00**          |
| osd.2  |   4    | 0xF9B1B224 |            0x2C890            |
| osd.3  |   4    | 0x42454470 |            0x111C0            |
| osd.4  |   4    | 0xE950E2F9 |            0x38BE4            |
| osd.5  |   4    | 0x8A844538 |            0x114E0            |

这是`r = 0`的情况，这时候，我们选出`(CRUSH_HASH & 0xFFFF) * weight`的值最大的一个，也就是`osd.1`的`0x39A00`,这就是我们选出的第一个 OSD。
然后，我们再让`r = 1`，再生成一组`CRUSH_HASH`的随机值，乘以 OSD 的 weight，再取一个最大的得到第二个 OSD，依此得到第三个 OSD，如果在此过程中，选中了相同的 OSD，那么将`r`再加一，生成一组随机值，再选一次，直到选中三个 OSD 为止。

## CRUSH 算法的应用

理解了上面 CRUSH 选择 OSD 的过程，我们就很容易进一步将 CRUSH 算法结合实际结构，这里给出 Sage 在他的博士论文中画的一个树状结构图：
[![Alt text](http://www.xuxiaopang.com/images/1478486778573.png)](http://www.xuxiaopang.com/images/1478486778573.png)

最下面的蓝色长条可以看成一个个主机，里面的灰色圆柱形可以看成一个个 OSD，紫色的 cabinet 可以也就是一个个机柜， 绿色的 row 可以看成一排机柜，顶端的 root 是我们的根节点，没有实际意义，你可以把它看成一个数据中心的意思，也可以看成一个机房的意思，不过只是起到了一个树状结构的根节点的作用。

基于这样的结构选择 OSD，我们提出了新的要求：

- 一共选出三个 OSD。
- 这三个 OSD 需要都位于一个 row 下面。
- 每个 cabinet 内至多有一个 OSD。

这样的要求，如果用上一节的 CRUSH 选 OSD 的方法，不能满足二三两个要求，因为 OSD 的分布是随机的。

那么要完成这样的要求，先看看我们现在有什么：

- 每个 OSD 的 weight。
- 每个主机也可以有一个 weight，这个 weight 由主机内的所有 OSD 的 weight 累加而得。
- 每个 cabinet 的 weight 由所有主机的 weight 累加而得，其实就是这个 cabinet 下的所有 OSD 的权重之和。
- 同理推得每个 row 的 weight 有 cabinet 累加而得。
- root 的 weight 其实就是所有的 OSD 的权重之和。

所以在这棵树状结构中，每个节点都有了自己的权重，每个节点的权重由`下一层`节点的权重累加而得，因此根节点 root 的权重就是这个集群所有的 OSD 的权重之和，那么有了这么多权重之后，我们怎么选出那三个 OSD 呢？

仿照 CRUSH 选 OSD 的方法：

- CRUSH 从 root 下的所有的 row 中选出一个 row。
- 在刚刚的一个 row 下面的所有 cabinet 中，CRUSH 选出三个 cabinet。
- 在刚刚的三个 cabinet 下面的所有 OSD 中，CRUSH 分别选出一个 OSD。

因为每个 row 都有自己的权重，所以 CRUSH 选 row 的方法和选 OSD 的方法完全一样，用 row 的权重乘以一个随机数，取最大。然后在这个 row 下面继续选出三个 cabinet，再在每个 cabinet 下面选出一个 OSD。

这样做的根本意义在于，将数据平均分布在了这个集群里面的所有 OSD 上，如果两台机器的权重是 16：32，那么这两台机器上分布的数据量也是 1：2。同时，这样选择做到了三个 OSD 分布在三个不同的 cabinet 上。

那么结合图例这里给出 CRUSH 算法的流程：

- take(root) ============> [root]
- choose(1, row) ========> [row2]
- choose(3, cabinet) =====> [cab21, cab23, cab24] *在[row2]下*
- choose(1, osd) ========> [osd2107, osd2313, osd2437] *在三个 cab 下*
- emit ================> [osd2107, osd2313, osd2437]

这里给出 CRUSH 算法的两个重要概念：

- BUCKET/OSD : OSD 和我们的磁盘一一对应，bucket 是除了 OSD 以外的所有非子叶节点，比如上面的 cabinet,row,root 等都是。
- RULE ： CRUSH 选择遵循一条条选择路径，一个选择路径就是一个 rule。

RULE 一般分为三步走 : `take`–>`choose N`–>`emit`。`Take`这一步负责选择一个根节点，这个根节点不一定是`root`，也可以是任何一个 Bucket。`choose N`做的就是按照每个 Bucket 的 weight 以及每个`choose`语句选出符合条件的 Bucket，并且，**下一个 choose 的选择对象为上一步得到的结果**。`emit`就是输出最终结果，相当于出栈。

这里再举个简单的例子，也就是我们最常见的三个主机每个主机三个 OSD 的结构：
[![Alt text](http://www.xuxiaopang.com/images/1478497045877.png)](http://www.xuxiaopang.com/images/1478497045877.png)

我们要从三个 host 下面各选出一个 OSD，使得三个副本各落在一个 host 上，这时候，就能保证挂掉两个 host，还有一个副本在运行了，那么这样的 RULE 就形如：

- take(root) ============> [default] 注意是根节点的名字
- choose(3, host) ========> [ceph-1, ceph-2, ceph-3]
- choose(1, osd) ========> [osd.3, osd.1, osd.8]
- emit()

这里我们来简单总结一下：我们把一个生产环境的机房画成一个树状结构，最下面一层为 OSD 层，每个 OSD 有自己的权重，OSD 的上面由 host/rack/row/room/root 等等节点构成，每个节点的权重都是由下层的节点累加而成，CRUSH 选择每个节点的算法(straw)都是一样的，用它们的 weight 乘以一个随机数取其中最大，只是我们通过`choose`的语句来判断选择的节点类型和个数。最后不要忘了选出来的结果是 PG->OSD 的映射，比如:`pg 0.a2 ---> [osd.3, osd.1, osd.8]`和`pg 0.33 ---> [osd.0, osd.5, osd.7]`, 每个 PG 都有自己到 OSD 的映射关系，这个关系用公式总结就是： `CRUSH(pg_id) ---> [osd.a, osd.b ...osd.n]`。

到目前为止，我们已经完成了一份数据保存到一群 Server 的第二步，再整体回顾下这个流程：

- 每个文件都有一个唯一的对象名。
- Pool_ID + HASH(对象名) % PG_NUM 得到 PG_ID
- CRUSH(PG_ID) 得到该 PG 将要保存的 OSD 组合
- 这个对象就会保存到位于这些 OSD 上的 PG 上(PG 就是磁盘上的目录)

所以，HASH 算法负责计算对象名到 PG 的映射，CRUSH 负责计算 PG 到 OSD 的映射，暂且记住这一点。

## CRUSH 里的虚虚实实

现在，我们有三台主机，每台主机上的配置如下：

| 主机名 |          磁盘数          |
| :----: | :----------------------: |
| ceph-1 | 4T SATA * 3  800G SSD *1 |
| ceph-2 | 4T SATA * 3  800G SSD *1 |
| ceph-3 | 4T SATA * 3  800G SSD *1 |

但是想要构建成如下的结构：
[![Alt text](http://www.xuxiaopang.com/images/1478501078240.png)](http://www.xuxiaopang.com/images/1478501078240.png)

这里我们不能把一台主机劈成两半把 SATA 盘和 SSD 各分一半，所以就来介绍下 CRUSH 里面的虚虚实实，什么是实？所有的 OSD 都是实实在在的节点！什么是虚？除了 OSD 之外的所有 Bucket 都是虚的！

也就是说，我们可以建立几个 Bucket，分别名叫`ceph-1-sata`,`root-sata`,`ceph-1-ssd`, `root-ssd`，而这些 Bucket 不需要和实际结构有任何关系，可以看成是我们假想出来的结构，为了达到分层的目的，我们可以假象出任意形式的 bucket。

将所有的 SATA 添加到`ceph-x-sata`节点下，再将`ceph-x-sata`加入到根节点`root-sata`下，同理处理剩下的三个 SSD 盘。那么现在可以制定两个 RULE：

- rule-sata：
  - take(root-sata)
  - choose(3, host)
  - choose(1, osd)
  - emit
- rule-ssd:
  - take(root-ssd)
  - choose(3, host)
  - choose(1, osd)
  - emit

具体的建造指令可以参考之前的[自定义 CRUSH 一节](http://xuxiaopang.com/2016/10/10/ceph-full-install-el7-jewel/#自定义crush)

这一节想要说明的是，CRUSH 里面的节点除了 OSD 之外的所有 bucket 都是可以自定义的，并不需要和实际的物理结构相关，但要记住这样做的目的是将 OSD 分开，从而建立适当的 RULE 去选择 OSD，所以不要把树状结构建立的脱离了实际情况，比如从三个机器上各挑一个 OSD 然后放到一个自定义的 host 节点下，虽然可以这样做，但是是没有意义的，说白了要根据自己的数据分布要求去构建 OSD 树结构，因为 CRUSH 只认 RULE,并不知道你底层的实际结构！！！

甚至，你可以像[这篇文章](http://cephnotes.ksperis.com/blog/2015/02/02/crushmap-example-of-a-hierarchical-cluster-map/)里面一样构建出花式的树状结构！一切都在于你的想象力以及集群的应用需求。

[![Alt text](http://www.xuxiaopang.com/images/1478503163385.png)](http://www.xuxiaopang.com/images/1478503163385.png)

## Ceph 中的 CRUSH

现在再正式介绍 CRUSH 算法在 Ceph 中的存在形式，首先导出一个集群的 CRUSH Map:

```plain
[root@ceph-1 ~]# ceph osd getcrushmap -o /tmp/mapgot crush map from osdmap epoch 67[root@ceph-1 ~]# crushtool -d /tmp/map -o /tmp/map.txt [root@ceph-1 ~]# cat /tmp/map.txt # begin crush maptunable choose_local_tries 0tunable choose_local_fallback_tries 0tunable choose_total_tries 50tunable chooseleaf_descend_once 1tunable straw_calc_version 1# devicesdevice 0 osd.0device 1 osd.1device 2 osd.2device 3 osd.3device 4 osd.4device 5 osd.5device 6 osd.6device 7 osd.7device 8 osd.8# typestype 0 osdtype 1 hosttype 2 chassistype 3 racktype 4 rowtype 5 pdutype 6 podtype 7 roomtype 8 datacentertype 9 regiontype 10 root# bucketshost ceph-2 {	id -2		# do not change unnecessarily	# weight 5.970	alg straw	hash 0	# rjenkins1	item osd.0 weight 1.990	item osd.1 weight 1.990	item osd.2 weight 1.990}host ceph-1 {	id -3		# do not change unnecessarily	# weight 5.970	alg straw	hash 0	# rjenkins1	item osd.3 weight 1.990	item osd.4 weight 1.990	item osd.5 weight 1.990}host ceph-3 {	id -4		# do not change unnecessarily	# weight 5.970	alg straw	hash 0	# rjenkins1	item osd.6 weight 1.990	item osd.7 weight 1.990	item osd.8 weight 1.990}root default {	id -1		# do not change unnecessarily	# weight 17.910	alg straw	hash 0	# rjenkins1	item ceph-2 weight 5.970	item ceph-1 weight 5.970	item ceph-3 weight 5.970}# rulesrule replicated_ruleset {	ruleset 0	type replicated	min_size 1	max_size 10	step take default	step chooseleaf firstn 0 type host	step emit}# end crush map[root@ceph-1 ~]#
```

简单介绍下几个区域的意义：

- `tunable`：还记得`CRUSH_HASH`算法中的`r`变量吗，选择失败的时候这个值经常会自加一，`choose_total_tries 50`这个 50 就是用来限定总共失败的次数的，CRUSH 算法本身是个递归算法，所以给定一个总共失败次数防止算法无限选择失败。那么如果要选出 3 副本，选失败了 50 次只选出一个 OSD，那么最终结果是？CRUSH 将输出`[osd.a， ，]`这样的输出，也就是说只给出一个 OSD，一般很少会遇到这种情况，除非你要从一个只有一个 host 的 root 下面去选出三个 host。
- `devices` : 就是所有的 OSD 的集合。
- `types`: 就是集群内所有的 Bucket+OSD 的类型的取值范围，所有的 Bucket 都要属于这些类型，当然，你可以自己增删这里给出的类型，注意`type`后面的数字必须唯一，因为 CRUSH 算法在保存类型时不是使用字符串，而是类型对应的数字，所以类型名称在 CRUSH 眼里是没有意义的。
- `buckets`：就是树上的除了 OSD 以外的节点，从内容来看可以发现，每个 bucket 都有向下包含关系，这里看到 ID 和类型的 ID 是一样的，CRUSH 在底层并不保存节点的名称字符串，而是以数字保存的，值得一提的是，OSD 的 ID 是大于等于零的，bucket 的 ID 是小于零的。还有就是`alg straw`，因为 straw 是最公平的选择方法，其实还有三个算法(uniform, tree, list)，因为没有 straw 综合分高，所以就不介绍了。
- `rules`： 最下面的 rule 区域是我们修改的最多的地方，`replicated_ruleset`这个是这个 rule 的名称，需要唯一，同样 CRUSH 只保存这个 rule 的 ID，其 ID 就是`ruleset 0`这里的`0`,所以需要添加一个 rule 的时候需要注意名称和 ID 都不能重复。下面的三个`step`就是 RULE 的三步走策略，里面具体的参数我就不再赘述，可以[参考官方文档的这一章](http://docs.ceph.com/docs/master/rados/operations/crush-map/)。

还是简单的讲解下这句`step chooseleaf firstn 0 type host`， 实际的 RULE 里面分为`choose`和`chooseleaf`两种，其中`choose`用于选择多个 Bucket，Bucket 是最终选择结果，相当于`choose(3, Bucket)`。`chooseleaf`用于选择多个 Bucket，并在这些 Bucket 下各选出一个 OSD，OSD 是最终选择结果，相当于`choose(3, Bucket) + choose(1, osd)`。`type`后面的`host`就是要选择的 Bucket 类型。`firstn`后面的`0`,是选择的副本数，`0`等于副本数，也就是 3 的意思，具体参考官方文档的解释。

所以 Sage 论文中的图，对应到实际 CRUSH 的 RULE 就是：

```plain
rule Sage_Paper {	ruleset 0	type replicated	min_size 1	max_size 10	step take root	step choose firstn 1 type row	step chooseleaf firstn 0 type cabinet	step emit}
```

## 总结

介绍完了这两步走的核心流程之后，最后再着重强调下`计算`两字，可以发现，从对象计算 PG 再到 PG 计算 OSD 组合，从头到尾都是通过计算得到最终的映射关系的，但是这些计算不论放在客户端还是服务器端，计算的结果都是相同的，因为里面所谓的随机值都是伪随机，只要传入一样的输入得到的输出结果都是一样的，所以 Ceph 把计算对象存储位置的任务发放给客户端，实际上，客户端在计算完一个对象需要保存的 OSD 之后，直接和 OSD 建立通讯，将数据直接存入 OSD 中，只要集群的 Map 没有变化，客户端和服务端计算出来的保存位置都是一样的，所以这大大的降低了服务器端的计算压力。

本文没有直接介绍 CRUSH 算法，而是从`把一个对象存进Ceph`的流程来分析，着重解释了对象到 PG 的映射，PG 到 OSD 的映射这两个流程，介绍了它们的计算方法。

最后再给一个别人画的计算路径图，仅供理解。
[![Alt text](http://www.xuxiaopang.com/images/1478573403493.png)](http://www.xuxiaopang.com/images/1478573403493.png)

## 参考链接
[大话 Ceph--CRUSH 那点事儿](http://www.xuxiaopang.com/2016/11/08/easy-ceph-CRUSH/)