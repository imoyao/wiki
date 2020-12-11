---
title: 列表

tags: 
  - 算法
categories: 
  - 💻 工作
  - 数据结构与算法
  - Python_stdin_data_structures
date: 2020-05-26 18:21:46
permalink: /pages/39ff38/
---

## `list`内置操作的时间复杂度

| 操作                 | 操作说明                                 | 时间复杂度 |
| -------------------- | -------------------------------------------- | ---------- |
| index(value)         | 查找 list 某个元素的索引              | O(1)       |
| a = index(value)     | 索引赋值                                 | O(1)       |
| append(value)        | 队尾添加                                 | O(1)       |
| pop()                | 队尾删除                                 | O(1)       |
| pop(index)           | 根据索引删除某个元素               | O(n)       |
| insert(index, value) | 根据索引插入某个元素               | O(n)       |
| iterration           | 列表迭代                                 | O(n)       |
| item `in` List         | 列表搜索（in 关键字）                | O(n)       |
| slice [x:y]          | 切片, 获取 x, y 为 O(1), 获取 x,y 中间的值为 O(k) | O(k)       |
| del slice [x:y]      | 删除切片，删除切片后数据需要重新移动/合并 | O(n)       |
| reverse              | 列表反转                                 | O(n)       |
| sort                 | 排序                                       | O(nlogn)   |

`index`和`append`是两个常见操作，它们无论列表多大，操作花费的时间都相同。当
一个操作的速度不因列表的大小发生变化时，其操作复杂度就是 `O(1)`。

随着列表长度的增加，从列表末端删除元素的 `pop()` 操作时间保持稳定，而从列表开头删除元素的 `pop(x)` 操作则随着长度的增加而增加。参见[代码](./code_test.py)`list_test.py:67`。

- 说明
当 `pop` 操作每次从列表的最后一位删除元素时复杂度为 `O（1）`，而将列表的第一个元素或中间任意一个位置的元素删除时，复杂度则为 `O（n）`。这样迥然不同的结果是由 `Python` 对列表的执行方式造成的。在 `Python` 的执行过程中，当从列表的第一位删除一个元素，其后的每一位元素都将向前挪动一位。你可能觉得这种操作很愚蠢，但当你仔细看完上表会发现这种执行方式是为了让 `index` 索引操作的复杂度降为 `O（1）`。这种在运行时间上的权衡是 `Python` 设计者的良苦用心。

## 实现
Python 中的列表基于 PyListObject 实现，列表支持元素的插入、删除、更新操作，因此 PyListObject 是一个变长对象（列表的长度随着元素的增加和删除而变长和变短），同时它还是一个可变对象（列表中的元素根据列表的操作而发生变化，内存大小动态的变化），PyListObject 的定义：
```c
typedef struct {
    \# 列表对象引用计数
    int ob\_refcnt;  
    \# 列表类型对象 
    struct \_typeobject \*ob\_type;
    \# 列表元素的长度
    int ob\_size; /\* Number of items in variable part \*/
    \# 真正存放列表元素容器的指针，list\[0\] 就是 ob\_item\[0\]
    PyObject \*\*ob\_item;
    \# 当前列表可容纳的元素大小
    Py\_ssize\_t allocated;
} PyListObject;
```
乍一看 PyListObject 对象的定义非常简单，除了通用对象都有的引用计数（ob\_refcnt）、类型信息（ob\_type），以及变长对象的长度（ob\_size）之外，剩下的只有 ob\_item，和 allocated，ob\_item 是真正存放列表元素容器的指针，专门有一块内存用来存储列表元素，这块内存的大小就是 allocated 所能容纳的空间。alloocated 是列表所能容纳的元素大小，而且满足条件：

*   0 <= ob\_size <= allocated
*   len(list) == ob\_size
*   ob\_item == NULL 时 ob\_size == allocated == 0

![pylistobject](http://img.foofish.net/pylistobject.jpg)

## 列表对象的创建

PylistObject 对象的是通过函数 PyList\_New 创建而成，接收参数**size**，该参数用于指定列表对象所能容纳的最大元素个数。
```c
// 列表缓冲池, PyList\_MAXFREELIST为80
static PyListObject \*free\_list\[PyList\_MAXFREELIST\];
//缓冲池当前大小
static int numfree \= 0;

PyObject \*PyList\_New(Py\_ssize\_t size)
{
    PyListObject \*op; //列表对象
    size\_t nbytes;    //创建列表对象需要分配的内存大小

    if (size < 0) {
        PyErr\_BadInternalCall();
        return NULL;
    }
    /\* Check for overflow without an actual overflow,
     \*  which can cause compiler to optimise out \*/
    if ((size\_t)size \> PY\_SIZE\_MAX / sizeof(PyObject \*))
        return PyErr\_NoMemory();
    nbytes \= size \* sizeof(PyObject \*);
    if (numfree) {
        numfree\--;
        op \= free\_list\[numfree\];
        \_Py\_NewReference((PyObject \*)op);

    } else {
        op \= PyObject\_GC\_New(PyListObject, &PyList\_Type);
        if (op \== NULL)
            return NULL;

    }
    if (size <= 0)
        op\->ob\_item \= NULL;
    else {
        op\->ob\_item \= (PyObject \*\*) PyMem\_MALLOC(nbytes);
        if (op\->ob\_item \== NULL) {
            Py\_DECREF(op);
            return PyErr\_NoMemory();
        }
        memset(op\->ob\_item, 0, nbytes);
    }
    \# 设置ob\_size
    Py\_SIZE(op) \= size;
    op\->allocated \= size;
    \_PyObject\_GC\_TRACK(op);
    return (PyObject \*) op;
}
```
创建过程大致是：

1.  检查 size 参数是否有效，如果小于 0，直接返回 NULL，创建失败
2.  检查 size 参数是否超出 Python 所能接受的大小，如果大于 PY\_SIZE\_MAX（64 位机器为 8 字节，在 32 位机器为 4 字节），内存溢出。
3.  检查缓冲池 free\_list 是否有可用的对象，有则直接从缓冲池中使用，没有则创建新的 PyListObject，分配内存。
4.  初始化 ob\_item 中的元素的值为 Null
5.  设置 PyListObject 的 allocated 和 ob\_size。

## PyListObject 对象的缓冲池

free\_list 是 PyListObject 对象的缓冲池，其大小为 80，那么 PyListObject 对象是什么时候加入到缓冲池 free\_list 的呢？答案在 list\_dealloc 方法中：
```c
static void
list\_dealloc(PyListObject \*op)
{
    Py\_ssize\_t i;
    PyObject\_GC\_UnTrack(op);
    Py\_TRASHCAN\_SAFE\_BEGIN(op)
    if (
        i \= Py\_SIZE(op);
        while (\--i \>= 0) {
            Py\_XDECREF(op\->ob\_item\[i\]);
        }
        PyMem\_FREE(op\->ob\_item);
    }
    if (numfree < PyList\_MAXFREELIST && PyList\_CheckExact(op))
        free\_list\[numfree++\] \= op;
    else
        Py\_TYPE(op)\->tp\_free((PyObject \*)op);
    Py\_TRASHCAN\_SAFE\_END(op)
}
```
当 PyListObject 对象被销毁的时候，首先将列表中所有元素的引用计数减一，然后释放 ob\_item 占用的内存，只要缓冲池空间还没满，那么就把该 PyListObject 加入到缓冲池中（此时 PyListObject 占用的内存并不会正真正回收给系统，下次创建 PyListObject 优先从缓冲池中获取 PyListObject），否则释放 PyListObject 对象的内存空间。

## 列表元素插入

设置列表某个位置的值时，如“list\[1\]=0”，列表的内存结构并不会发生变化，而往列表中插入元素时会改变列表的内存结构：
```c
static int
ins1(PyListObject \*self, Py\_ssize\_t where, PyObject \*v)
{
    // n是列表元素长度
    Py\_ssize\_t i, n \= Py\_SIZE(self);
    PyObject \*\*items;
    if (v \== NULL) {
        PyErr\_BadInternalCall();
        return \-1;
    }
    if (n \== PY\_SSIZE\_T\_MAX) {
        PyErr\_SetString(PyExc\_OverflowError,
            "cannot add more objects to list");
        return \-1;
    }

    if (list\_resize(self, n+1) \== \-1)
        return \-1;

    if (where < 0) {
        where += n;
        if (where < 0)
            where \= 0;
    }
    if (where \> n)
        where \= n;
    items \= self\->ob\_item;
    for (i \= n; \--i \>= where; )
        items\[i+1\] \= items\[i\];
    Py\_INCREF(v);
    items\[where\] \= v;
    return 0;
}
```
相比设置某个列表位置的值来说，插入操作要多一次 PyListObject 容量大小的调整，逻辑是 list\_resize，其次是挪动 where 之后的元素位置。
```c
// newsize： 列表新的长度
static int  
list\_resize(PyListObject \*self, Py\_ssize\_t newsize)
{
    PyObject \*\*items;
    size\_t new\_allocated;
    Py\_ssize\_t allocated \= self\->allocated;

    if (allocated \>= newsize && newsize \>= (allocated \>> 1)) {
        assert(self\->ob\_item != NULL || newsize \== 0);
        Py\_SIZE(self) \= newsize;
        return 0;
    }

    new\_allocated \= (newsize \>> 3) + (newsize < 9 ? 3 : 6);

    /\* check for integer overflow \*/
    if (new\_allocated \> PY\_SIZE\_MAX \- newsize) {
        PyErr\_NoMemory();
        return \-1;
    } else {
        new\_allocated += newsize;
    }

    if (newsize \== 0)
        new\_allocated \= 0;
    items \= self\->ob\_item;
    if (new\_allocated <= (PY\_SIZE\_MAX / sizeof(PyObject \*)))
        PyMem\_RESIZE(items, PyObject \*, new\_allocated);
    else
        items \= NULL;
    if (items \== NULL) {
        PyErr\_NoMemory();
        return \-1;
    }
    self\->ob\_item \= items;
    Py\_SIZE(self) \= newsize;
    self\->allocated \= new\_allocated;
    return 0;
}
```
满足 `allocated >= newsize && newsize >= (allocated /2)`时，简单改变 list 的元素长度，PyListObject 对象不会重新分配内存空间，否则重新分配内存空间，如果`newsize<allocated/2`，那么会减缩内存空间，如果`newsize>allocated`，就会扩大内存空间。当`newsize==0`时内存空间将缩减为 0。 ![!python_list_resize](http://img.foofish.net/python_list_resize.jpg)

## 总结

*   PyListObject 缓冲池的创建发生在列表销毁的时候。
*   PyListObject 对象的创建分两步：先创建 PyListObject 对象，然后初始化元素列表为 NULL。
*   PyListObject 对象的销毁分两步：先销毁 PyListObject 对象中的元素列表，然后销毁 PyListObject 本身。
*   PyListObject 对象内存的占用空间会根据列表长度的变化而调整。

## 参考

*   [listobject.h](https://github.com/lzjun567/python2.7/blob/master/Include/listobject.h)
*   [listobject.c](https://github.com/lzjun567/python2.7/blob/master/Objects/listobject.c)
- [Python 列表对象实现原理 - FooFish-Python 之禅](https://foofish.net/python-list-implements.html)

## 更多阅读
[Python list implementation – Laurent Luce's Blog](http://www.laurentluce.com/posts/python-list-implementation/)
[Python 内存分析:list 和 array](https://www.cnblogs.com/hellcat/p/8795841.html)