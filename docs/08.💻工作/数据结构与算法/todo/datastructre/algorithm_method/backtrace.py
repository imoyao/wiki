#
# void backtrack(int t)          //t表示递归深度，即当前扩展节点在解空间树的深度
# {
#     if ( t > n ) output(x);    //n控制递归深度，如果算法已经搜索到叶节点，记录输出可行解X
#     else
#     {
#         for(int i = f(n,t) ; i <= g(n,t) ; i++)  //在深度t，i从未搜索过得起始编号到终止编号
#         {
#             x[t] = h(i);       //查看i这个点的值是否满足题目的要求
#             if( constraint(t) && bound(t))
#                 backtrack(t+1)
#        //constraint（t）为true表示在当前扩展节点处x[1:t]的取值满足问题的约束条件；
#        //bound(t)为true表示当前扩展节点取值没有使目标函数越界；
#        //为true表示还需要进一步的搜索子树，否则减去子树。
#          }
#     }
# }
