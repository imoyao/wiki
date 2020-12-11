"""

用数组实现一个顺序队列
用链表实现一个链式队列
实现一个循环队列

"""

class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        return self.items.pop(0)

    def empty(self):
        return self.size() == 0

    def size(self):
        return len(self.items)

class Node(object):
    def __init__(self,value):
        self.data = value
        self.next = None

class LinkedList:
    # 初始化，头结点为空
    def __init__(self):
        self.head = None

    # 添加节点，添加的新节点作为新的头结点
    def prepend(self, data):
        new_node = Node(data)
        new_node.next= self.head
        self.head = new_node


    def remove_first(self):
        tmp = self.head.data
        self.head = self.head.next
        return tmp

    def remove_last(self):
        tmp = self.head.data
        self.head = self.head.next
        return tmp

    def get_first(self):
        return self.head.data

    # 判断链表是否为空
    def is_empty(self):
        return not self.head

    # 返回链表长度
    def size(self):
        count = 0
        counting = self.head  # 从头结点开始计数
        while counting is not None:
            count += 1
            counting = counting.next
        return count




# 为了提供对队列的链表结构两端的快速访问，队列还有指向两端的外部指针。下图是一个包含了4个项的链表队列。
class LinkedQueue:
    def __init__(self):
        self.items = LinkedList()
        self.front = None
        self.rear = None
        self.size = 0

    def enqueue(self, item):
        """Adds item to the rear of the queue."""
        newNode = Node(item)
        if self.empty():
            self.front = newNode
        else:
            self.rear.next = newNode
        self.rear = newNode
        self.size += 1


    def dequeue(self):
        """
                Removes and returns the item at the front of the queue.
                Precondition: the queue is not empty.
                Raises: KeyError if the queue is empty.
                Postcondition: the front item is removed from the queue."""
        if self.empty():
            raise KeyError("The queue is empty.")
        oldItem = self.front.data
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        self.size -= 1
        return oldItem

    def empty(self):
        return self.size == 0

    def size(self):
        return self.size



class SqQueue(object):
    def __init__(self, maxsize):
        self.queue = [None] * maxsize
        self.maxsize = maxsize
        self.front = 0
        self.rear = 0

    # 返回当前队列的长度
    def QueueLength(self):
        return (self.rear - self.front + self.maxsize) % self.maxsize

    # 如果队列未满，则在队尾插入元素，时间复杂度O(1)
    def EnQueue(self, data):
        if (self.rear + 1) % self.maxsize == self.front:
            print("The queue is full!")
        else:
            self.queue[self.rear] = data
            self.rear = (self.rear + 1) % self.maxsize

    # 如果队列不为空，则删除队头的元素,时间复杂度O(1)
    def DeQueue(self):
        if self.rear == self.front:
            print("The queue is empty!")
        else:
            data = self.queue[self.front]
            self.queue[self.front] = None
            self.front = (self.front + 1) % self.maxsize
            return data

    # 输出队列中的元素
    def ShowQueue(self):
        for i in range(self.maxsize):
            print(self.queue[i],end=',')
        print(' ')