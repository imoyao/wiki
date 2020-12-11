---
title: 归并排序

tags: 
  - 算法
categories: 
  - 💻 工作
  - 数据结构与算法
  - sorts
  - merge_sort
date: 2020-05-25 18:21:46
permalink: /pages/d6be88/
---

## 概念

归并排序（Merge sort 或 mergesort），是创建在归并操作上的一种有效的排序算法。该算法是采用分治法（Divide and Conquer）的一个非常典型的应用，且各层分治递归可以同时进行。

## 原理

归并排序算法的运作如下：

**分解**：将待排序的 `n` 个元素分成各包含 `n/2` 个元素的子序列
**解决**：使用归并排序递归排序两个子序列
**合并**：合并两个已经排序的子序列以产生已排序的答案

## 图示

![归并排序算法](/images/Merge_sort_animation.gif)

![归并排序实例](/images/Merge-sort-example.gif)

## 复杂度

平均时间复杂度：`O(nlogn)`
