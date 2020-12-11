---
title: 如何理解 cookie、session 与 token
tags: 
  - Web
  - cookie
  - session
categories: 
  - 💻 工作
  - 👨‍💻Web
  - 其他
date: 2019-06-18 14:06:27
permalink: /pages/de1e30/
---
## Cookie 的机制

Cookie 是浏览器（User Agent）访问一些网站后，这些网站存放在客户端的一组数据，用于使网站等跟踪用户，实现用户自定义功能。

Cookie 的 Domain 和 Path 属性标识了这个 Cookie 是哪一个网站发送给浏览器的；Cookie 的 Expires 属性标识了 Cookie 的有 效时间，当 Cookie 的有效时间过了之后，这些数据就被自动删除了。

如果不设置过期时间，则表示这个 Cookie 生命周期为浏览器会话期间，只要关闭浏览器窗口，Cookie 就消失了。这种生命期为浏览会话期的 Cookie 被称为会话 Cookie。会话 Cookie 一般不保存在硬盘上而是保存在内存里。如果设置了过期时间，浏览器就会把 Cookie 保存到硬盘 上，关闭后再次打开浏览器，这些 Cookie 依然有效直到超过设定的过期时间。存储在硬盘上的 Cookie 可以在不同的浏览器进程间共享，比如两个 IE 窗 口。而对于保存在内存的 Cookie，不同的浏览器有不同的处理方式。

## Session 的机制

Session 是存放在服务器端的类似于 HashTable 结构（每一种 Web 开发技术的实现可能不一样，下文直接称之为 HashTable）来存放用户数据，当浏览器第一次发送请求时，服务器自动生成了一个 HashTable 和一个 Session ID 用来唯一标识这个 HashTable，并将其通过响应发送到浏览器。当浏览器第二次发送请求，会将前一次服务器响应中的 Session ID 放在请求中一并发送到服务器上，服务器从请求中提取出 Session ID，并和保存的所有 Session ID 进行对比，找到这个用户对应的 HashTable。

一般情况下，服务器会在一定时间内（默认 20 分钟）保存这个 HashTable，过了时间限制，就会销毁这个 HashTable。在销毁之前，程序员可以将用户的一些数据以 Key 和 Value 的形式暂时存放在这个 HashTable 中。当然，也有使用数据库将这个 HashTable 序列化后保存起来的，这样的好处是没了时间的限制，坏处是随着时间的增加，这个数据库会急速膨胀，特别是访问量增加的时候。一般还是采取前一种方式，以减轻服务器压力。
### 存放
客户端一般只存放 session_id 用于标识，真正的数据保存在服务端，如：disk、DB 等。

## token
token 也称作令牌，由 uid+time+sign[+固定参数]
token 的认证方式类似于临时的证书签名, 并且是一种服务端无状态的认证方式, 非常适合于 REST API 的场景. 所谓无状态就是服务端并不会保存身份认证相关的数据。

### 构成
- uid: 用户唯一身份标识
- time: 当前时间的时间戳
- sign: 签名, 使用 hash/encrypt 压缩成定长的十六进制字符串，以防止第三方恶意拼接
- 固定参数(可选): 将一些常用的固定参数加入到 token 中是为了避免重复查库

### 存放
token 在客户端一般存放于 localStorage，cookie，或 sessionStorage 中。在服务器一般存于数据库中。

## 参考阅读
[彻底弄懂 session，cookie，token](https://segmentfault.com/a/1190000017831088)
[token 与 sessionId 的区别——学习笔记](https://segmentfault.com/a/1190000015881055)
[彻底理解 cookie，session，token](https://www.liangzl.com/get-article-detail-16019.html)
[HTTP 是一个无状态的协议。这句话里的无状态是什么意思？](https://www.zhihu.com/question/23202402)
