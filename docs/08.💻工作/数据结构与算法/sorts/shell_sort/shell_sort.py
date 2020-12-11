#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/5/13 18:33

import pathlib
import sys

util_p = pathlib.Path('../..').resolve()

sys.path.append(str(util_p))
from util import utils


def shell_sort(unsorted_collection):
    """
    希尔排序
    它以插入排序为基础，将原来要排序的列表划分为一些子列表，再对每一个子列表执行插入排序，从而实现对插入排序性能的改进。
    划分子列的特定方法是希尔排序的关键。我们并不是将原始列表分成含有连续元素的子列，而是确定一个划分列表的增量'i'，
    这个i更准确地说，是划分的间隔。然后把每间隔为 i 的所有元素选出来组成子列表。
    :param unsorted_collection:待排序序列
    :return:排序后序列
    """
    gaps = [701, 301, 132, 57, 23, 10, 4, 1]        # 进行分割的步长列表
    for gap in gaps:
        i = gap
        # ----------------------此处为插入排序实现
        while i < len(unsorted_collection):
            temp = unsorted_collection[i]
            j = i
            while j >= gap and unsorted_collection[j-gap] > temp:
                unsorted_collection[j] = unsorted_collection[j-gap]
                j -= gap
            # -----------------
            unsorted_collection[j] = temp
            i += 1
    return unsorted_collection


if __name__ == '__main__':
    unsorted_li = utils.rand_list(100)
    print('Before sorted:', unsorted_li)
    print('After sorted:', shell_sort(unsorted_li))
