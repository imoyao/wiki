def minPathSum(matrix):
    m = len(matrix)
    n=len(matrix[0])
    path = [[0 for i in range(n)] for j in range(m)]
    path[0][0] = matrix[0][0]
    for i in range(1,m):
        path[i][0] = path[i-1][0]+matrix[i][0]
    for j in range(1,n):
        path[0][j] = path[0][j-1]+matrix[0][j]

    for i in range(1,m):
        for j in range(1,n):
            path[i][j] = matrix[i][j]+ min(path[i-1][j],path[i][j-1])
    for x in path:
        print(x)
    return path[m-1][n-1]

def minPathSum_recursive(matrix):
    m = len(matrix)
    n=len(matrix[0])
    path = [[0 for i in range(n)] for j in range(m)]
    path[0][0] = matrix[0][0]
    for i in range(1,m):
        path[i][0] = path[i-1][0]+matrix[i][0]
    for j in range(1,n):
        path[0][j] = path[0][j-1]+matrix[0][j]

    for i in range(1,m):
        for j in range(1,n):
            path[i][j] = matrix[i][j]+ min(path[i-1][j],path[i][j-1])
    for x in path:
        print(x)
    return path[m-1][n-1]

if __name__ == '__main__':
    matrix =[[1,2,5],[3,2,1]]
    minPathSum_recursive(matrix)