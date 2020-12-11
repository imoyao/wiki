---
title: 树

tags: 
  - 算法
categories: 
  - 💻 工作
  - 数据结构与算法
  - Tree
date: 2020-05-25 18:21:46
permalink: /pages/8d3dfe/
---

## 概念
在计算机科学中，树（tree）是一种抽象数据类型（ADT）或是实现这种抽象数据类型的数据结构，用来模拟具有树状结构性质的数据集合。它是由 n（n>0）个有限节点组成一个具有层次关系的集合。把它叫做“树”是因为它看起来像一棵倒挂的树，也就是说它是根朝上，而叶朝下的。

## 生活实例
族谱

## 特点

- 每个节点都只有有限个子节点或无子节点；
- 没有父节点的节点称为根节点；
- 每一个非根节点有且只有一个父节点；
- 除了根节点外，每个子节点可以分为多个不相交的子树；
- 树里面没有环路(cycle)

## 图示

![树](/images/Treedatastructure.png)

## 术语
- **节点的度**：一个节点含有的子树的个数称为该节点的度；
- **树的度**：一棵树中，最大的节点度称为树的度；
-  **叶节点**或终端节点：度为零的节点；
    ![节点与度](/images/21AKcEALa8.png)
- 非终端节点或分支节点：度不为零的节点；
- 父亲节点或**父节点**：若一个节点含有子节点，则这个节点称为其子节点的父节点；
- 孩子节点或**子节点**：一个节点含有的子树的根节点称为该节点的子节点；
- 兄弟节点：具有相同父节点的节点互称为兄弟节点；
- 节点的层次：从根开始定义起，根为第 1 层，根的子节点为第 2 层，以此类推；
- **深度**：对于任意节点 n,n 的深度为从根到 n 的唯一路径长，根的深度为 0；
- **高度**：对于任意节点 n,n 的高度为从 n 到一片树叶的最长路径长，所有树叶的高度为 0；
    ![深度](/images/G21BLhmll3.png)
- 堂兄弟节点：父节点在同一层的节点互为堂兄弟；
- 节点的祖先：从根到该节点所经分支上的所有节点；
- 子孙：以某节点为根的子树中任一节点都称为该节点的子孙。
- 森林：由 m（m>=0）棵互不相交的树的集合称为森林；

## 分类

<table cellspacing="0" class="nowraplinks collapsible autocollapse navbox-inner" style="border-spacing:0;background:transparent;color:inherit" id="collapsibleTable0"><tbody><tr><th scope="col" class="navbox-title" colspan="2"><div style="font-size:110%"><a href="https://wikipedia.hk.wjbk.site/baike-%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%A7%91%E5%AD%A6" title="计算机科学">计算机科学</a>中的<a href="https://wikipedia.hk.wjbk.site/baike-%E6%A0%91_(%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84)" title="树 (数据结构)">树</a></div></th></tr><tr style="height:2px"><td colspan="3"></td></tr><tr><th scope="row" class="navbox-group"><a href="https://wikipedia.hk.wjbk.site/baike-%E4%BA%8C%E5%8F%89%E6%A0%91" title="二叉树">二叉树</a></th><td class="navbox-list navbox-odd hlist" style="text-align:left;border-left-width:2px;border-left-style:solid;width:100%;padding:0px"><div style="padding:0em 0.25em">
<ul><li><a href="https://wikipedia.hk.wjbk.site/baike-%E4%BA%8C%E5%85%83%E6%90%9C%E5%B0%8B%E6%A8%B9" title="二叉搜索树">二叉查找树（BST）</a></li>
<li><a href="https://wikipedia.hk.wjbk.site/baike-%E7%AC%9B%E5%8D%A1%E5%B0%94%E6%A0%91" title="笛卡尔树">笛卡尔树</a></li>
<li><a href="/w/index.php?title=MVP%E6%A0%91&amp;action=edit&amp;redlink=1" class="new" title="MVP树（页面不存在）">MVP树</a></li>
<li><span class="ilh-all" data-orig-title="Top tree" data-lang-code="en" data-lang-name="英语" data-foreign-title="Top tree"><span class="ilh-page"><a href="/w/index.php?title=Top_tree&amp;action=edit&amp;redlink=1" class="new" original-title="Top tree（页面不存在）">Top tree</a></span><span class="noprint ilh-comment">（<span class="ilh-lang">英语</span><span class="ilh-colon">：</span><span class="ilh-link"><a href="https://en.wikipedia.org/wiki/Top_tree" class="extiw" title="en:Top tree"><span lang="en" dir="auto">Top tree</span></a></span>）</span></span></li>
<li><a href="/w/index.php?title=T%E6%A0%91&amp;action=edit&amp;redlink=1" class="new" title="T树（页面不存在）">T树</a></li></ul>
</div></td></tr><tr style="height:2px"><td colspan="3"></td></tr><tr><th scope="row" class="navbox-group"><a href="https://wikipedia.hk.wjbk.site/baike-%E8%87%AA%E5%B9%B3%E8%A1%A1%E4%BA%8C%E5%8F%89%E6%9F%A5%E6%89%BE%E6%A0%91" class="mw-redirect" title="自平衡二叉查找树">自平衡二叉查找树</a></th><td class="navbox-list navbox-even hlist" style="text-align:left;border-left-width:2px;border-left-style:solid;width:100%;padding:0px"><div style="padding:0em 0.25em">
<ul><li><a href="https://wikipedia.hk.wjbk.site/baike-AA%E6%A0%91" title="AA树">AA树</a></li>
<li><a href="https://wikipedia.hk.wjbk.site/baike-AVL%E6%A0%91" title="AVL树">AVL树</a></li>
<li><a href="https://wikipedia.hk.wjbk.site/baike-%E5%B7%A6%E5%80%BE%E7%BA%A2%E9%BB%91%E6%A0%91" title="左倾红黑树">左倾红黑树</a></li>
<li><a class="mw-selflink selflink">红黑树</a></li>
<li><a href="https://wikipedia.hk.wjbk.site/baike-%E6%9B%BF%E7%BD%AA%E7%BE%8A%E6%A0%91" title="替罪羊树">替罪羊树</a></li>
<li><a href="https://wikipedia.hk.wjbk.site/baike-%E4%BC%B8%E5%B1%95%E6%A0%91" title="伸展树">伸展树</a></li>
<li><a href="https://wikipedia.hk.wjbk.site/baike-%E6%A0%91%E5%A0%86" title="树堆">树堆</a></li>
<li><a href="https://wikipedia.hk.wjbk.site/baike-%E5%8A%A0%E6%9D%83%E5%B9%B3%E8%A1%A1%E6%A0%91" title="加权平衡树">加权平衡树</a></li></ul>
</div></td></tr><tr style="height:2px"><td colspan="3"></td></tr><tr><th scope="row" class="navbox-group"><a href="https://wikipedia.hk.wjbk.site/baike-B%E6%A0%91" title="B树">B树</a></th><td class="navbox-list navbox-odd hlist" style="text-align:left;border-left-width:2px;border-left-style:solid;width:100%;padding:0px"><div style="padding:0em 0.25em">
<ul><li><a href="https://wikipedia.hk.wjbk.site/baike-B%2B%E6%A0%91" title="B+树">B+树</a></li>
<li><a href="/w/index.php?title=B*%E6%A0%91&amp;action=edit&amp;redlink=1" class="new" title="B*树（页面不存在）">B*树</a></li>
<li><a href="/w/index.php?title=Bx%E6%A0%91&amp;action=edit&amp;redlink=1" class="new" title="Bx树（页面不存在）">B<small><sup>x</sup></small>树</a></li>
<li><a href="/w/index.php?title=UB%E6%A0%91&amp;action=edit&amp;redlink=1" class="new" title="UB树（页面不存在）">UB树</a></li>
<li><a href="https://wikipedia.hk.wjbk.site/baike-2-3%E6%A0%91" title="2-3树">2-3树</a></li>
<li><a href="https://wikipedia.hk.wjbk.site/baike-2-3-4%E6%A0%91" title="2-3-4树">2-3-4树</a></li>
<li><a href="/w/index.php?title=(a,b)-%E6%A0%91&amp;action=edit&amp;redlink=1" class="new" title="(a,b)-树（页面不存在）">(a,b)-树</a></li>
<li><span class="ilh-all" data-orig-title="Dancing tree" data-lang-code="en" data-lang-name="英语" data-foreign-title="Dancing tree"><span class="ilh-page"><a href="/w/index.php?title=Dancing_tree&amp;action=edit&amp;redlink=1" class="new" original-title="Dancing tree（页面不存在）">Dancing tree</a></span><span class="noprint ilh-comment">（<span class="ilh-lang">英语</span><span class="ilh-colon">：</span><span class="ilh-link"><a href="https://en.wikipedia.org/wiki/Dancing_tree" class="extiw" title="en:Dancing tree"><span lang="en" dir="auto">Dancing tree</span></a></span>）</span></span></li>
<li><a href="https://wikipedia.hk.wjbk.site/baike-H%E6%A0%91" title="H树">H树</a></li></ul>
</div></td></tr><tr style="height:2px"><td colspan="3"></td></tr><tr><th scope="row" class="navbox-group"><a href="https://wikipedia.hk.wjbk.site/baike-%E5%A0%86_(%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84)" class="mw-redirect" title="堆 (数据结构)">堆</a></th><td class="navbox-list navbox-even hlist" style="text-align:left;border-left-width:2px;border-left-style:solid;width:100%;padding:0px"><div style="padding:0em 0.25em">
<ul><li><a href="https://wikipedia.hk.wjbk.site/baike-%E4%BA%8C%E5%8F%89%E5%A0%86" title="二叉堆">二叉堆</a></li>
<li><a href="https://wikipedia.hk.wjbk.site/baike-%E4%BA%8C%E9%A1%B9%E5%A0%86" title="二项堆">二项堆</a></li>
<li><a href="https://wikipedia.hk.wjbk.site/baike-%E6%96%90%E6%B3%A2%E9%82%A3%E5%A5%91%E5%A0%86" title="斐波那契堆">斐波那契堆</a></li>
<li><a href="https://wikipedia.hk.wjbk.site/baike-%E5%B7%A6%E5%81%8F%E6%A0%91" title="左偏树">左偏树</a></li>
<li><a href="https://wikipedia.hk.wjbk.site/baike-%E9%85%8D%E5%AF%B9%E5%A0%86" title="配对堆">配对堆</a></li>
<li><a href="https://wikipedia.hk.wjbk.site/baike-%E6%96%9C%E5%A0%86" title="斜堆">斜堆</a></li>
<li><span class="ilh-all" data-orig-title="Van Emde Boas tree" data-lang-code="en" data-lang-name="英语" data-foreign-title="Van Emde Boas tree"><span class="ilh-page"><a href="/w/index.php?title=Van_Emde_Boas_tree&amp;action=edit&amp;redlink=1" class="new" original-title="Van Emde Boas tree（页面不存在）">Van Emde Boas tree</a></span><span class="noprint ilh-comment">（<span class="ilh-lang">英语</span><span class="ilh-colon">：</span><span class="ilh-link"><a href="https://en.wikipedia.org/wiki/Van_Emde_Boas_tree" class="extiw" title="en:Van Emde Boas tree"><span lang="en" dir="auto">Van Emde Boas tree</span></a></span>）</span></span></li></ul>
</div></td></tr><tr style="height:2px"><td colspan="3"></td></tr><tr><th scope="row" class="navbox-group"><a href="https://wikipedia.hk.wjbk.site/baike-Trie" title="Trie">Trie</a></th><td class="navbox-list navbox-odd hlist" style="text-align:left;border-left-width:2px;border-left-style:solid;width:100%;padding:0px"><div style="padding:0em 0.25em">
<ul><li><a href="https://wikipedia.hk.wjbk.site/baike-%E5%90%8E%E7%BC%80%E6%A0%91" title="后缀树">后缀树</a></li>
<li><a href="https://wikipedia.hk.wjbk.site/baike-%E5%9F%BA%E6%95%B0%E6%A0%91" title="基数树">基数树</a></li>
<li><a href="https://wikipedia.hk.wjbk.site/baike-%E4%B8%89%E5%8F%89%E6%90%9C%E7%B4%A2%E6%A0%91" title="三叉搜索树">三叉查找树</a></li>
<li><a href="/w/index.php?title=X-%E5%BF%AB%E9%80%9F%E5%89%8D%E7%BC%80%E6%A0%91&amp;action=edit&amp;redlink=1" class="new" title="X-快速前缀树（页面不存在）">X-快速前缀树</a></li>
<li><a href="/w/index.php?title=Y-%E5%BF%AB%E9%80%9F%E5%89%8D%E7%BC%80%E6%A0%91&amp;action=edit&amp;redlink=1" class="new" title="Y-快速前缀树（页面不存在）">Y-快速前缀树</a></li>
<li><a href="https://wikipedia.hk.wjbk.site/baike-AC%E8%87%AA%E5%8A%A8%E6%9C%BA%E7%AE%97%E6%B3%95" title="AC自动机算法">AC自动机</a></li></ul>
</div></td></tr><tr style="height:2px"><td colspan="3"></td></tr><tr><th scope="row" class="navbox-group"><a href="https://wikipedia.hk.wjbk.site/baike-%E4%BA%8C%E5%8F%89%E7%A9%BA%E9%97%B4%E5%88%86%E5%89%B2" title="二叉空间分割">二叉空间分割（BSP）</a>树</th><td class="navbox-list navbox-even hlist" style="text-align:left;border-left-width:2px;border-left-style:solid;width:100%;padding:0px"><div style="padding:0em 0.25em">
<ul><li><a href="https://wikipedia.hk.wjbk.site/baike-%E5%9B%9B%E5%8F%89%E6%A0%91" title="四叉树">四叉树</a></li>
<li><a href="https://wikipedia.hk.wjbk.site/baike-%E5%85%AB%E5%8F%89%E6%A0%91" title="八叉树">八叉树</a></li>
<li><a href="https://wikipedia.hk.wjbk.site/baike-K-d%E6%A0%91" title="K-d树"><i>k</i>-d树</a></li>
<li><a href="/w/index.php?title=%E9%9A%90%E5%BC%8Fk-d%E6%A0%91&amp;action=edit&amp;redlink=1" class="new" title="隐式k-d树（页面不存在）">隐式<i>k</i>-d树</a></li>
<li><a href="/w/index.php?title=VP%E6%A0%91&amp;action=edit&amp;redlink=1" class="new" title="VP树（页面不存在）">VP树</a></li></ul>
</div></td></tr><tr style="height:2px"><td colspan="3"></td></tr><tr><th scope="row" class="navbox-group">非二叉树</th><td class="navbox-list navbox-odd hlist" style="text-align:left;border-left-width:2px;border-left-style:solid;width:100%;padding:0px"><div style="padding:0em 0.25em">
<ul><li><a href="/w/index.php?title=%E6%8C%87%E6%95%B0%E6%A0%91&amp;action=edit&amp;redlink=1" class="new" title="指数树（页面不存在）">指数树</a></li>
<li><a href="/w/index.php?title=%E8%9E%8D%E5%90%88%E6%A0%91&amp;action=edit&amp;redlink=1" class="new" title="融合树（页面不存在）">融合树</a></li>
<li><a href="/w/index.php?title=%E5%8C%BA%E9%97%B4%E6%A0%91&amp;action=edit&amp;redlink=1" class="new" title="区间树（页面不存在）">区间树</a></li>
<li><a href="/w/index.php?title=PQ%E6%A0%91&amp;action=edit&amp;redlink=1" class="new" title="PQ树（页面不存在）">PQ树</a></li>
<li><span class="ilh-all" data-orig-title="Range tree" data-lang-code="en" data-lang-name="英语" data-foreign-title="Range tree"><span class="ilh-page"><a href="/w/index.php?title=Range_tree&amp;action=edit&amp;redlink=1" class="new" original-title="Range tree（页面不存在）">Range tree</a></span><span class="noprint ilh-comment">（<span class="ilh-lang">英语</span><span class="ilh-colon">：</span><span class="ilh-link"><a href="https://en.wikipedia.org/wiki/Range_tree" class="extiw" title="en:Range tree"><span lang="en" dir="auto">Range tree</span></a></span>）</span></span></li>
<li><a href="/w/index.php?title=SPQR%E6%A0%91&amp;action=edit&amp;redlink=1" class="new" title="SPQR树（页面不存在）">SPQR树</a></li></ul>
</div></td></tr><tr style="height:2px"><td colspan="3"></td></tr><tr><th scope="row" class="navbox-group"><a href="/w/index.php?title=%E7%A9%BA%E9%97%B4%E6%95%B0%E6%8D%AE%E5%BA%93&amp;action=edit&amp;redlink=1" class="new" title="空间数据库（页面不存在）">空间</a>数据分割树</th><td class="navbox-list navbox-even hlist" style="text-align:left;border-left-width:2px;border-left-style:solid;width:100%;padding:0px"><div style="padding:0em 0.25em">
<ul><li><a href="https://wikipedia.hk.wjbk.site/baike-R%E6%A0%91" title="R树">R树</a></li>
<li><a href="https://wikipedia.hk.wjbk.site/baike-R*%E6%A0%91" title="R*树">R*树</a></li>
<li><a href="https://wikipedia.hk.wjbk.site/baike-R%2B%E6%A0%91" title="R+树">R+树</a></li>
<li><a href="/w/index.php?title=X%E6%A0%91&amp;action=edit&amp;redlink=1" class="new" title="X树（页面不存在）">X树</a></li>
<li><a href="/w/index.php?title=M%E6%A0%91&amp;action=edit&amp;redlink=1" class="new" title="M树（页面不存在）">M树</a></li>
<li><a href="https://wikipedia.hk.wjbk.site/baike-%E7%B7%9A%E6%AE%B5%E6%A8%B9_(%E5%84%B2%E5%AD%98%E5%8D%80%E9%96%93)" class="mw-redirect" title="线段树 (存储区间)">线段树</a></li>
<li><a href="https://wikipedia.hk.wjbk.site/baike-%E5%8F%AF%E6%8C%81%E4%B9%85%E5%8C%96%E7%BA%BF%E6%AE%B5%E6%A0%91" title="可持久化线段树">可持久化线段树</a></li>
<li><a href="/w/index.php?title=%E5%B8%8C%E5%B0%94%E4%BC%AF%E7%89%B9R%E6%A0%91&amp;action=edit&amp;redlink=1" class="new" title="希尔伯特R树（页面不存在）">希尔伯特R树</a></li>
<li><a href="/w/index.php?title=%E4%BC%98%E5%85%88R%E6%A0%91&amp;action=edit&amp;redlink=1" class="new" title="优先R树（页面不存在）">优先R树</a></li></ul>
</div></td></tr><tr style="height:2px"><td colspan="3"></td></tr><tr><th scope="row" class="navbox-group">其他树</th><td class="navbox-list navbox-odd hlist" style="text-align:left;border-left-width:2px;border-left-style:solid;width:100%;padding:0px"><div style="padding:0em 0.25em">
<ul><li><a href="/w/index.php?title=%E6%95%A3%E5%88%97%E6%97%A5%E5%8E%86&amp;action=edit&amp;redlink=1" class="new" title="散列日历（页面不存在）">散列日历</a></li>
<li><a href="/w/index.php?title=%E6%95%A3%E5%88%97%E6%A0%91&amp;action=edit&amp;redlink=1" class="new" title="散列树（页面不存在）">散列树</a></li>
<li><span class="ilh-all" data-orig-title="Finger tree" data-lang-code="en" data-lang-name="英语" data-foreign-title="Finger tree"><span class="ilh-page"><a href="/w/index.php?title=Finger_tree&amp;action=edit&amp;redlink=1" class="new" original-title="Finger tree（页面不存在）">Finger tree</a></span><span class="noprint ilh-comment">（<span class="ilh-lang">英语</span><span class="ilh-colon">：</span><span class="ilh-link"><a href="https://en.wikipedia.org/wiki/Finger_tree" class="extiw" title="en:Finger tree"><span lang="en" dir="auto">Finger tree</span></a></span>）</span></span></li>
<li><a href="https://wikipedia.hk.wjbk.site/baike-%E9%A1%BA%E5%BA%8F%E7%BB%9F%E8%AE%A1%E6%A0%91" title="顺序统计树">顺序统计树</a></li>
<li><span class="ilh-all" data-orig-title="Metric tree" data-lang-code="en" data-lang-name="英语" data-foreign-title="Metric tree"><span class="ilh-page"><a href="/w/index.php?title=Metric_tree&amp;action=edit&amp;redlink=1" class="new" original-title="Metric tree（页面不存在）">Metric tree</a></span><span class="noprint ilh-comment">（<span class="ilh-lang">英语</span><span class="ilh-colon">：</span><span class="ilh-link"><a href="https://en.wikipedia.org/wiki/Metric_tree" class="extiw" title="en:Metric tree"><span lang="en" dir="auto">Metric tree</span></a></span>）</span></span></li>
<li><span class="ilh-all" data-orig-title="Cover tree" data-lang-code="en" data-lang-name="英语" data-foreign-title="Cover tree"><span class="ilh-page"><a href="/w/index.php?title=Cover_tree&amp;action=edit&amp;redlink=1" class="new" original-title="Cover tree（页面不存在）">Cover tree</a></span><span class="noprint ilh-comment">（<span class="ilh-lang">英语</span><span class="ilh-colon">：</span><span class="ilh-link"><a href="https://en.wikipedia.org/wiki/Cover_tree" class="extiw" title="en:Cover tree"><span lang="en" dir="auto">Cover tree</span></a></span>）</span></span></li>
<li><a href="/w/index.php?title=BK%E6%A0%91&amp;action=edit&amp;redlink=1" class="new" title="BK树（页面不存在）">BK树</a></li>
<li><span class="ilh-all" data-orig-title="Doubly chained tree" data-lang-code="en" data-lang-name="英语" data-foreign-title="Doubly chained tree"><span class="ilh-page"><a href="/w/index.php?title=Doubly_chained_tree&amp;action=edit&amp;redlink=1" class="new" original-title="Doubly chained tree（页面不存在）">Doubly chained tree</a></span><span class="noprint ilh-comment">（<span class="ilh-lang">英语</span><span class="ilh-colon">：</span><span class="ilh-link"><a href="https://en.wikipedia.org/wiki/Doubly_chained_tree" class="extiw" title="en:Doubly chained tree"><span lang="en" dir="auto">Doubly chained tree</span></a></span>）</span></span></li>
<li><span class="ilh-all" data-orig-title="iDistance" data-lang-code="en" data-lang-name="英语" data-foreign-title="iDistance"><span class="ilh-page"><a href="/w/index.php?title=IDistance&amp;action=edit&amp;redlink=1" class="new" original-title="IDistance（页面不存在）">iDistance</a></span><span class="noprint ilh-comment">（<span class="ilh-lang">英语</span><span class="ilh-colon">：</span><span class="ilh-link"><a href="https://en.wikipedia.org/wiki/iDistance" class="extiw" title="en:iDistance"><span lang="en" dir="auto">iDistance</span></a></span>）</span></span></li>
<li><span class="ilh-all" data-orig-title="Link-cut tree" data-lang-code="en" data-lang-name="英语" data-foreign-title="Link-cut tree"><span class="ilh-page"><a href="/w/index.php?title=Link-cut_tree&amp;action=edit&amp;redlink=1" class="new" original-title="Link-cut tree（页面不存在）">Link-cut tree</a></span><span class="noprint ilh-comment">（<span class="ilh-lang">英语</span><span class="ilh-colon">：</span><span class="ilh-link"><a href="https://en.wikipedia.org/wiki/Link-cut_tree" class="extiw" title="en:Link-cut tree"><span lang="en" dir="auto">Link-cut tree</span></a></span>）</span></span></li>
<li><span class="ilh-all" data-orig-title="Log-structured merge-tree" data-lang-code="en" data-lang-name="英语" data-foreign-title="Log-structured merge-tree"><span class="ilh-page"><a href="/w/index.php?title=Log-structured_merge-tree&amp;action=edit&amp;redlink=1" class="new" original-title="Log-structured merge-tree（页面不存在）">Log-structured merge-tree</a></span><span class="noprint ilh-comment">（<span class="ilh-lang">英语</span><span class="ilh-colon">：</span><span class="ilh-link"><a href="https://en.wikipedia.org/wiki/Log-structured_merge-tree" class="extiw" title="en:Log-structured merge-tree"><span lang="en" dir="auto">Log-structured merge-tree</span></a></span>）</span></span></li>
<li><a href="https://wikipedia.hk.wjbk.site/baike-%E6%A0%91%E7%8A%B6%E6%95%B0%E7%BB%84" title="树状数组">树状数组</a></li>
<li><a href="https://wikipedia.hk.wjbk.site/baike-%E5%93%88%E5%B8%8C%E6%A0%91" title="哈希树">哈希树</a>(Merkle tree)</li></ul>
</div></td></tr></tbody></table>

- 无序树：树中任意节点的子节点之间没有顺序关系，这种树称为无序树，也称为自由树；
- 有序树：树中任意节点的子节点之间有顺序关系，这种树称为有序树；
- 二叉树：每个节点最多含有两个子树的树称为二叉树；
- 完全二叉树：对于一颗二叉树，假设其深度为 d（d>1）。除了第 d 层外，其它各层的节点数目均已达最大值，且第 d 层所有节点从左向右连续地紧密排列，这样的二叉树被称为完全二叉树；
- 满二叉树：所有叶节点都在最底层的完全二叉树；
- 平衡二叉树（AVL 树）：当且仅当任何节点的两棵子树的高度差不大于 1 的二叉树；
- 排序二叉树(二叉查找树（英语：Binary Search Tree))：也称二叉搜索树、有序二叉树；
- 霍夫曼树：带权路径最短的二叉树称为哈夫曼树或最优二叉树；
- B 树：一种对读写操作进行优化的自平衡的二叉查找树，能够保持数据有序，拥有多于两个子树。
- 红黑树   
 [漫画：什么是红黑树？](https://juejin.im/post/5a27c6946fb9a04509096248)
## 更多

- [树 (数据结构)-维基百科](https://wiwiwiki.kfd.me/wiki/%E6%A0%91_(%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84))
- [[Data Structure] 数据结构中各种树](https://www.cnblogs.com/maybe2030/p/4732377.html)
- [数据结构树(Tree)详解](http://data.biancheng.net/tree/)
- [【图解数据结构】 树](https://www.cnblogs.com/songwenjie/p/8878851.html)