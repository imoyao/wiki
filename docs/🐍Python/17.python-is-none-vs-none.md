---
title: Ptyhon 中使用 is None 而不是 ==None 问题
tags: 
  - Python
  - 编程
categories: 
  - 💻 工作
  - 🐍Python
date: 2020-08-10 12:27:56
permalink: /pages/0ae4f5/
---
首先需要区分 Python 中`is`和`==`的区别：
- [python - Is there a difference between "==" and "is"? - StackOverflow](https://stackoverflow.com/questions/132988/is-there-a-difference-between-and-is)
- [python - Is there any difference between "foo is None" and "foo == None"? - StackOverflow](https://stackoverflow.com/questions/26595/is-there-any-difference-between-foo-is-none-and-foo-none)

`is`比较在两个对象是否相同时使用（即通过比较在内存中的标识符（`id(obj)`）），而`==`通过调用`__eq__()`方法比较两个的值是否相等。

看下面的 [回答](https://stackoverflow.com/a/14247419) ：
> `is` is generally preferred when comparing arbitrary objects to singletons like `None` because it is faster and more predictable. `is` always compares by object identity, whereas what `==` will do depends on the exact type of the operands and even on their ordering.
>
> This recommendation is supported by PEP 8, which explicitly states that "comparisons to singletons like None should always be done with is or is not, never the equality operators."

通常，在将任意对象与`None`之类的单个对象进行比较时首选`is`，因为它更快且更可预测。 `is`总是根据对象标识进行比较，而`==`的作用取决于运算对象的确切类型，甚至取决于它们的顺序。
PEP 8 支持此建议，该声明明确指出“与单例的比较（如`None`，应该始终使用`is`或 `not`进行比较，**永远不要**使用相等运算符进行比较）”。
在工作效率上，`is`的效率明显高于`==`：
```plain
>>> a = timeit.timeit("1 is None", number=10000000) # 0.6208912429997326

>>> b = timeit.timeit("1 == None", number=10000000) # 0.9341017190004095

>>> a /b
0.6125248705781231
```
当然，在数值上来看差距不是很大，但是量变引起质变。

## 参考链接

[Python: "is None" vs "==None" | Jared Grubb](http://jaredgrubb.blogspot.com/2009/04/python-is-none-vs-none.html)
[python - What is the difference between " is None " and " ==None " - StackOverflow](https://stackoverflow.com/questions/3257919/what-is-the-difference-between-is-none-and-none)