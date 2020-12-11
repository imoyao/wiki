class Graph(object):
    def __init__(self,v,graph=None):
        if graph :
            self.graph = graph
        else:
            self.graph = [[0 for i in range(v)] for j in range(v)]
        self.v = v


    def add_edge(self,begin,end,weight):
        if begin>self.v-1 or end < 0:
            print("edge error")
            return
        self.graph[begin][end] = weight

    def show_graph_matrix(self):

        for i in range(self.v):
            for j in range(self.v):
                print(self.graph[i][j],end=" ")
            print()

    def dfs_recursive(self,now,visited,result):  # 深度优先搜索
        visited[now] = True
        result.append(now)
        for i in range(self.v):
            if self.graph[now][i] != 0 and not visited[i]:
                self.dfs_recursive(i,visited,result)


    def dfs(self,start):
        visited = [False for i in range(self.v)]
        result = []
        self.dfs_recursive(start, visited, result)
        for i in range(self.v):
            if not visited[i]:
                self.dfs_recursive(i,visited,result)
        return result

    # 初始化栈
    # 输出起始顶点，起始顶点改为“已访问”标志，将起始顶点进栈
    # 重复以下操作直至栈空：
    # 去栈顶元素顶点，找到未被访问的邻接结点W
    # 输出W，W改为“已访问”，将W进栈
    # 否则当前顶点退栈

    def dfs_by_stack(self,start):
        visited = [False for i in range(self.v)]

        stack = [start]
        result = []
        while stack:
            # print(stack)
            now = stack.pop()
            if not visited[now]:
                result.append(now)
                visited[now] = True
                for i in range(self.v):
                    if (not visited[i]) and self.graph[now][i]!= 0:#若当前邻接顶点没有被访问过，则进行访问并入栈
                        stack.append(i)
                    else:
                        # 若当前邻接顶点已经被访问过，则沿边找到下一个顶点
                        pass
                # 若某一方向被访问完，则回溯寻找未被访问的顶点

        return  result


    def bfs(self,start):
        queue = [start]
        result = []
        visited = [False for i in range(self.v)]

        while queue:
            now = queue.pop(0)
            if not visited[now]:
                visited[now] = True
                result.append(now)
            for i in range(self.v):
                if self.graph[now][i]!= 0 and  visited[i] is False:
                    queue.append(i)
        return result


    def dijkstra(self,start):
        result = [0 for i in range(self.v)]
        # 源顶点到其余各顶点的初始路程

        dis = dict((i, float('inf')) for i in range(self.v))


        dis[v0] = 0
        return result

if __name__ == '__main__':

    matrix=[[0,0,1,1,1],[0,0,1,0,1],[1,1,0,0,1],[1,0,0,0,0],[1,1,1,0,0]]
    graph = Graph(5,matrix)

    # graph.add_edge(0,1,1)
    #
    # graph.add_edge(0, 1, 1)
    # graph.add_edge(0, 2, 1)
    # graph.add_edge(2, 3, 1)
    # graph.add_edge(3, 1, 1)
    graph.show_graph_matrix()
    print(graph.dfs(0))
    print(graph.dfs_by_stack(0))
    print(graph.bfs(0))
    print(graph.dijkstra(0))
