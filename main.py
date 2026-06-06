def factorial(n):
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

def n_choose_k(n, k):
    if k < 0 or k > n:
        return 0
    return factorial(n) // (factorial(k) * factorial(n - k))

print(factorial(5))