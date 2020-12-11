bestV = 0
ans = []
wi = []
vi = []
w = 0
n = 0


def bag(n_, w_, vi_, wi_):
    global bestV, wi, vi, w, n
    wi = wi_
    vi = vi_
    w = w_
    n = n_
    backtrace(0, 0, 0,[])



def backtrace(i, sum_v, sum_w, result):
    global bestV,ans
    if i >= n:
        if bestV<sum_v:
            bestV = sum_v
            print(result)
            ans = result
        return
    if wi[i] + sum_w > w:
        backtrace(i+1,sum_v,sum_w,result)
    else:
        result.append(i)
        backtrace(i + 1, sum_v+vi[i], sum_w+wi[i], result.copy())
        result.pop()
        backtrace(i+1,sum_v,sum_w,result)

if __name__ == '__main__':
    num = 5
    capacity = 10
    weight_list = [2, 2, 6, 5, 4]
    value_list = [6, 3, 5, 4, 6]
    bag(num, capacity, value_list,weight_list)
    print(ans)
    print(bestV)