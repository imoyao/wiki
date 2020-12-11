#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/6/10 18:34


from Queue.queue import Queue


def hot_potato(name_lists, num):  # TODO:待验证
    """
    假设拿着土豆的孩子位于队首，当开始传递土豆时，模拟器会将那个孩子从队首移出队列然后立即让他从队尾进入队列。所有在他前面的人都
    轮过一遍后才会再次轮到他传土豆。每经过'num'次出队入队的过程后，站在队首的孩子就会永久离开队列，游戏将在新的圆圈中继续进行。
    这个过程会一直持续到只有一个名字剩下（即队列大小为 1 时）。
    :param name_lists: 玩游戏的人员名称
    :param num: 计数的出列标志
    :return:
    """
    sq = Queue()
    for user in name_lists:  # 全部入队
        sq.enqueue(user)

    while sq.size() > 1:  # 最后剩下一个元素
        for i in range(num):
            sq.enqueue(sq.dequeue())  # 计数过的元素，重新插入队尾，继续新一轮的计数

        sq.dequeue()  # 每次计数完成，该元素出队
    return sq.dequeue()  # 弹出元素名称


if __name__ == '__main__':
    print(hot_potato(["Bill", "David", "Susan", "Jane", "Kent", "Brad"], 7))
