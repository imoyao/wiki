#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/10/28 18:15

# https://blog.csdn.net/xinxin957_/article/details/81915443
# https://blog.csdn.net/zzfightingy/article/details/86742755
class Node:
    """
    定义Node类，用于表示树上的节点
    """

    def __init__(self, data, left_tree=None, right_tree=None):
        """
        节点值、左子树、右子树
        :param data:
        :param left_tree:
        :param right_tree:
        """
        self.data = data
        self.left_subtree = left_tree
        self.right_subtree = right_tree


class BinTree:
    """
    定义二叉树类
    """

    def __init__(self, root=None):
        self.root = root

    def add_node(self, val):
        """
        添加元素
        :param val:
        :return:
        """
        new_node = Node(val)
        if self.root is None:
            self.root = new_node
        else:
            queue = list()
            queue.append(self.root)
            while queue:
                current = queue.pop(0)  # 从列表头部拿元素
                if current.left_subtree is None:
                    current.left_subtree = new_node
                    return
                elif current.right_subtree is None:
                    current.right_subtree = new_node
                    return
                else:
                    queue.append(current.left_subtree)
                    queue.append(current.right_subtree)

    def bfs_travel(self):
        """
        广度优先遍历
        :return:
        """
        if self.root is None:
            return
        else:
            queue = list()
            queue.append(self.root)
            while queue:
                current = queue.pop(0)
                print(current.data, end=' ')
                if current.left_subtree is not None:
                    queue.append(current.left_subtree)
                if current.right_subtree is not None:
                    queue.append(current.right_subtree)

    def dfs_travel_preorder(self, node):
        """
        深度优先前序遍历（递归实现）
        :param node:
        :return:
        """
        if node is None:
            return
        else:
            print(node.data, end=' ')
            self.dfs_travel_preorder(node.left_subtree)
            self.dfs_travel_preorder(node.right_subtree)

    def dfs_travel_inorder(self, node):
        """
        深度优先中序遍历（递归实现）
        :param node:
        :return:
        """
        if node is None:
            return
        else:
            self.dfs_travel_inorder(node.left_subtree)
            print(node.data, end=' ')
            self.dfs_travel_inorder(node.right_subtree)

    def dfs_travel_postorder(self, node):
        """
        深度优先后序遍历（递归实现）
        :param node:
        :return:
        """
        if node is None:
            return
        else:
            self.dfs_travel_postorder(node.left_subtree)
            self.dfs_travel_postorder(node.right_subtree)
            print(node.data, end=' ')


class BinTreeStack:
    """
    使用栈模拟二叉树
    栈：后进先出（LIFO）
    """

    def __init__(self, root=None):
        super().__init__(root)  # python3
        # super(BinTreeStack, self).__init__(root)  # python2
        self.root = root
        self.stack = []

    def make_tree(self, tree, val):
        if val is None:
            return
        else:
            tree.data = val
            tree.left_subtree = Node(val)
            self.make_tree(tree.left_subtree, val)
            tree.right_subtree = Node(val)
            self.make_tree(tree.right_subtree, val)

    def dfs_travel_stack_preorder(self, tree):
        """
        栈的方式前序遍历
        先把根节点入栈，然后左节点，最后右节点
        :return:
        """
        if self.root is None:
            return
        stack = []
        node = tree
        while node or stack:
            while node:
                print(node.data)
                stack.append(node)
                node = node.left_subtree
            node = stack.pop()
            node = node.right_subtree

    def dfs_travel_stack_inorder(self, tree):
        """
        以栈的方式中序遍历 左 -> 根 -> 右
        :param tree:
        :return:
        """
        if self.root is None:
            return
        stack = []
        node = tree
        while node or stack:
            stack.append(node)
            node = node.left_subtree
        node = stack.pop()
        print(node.data)
        node = node.right_subtree

    def dfs_travel_stack_postorder(self, tree):
        if self.root is None:
            return
        stack_1 = []
        stack_2 = []
        node = tree
        stack_1.append(node)
        while stack_1:
            node = stack_1.pop()
            if node.left_subtree:
                stack_1.append(node.left_subtree)
            if node.right_subtree:
                stack_1.append(node.right_subtree)
            stack_2.append(node)
        while stack_2:
            node = stack_2.pop()
            print(node.data)


if __name__ == '__main__':
    t = BinTree()
    for i in range(10):
        t.add_node(i)

    print('bfs_travel:')
    t.bfs_travel()
    print('\ndfs_travel_preorder:')
    t.dfs_travel_preorder(t.root)
    print('\ndfs_travel_inorder:')
    t.dfs_travel_inorder(t.root)
    print('\ndfs_travel_postorder:')
    t.dfs_travel_postorder(t.root)
    '''
    bfs_travel:
    0 1 2 3 4 5 6 7 8 9 
    dfs_travel_preorder:
    0 1 3 7 8 4 9 2 5 6 
    dfs_travel_inorder:
    7 3 8 1 9 4 0 5 2 6 
    dfs_travel_postorder:
    7 8 3 9 4 1 5 6 2 0 
    '''
    print('*' * 20, end='\n')
    # st = BinTreeStack()
    # for i in range(10):
    #     st.make_tree(st, i)
    # st.dfs_travel_stack_preorder(st)
    # # st.dfs_travel_stack_inorder(st.root)
