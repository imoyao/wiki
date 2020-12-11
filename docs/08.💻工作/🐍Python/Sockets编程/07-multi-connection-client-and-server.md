---
title: 多连接的客户端 / 服务器程序

tags: 
  - sockets
categories: 
  - 💻 工作
  - 🐍Python
  - 网络编程
date: 2020-10-07 11:16:53
permalink: /pages/18ef28/
---

下面两节中，我们将使用 selectors 模块中的 selector 对象来创建一个可以同时处理多个请求的客户端和服务端

## 多连接的服务端

首先，我们来看眼多连接服务端程序的代码，`multiconn-server.py`。这是开始建立监听 socket 部分

```python
import selectors
sel = selectors.DefaultSelector()
# ...
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print('listening on', (host, port))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)
```

这个程序和之前打印程序服务端最大的不同是使用了 `lsock.setblocking(False)` 配置 socket 为非阻塞模式，这个 socket 的调用将不在是阻塞的。当它和 `sel.select()` 一起使用的时候（下面会提到），我们就可以等待 socket 就绪事件，然后执行读写操作

`sel.register()` 使用 `sel.select()` 为你感兴趣的事件注册 socket 监控，对于监听 socket，我们希望使用 `selectors.EVENT_READ` 读取到事件

`data` 用来存储任何你 socket 中想存的数据，当 `select()` 返回的时候它也会返回。我们将使用 `data` 来跟踪 socket 上发送或者接收的东西

下面就是事件循环：

```python
import selectors
sel = selectors.DefaultSelector()

# ...

while True:
    events = sel.select(timeout=None)
    for key, mask in events:
        if key.data is None:
            accept_wrapper(key.fileobj)
        else:
            service_connection(key, mask)
```

`sel.select(timeout=None)` 调用会阻塞直到 socket I/O 就绪。它返回一个 (key, events) 元组，每个 socket 都有一个。key 就是一个包含 `fileobj` 属性的具名元组。`key.fileobj` 是一个 socket 对象，`mask` 表示一个操作就绪的事件掩码

如果 `key.data` 为空，我们就可以知道它来自于监听 socket，我们需要调用 `accept()` 方法来授受连接请求。我们将使用一个 `accept()` 包装函数来获取新的 socket 对象并注册到 `selector` 上，我们马上就会看到

如果 `key.data` 不为空，我们就可以知道它是一个被接受的客户端 socket，我们需要为它服务，接着 `service_connection()` 会传入 `key` 和 `mask` 参数并调用，这包含了所有我们需要在 socket 上操作的东西

让我们一起来看看 `accept_wrapper()` 方法做了什么：

```python
def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print('accepted connection from', addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)
```

由于监听 socket 被注册到了 `selectors.EVENT_READ` 上，它现在就能被读取，我们调用 `sock.accept()` 后立即再立即调 `conn.setblocking(False)` 来让 socket 进入非阻塞模式

请记住，这是这个版本服务器程序的主要目标，因为我们不希望它被阻塞。如果被阻塞，那么整个服务器在返回前都处于挂起状态。这意味着其它 socket 处于等待状态，这是一种 **非常严重的** 谁都不想见到的服务被挂起的状态

接着我们使用了 `types.SimpleNamespace` 类创建了一个对象用来保存我们想要的 socket 和数据，由于我们得知道客户端连接什么时候可以写入或者读取，下面两个事件都会被用到：

```python
events = selectors.EVENT_READ | selectors.EVENT_WRITE
```

事件掩码、socket 和数据对象都会被传入 `sel.register()`

现在让我们来看下，当客户端 socket 就绪的时候连接请求是如何使用 `service_connection()` 来处理的

```python
def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            data.outb += recv_data
        else:
            print('closing connection to', data.addr)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print('echoing', repr(data.outb), 'to', data.addr)
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]
```

这就是多连接服务端的核心部分，`key` 就是从调用 `select()` 方法返回的一个具名元组，它包含了 socket 对象「fileobj」和数据对象。`mask` 包含了就绪的事件

如果 socket 就绪而且可以被读取，`mask & selectors.EVENT_READ` 就为真，`sock.recv()` 会被调用。所有读取到的数据都会被追加到 `data.outb` 里面。随后被发送出去

注意 `else:` 语句，如果没有收到任何数据：

```python
if recv_data:
    data.outb += recv_data
else:
    print('closing connection to', data.addr)
    sel.unregister(sock)
    sock.close()
```

这表示客户端关闭了它的 socket 连接，这时服务端也应该关闭自己的连接。不过别忘了先调用 `sel.unregister()` 来撤销 `select()` 的监控

当 socket 就绪而且可以被读取的时候，对于正常的 socket 应该一直是这种状态，任何接收并被 `data.outb` 存储的数据都将使用 `sock.send()` 方法打印出来。发送出去的字节随后就会被从缓冲中删除

```python
data.outb = data.outb[sent:]
```

## 多连接的客户端

现在让我们一起来看看多连接的客户端程序，`multiconn-client.py`，它和服务端很相似，不一样的是它没有监听连接请求，它以调用 `start_connections()` 开始初始化连接：

```python
messages = [b'Message 1 from client.', b'Message 2 from client.']


def start_connections(host, port, num_conns):
    server_addr = (host, port)
    for i in range(0, num_conns):
        connid = i + 1
        print('starting connection', connid, 'to', server_addr)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(server_addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        data = types.SimpleNamespace(connid=connid,
                                     msg_total=sum(len(m) for m in messages),
                                     recv_total=0,
                                     messages=list(messages),
                                     outb=b'')
        sel.register(sock, events, data=data)
```

`num_conns` 参数是从命令行读取的，表示为服务器建立多少个链接。就像服务端程序一样，每个 socket 都设置成了非阻塞模式

由于 `connect()` 方法会立即触发一个 `BlockingIOError` 异常，所以我们使用 `connect_ex()` 方法取代它。`connect_ex()` 会返回一个错误指示 `errno.EINPROGRESS`，不像 `connect()` 方法直接在进程中返回异常。一旦连接结束，socket 就可以进行读写并且通过 `select()` 方法返回

socket 建立完成后，我们将使用 `types.SimpleNamespace` 类创建想会传送的数据。由于每个连接请求都会调用 `socket.send()`，发送到服务端的消息得使用 `list(messages)` 方法转换成列表结构。所有你想了解的东西，包括客户端将要发送的、已发送的、已接收的消息以及消息的总字节数都存储在 `data` 对象中

让我们再来看看 `service_connection()`。基本上和服务端一样：

```bash
def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            print('received', repr(recv_data), 'from connection', data.connid)
            data.recv_total += len(recv_data)
        if not recv_data or data.recv_total == data.msg_total:
            print('closing connection', data.connid)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if not data.outb and data.messages:
            data.outb = data.messages.pop(0)
        if data.outb:
            print('sending', repr(data.outb), 'to connection', data.connid)
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]
```

有一个不同的地方，客户端会跟踪从服务器接收的字节数，根据结果来决定是否关闭 socket 连接，服务端检测到客户端关闭则会同样的关闭服务端的连接

## 运行多连接的客户端和服务端程序

现在让我们把 `multiconn-server.py` 和 `multiconn-client.py` 两个程序跑起来。他们都使用了命令行参数，如果不指定参数可以看到参数调用的方法：

服务端程序，传入主机和端口号

```bash
$ ./multiconn-server.py
usage: ./multiconn-server.py <host> <port>
```

客户端程序，传入启动服务端程序时同样的主机和端口号以及连接数量

```bash
$ ./multiconn-client.py
usage: ./multiconn-client.py <host> <port> <num_connections>
```

下面就是服务端程序运行起来在 65432 端口上监听回环地址的输出：

```bash
$ ./multiconn-server.py 127.0.0.1 65432
listening on ('127.0.0.1', 65432)
accepted connection from ('127.0.0.1', 61354)
accepted connection from ('127.0.0.1', 61355)
echoing b'Message 1 from client.Message 2 from client.' to ('127.0.0.1', 61354)
echoing b'Message 1 from client.Message 2 from client.' to ('127.0.0.1', 61355)
closing connection to ('127.0.0.1', 61354)
closing connection to ('127.0.0.1', 61355)
```

下面是客户端，它创建了两个连接请求到上面的服务端：

```bash
$ ./multiconn-client.py 127.0.0.1 65432 2
starting connection 1 to ('127.0.0.1', 65432)
starting connection 2 to ('127.0.0.1', 65432)
sending b'Message 1 from client.' to connection 1
sending b'Message 2 from client.' to connection 1
sending b'Message 1 from client.' to connection 2
sending b'Message 2 from client.' to connection 2
received b'Message 1 from client.Message 2 from client.' from connection 1
closing connection 1
received b'Message 1 from client.Message 2 from client.' from connection 2
closing connection 2
```

