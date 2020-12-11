class Node(object):
    def __init__(self,data):
        self.data = data
        self.left_child = None
        self.right_child = None

    def gatherAttrs(self):
        return ",".join("{}={}"
                        .format(k, getattr(self, k))
                        for k in self.__dict__.keys())
        # attrs = []
        # for k in self.__dict__.keys():
        #     item = "{}={}".format(k, getattr(self, k))
        #     attrs.append(item)
        # return attrs
        # for k in self.__dict__.keys():
        #     attrs.append(str(k) + "=" + str(self.__dict__[k]))
        # return ",".join(attrs) if len(attrs) else 'no attr'

    def __str__(self):
        return "[{}:{}]".format(self.__class__.__name__, self.gatherAttrs())




class BinaryTree(object):
    def __init__(self,root=None):
        self.root = root

    def find_min(self):
        if self.root is None:
            return None
        tmp = self.root
        while tmp.left_child is not None:
            tmp = tmp.left_child
        return tmp.data

    def find_max(self):
        if self.root is None:
            return None

        tmp = self.root
        while tmp.left_child is not None:
            tmp = tmp.left_child
        return tmp.data




    def insert(self,data):
        if self.root is None:
            self.root = Node(data)
        tmp = self.root
        while True:
            if tmp.data == data:
                print("data already exists!")
            elif tmp.data > data:
                if tmp.left_child is None:
                    tmp.left_child = Node(data)
                    return
                tmp = tmp.left_child
            else:
                if tmp.right_child is None:
                    tmp.right_child = Node(data)
                    return
                tmp = tmp.right_child

    def search(self,data):
        if self.root is None:
            return None
        current = self.root
        while current is not None:
            if current.data == data:
                return current
            current = current.left_child if current.data > data else current.right_child
        return current  #not find


    # 如果待删除的节点是叶子节点，那么可以立即被删除
    # 如果节点只有一个儿子，则将此节点parent的指针指向此节点的儿子，然后删除节点
    # 如果节点有两个儿子，则将其右子树的最小数据代替此节点的数据，并将其右子树的最小数据删除
    # 想一想中序遍历输出的序列删除某一个值得操作

    def delete_node(self,root,data):
        if root is None:
            return None
        if root.data < data:
           root.right_child = self.delete_node(root.right_child,data)
        elif root.data > data:
            root.left_child =  self.delete_node(root.left_child,data)
        else:  # equal
            if root.left_child and root.right_child:
                root.data  = self.find_min_by_root(root.right_child) # 找到后继结点
                root.right_child = self.delete_node(root.right_child, root.data)  # 实际删除的是这个后继结点
            else:
                if root.left_child is None:
                    root = root.right_child
                elif root.right_child is None:
                    root = root.left_child     ###如果两个都为空 已经包含在这里了
        return root



    def delete(self,data):
        self.delete_node(self.root,data)



def find_max_by_root(root):
    if root is None:
        return None
    tmp = root
    while tmp.right_child is not None:
        tmp = tmp.right_child
    return tmp

def find_min_by_root(root):
    if root is None:
        return None
    tmp = root
    while tmp.left_child is not None:
        tmp = tmp.left_child
    return tmp

# 规则中我们是从下往上找，但实际代码中是不允许我们这么操作的（由于我们没有父亲指针），
# 我们可以在寻找对应val节点的过程中从上向下找，并且过程中记录下parent节点和firstRParent节点
# （最后一次在查找路径中出现右拐的节点）。
# 实现如下：
def find_pre_node(root,data):
    if root is None:
        return None
    parent = None
    firstRParent = None
    node = None

    while root:
        if root.data == data:
            node = root
            break
        parent = root
        if root.data > data:
            root = root.left_child
        else:
            firstRParent = root
            root = root.right_child

    if node is None:
        return None
    if node.left_child is not None:
        return find_max_by_root(node.left_child)

    if (parent is None) or (parent is not None and firstRParent is None):
        return None  #没有前驱节点的情况
    if node == parent.right_child:# 没有左子树 是其父节点的右边节点
        return parent
    else:   #//没有左子树 是其父节点的左边节点
        return firstRParent


# 同样，求后继节点我们不能从底向上找，也是从上向下找，
# 首先是找到对应val值的节点，顺便把其的parent节点和firstlParent节点（最后一次在查找路径中出现左拐的节点）。
# 实现如下：

def find_post_node(root,data):
    if root is None:
        return None
    parent = None
    firstLParent = None
    node = None
    while root:
        if root.data == data:
            node = root
            break
        parent = root
        if root.data < data:
            root = root.right_child
        else:
            firstLParent = root
            root = root.left_child

    if node is None:
        return None

    if node.right_child is not None:
        return find_min_by_root(root)

    if parent is None or (parent is not None and firstLParent is None):
        return None
    if parent.left_child == node:
        return parent
    else:
        return firstLParent




def pre_order_traverse(root):
    if root is None:
        return
    print(root.data)
    pre_order_traverse(root.left_child)
    pre_order_traverse(root.right_child)

def in_order_traverse(root):
    if root is None:
        return
    in_order_traverse(root.left_child)
    print(root.data,end=" ")
    in_order_traverse(root.right_child)

def post_order_traverse(root):
    if root is None:
        return
    post_order_traverse(root.left_child)
    post_order_traverse(root.right_child)
    print(root.data)

def post_order_traverse_no_recursion(root):  #借助栈的逆序输出就是后序
    if root is None:
        return
    stack = [root]
    result = []
    while len(stack) > 0:
        current = stack.pop()
        result.append(current.data)
        if current.left_child is not None:
            stack.append(current.left_child)
        if current.right_child is not None:
            stack.append(current.right_child)
    print(result[::-1])



def level_traverse(root):
    if not root:
        return
    print("Print binary tree by level")
    queue = [root]
    last = root
    level = 1
    print("Level " + str(level) + ':', end=' ')
    while queue:
        root = queue.pop(0)
        print(root.data, end=' ')
        if root.left_child:
            nlast = root.left_child
            queue.append(root.left_child)
        if root.right_child:
            nlast = root.right_child
            queue.append(root.right_child)
        if root == last and queue:
            last = nlast
            print()
            level += 1
            print("Level " + str(level) + ":", end=' ')


def level_traverse_v2(root):
    if root is None:
        return None
    result = []
    queue = [root]
    while queue:
        number_level = len(queue)
        level_result = []
        while number_level:
            current = queue.pop(0)
            level_result.append(current.data)
            if current.left_child:
                queue.append(current.left_child)
            if current.right_child:
                queue.append(current.right_child)
            number_level -= 1    ####注意自己写while循环总是忘记对变量-1或+1
        result.append(level_result)
    return result





if __name__ == '__main__':
    BinaryTree = BinaryTree(Node(7))
    BinaryTree.insert(4)
    BinaryTree.insert(11)
    BinaryTree.insert(3)
    BinaryTree.insert(5)
    BinaryTree.insert(9)
    print(level_traverse_v2(BinaryTree.root))