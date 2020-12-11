class Bag(object):
    def __init__(self,n,capacity,weights,values):
        self.capacity = capacity
        self.weights = weights
        self.values = values
        self.n = n



    def get_max_value(self):
        sum_v = [[0 for i in range(self.capacity+1)] for j in range(self.n+1)]

        for i in range(1,self.n+1):
            for j in range(1,self.capacity+1):
                # sum_v[i][0]=0
                #  sum_v[0][j]=0
                sum_v[i][j] = sum_v[i - 1][j]
                if j-self.weights[i-1]>=0 :  ##这里是i-1，因为weights数组是从0开始的
                    # 这个判断是背包总容量够放当前物体
                    sum_v[i][j] = max(sum_v[i-1][j-self.weights[i-1]]+self.values[i-1], sum_v[i-1][j])
        self.print_matrix(sum_v)
        return sum_v[self.n-1][self.n-1]

    def print_matrix(self,matrix):
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                print(matrix[i][j],end=" ")
            print()

def bag(n, c, w, v):
    """
    测试数据：
    n = 6  物品的数量，
    c = 10 书包能承受的重量，
    w = [2, 2, 3, 1, 5, 2] 每个物品的重量，
    v = [2, 3, 1, 5, 4, 3] 每个物品的价值
    """
    # 置零，表示初始状态
    value = [[0 for j in range(c + 1)] for i in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, c + 1):
            value[i][j] = value[i - 1][j]
            # 背包总容量够放当前物体，遍历前一个状态考虑是否置换
            if j >= w[i - 1] and value[i][j] < value[i - 1][j - w[i - 1]] + v[i - 1]:
                value[i][j] = value[i - 1][j - w[i - 1]] + v[i - 1]
    for x in value:
        print(x)
    return value


if __name__ == '__main__':
    num = 5
    capacity = 10
    weight_list = [2, 2, 6, 5, 4]
    value_list = [6, 3, 5, 4, 6]
    q = Bag(num, capacity, weight_list, value_list)
    q.get_max_value()
    bag(num,capacity,weight_list,value_list)