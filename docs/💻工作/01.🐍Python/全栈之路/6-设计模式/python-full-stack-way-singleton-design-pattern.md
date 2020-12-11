---
title: Python 全栈之路系列之单例设计模式

tags: 
  - 编码
  - 单例模式
categories: 
  - 💻 工作
  - 🐍Python
  - 全栈之路
  - 6-设计模式
date: 2020-05-23 18:21:46
permalink: /pages/ea281b/
---

## 设计模式介绍

设计模式是经过总结、优化的，对我们经常会碰到的一些编程问题的可重用解决方案。一个设计模式并不像一个类或一个库那样能够直接作用于我们的代码。反之，设计模式更为高级，它是一种必须在特定情形下实现的一种方法模板。设计模式不会绑定具体的编程语言。一个好的设计模式应该能够用大部分编程语言实现(如果做不到全部的话，具体取决于语言特性)。最为重要的是，设计模式也是一把双刃剑，如果设计模式被用在不恰当的情形下将会造成灾难，进而带来无穷的麻烦。然而如果设计模式在正确的时间被用在正确地地方，它将是你的救星。

起初，你会认为“模式”就是为了解决一类特定问题而特别想出来的明智之举。说的没错，看起来的确是通过很多人一起工作，从不同的角度看待问题进而形成的一个最通用、最灵活的解决方案。也许这些问题你曾经见过或是曾经解决过，但是你的解决方案很可能没有模式这么完备。

## 单例模式存在意义

**模式特点：**

保证类仅有一个实例，并提供一个访问它的全局访问点。

1. 设计模式在所有语言内都是通用的
2. 设计模式存在的意义就是让代码设计结构设计的更好

## 实例代码

```Python
#!/usr/bin/env python
# -*- coding:utf-8 -*-

from wsgiref.simple_server import make_server

class ConnectionPool:

    __instance = None

    def __init__(self):
        self.ip = "1.1.1.1"
        self.port = 3306
        self.pwd = "123123"
        self.username = 'xxxx'
        # 去连接
        self.conn_list = [1,2,3,4,5,6,7,8,9, 10]

    @staticmethod
    def get_instance():
        if ConnectionPool.__instance:
            return ConnectionPool.__instance
        else:
            # 创建一个对象，并将对象赋值给静态字段 __instance
            ConnectionPool.__instance = ConnectionPool()
            return ConnectionPool.__instance

    def get_connection(self):
        # 获取连接
        import random
        r = random.randrange(1,11)
        return r

def index():
    # p = ConnectionPool()
    # print(p)
    p = ConnectionPool.get_instance()
    conn = p.get_connection()
    return "iiiiiii" + str(conn)

def news():
    return 'nnnnnnn'

def RunServer(environ, start_response):
    start_response(status='200 OK', headers=[('Content-Type', 'text/html')])

    url = environ['PATH_INFO']
    if url.endswith('index'):
        ret = index()
        return ret
    elif url.endswith('news'):
        ret = news()
        return ret
    else:
        return "404"

if __name__ == '__main__':
    httpd = make_server('', 80, RunServer)
    print("Serving HTTP on port 80...")
    httpd.serve_forever()
```