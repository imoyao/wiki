

#
# count = 1
#
# def queen(A, cur=0):
#     global count
#     if cur == len(A):
#         print("-----------",count,"---------")
#
#         print(A)
#         print()
#         count +=1
#         return
#     for col in range(len(A)):
#         A[cur], flag = col, True
#         for row in range(cur):
#             if A[row] == col or abs(col - A[row]) == cur - row:
#                 flag = False
#                 break
#         if flag:
#             queen(A, cur+1)

def check(board,row,col):
    i = 0
    while i < row:
        if abs(col-board[i]) in (0,abs(row-i)):
            return False
        i += 1
    return True

def EightQueen(board,row):
    blen = len(board)
    if row == blen:    # 来到不存在的第九行了
        printBoard(board)
        return True
    col = 0
    while col < blen:
        if check(board,row,col):
            board[row] = col
            if EightQueen(board,row+1):
                return True
        col += 1
    return False

def printBoard(board):
    '''为了更友好地展示结果 方便观察'''
    import sys
    for i,col in enumerate(board):
        sys.stdout.write('□ ' * col + '■ ' + '□ ' * (len(board) - 1 - col))
        print()

if __name__ == '__main__':

    # queen([None]*8)
    EightQueen([-1]*8,8)