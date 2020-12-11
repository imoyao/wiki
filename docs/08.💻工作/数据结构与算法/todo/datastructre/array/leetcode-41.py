"""

41. First Missing Positive

Given an unsorted integer array, find the smallest missing positive integer.

Example 1:

Input: [1,2,0]
Output: 3
Example 2:

Input: [3,4,-1,1]
Output: 2
Example 3:

Input: [7,8,9,11,12]
Output: 1
Note:

Your algorithm should run in O(n) time and uses constant extra space.
"""
from typing import List


# 思路：抽屉原理，缺的一定是1-n+1中的一个 tricky
class Solution:
    def firstMissingPositive(self, nums: List[int]) -> int:
        n = len(nums)
        for i in range(n):
            if nums[i] <= 0: nums[i] = n + 2
        for i in range(n):
            if abs(nums[i]) <= n:
                curr = abs(nums[i]) - 1
                nums[curr] = -abs(nums[curr])
        for i in range(n):
            if nums[i] > 0: return i + 1
        return n + 1

