---
title: Python 全栈之路系列之基于 socket 实现文件上传

tags: 
  - 编码
  - socket
top: 3
categories: 
  - 💻 工作
  - 🐍Python
  - 全栈之路
  - 4-网络编程
date: 2020-05-23 18:21:46
permalink: /pages/c45da2/
---

## 前言

此处没有前言

## 粘包

在实现发送文件功能之前我们先来理解下粘包的问题，下面有两张图，我觉得很清晰的就可以理解到了。

- 正常情况下发送文件

![socket-sticky-package-01](https://ansheng.me/wp-content/uploads/2016/12/1483021785.png)

1. **第一步：** 客户端把获取到的文件总大小(size=65426)先放到缓冲区，然后发送给服务端
2. **第二步：** 此时客户端接收到的文件总大小就是 65426

- 粘包的问题下发送文件

![socket-sticky-package-02](https://ansheng.me/wp-content/uploads/2016/12/1483021810.png)

1. **第一步：** 客户端把获取到的文件总大小(size=65426)先放到缓冲区
2. **第二步：** 此时可能由于文件读取太快，导致缓存区的内容还没有发送到服务端，客户端就把读取到的文件内容(hello)也放到缓存区；
3. **第三步：** 然后客户端就把缓存区的全部内容都发送到服务端，那么客户端本来第一次应该接收到的数据室文件大小(size=65426)，但实际接收到的数据确实：65426+hello，那么这个流程就是粘包的问题；

- 解决粘包问题

如果出现粘包的问题，那么传输的数据就有问题了，如何解决这个问题呢？看下图：

![socket-sticky-package-03](https://ansheng.me/wp-content/uploads/2016/12/1483021831.png)

1. **第一步：** 客户端把文件大小放到缓冲区
2. **第二步：** 放入缓冲区之后立刻陷入阻塞的状态，等待服务端回复已收到文件大小，此时是不会再向服务端发送任何数据的
3. **第三步：** 缓存区的数据会发送到服务端
4. **第四步：** 服务端接收到客户端发来的文件大小之后立刻回复客户端，说我收到你发过来的文件大小了；

## 文件上传

执行结果如下

![socket-03](https://ansheng.me/wp-content/uploads/2016/12/1483021854.png)

`client.py`文件内容

```bash
ansheng@Darker:~/socket_file$ cat client.py
#!/usr/bin/env python
# _*_coding:utf-8 _*_

import socket
import os

# 创建一个socket对象
obj = socket.socket()

# 服务端的IP和端口
obj.connect(('127.0.0.1', 6542))

# 用os模块获取要传送的文件总大小
size = os.stat("old_file.txt").st_size

# 把文件总大小发送给服务端
obj.sendall(bytes(str(size), encoding="utf-8"))

# 接受服务端返回的信息
obj.recv(1024)

# 以rb的模式打开一个要发送的文件d
with open("old_file.txt", "rb") as f:

    # 循环文件的所有内容
    for line in f:

        # 发送给服务端
        obj.sendall(line)

# 关闭退出
obj.close()
```

`service.py`文件内容

```Python
ansheng@Darker:~/socket_file$ cat service.py
#!/usr/bin/env python
# _*_coding:utf-8 _*_

import socket
# 创建一个socket对象
sk = socket.socket()
# 允许连接的IP和端口
sk.bind(('127.0.0.1', 6542))
# 最大连接数
sk.listen(5)

while True:
    # 会一直阻塞，等待接收客户端的请求，如果有客户端连接会获取两个值，conn=创建的连接，address=客户端的IP和端口
    conn, address = sk.accept()

    # 客户端发送过来的文件大小
    file_size = str(conn.recv(1024),encoding="utf-8")

    # 给客户端发送已经收到文件大小
    conn.sendall(bytes("ack", encoding="utf-8"))

    # 文件大小转换成int类型
    total_size = int(file_size)

    # 创建一个默认的值
    has_recv = 0

    # 打开一个新文件，以wb模式打开
    f = open('new_file.txt', 'wb')

    # 进入循环
    while True:

        # 如果传送过来的大小等于文件总大小，那么就退出
        if total_size == has_recv:
            break

        # 接受客户端发送过来的内容
        data = conn.recv(1024)

        # 写入到文件当中
        f.write(data)

        # 现在的大小加上客户端发送过来的大小
        has_recv += len(data)

    # 关闭
    f.close()
```