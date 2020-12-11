---
title: Python 整数对象实现原理

tags: 
  - 算法
categories: 
  - 💻 工作
  - 数据结构与算法
  - Python_stdin_data_structures
date: 2020-05-25 18:21:46
permalink: /pages/d7f572/
---
整数对象在 Python 内部用`PyIntObject`结构体表示：

```c
typedef struct {
    PyObject\_HEAD
    long ob\_ival;
} PyIntObject;
```
PyObject\_HEAD 宏中定义的两个属性分别是：
```c
int ob\_refcnt;
struct \_typeobject \*ob\_type;
```
这两个属性是所有 Python 对象固有的：

*   ob\_refcnt：对象的引用计数，与 Python 的内存管理机制有关，它实现了基于引用计数的垃圾收集机制
*   ob\_type：用于描述 Python 对象的类型信息。

由此看来 PyIntObject 就是一个对 C 语言中 long 类型的数值的扩展，出于性能考虑,对于小整数，Python 使用小整数对象池`small_ints`缓存了\[-5，257）之间的整数，该范围内的整数在 Python 系统中是共享的。
```c
#define NSMALLPOSINTS           257
#define NSMALLNEGINTS           5
static PyIntObject \*small\_ints\[NSMALLNEGINTS + NSMALLPOSINTS\];
```
![pythonblock_small_int](http://img.foofish.net/pythonblock_small_int.png)

而超过该范围的整数即使值相同，但对象不一定是同一个，如下所示：当 a 与 b 的值都是 10000，但并不是同一个对象，而值为 1 的时候，a 和 b 属于同一个对象。
```python
\>>> a = 10000
>>> b = 10000
>>> print a is b
False
>>> a = 1
>>> b = 1
>>> print a is b
True
```
对于超出了\[-5, 257)之间的其他整数，Python 同样提供了专门的缓冲池，供这些所谓的大整数使用，避免每次使用的时候都要不断的 malloc 分配内存带来的效率损耗。这块内存空间就是`PyIntBlock`。
```c
struct \_intblock {

    struct \_intblock \*next;
    PyIntObject objects\[N\_INTOBJECTS\];
};
typedef struct \_intblock PyIntBlock;

static PyIntBlock \*block\_list = NULL;
static PyIntObject \*free\_list = NULL;
```
这些内存块（PyIntBlock）通过一个单向链表组织在一起，表头是`block_list`，表头始终指向最新创建的 PyIntBlock 对象。

PyIntBlock 有两个属性：next，objects。next 指针指向下一个 PyIntBlock 对象，objects 是一个 PyIntObject 数组（最终会转变成单向链表），它是真正用于存储被缓存的 PyIntObjet 对象的内存空间。

`free_list`单向链表是所有 PyIntBlock 内存块中空闲的内存。所有空闲内存通过一个链表组织起来的好处就是在 Python 需要新的内存来存储新的 PyIntObject 对象时，能够通过`free_list`快速获得所需的内存。

![python int blcik](http://img.foofish.net/python_int_block.jpg)

创建一个整数对象时，如果它在小整数范围内，就直接从小整数缓冲池中直接返回，如果不在该范围内，就开辟一个大整数缓冲池内存空间：
```c
\[intobject.c\]
PyObject\* PyInt\_FromLong(long ival)
{
     register PyIntObject \*v;
#if NSMALLNEGINTS + NSMALLPOSINTS > 0
     //\[1\] ：尝试使用小整数对象池
     if (-NSMALLNEGINTS <\= ival && ival < NSMALLPOSINTS) {
 v = small\_ints\[ival + NSMALLNEGINTS\];
 Py\_INCREF(v);
 return (PyObject \*) v;
 }
#endif
    //\[2\] ：为通用整数对象池申请新的内存空间
    if (free\_list \=\= NULL) {
 if ((free\_list = fill\_free\_list()) == NULL)
 return NULL;
 }
 //\[3\] : (inline)内联PyObject\_New的行为
 v = free\_list;
 free\_list = (PyIntObject \*)v->ob\_type;
 PyObject\_INIT(v, &PyInt\_Type);
 v->ob\_ival = ival;
 return (PyObject \*) v;
}
```
`fill_free_list`就是创建大整数缓冲池内存空间的逻辑，该函数返回一个`free_list`链表，当整数对象 ival 创建成功后，`free_list`表头就指向了`v->ob_type`，`ob_type`不是所有 Python 对象中表示类型信息的字段吗？怎么在这里作为一个连接指针呢？这是 Python 在性能与代码优雅之间取中庸之道，对名称的滥用，放弃了对类型安全的坚持。把它理解成指向下一个 PyIntObject 的指针即可。
```c
\[intobject.c\]
static PyIntObject\* fill\_free\_list(void)
{
    PyIntObject \*p, \*q;
    // 申请大小为sizeof(PyIntBlock)的内存空间
    // block list始终指向最新创建的PyIntBlock
    p \= (PyIntObject \*) PyMem\_MALLOC(sizeof(PyIntBlock));
 ((PyIntBlock \*)p)->next = block\_list;
 block\_list = (PyIntBlock \*)p;

    //：将PyIntBlock中的PyIntObject数组(objects)转变成单向链表
    p \= &((PyIntBlock \*)p)->objects\[0\];
 q = p + N\_INTOBJECTS;
 while (--q > p)
 // ob\_type指向下一个未被使用的PyIntObject。
 q->ob\_type = (struct \_typeobject \*)(q-1);
 q->ob\_type = NULL;
 return p + N\_INTOBJECTS - 1;
}
```
不同的 PyIntBlock 里面的空闲的内存是怎样连接起来构成`free_list`的呢？这个秘密放在了整数对象垃圾回收的时候，在 PyIntObject 对象的 tp\_dealloc 操作中可以看到：
```c
\[intobject.c\]
static void int\_dealloc(PyIntObject \*v)
{
    if (PyInt\_CheckExact(v)) {
        v->ob\_type \= (struct \_typeobject \*)free\_list;
 free\_list = v;
 }
 else
 v->ob\_type->tp\_free((PyObject \*)v);
}
```
原来 PyIntObject 对象销毁时，它所占用的内存并不会释放，而是继续被 Python 使用，进而将`free_list`表头指向了这个要被销毁的对象上。

#### 总结

*   Python 中的 int 对象就是 c 语言中 long 类型数值的扩展
*   小整数对象\[-5, 257\]在 python 中是共享的
*   整数对象都是从缓冲池中获取的。
*   整数对象回收时，内存并不会归还给系统，而是将其对象的 ob\_type 指向 free\_list，供新创建的整数对象使用

源码参考：

*   [intobject.c](https://github.com/lzjun567/python2.7/blob/master/Objects/intobject.c)
*   [Python 字符串实现原理](http://foofish.net/blog/90/python_str_inplements)
*   [Python 列表对象实现原理](http://foofish.net/blog/91/python-list-implements)
*   [Python 字典对象实现原理](http://foofish.net/blog/92/python_dict_implements)
