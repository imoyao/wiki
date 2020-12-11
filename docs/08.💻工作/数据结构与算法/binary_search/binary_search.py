#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/5/13 18:33

import pathlib
import sys

util_p = pathlib.Path('..').resolve()
sys.path.append(str(util_p))

from util import utils


@utils.show_time
def binary_search_while(sorted_lists, wanted_item):
    """
    二分查找( while 实现)
    :param sorted_lists: 有序数组
    :param wanted_item: 需要查找的元素
    :return: 索引值 / None
    """
    low_index = 0
    high_index = len(sorted_lists) - 1  # 查找范围为整个有序列表的索引
    _count = 0
    while low_index <= high_index:
        _count += 1
        mid_index = (low_index + high_index) // 2  # py3中的整数除
        mid_item = sorted_lists[mid_index]
        if mid_item == wanted_item:
            print(f'It takes {_count} times to find {wanted_item} in index {mid_index}')
            return mid_index
        elif mid_item < wanted_item:  # 如果猜的值小于目的值，则在大端继续查找
            low_index = mid_index + 1
        else:
            high_index = mid_index - 1  # 否则，在小端查找
    return None  # 没有找到，返回None


count = 0


@utils.show_time
def binary_search_recurse(sorted_lists, wanted_item, low_index=0, high_index=None):
    """
    二分查找(递归实现)
    :param sorted_lists: 有序序列
    :param wanted_item: 查找的元素
    :param low_index: 开始位索引
    :param high_index: 结束位索引
    :return: 索引值 / None
    """
    global count

    if high_index is None:
        high_index = len(sorted_lists) - 1

    mid_index = (low_index + high_index) // 2
    mid_item = sorted_lists[mid_index]
    count += 1
    if low_index > high_index:  # 注意此处，表示遍历序列，也没找到
        return None
    if mid_item < wanted_item:  # 猜值小于目的值，则在大端继续查找
        return binary_search_recurse(sorted_lists, wanted_item, mid_index + 1, high_index)
    elif mid_item > wanted_item:  # 小端查找
        return binary_search_recurse(sorted_lists, wanted_item, low_index, mid_index - 1)

    print(f'It takes {count} times to find {wanted_item} in index {mid_index}')
    return mid_index


if __name__ == '__main__':
    print(binary_search_while(list(range(100)), 0))
    print(binary_search_recurse(list(range(100)), 0, 0, len(list(range(100))) - 1))
