---
title: Python 字符串对象实现原理

tags: 
  - 算法
categories: 
  - 💻 工作
  - 数据结构与算法
  - Python_stdin_data_structures
date: 2020-05-24 18:21:46
permalink: /pages/d36225/
---
在 Python 世界中将对象分为两种：一种是定长对象，比如整数，整数对象定义的时候就能确定它所占用的内存空间大小，另一种是变长对象，在对象定义时并不知道是多少，比如：str，list, set, dict 等。
```plain
\>>> import sys
\>>> sys.getsizeof(1000)
28
\>>> sys.getsizeof(2000)
28
\>>> sys.getsizeof("python")
55
\>>> sys.getsizeof("java")
53
```
如上，整数对象所占用的内存都是 28 字节，和具体的值没关系，而同样都是字符串对象，不同字符串对象所占用的内存是不一样的，这就是变长对象，对于变长对象，在对象定义时是不知道对象所占用的内存空间是多少的。

字符串对象在 Python 内部用 PyStringObject 表示，PyStringObject 和 PyIntObject 一样都属于不可变对象，对象一旦创建就不能改变其值。（注意：**变长对象**和**不可变对象**是两个不同的概念）。PythonStringObject 的定义：
```c
\[stringobject.h\]
typedef struct {
    PyObject\_VAR\_HEAD
    long ob\_shash;
    int ob\_sstate;
    char ob\_sval\[1\];
} PyStringObject;
```
不难看出 Python 的字符串对象内部就是由一个字符数组维护的，在[整数的实现原理](http://foofish.net/blog/89/python_int_implement)一文中提到`PyObject_HEAD`，对于`PyObject_VAR_HEAD`就是在`PyObject_HEAD`基础上多出一个`ob_size`属性：
```c
\[object.h\]
#define PyObject\_VAR\_HEAD 
    PyObject\_HEAD           
    int ob\_size; /\* Number of items in variable part \*/

typedef struct {
    PyObject\_VAR\_HEAD
} PyVarObject;
```
*   `ob_size`保存了变长对象中元素的长度，比如 PyStringObject 对象"Python"的`ob_size`为 6。
*   `ob_sval`是一个初始大小为 1 的字符数组，且 ob\_sval\[0\] = '\\0'，但实际上创建一个 PyStringObject 时`ob_sval`指向的是一段长为`ob_size`+1 个字节的内存。
*   `ob_shash`是字符串对象的哈希值，初始值为-1，在第一次计算出字符串的哈希值后，会把该值缓存下来，赋值给`ob_shash`。
*   `ob_sstate`用于标记该字符串对象是否进过 intern 机制处理（后文会介绍)。

## PyStringObject 对象创建过程
```c
\[stringobject.c\]
PyObject \* PyString\_FromString(const char \*str)
{
    register size\_t size;
    register PyStringObject \*op;

    assert(str !\= NULL);
 size = strlen(str);
 // \[1\]
 if (size > PY\_SSIZE\_T\_MAX - PyStringObject\_SIZE) {
 PyErr\_SetString(PyExc\_OverflowError,
 "string is too long for a Python string");
 return NULL;
 }
 // \[2\]
 if (size == 0 && (op = nullstring) != NULL) {
#ifdef COUNT\_ALLOCS
        null\_strings++;
#endif
        Py\_INCREF(op);
        return (PyObject \*)op;
    }
    // \[3\]
    if (size \=\= 1 && (op = characters\[\*str & UCHAR\_MAX\]) != NULL) {
#ifdef COUNT\_ALLOCS
        one\_strings++;
#endif
        Py\_INCREF(op);
        return (PyObject \*)op;
    }

    // \[4\]
    /\* Inline PyObject\_NewVar \*/
    op \= (PyStringObject \*)PyObject\_MALLOC(PyStringObject\_SIZE + size);
 if (op == NULL)
 return PyErr\_NoMemory();
 PyObject\_INIT\_VAR(op, &PyString\_Type, size);
 op->ob\_shash = -1;
 op->ob\_sstate = SSTATE\_NOT\_INTERNED;
 Py\_MEMCPY(op->ob\_sval, str, size+1);
 /\* share short strings \*/
 if (size == 0) {
 PyObject \*t = (PyObject \*)op;
 PyString\_InternInPlace(&t);
 op = (PyStringObject \*)t;
 nullstring = op;
 Py\_INCREF(op);
 } else if (size == 1) {
 PyObject \*t = (PyObject \*)op;
 PyString\_InternInPlace(&t);
 op = (PyStringObject \*)t;
 characters\[\*str & UCHAR\_MAX\] = op;
 Py\_INCREF(op);
 }
 return (PyObject \*) op;
}
```
1.  如果字符串的长度超出了 Python 所能接受的最大长度(32 位平台是 2G)，则返回 Null。
2.  如果是空字符串，那么返回特殊的 PyStringObject，即 nullstring。
3.  如果字符串的长度为 1，那么返回特殊 PyStringObject，即 onestring。
4.  其他情况下就是分配内存，初始化 PyStringObject，把参数 str 的字符数组拷贝到 PyStringObject 中的`ob_sval`指向的内存空间。

## 字符串的 intern 机制

PyStringObject 的`ob_sstate`属性用于标记字符串对象是否经过 intern 机制处理，intern 处理后的字符串，比如"Python"，在解释器运行过程中始终只有唯一的一个字符串"Python"对应的 PyStringObject 对象。
```plain
\>>> a = "python"
>>> b = "python"
>>> a is b
True
```
如上所示，创建 a 时，系统首先会创建一个新的 PyStringObject 对象出来，然后经过 intern 机制处理（PyString\_InternInPlace），接着查找经过 intern 机制处理的 PyStringObject 对象，如果发现有该字符串对应的 PyStringObject 存在，则直接返回该对象，否则把刚刚创建的 PyStringObject 加入到 intern 机制中。由于 a 和 b 字符串字面值是一样的，因此 a 和 b 都指向同一个 PyStringObject("python")对象。那么 intern 内部又是一个什么样的机制呢？
```c
\[stringobject.c\]
static PyObject \*interned;

void PyString\_InternInPlace(PyObject \*\*p)
{
    register PyStringObject \*s \= (PyStringObject \*)(\*p);
 PyObject \*t;
 if (s == NULL || !PyString\_Check(s))
 Py\_FatalError("PyString\_InternInPlace: strings only please!");
 /\* If it's a string subclass, we don't really know what putting
 it in the interned dict might do. \*/
 // \[1\]
 if (!PyString\_CheckExact(s))
 return;
 // \[2\]
 if (PyString\_CHECK\_INTERNED(s))
 return;
 // \[3\]
 if (interned == NULL) {
 interned = PyDict\_New();
 if (interned == NULL) {
 PyErr\_Clear(); /\* Don't leave an exception \*/
 return;
 }
 }
 t = PyDict\_GetItem(interned, (PyObject \*)s);
 if (t) {
 Py\_INCREF(t);
 Py\_DECREF(\*p);
 \*p = t;
 return;
 }

    if (PyDict\_SetItem(interned, (PyObject \*)s, (PyObject \*)s) < 0) {
        PyErr\_Clear();
        return;
    }
    /\* The two references in interned are not counted by refcnt.
       The string deallocator will take care of this \*/
    Py\_REFCNT(s) -\= 2;
 PyString\_CHECK\_INTERNED(s) = SSTATE\_INTERNED\_MORTAL;
}
```
1.  先类型检查，intern 机制只处理字符串
2.  如果该 PyStringObject 对象已经进行过 intern 机制处理，则直接返回
3.  interned 其实一个字典对象，当它为 null 时，初始化一个字典对象，否则，看该字典中是否存在一个 key 为`(PyObject *)s`的 value，如果存在，那么就把该对象的引用计数加 1，临时创建的那个对象的引用计数减 1。否则，把`(PyObject *)s`同时作为 key 和 value 添加到 interned 字典中，与此同时它的引用计数减 2，这两个引用计数减 2 是因为被 interned 字典所引用，但这两个引用不作为垃圾回收的判断依据，否则，字符串对象永远都不会被垃圾回收器收集了。

![intern](http://img.foofish.net/python_str_intern.jpg)

上述代码中，给 b 赋值为"python"后，系统中创建了几个 PyStringObject 对象呢？答案是：2，在创建 b 的时候，一定会有一个临时的 PyStringObject 作为字典的 key 在 interned 中查找是否存在一个 PyStringObject 对象的值为"python"。

## 字符串的缓冲池

字符串除了有 intern 机制缓存字符串之外，字符串还有一种专门的短字符串缓冲池`characters`。用于缓存字符串长度为 1 的 PyStringObject 对象。
```c
    static PyStringObject \*characters\[UCHAR\_MAX + 1\];   //UCHAR\_MAX = 255
```
创建长度为 1 的字符串时流程：
```c
...
 else if (size \== 1) {
    PyObject \*t \= (PyObject \*)op;
    PyString\_InternInPlace(&t);
    op \= (PyStringObject \*)t;
    characters\[\*str & UCHAR\_MAX\] \= op;
    Py\_INCREF(op);
```
1.  首先创建一个 PyStringObject 对象。
2.  进行 intern 操作
3.  将 PyStringObject 缓存到 characters 中
4.  引用计数增 1

![characters](http://img.foofish.net/python_str_charaters.jpg)

## 总结
1. 字符串用 PyStringObject 表示 
2. 字符串属于变长对象 
3. 字符串属于不可变对象 
4. 字符串用 intern 机制提高 python 的效率 
5. 字符串有专门的缓冲池存储长度为 1 的字符串对象

## 参考  
 - [stringobject.c](https://github.com/lzjun567/python2.7/blob/master/Objects/stringobject.c)
- [Python 整数对象实现原理](http://foofish.net/blog/89/python_int_implement) 
- [Python 列表对象实现原理](http://foofish.net/blog/91/python-list-implements)
- [Python 字典对象实现原理](http://foofish.net/blog/92/python_dict_implements)
