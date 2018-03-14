# Prime Number Sieve
# http://inventwithpython.com/hacking (BSD Licensed)

import math

# 判断是否是质数
# 质数：大于1且因数只有1和它本身的整数
# 使用除法判断
def isPrime(num):
    # Returns True if num is a prime number, otherwise False.

    # Note: Generally, isPrime() is slower than primeSieve().

    # all numbers less than 2 are not prime
    if num < 2:
        return False

    # see if num is divisible by any number up to the square root of num
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

# 埃拉托色尼筛选算法，比上面的算法更快算出是否是质数
# 它可以算出sieveSize以内的质数列表
# 算法：把1标记为非质数，然后把所有2的倍数（除2本身）标记为非质数，3的倍数标记为
# 非质数...一直算到8，大于7.071（50的平方根）就可以算出50以内的所有质数
def primeSieve(sieveSize):
    # Returns a list of prime numbers calculated using
    # the Sieve of Eratosthenes algorithm.

    sieve = [True] * sieveSize
    sieve[0] = False  # zero and one are not prime numbers
    sieve[1] = False

    # create the sieve
    for i in range(2, int(math.sqrt(sieveSize)) + 1):
        pointer = i * 2
        while pointer < sieveSize:
            sieve[pointer] = False
            pointer += i

    # compile the list of primes
    primes = []
    for i in range(sieveSize):
        if sieve[i] == True:
            primes.append(i)

    return primes
