"""

169. Majority Element

Given an array of size n, find the majority element. The majority element is the element that appears more than ⌊ n/2 ⌋ times.

You may assume that the array is non-empty and the majority element always exist in the array.

Example 1:

Input: [3,2,3]
Output: 3
Example 2:

Input: [2,2,1,1,1,2,2]
Output: 2


"""
from typing import List


class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        my_dict = {}
        for x in nums:

            if x in my_dict.keys():
                my_dict[x] += 1
            else:
                my_dict[x] = 1

        my_dict = sorted(my_dict.items(), key=lambda x: x[1], reverse=True)  #按照值排序
        return my_dict[0][0]


