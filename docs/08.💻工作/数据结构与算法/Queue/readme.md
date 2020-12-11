---
title: 队列

tags: 
  - 算法
categories: 
  - 💻 工作
  - 数据结构与算法
  - Queue
date: 2020-05-25 18:21:46
permalink: /pages/341bd2/
---

## 概念
队列，（queue），是*先进先出*（FIFO, First-In-First-Out）的线性表。在具体应用中通常用链表或者数组来实现。队列只允许在后端（称为 rear）进行插入操作，在前端（称为 front）进行删除操作。
![先进先出](/images/queue.png)

## 生活实例
- 车站排队购票
![春运排队](/images/queue-example.jpg)

## 操作
队列的操作方式和堆栈类似，唯一的区别在于队列只允许新数据在后端进行添加。  
- Queue()创建一个空队列对象，无需参数，返回空的队列；
- enqueue(item)将数据项添加到队尾，无返回值；
- dequeue()从队首移除数据项，无需参数，返回值为队首数据项；
- isEmpty()测试是否为空队列，无需参数，返回值为布尔值；
- size()返回队列中的数据项的个数，无需参数。

| 队列操作     | 队列中的内容 | 返回值 | 说明       |
| ---------------- | ------------------ | ------ | ------------ |
| q.isEmpty()      | []                 | True   | 是否为空 |
| q.enqueue(4)     | [4]                |        | 添加到队尾 |
| q.enqueue('dog') | ['dog',4]          |        |              |
| q.enqueue(True)  | [True,'dog',4]     |        |              |
| q.size()         | [True,'dog',4]     | 3      | 返回队列大小 |
| q.isEmpty()      | [True,'dog',4]     | False  |              |
| q.enqueue(8.4)   | [8.4,True,'dog',4] |        |              |
| q.dequeue()      | [8.4,True,'dog']   | 4      | 队首移除 |
| q.dequeue()      | [8.4,True]         | 'dog'  |              |
| q.size()         | [8.4,True]         | 2      |              |

## 更多
