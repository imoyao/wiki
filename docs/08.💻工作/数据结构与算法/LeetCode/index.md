---
title: 力扣刷题学算法

tags: 
  - 算法
  - 数据结构
  - 面试
categories: 
  - 💻 工作
  - 数据结构与算法
  - LeetCode
date: 2020-05-26 12:27:56
permalink: /pages/06f564/
---

一、入门篇
=====

刚开刷 lc 时遇到二叉树翻转题目，想了一天也没明白，当时无比痛苦。因为我的方法不对，我总想着自己在脑子里面想明白再写，还想着用本地 IDE 写个二叉树结构进行 debug，现在看来都是走了弯路。

**对于新人而言，不应该自己硬扣一个题目，如果想了一会没有任何思路，就应该果断看别人怎么写的。在理解了别人的做法之后，再凭理解和记忆在 LeetCode 的代码框里敲一遍。**

就像每个课本都会有例题一样，只学纯知识大家都不知道怎么运用的。而我们在刷 LeetCode 的时候并没有例题可以给我们学习，因此新手会感到痛苦。新手不要害怕看别人的解法和答案，度过痛苦时期，后面就会越刷越快。

新手应该注重三个方面：基础知识、跟别人学习、做好笔记 。

1\. 基础知识
--------

需要掌握常用的数据结构和算法的思想和适用场景。

我推荐《算法第 4 版》，看这个书的时候不用全部看，只看重点，比如前面的 Java 知识不用看，数学推导不用看。再推荐一本侯捷的《STL 源码剖析》，这本书对理解 C++ STL 有重大帮助，看了之后绝对会对数据结构和算法有更深的理解，我看完这本书之后感觉相见恨晚啊。

2\. 跟别人学习
---------

> 向别人学习是非常必要的。

又分为两种：

### 1）看别人的题解

主要看别人在解决这个题目的思路是什么。

推荐的题解作者有：

[花花酱](https://zxi.mytechroad.com/blog/)：基本每个题都有博客和视频，强烈推荐看他的视频。
[负雪明烛](https://blog.csdn.net/fuxuemingzhu)：把重点放在分析上，每篇质量都很高。
[Grandyang](https://www.cnblogs.com/grandyang/)：通过举例子来让你明白该怎么做。
[李威威](https://liweiwei1419.gitee.io/leetcode-algo/)，[甜姨](https://zhuanlan.zhihu.com/c_1224355183452614656)，[柳婼](https://www.liuchuo.net/)，[书影博客](http://bookshadow.com/leetcode/)。

题解区的答案：英文版看 lee215，中文版看 liweiwei 和 sweetie，以及官方解答。

如果你会做这个题目，我也觉得应该看下别人怎么解决的，思路是不是一样。

比如想看负雪明烛的 two sum 题解，那么搜索方式就是加上 fuxuemingzhu 在后面搜：

![搜题解](https://imgconvert.csdnimg.cn/aHR0cHM6Ly9waWM0LnpoaW1nLmNvbS84MC92Mi1jMDJlMzQ1OGI2NzY2Zjk2YWE0MWViMzdlNGQ5YzNkOV8xNDQwdy5qcGc?x-oss-process=image/format,png)

### 2）看别人的总结

这部分包括算法讲解、套路整理、刷题模板等。

负雪明烛说：”做题 = 想法 + 模板“，想法需要通过看别人的解答以及讲解获得，模板就是做题的套路和模板，既可以自己总结，也可以看别人总结好的。

首先是[labuladong 的算法小抄](https://labuladong.gitbook.io/algo/)，在 Github 上两周就获得了 10k star！！！强烈推荐，特别是动态规划不懂的，可以看。

然后有负雪明烛的[【LeetCode】代码模板，刷题必会](https://blog.csdn.net/fuxuemingzhu/article/details/101900729)，基本总结了所有的做题模板。

3\. 做好笔记
--------

在很多年前我就开始把每个做过的题目记录在 CSDN 上，现在[我的博客](https://blog.csdn.net/fuxuemingzhu)浏览量已经将近 100 万了。

![负雪明烛的博客](https://imgconvert.csdnimg.cn/aHR0cHM6Ly9waWMzLnpoaW1nLmNvbS84MC92Mi0xZjhjMzgyNmIzMzFhM2IzOWM1MWE3OGM0NjY4ZmU4NV8xNDQwdy5qcGc?x-oss-process=image/format,png)
我的做法是：任何题，无论难度，我都进行记录题目、想法、代码。虽然经常写博客的时间比写题的时间还多，但是把自己的想法讲解一遍才是真的懂了，更方便了自己之后看、以及大家交流。

当然，除了写题解，还要整理做题的方法、套路、模板，这些会随着你的经验慢慢形成的。

在 B 站有个小姐姐演示了如何用 iPad 做笔记，也讲了小白如何上手 LeetCode，值得一看。

程序媛分享 | LeetCode 小白如何上手刷题？iPad 学习方法 | 刷题清单 | 新手指南 | 刷题找工作 | IT 类

4\. 交流和监督
---------

刷题最大的障碍是自己。特别是新手，很可能由于刚接触 LeetCode 感觉太难就没有毅力坚持下去，导致半途而废。而且，刷题更重要的是坚持，做题的感觉都需要手感进行保持的。

所以，如果能有个组织交流和监督就好了。

我组织了”每日一题交流群“的活动，并且做了个网站[https://ojeveryday.com](https://ojeveryday.com)来监督大家打卡。群的规则是每天发题和打卡，如果一周没有参加的话就会被踢出群（如果有更好的监督方式请告诉我）。

![在这里插入图片描述](https://imgconvert.csdnimg.cn/aHR0cHM6Ly9waWMzLnpoaW1nLmNvbS84MC92Mi0yMjIzOTUzZTUxYzkzMjJiZjY0ZDM2MTk1ZDFjY2JjMV8xNDQwdy5qcGc?x-oss-process=image/format,png)

事实证明这种大家一起做同一道题目，并且一起交流讨论的氛围非常好。更多规则可以看下面的文章，我的联系方式在网站的首页。

[负雪明烛：助力每日一题！每日一题打卡网站上线！](https://zhuanlan.zhihu.com/p/120245953)

二、提高篇
=====

如果你已经过了小白的阶段，那么应该做些提高项目。

1\. 周赛
------

所谓周赛，就是每周日上午，LeetCode 组织的一场比赛，总共 4 道题，一般是 Easy 一道，Medium 两道，Hard 一道。中英文网站同时开始，题目相同。

做周赛的目的是检验我们的学习成果，毕竟这些题目都是新的，就像考试一样。

不要担心自己做不出来，只要尽力而为就好了，我一般的目标是解决前三道，第 4 道 Hard 做不出来也没有心理负担。

参加完比赛之后，看下别人的解答，因为都是自己苦思冥想过的方法，因此可以提高地特别快。

我最好的周赛成绩是全球 28 名，当时非常兴奋，开心了一整天。

2\. 总结与分享
---------

这一点和入门篇的做好笔记 略有重复，但是仍然要说，因为如果只是单纯的记录笔记和写每个题目的记录是不够的。

我在写博客的时候就落入了只记录不总结的误区中，单个题目的解决方案只会有正在做这个题的人看，但是你的提炼总结可以让你和大家都获得成长，这也是我写这个回答的原因。

上文中提到的 labuladong 的算法小抄就是个很好的总结与分享例子。

**最后，希望大家都能够通过刷 LeetCode 获得成长，拿到自己满意的 Offer。**

期待你的点赞、关注、分享。