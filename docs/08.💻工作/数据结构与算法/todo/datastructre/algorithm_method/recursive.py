
def fibonacci(n,result):
	if n==0:
		return 0
	if n == 1:
		return 1
	if result[n] == -1:
		result[n] = fibonacci(n-1,result)+fibonacci(n-2,result)
	return result[n]
if __name__ == '__main__':
    n= 10
    result = [-1 for i in range(n+1)]
    print(fibonacci(n,result))
    print(result)