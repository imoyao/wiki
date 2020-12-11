
def partition(vi,wi,start,end):
    if start>=end:
        return
    i,j=start,end
    base_v = vi[i]
    base_w = wi[i]
    base =vi[i]/wi[i]
    while i < j:
        while i<j and base > vi[i]/wi[i]:
            i+=1
        # 如找到,则把第i个元素赋值给第个元素j,此时表中i,j个元素相等
        vi[j] = vi[i]
        vi[j] = vi[i]
        while i<j and base < vi[j]/wi[j]:
            j-=1
        # 如找到,则把第j个元素赋值给第个元素i
        vi[i] = vi[j]
        wi[i] = wi[j]
    vi[j] = base_v
    wi[j] = base_w
    # 递归前后半区
    partition(vi,wi, start, i - 1)
    partition(vi,wi, j + 1, end)




def bag(n,w,vi,wi):
    sum_v = 0
    sum_w = 0
