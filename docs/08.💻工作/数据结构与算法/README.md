---
title: 数据结构与算法

tags: 
  - 数据结构
  - 算法
categories: 
  - 💻 工作
  - 数据结构与算法
date: 2020-05-26 12:27:56
permalink: /pages/1e25ff/
---
## 目录

### 基本数据结构
- [数组](.)
- [链表](./Linked_list)
- [堆](./Heap)
- [栈](./Stack)
- [队列](./Queue)
    - [烫手山芋问题/约瑟夫环问题](./Queue/hot_potato)   
        注：很多文章把这个单词译为“热土豆”，我觉得这么翻译更符合汉语语境。当然，解决问题的思路是一样的。
- [双端队列](./Deque)

### 基本排序算法
- [快速排序](sorts/quick_sort)
- [冒泡排序](sorts/bubble_sort)
- [插入排序](sorts/insertion_sort)
- [归并排序](sorts/merge_sort)
- [选择排序](sorts/selection_sort)
- [希尔排序](sorts/shell_sort)

### 其他数据结构
#### TODO
- [树](./Tree)
- [图](./Graph)
- 第一周：数组与链表、栈与队列
- 第二周：哈希表、映射、集合
- 第二周：树、二叉数和图
- 第三周：递归、分治和回溯
- 第四周：深度、广度优先搜索与剪枝
- 第四周：贪心算法与二分查找
- 第五周：动态规划
- 第六周：并查集、字典树、红黑树和 AVL 树
- 第七周：位运算、布隆过滤器和 LRU Cache
- 第七周：排序、字符串操作串讲

## 书籍及资源

对使用 `Python` 学习数据结构和算法的资料进行收集并学习。对于外文资料，会列出英文原版，并尽量找到中文译文版。

### Problem Solving with Algorithms and Data Structures using Python

[Problem Solving with Algorithms and Data Structures using Python-原版在线阅读](https://runestone.academy/runestone/static/pythonds/index.html)

[北大教材（含电子书）](http://gis4g.pku.edu.cn/course/pythonds/)

[网友翻译版本-Gitbooks](https://facert.gitbooks.io/python-data-structure-cn/)

### 数据结构与算法（基于 Python 语言）

北大出品，[这里](http://www.math.pku.edu.cn/teachers/qiuzy/ds_python/courseware/index.htm)有教材幻灯片。

[数据结构与算法（基于 Python 语言）](http://www.math.pku.edu.cn/teachers/qiuzy/ds_python/)

### 算法图解

像小说一样有趣的算法入门书，科普入门向。

[算法图解-豆瓣](https://book.douban.com/subject/26979890/)    

### ~~`Python`算法与数据结构教程~~

~~含视频（收费），前知乎工程师写的。~~

[`Python` 算法与数据结构教程-readthedocs](https://python-data-structures-and-algorithms.readthedocs.io/zh/latest/)

这个好像是腾讯工程师写的学习总结，参考资料和上面的差不多，可以对照着看一下。

[python-algorithm](https://hujiaweibujidao.github.io/tags/algorithm/)

### Github
- [LeetCode Solutions: A Record of My Problem Solving Journey.( leetcode 题解，记录自己的 leetcode 解题之路。)](https://github.com/azl397985856/leetcode)
- [MisterBooo/LeetCodeAnimation: Demonstrate all the questions on LeetCode in the form of animation.（用动画的形式呈现解 LeetCode 题目的思路）](https://github.com/MisterBooo/LeetCodeAnimation)
- [Algorithms-Python](https://github.com/TheAlgorithms/Python)

### Data Structures and Algorithms in Python

[Data Structures and Algorithms in Python](https://doc.lagout.org/programmation/python/Data%20Structures%20and%20Algorithms%20in%20Python%20[Goodrich,%20Tamassia%20&%20Goldwasser%202013-03-18].pdf)

[算法与数据结构入门教程](https://liweiwei1419.gitee.io/leetcode-algo/)

## 可视化

- [数据结构和算法动态可视化 (中文)](https://visualgo.net/zh)
- [Data Structure Visualizations-旧金山大学](https://www.cs.usfca.edu/~galles/visualization/Algorithms.html)
- [Algorithm Visualizer](https://algorithm-visualizer.org/)

## 视频
[Python 数据结构和算法](https://www.bilibili.com/video/av43431667)

## 其他
[数据结构与算法教程-C 语言版教程](http://data.biancheng.net/)

## 约定

本仓库中代码全部使用`Python3.6+`实现，使用`Linux`操作系统运行。内页`readme`中的代码默认指同目录下`.py`文件中的代码片段。
```plain
imoyao@local:~$ lsb_release -a

No LSB modules are available.
Distributor ID:	Ubuntu
Description:	Ubuntu 18.04 LTS
Release:	18.04
Codename:	bionic

imoyao@local:~$ uname -a

Linux local 4.15.0-22-generic #24-Ubuntu SMP Wed May 16 12:15:17 UTC 2018 x86_64 x86_64 x86_64 GNU/Linux

```

>蜀之鄙有二僧，其一贫，其一富。贫者语于富者曰：“吾欲之南海，何如？”富者曰：“子何恃而往？”曰：“吾一瓶一钵足矣。”富者曰：“吾数年来欲买舟而下，犹未能也。子何恃而往？”越明年，贫者自南海还，以告富者。富者有惭色。