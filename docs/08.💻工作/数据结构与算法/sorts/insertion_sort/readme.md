---
title: 插入排序

tags: 
  - 算法
categories: 
  - 💻 工作
  - 数据结构与算法
  - sorts
  - insertion_sort
date: 2020-05-25 18:21:46
permalink: /pages/f39c49/
---

## 概念

插入排序（Insertion Sort）是一种简单直观的排序算法。它的工作原理是通过构建有序序列，对于未排序数据，在已排序序列中从后向前扫描，找到相应位置并插入。插入排序在实现上，通常采用`in-place`排序（即只需用到 `O(1)` 的额外空间的排序），因而在从后向前扫描过程中，需要反复把已排序元素逐步向后挪位，为最新元素提供插入空间。

## 图示

![插入排序算法](/images/Insertion_sort_animation.gif)

![插入排序实例](/images/Insertion-sort-example.gif)

## 复杂度

平均时间复杂度：`O(n^2)`
