---
title: 递归

tags: 
  - 算法
categories: 
  - 💻 工作
  - 数据结构与算法
  - Recursion
date: 2020-05-25 18:21:46
permalink: /pages/2cd013/
---

## 引言

> 从前有座山，山里有座庙，庙里有个老和尚，正在给小和尚讲故事呢！故事是什么呢？“从前有座山，山里有座庙，庙里有个老和尚，正在给小和尚讲故事呢！故事是什么呢？‘从前有座山，山里有座庙，庙里有个老和尚，正在给小和尚讲故事呢！故事是什么呢？……’”

## 概念

递归指在函数的定义中使用函数自身的方法。指由一种（或多种）简单的基本情况定义的一类对象或方法，并规定其他所有情况都能被还原为其基本情况。

## 日常事例

- 查字典
- 阅读维基百科（内链）

## 图示

![自然界中的递归](/images/fab_in_culture.jpg)

![生活中中的递归](/images/recurse_in_life.jpg)

## 特点

- 方法里调用自身。   
- 在使用递增归策略时，必须有一个明确的递归结束条件，称为递归出口。                 
- 递归算法解题通常显得很简洁，但递归算法解题的*运行效率较低*。所以一般不提倡用递归算法设计程序。
- 在递归调用的过程当中系统为每一层的返回点、局部量等开辟了栈来存储。递归次数过多容易造成`栈溢出`等，所以一般不提倡用递归算法设计程序。

表现在 `Python` 语言中，即为报错信息`RecursionError: maximum recursion depth exceeded in comparison.`
默认递归深度为 1000 ，我们可以通过修改下面的代码设置调节，但是**通常不建议这样操作**。（效率太低）
```python
import sys
sys.setrecursionlimit(100000)
```
## 伪代码比较`迭代`和`递归`

我们通过一个在大箱子中找钥匙的场景来对`迭代`和`递归`进行比较。(参照*算法图解*)
```python
def look_for_key_with_iteration(big_box):
    pile = big_box.make_a_pile_to_look_through()        # 把大箱子里面的东西一股脑倒出来
    while pile.is_not_empty():      # 在堆里开始查找
        box = pile.grap_a_box()     # 拿起大箱子中的一个物品
        for item in box:            
            if item.is_box():       # 如果是盒子
                pile.append(item)   # 收集到盒子堆里，等待后续可能的进一步查找
            elif item.is_key():     # 如果是钥匙，说明找到了
                return 'found key'


def look_for_key_with_recursion(big_box):
    for item in big_box:
        if item.is_box():
            look_for_key_with_recursion(item)       # 如果拿到的是盒子，把这个盒子先翻个底朝天
        elif item.is_key():                         # 如果拿到钥匙，则大功告成
            return 'found key'
```
如果使用循环，程序的性能可能更好；如果使用递归，程序可能更容易（被程序员）理解。如何选择要看你更看重选择。[参见此处](http://stackoverflow.com/a/72694/139117)

## 代码

见[此处](./recursion.py)

# **尾递归**

在函数返回的时候，调用自身本身，并且，`return`语句不能包含表达式。

```python
def bar():
    pass
    
def foo():
    return bar()
```
上面代码中，函数`foo()`的最后一步是调用函数`bar()`，这就叫尾调用。
具体实现见[代码](./recursion.py)中的`tail_recursion_fact()`函数。

`Python`解释器没有做优化，所以，即使把上面的`factorial(n)`函数改成尾递归方式的`tail_recursion_fact()`，也会导致栈溢出。

通过特殊的装饰器，我们也可以实现[Python 开启尾递归优化](https://segmentfault.com/a/1190000007641519),详见代码中的`tail_call_optimized()`函数。

## 注意

尽管使用递归思想编写程序通常可以使条理更加清晰，但是有可能导致消耗的空间和时间使我们得不偿失。
比如`fib_normal()`、`fib_recursion()`和`fib_tail_recursion()`在计算`Fibonacci`数列前 30 项时，消耗的时间分别是:
```bash
The function **fib_normal** takes 0.00020684471130371094 time.      
The function **fib_recursion** takes 4.22707200050354 time.
The function **fib_tail_recursion** takes 0.0005285739898681641 time.
```

## 参考阅读

- [递归函数](https://www.liaoxuefeng.com/wiki/897692888725344/897693398334720)


