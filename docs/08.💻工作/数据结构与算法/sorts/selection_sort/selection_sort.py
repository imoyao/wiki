#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/5/13 18:33

import pathlib
import sys

util_p = pathlib.Path('../..').resolve()

sys.path.append(str(util_p))
from util import utils


def selection_sort(unsorted_collection):
    """
    选择排序

    如何找到一个数组中最小的元素呢？先取出序列中的首个元素（index=0）,然后循环序列，如果后面的元素中有比该元素更小的，则新元素取而代之；否则，则为该元素。
    对于剩下的序列（即未排序的序列），重复上面的操作，直至遍历整个序列。

    :param unsorted_collection: 未排序的序列，其中元素必须是可比较的。
    :return:
    """
    count = 0
    length = len(unsorted_collection)
    for i in range(length - 1):
        least = i  # 第一次循环，直接拿第一个作为基准去和剩余的元素进行比较
        for k in range(i + 1, length):
            if unsorted_collection[k] < unsorted_collection[least]:  # 如果发现原以为最小的比剩余序列中元素大（此处为顺排，如果逆序，应为大于）
                count += 1
                least = k       # 则指定最小的为新发现的元素（此处是索引重新赋值）
        # 交换位置
        unsorted_collection[least], unsorted_collection[i] = unsorted_collection[i], unsorted_collection[least]
    print(f'It takes {count} times.')
    return unsorted_collection


if __name__ == '__main__':
    unsorted_li = utils.rand_list()
    print('Before sorted:', unsorted_li)
    print('After sorted:', selection_sort(unsorted_li))
