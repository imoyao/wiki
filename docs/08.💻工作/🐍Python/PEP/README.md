---
title: PEP 中文翻译计划
tags: 
  - TODO
  - 待学清单
cover: https://cdn.jsdelivr.net/gh/masantu/statics/image/jessica-lewis-fJXv46LT7Xk-unsplash.jpg
subtitle: 人人都有松鼠癖，人人都是马来人。😑
top: 10

categories: 
  - 💻 工作
  - 🐍Python
  - PEP
date: 2019-11-27 23:34:31
permalink: /pages/a11f68/
---
出处：[PEP 中文翻译计划](https://github.com/chinesehuazhou/peps-cn)
## 什么是 PEP

全称是 `Python Enhancement Proposals`，其中 Enhancement 是增强改进的意思，Proposals 则可译为提案或建议书，所以合起来，比较常见的翻译是 `Python增强提案`或`Python改进建议书`。

PEP 的官网是：https://www.python.org/dev/peps/ ，这也就是 PEP 0 的地址。其它 PEP 的地址是将编号拼接在后面，例如：https://www.python.org/dev/peps/pep-0020/  就是 PEP 20 的链接，以此类推。

第一个 PEP 诞生于 2000 年，现在正好是 18 岁成年。到目前为止，它拥有 478 个“兄弟姐妹”。

官方将 PEP 分成三类:

>I - Informational PEP
>
>P - Process PEP
>
>S - Standards Track PEP

其含义如下:

信息类：这类 PEP 就是提供信息，有告知类信息，也有指导类信息等等。例如 PEP 20（The Zen of Python，即著名的 Python 之禅）、PEP 404 (Python 2.8 Un-release Schedule，即宣告不会有 Python2.8 版本)。

流程类：这类 PEP 主要是 Python 本身之外的周边信息。例如 PEP 1（PEP Purpose and Guidelines，即关于 PEP 的指南）、PEP 347（Migrating the Python CVS to Subversion，即关于迁移 Python 代码仓）。

标准类：这类 PEP 主要描述了 Python 的新功能和新实践（implementation），是数量最多的提案。例如我之前推文《[详解 Python 拼接字符串的七种方式](https://mp.weixin.qq.com/s/Whrd6NiD4Y2Z-YSCy4XJ1w)》提到过的 f-string 方式，它出自 PEP 498（Literal String Interpolation，字面字符串插值）。

每个 PEP 最初都是一个草案（Draft），随后会经历一个过程，因此也就出现了不同的状态。以下是一个流程图：

![PEP process flow diagram](https://www.python.org/m/dev/peps/pep-0001/pep-0001-process_flow.png)

>A – Accepted (Standards Track only) or Active proposal 已接受（仅限标准跟踪）或有效提案
>
>D – Deferred proposal 延期提案
>
>F – Final proposal 最终提案
>
>P – Provisional proposal 暂定提案
>
>R – Rejected proposal 被否决的提案
>
>S – Superseded proposal 被取代的提案
>
>W – Withdrawn proposal 撤回提案

在 PEP 0（Index of Python Enhancement Proposals (PEPs)）里，官方列举了所有的 PEP，你可以按序号、按类型以及按状态进行检索。而在 PEP 1（PEP Purpose and Guidelines）里，官方详细说明了 PEP 的意图、如何提交 PEP、如何修复和更新 PEP、以及 PEP 评审的机制等等。

为什么要读 PEP
----------

无论你是刚入门 Python 的小白、有一定经验的从业人员，还是资深的黑客，都应该阅读 Python 增强提案。

依我之见，阅读 PEP 至少有如下好处:

（1）了解 Python 有哪些特性，它们与其它语言特性的差异，为什么要设计这些特性，是怎么设计的，怎样更好地运用它们；

（2）跟进社区动态，获知业内的最佳实践方案，调整学习方向，改进工作业务的内容；

（3）参与热点议题讨论，或者提交新的 PEP，为 Python 社区贡献力量。

说到底，学会用 Python 编程，只是掌握了皮毛。PEP 提案是深入了解 Python 的途径，是真正掌握 Python 语言的一把钥匙，也是得心应手使用 Python 的一本指南。


哪些 PEP 是必读的
---------

如前所述，PEP 提案已经累积产生了 478 个，我们并不需要对每个 PEP 都熟知，没有必要。下面，我列举了一些 PEP，推荐大家一读：

PEP 0 -- Index of Python Enhancement Proposals

PEP 7 -- Style Guide for C Code，C 扩展

PEP 8 -- Style Guide for Python Code，Python 编码规范（必读）

PEP 20 -- The Zen of Python，Python 之禅

PEP 202 -- List Comprehensions，列表生成式

PEP 274 -- Dict Comprehensions，字典生成式

PEP 234 -- Iterators，迭代器

PEP 257 -- Docstring Conventions，文档注释规范

PEP 279 -- The enumerate() built-in function，enumerate 枚举

PEP 282 -- A Logging System，日志模块

PEP 285 -- Adding a bool type，布尔值

PEP 289 -- Generator Expressions，生成器表达式

PEP 318 -- Decorators for Functions and Methods，装饰器

PEP 342 -- Coroutines via Enhanced Generators，协程

PEP 343 -- The "with" Statement，with 语句

PEP 380 -- Syntax for Delegating to a Subgenerator，yield from 语法

PEP 405 -- Python Virtual Environments，虚拟环境

PEP 471 -- os.scandir() function，遍历目录

PEP 484 -- Type Hints，类型约束

PEP 492 -- Coroutines with async and await syntax，async/await 语法

PEP 498 -- Literal String Interpolation Python，字面字符串插值

PEP 525 -- Asynchronous Generators，异步生成器

PEP 572 -- Assignment Expressions，表达式内赋值（最具争议）

PEP 3105 -- Make print a function，print 改为函数

PEP 3115 -- Metaclasses in Python 3000，元类

PEP 3120 -- Using UTF-8 as the default source encoding，默认 UTF-8

PEP 3333 -- Python Web Server Gateway Interface v1.0.1，Web 开发

PEP 8000 -- Python Language Governance Proposal Overview，GvR 老爹退出决策层后，事关新决策方案

关于 PEP，知乎上有两个问题，推荐大家关注：[哪些 PEP 值得阅读](https://dwz.cn/7CHMBlLu)，[如何看待 PEP 572？](https://dwz.cn/L46jpzMB)。

对 PEP 的贡献
-------------
虽无确切数据作证，我国 Python 开发者的数量应该比任何国家都多。然而，纵观 PEP 0 里面列举的 200 多个 PEP 作者，我只看到了一个像是汉语拼音的国人名字（不排除看漏，或者使用了英文名的）。反差真是太大了。

我特别希望，国内的 Python 黑客们的名字，能越来越多地出现在那个列表里，出现在 Python 核心开发者的列表里。

此外，关于对 PEP 的贡献，还有一种很有效的方式，就是将 PEP 翻译成中文，造福国内的 Python 学习社区。经过一番搜索，我还没有看到系统性翻译 PEP 的项目，只找到了零星的对于某个 PEP 的翻译。

原文链接：https://mp.weixin.qq.com/s/oRoBxZ2-IyuPOf_MWyKZyw

## 相关链接

官方索引地址：https://www.python.org/dev/peps/

官方文档地址：https://github.com/python/peps

## 翻译成果

（由于版权缘故，未获得译者授权的 PEP，未放入仓库）

- PEP8 -- [Python 编码风格指南](https://dwz.cn/W01HexFD)
- PEP202 -- [列表推导式](https://github.com/chinesehuazhou/peps-cn/blob/master/StandardsTrack/202--%E5%88%97%E8%A1%A8%E6%8E%A8%E5%AF%BC%E5%BC%8F.md)
- PEP255 -- [简单的生成器](https://github.com/chinesehuazhou/peps-cn/blob/master/StandardsTrack/255--%E7%AE%80%E5%8D%95%E7%9A%84%E7%94%9F%E6%88%90%E5%99%A8.md)
- PEP257 -- [Docstring 约定](https://dwz.cn/JLctlNLC)
- PEP285 -- [添加一种布尔类型](https://github.com/chinesehuazhou/peps-cn/blob/master/StandardsTrack/285--%E6%B7%BB%E5%8A%A0%E5%B8%83%E5%B0%94%E7%B1%BB%E5%9E%8B.md)
- PEP318 -- [函数和方法的装饰器](https://github.com/chinesehuazhou/peps-cn/blob/master/StandardsTrack/318--%E5%87%BD%E6%95%B0%E5%92%8C%E6%96%B9%E6%B3%95%E7%9A%84%E8%A3%85%E9%A5%B0%E5%99%A8.md)
- PEP328 -- [导入：多行及绝对/相对](https://github.com/chinesehuazhou/peps-cn/blob/master/StandardsTrack/328--%E5%AF%BC%E5%85%A5%EF%BC%8C%E5%A4%9A%E8%A1%8C%E5%8F%8A%E7%BB%9D%E5%AF%B9%E7%9B%B8%E5%AF%B9.md)
- PEP333 -- [Python Web 服务器网关接口 v1.0](https://dwz.cn/TAXIZdzc)
- PEP342 -- [增强型生成器：协程](https://github.com/chinesehuazhou/peps-cn/blob/master/StandardsTrack/342--%E5%A2%9E%E5%BC%BA%E5%9E%8B%E7%94%9F%E6%88%90%E5%99%A8%EF%BC%9A%E5%8D%8F%E7%A8%8B.md)
- PEP380 -- [子生成器的语法](https://github.com/chinesehuazhou/peps-cn/blob/master/StandardsTrack/380--%E5%AD%90%E7%94%9F%E6%88%90%E5%99%A8%E7%9A%84%E8%AF%AD%E6%B3%95.md)
- PEP443 -- [单分派泛型函数（Single-dispatch generic functions）](https://www.cnblogs.com/popapa/p/PEP443.html)
- PEP482 -- [类型提示的文档性概述（Literature Overview for Type Hints）](https://www.cnblogs.com/popapa/p/PEP482.html)
- PEP483 -- [类型提示的理论（The Theory of Type Hints）](https://www.cnblogs.com/popapa/p/PEP483.html)
- PEP484 -- [类型提示](https://github.com/chinesehuazhou/peps-cn/blob/master/StandardsTrack/484--%E7%B1%BB%E5%9E%8B%E6%8F%90%E7%A4%BA.md) \ [另一篇译文](https://www.cnblogs.com/popapa/p/PEP484.html)
- PEP492 -- [使用 async 和 await 语法的协程](http://t.cn/EALeaL0)
- PEP518 --  [指定构建 Python 项目的最低系统要求](https://blog.csdn.net/weixin_38382105/article/details/80331816)
- PEP525 -- [异步生成器](https://github.com/chinesehuazhou/peps-cn/blob/master/StandardsTrack/525--%E5%BC%82%E6%AD%A5%E7%94%9F%E6%88%90%E5%99%A8.md)
- PEP526 -- [变量注解的语法（Syntax for Variable Annotations）](https://www.cnblogs.com/popapa/p/PEP526.html)
- PEP530 -- [异步推导式](https://github.com/chinesehuazhou/peps-cn/blob/master/StandardsTrack/530--%E5%BC%82%E6%AD%A5%E6%8E%A8%E5%AF%BC%E5%BC%8F.md) 
- PEP541 -- [包索引名的保留](https://dwz.cn/ce98vc27)
- PEP570 -- [Positional-Only 参数](https://mp.weixin.qq.com/s/gxEmUs8f9tVqhfd5kERDCg)
- PEP614 -- [放宽对装饰器的语法限制](https://github.com/chinesehuazhou/peps-cn/blob/master/StandardsTrack/614--%E6%94%BE%E5%AE%BD%E5%AF%B9%E8%A3%85%E9%A5%B0%E5%99%A8%E7%9A%84%E8%AF%AD%E6%B3%95%E9%99%90%E5%88%B6.md)
- PEP618 -- [给 zip 添加可选的长度检查](https://github.com/chinesehuazhou/peps-cn/blob/master/StandardsTrack/618--%E7%BB%99%20zip%20%E6%B7%BB%E5%8A%A0%E5%8F%AF%E9%80%89%E7%9A%84%E9%95%BF%E5%BA%A6%E6%A3%80%E6%9F%A5.md)
- PEP3099 -- [Python 3 中不会改变的事情](https://github.com/chinesehuazhou/peps-cn/blob/master/Informational/3099--Python%203%20%E4%B8%AD%E4%B8%8D%E4%BC%9A%E6%94%B9%E5%8F%98%E7%9A%84%E4%BA%8B%E6%83%85.md)
- PEP3105 -- [改 print 为函数](https://github.com/chinesehuazhou/peps-cn/blob/master/StandardsTrack/3105--%E6%94%B9%20print%20%E4%B8%BA%E5%87%BD%E6%95%B0.md)
- PEP3107 -- [函数注解](https://github.com/chinesehuazhou/peps-cn/blob/master/StandardsTrack/3107--%E5%87%BD%E6%95%B0%E6%B3%A8%E8%A7%A3.md) \ [另一篇译文](https://www.cnblogs.com/popapa/p/PEP3107.html)
- PEP3129 -- [类装饰器](https://github.com/chinesehuazhou/peps-cn/blob/master/StandardsTrack/3129--%E7%B1%BB%E8%A3%85%E9%A5%B0%E5%99%A8.md)
- PEP3141 -- [数值类型的层次结构（A Type Hierarchy for Numbers）](https://www.cnblogs.com/popapa/p/PEP3141.html)
- PEP3155 -- [类和方法的特定名称](https://github.com/chinesehuazhou/peps-cn/blob/master/StandardsTrack/3155--%E7%B1%BB%E5%92%8C%E6%96%B9%E6%B3%95%E7%9A%84%E7%89%B9%E5%AE%9A%E5%90%8D%E7%A7%B0.md) 
- PEP3333 -- [PythonWeb 服务器网关接口 v1.0.1](https://dwz.cn/si3xylgw)
