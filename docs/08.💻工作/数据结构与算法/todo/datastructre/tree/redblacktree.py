import random


class RBNode:
    def __init__(self, val, color="R"):
        self.val = val
        self.color = color
        self.left = None
        self.right = None
        self.parent = None

    def is_black_node(self):
        return self.color == "B"

    def set_black_node(self):
        self.color = "B"

    def set_red_node(self):
        self.color = "R"

    def print(self):
        if self.left:
            self.left.print()
        print(self.val)
        if self.right:
            self.right.print()


class RBTree:
    """
        红黑树 五大特征
        性质一：节点是红色或者是黑色；
        性质二：根节点是黑色；
        性质三：每个叶节点（NIL或空节点）是黑色；
        性质四：每个红色节点的两个子节点都是黑色的（也就是说不存在两个连续的红色节点）；
        性质五：从任一节点到其没个叶节点的所有路径都包含相同数目的黑色节点
    """
    def __init__(self):
        self.root = None
        self.action = ""
    """
             * 左旋示意图：对节点x进行左旋
             *     parent               parent
             *    /                       /
             *   node                   right
             *  / \                     / \
             * ln  right   ----->     node  ry
             *    / \                 / \
             *   ly ry               ln ly
             * 左旋做了三件事：
             * 1. 将right的左子节点ly赋给node的右子节点,并将node赋给right左子节点ly的父节点(ly非空时)
             * 2. 将right的左子节点设为node，将node的父节点设为right
             * 3. 将node的父节点parent(非空时)赋给right的父节点，同时更新parent的子节点为right(左或右)
            :param node: 要左旋的节点
            :return:
    """
    def left_rotate(self,node):
        parent = node.parent
        right = node.right

        ### 维护每个parent

        # 把右子子点的左子点节   赋给右节点 步骤1
        # if right.left is not None:
        #     node.right = right.left
        node.right = right.left
        if node.right:
            node.right.parent = node

        # 把 node 变成基右子节点的左子节点 步骤2
        right.left = node
        node.parent = right

        # 右子节点的父节点更并行为原来节点的父节点。 步骤3
        right.parent = parent
        if not parent:        ###这一段维护parent的子节点
            self.root = right
        else:
            if parent.left == node :
                parent.left=right
            else:
                parent.right =right


    def right_rotate(self, node):
        print("right rotate", node.val)
        '''
         * 旋示意图：对节点y进行右旋
         *        parent           parent
         *       /                   /
         *      node                left
         *     /    \               / \
         *    left  ry   ----->   ln  node
         *   / \                     / \
         * ln  rn                   rn ry
         * 右旋做了三件事：
         * 1. 将left的右子节点rn赋给node的左子节点,并将node赋给rn右子节点的父节点(left右子节点非空时)
         * 2. 将left的右子节点设为node，将node的父节点设为left
         * 3. 将node的父节点parent(非空时)赋给left的父节点，同时更新parent的子节点为left(左或右)
        :param node:
        :return:
        '''
        parent = node.parent
        left = node.left

        node.left = left.right
        if node.left:     ##赋值之后存在的话换他的parent
            node.left.parent = node


        left.right = node
        node.parent = left

        left.parent = parent
        if not parent:
            self.root =left
        else:
            if parent.left == node:
                parent.left = left
            else:
                parent.right = left




    def add_node(self, node):
        self.action = 'inser node {}'.format(node.val)
        self.insert_node(node)
        self.check_node(node)
        pass

    def insert_node(self, node):
        """
        二叉树添加往红黑树中添加一个红色节点
        :param node:
        :return:
        """
        if not self.root:
            self.root = node
            return

        cur = self.root
        while cur:

            if cur.val < node.val:
                if not cur.right:
                    node.parent = cur
                    cur.right = node
                    break
                cur = cur.right
                continue

            if cur.val > node.val:
                if not cur.left:
                    node.parent = cur
                    cur.left = node
                    break
                cur = cur.left
        pass

    """

    插入操作
    
    如果插入的是黑色节点时，则每次插入都会违返性质5, 都需要重新调整树。
    所以 插入时，每次都认为只插入红色节点。这样调整的次数就会减少很多。 倡但是还是有要调整的情况

    1 如果插入的是根节点，则直接把点变成黑色（性质二）， 示例中插入第一个节点5的情况
    
    2 如果插入的节点的父节点是黑色节点，则不调整颜色。 示例中 插入点10 就属于这种情况
    
    3 如果插入节点的父节点的红色节点（违反性质四），且父节点的兄弟节点为红色节点。 
        1) 把父节点及其兄弟节点变成黑色，把组父节点变成红色（使其不违反性质五）。 
        2)再检查祖父节点是否违反红黑树的性质（一或四）
    
    4 如果插入节点的父节点的红色节点（违反性质四），且父节点的兄弟节点为黑色节点。  
      并且插入节点，父节点，及祖父节点同侧。 
      即node = node.parent.left && node.parent = node.parent.parent.left(同左则), 
      或 node = node.parent.right && node.parent = node.parent.parent.right（同右则）

      处理方法： 把父节点变成黑色节点，把祖父节点变成红色节点， 同时反向旋转祖父节点（同左则，右旋； 同右则左旋）
      不需要再检查祖父节点，一定满足红黑树定义
    
    5 如果插入节点的父节点的红色节点（违反性质四），且父节点的兄弟节点为黑色节点。  
      并且插入节点，父节点，及祖父节点不同则。

      处理方法：旋转父节点，使期变成同则（第4种情况）， 再根据情况4来处理。
      
   
    """

    def check_node(self, node):
        """
        检查节点及父节是否破坏了
        性质二：根节点是黑色；
        性质四：每个红色节点的两个子节点都是黑色的（也就是说不存在两个连续的红色节点）；
        @@ 性质四可反向理解为， 节点和其父点必定不能够同时为红色节点
        :param node:
        :return:
        """
        # 如果是父节点直接设置成黑色节点，退出
        if self.root == node or self.root == node.parent:
            self.root.set_black_node()
            print("set black ", node.val)
            return

        # 如果父节点是黑色节点，直接退出
        if node.parent.is_black_node():
            return

        # 如果父节点的兄弟节点也是红色节点,
        grand = node.parent.parent
        if not grand:
            self.check_node(node.parent)
            return
        if grand.left and grand.left.is_red_node() and grand.right and grand.right.is_red_node():
            grand.left.set_black_node()
            grand.right.set_black_node()
            grand.set_red_node()
            self.check_node(grand)
            return

        # 如果父节点的兄弟节点也是黑色节点,
        # node node.parent node.parent.parent 不同边
        parent = node.parent
        if parent.left == node and grand.right == node.parent:
            self.right_rotate(node.parent)
            self.check_node(parent)
            return
        if parent.right == node and grand.left == node.parent:
            parent = node.parent
            self.left_rotate(node.parent)
            self.check_node(parent)
            return

        # node node.parent node.parent.parent 同边
        parent.set_black_node()
        grand.set_red_node()
        if parent.left == node and grand.left == node.parent:
            self.right_rotate(grand)
            return
        if parent.right == node and grand.right == node.parent:
            self.left_rotate(grand)
            return




    def check_delete_node(self, node):
        '''
        检查删除节点node
        :param node:
        :return:
        '''
        if self.root == node or node.is_red_node():
            return

        node_is_left = node.parent.left == node
        brother = node.parent.right if node_is_left else node.parent.left
        #brother 必不为空
        if brother.is_red_node():
            # 如果是黑色节点，兄弟节点是红色节点， 旋转父节点： 把你节点变成黑色，兄弟节点变黑色。 重新平衡
            if node_is_left:
                self.left_rotate(node.parent)
            else:
                self.right_rotate(node.parent)
            node.parent.set_red_node()
            brother.set_black_node()
            print("check node delete more ")
            #再重新检查当前节点
            self.check_delete_node(node)
            return

        all_none = not brother.left and not brother.right
        all_black = brother.left and brother.right and brother.left.is_black_node() and brother.right.is_black_node()
        if all_none or all_black:
            brother.set_red_node()
            if node.parent.is_red_node():
                node.parent.set_black_node()
                return
            self.check_delete_node(node.parent)
            return

        #检查兄弟节点的同则子节点存丰并且是是红色节点
        brother_same_right_red = node_is_left and brother.right and brother.right.is_red_node()
        brother_same_left_red = not node_is_left and brother.left and brother.left.is_red_node()
        if brother_same_right_red or brother_same_left_red:

            if node.parent.is_red_node():
                brother.set_red_node()
            else:
                brother.set_black_node()
            node.parent.set_black_node()

            if brother_same_right_red:
                brother.right.set_black_node()
                self.left_rotate(node.parent)
            else:
                brother.left.set_black_node()
                self.right_rotate(node.parent)

            return

        # 检查兄弟节点的异则子节点存丰并且是是红色节点
        brother_diff_right_red = not node_is_left and brother.right and brother.right.is_red_node()
        brother_diff_left_red = node_is_left and brother.left and brother.left.is_red_node()
        if brother_diff_right_red or brother_diff_left_red:
            brother.set_red_node()
            if brother_diff_right_red:
                brother.right.set_black_node()
                self.left_rotate(brother)
            else:
                brother.left.set_black_node()
                self.right_rotate(brother)

            self.check_delete_node(node)
            return





    def pre_delete_node(self, node):
        '''
        删除前检查，返回最终要删除的点
        :param node:
        :return:
        '''
        post_node = self.get_post_node(node)
        if post_node:
            node.val, post_node.val = post_node.val, node.val
            return self.pre_delete_node(post_node)
        pre_node = self.get_pre_node(node)
        if pre_node:
            pre_node.val, node.val = node.val, pre_node.val
            return self.pre_delete_node(pre_node)
        #没有前驱节点，也没有后续节点
        return node

    def get_pre_node(self, node):
        '''
        获取 前驱 节点 ， 树中比node小的节点中最大的值
        :param node:
        :return:
        '''
        if not node.left:
            return None
        pre_node = node.left
        while pre_node.right:
            pre_node = pre_node.right
        return pre_node

    def get_post_node(self, node):
        '''
        获取后续节点:
        :param node:树中比node大的节点中最小的值
        :return:
        '''
        if not node.right:
            return None
        post_node = node.right
        while post_node.left:
            post_node = post_node.left
        return post_node

    def get_node(self, val):
        '''
        根据值查询节点信息
        :param val:
        :return:
        '''
        if not self.root:
            return None
        node = self.root
        while node:
            if node.val == val:
                break
            if node.val > val:
                node = node.left
                # continue
            else:
                node = node.right
        return node

    def delete_node(self, val):

        node = self.get_node(val)
        if not node:
            print("node error {}".format(val))
            return
        # 获取真正要删除的节点
        node = self.pre_delete_node(node)
        # node 节点必不为空，且子节点也都为空
        self.check_delete_node(node)
        #真正删除要删除的节点
        self.real_delete_node(node)
        pass


    def real_delete_node(self, node):
        '''
        真正删除节点函数  ，要维护父节点的left/right节点
        :param node:
        :return:
        '''
        if self.root == node:
            self.root = None
            return
        if node.parent.left == node:
            node.parent.left = None
            return
        if node.parent.right == node:
            node.parent.right = None
        return

if __name__ == '__main__':

    tree = RBTree()
    data = list(range(1, 20))
    random.shuffle(data)
    print(data)
    for i in data:
        tree.add_node(RBNode(i))

    random.shuffle(data)
    for i in data:
        print("delete ", i)
        tree.delete_node(i)
    pass