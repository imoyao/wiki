#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/5/13 18:33

import pathlib
import sys

util_p = pathlib.Path('../..').resolve()

sys.path.append(str(util_p))
from util import utils


def bubble_sort(unsorted_collection):
    """
    冒泡排序
    注意：swapped 标志是为了优化冒泡循环的，减少循环次数，不加标志也是可以的
    :param unsorted_collection:待排序序列
    :return:排序后序列
    """
    length = len(unsorted_collection)
    for i in range(length - 1):  # 第一次比较 n-1 个元素，因为比较总是和下一个元素比较，所以第一次循环的最后一次比较会“捎带”上最后一个元素
        swapped = False
        for j in range(length - 1 - i):  # 每一次冒泡，倒数i位的顺序肯定是已经排好顺序的,所以比较的长度变为 len-1-i
            if unsorted_collection[j] > unsorted_collection[j + 1]:  # 如果前面的大于后面的，则交换位置（上浮）
                swapped = True
                unsorted_collection[j], unsorted_collection[j + 1] = unsorted_collection[j + 1], unsorted_collection[j]
        if not swapped:  # 如果在某一次排序中，没有发生元素交换，则说明已经排好，break 使其在已知列表排好的情况下提前结束
            break
    return unsorted_collection


if __name__ == '__main__':
    unsorted_li = utils.rand_list(100)
    print('Before sorted:', unsorted_li)
    print('After sorted:', bubble_sort(unsorted_li))
