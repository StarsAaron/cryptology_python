# RSA Key Generator
# http://inventwithpython.com/hacking (BSD Licensed)

import os
from Toolslib import rabinMiller拉宾米勒质数检测算法
import random
import sys

from RSA非对称加密 import cryptomath


def main():
    # create a public/private keypair with 1024 bit keys
    print('Making key files...')
    makeKeyFiles('al_sweigart', 1024)
    print('Key files made.')


# 生成RSA密钥对
def generateKey(keySize):
    # Creates a public/private key pair with keys that are keySize bits in
    # size. This function may take a while to run.

    # Step 1: Create two prime numbers, p and q. Calculate n = p * q.
    # 生成两个随机大质数，他们的积保存为n
    print('Generating p prime...')
    p = rabinMiller拉宾米勒质数检测算法.generateLargePrime(keySize)
    print('Generating q prime...')
    q = rabinMiller拉宾米勒质数检测算法.generateLargePrime(keySize)
    n = p * q

    # Step 2: Create a number e that is relatively prime to (p-1)*(q-1).
    # 获取一个随机的跟(p - 1) * (q - 1)互质的e
    print('Generating e that is relatively prime to (p-1)*(q-1)...')
    while True:
        # Keep trying random numbers for e until one is valid. 返回一个随机整数
        e = random.randrange(2 ** (keySize - 1), 2 ** (keySize))
        # 检查是否互质
        if cryptomath.gcd(e, (p - 1) * (q - 1)) == 1:
            break

    # Step 3: Calculate d, the mod inverse of e.找出e的模逆
    # 找出e的模逆d
    print('Calculating d that is mod inverse of e...')
    d = cryptomath.findModInverse(e, (p - 1) * (q - 1))

    # 每个密钥由两个数组成
    publicKey = (n, e)
    privateKey = (n, d)

    print('Public key:', publicKey)
    print('Private key:', privateKey)

    return (publicKey, privateKey)


# 生成密钥文件
def makeKeyFiles(name, key_size):
    # Creates two files 'x_pubkey.txt' and 'x_privkey.txt' (where x is the
    # value in name) with the the n,e and d,e integers written in them,
    # delimited by a comma.

    # Our safety check will prevent us from overwriting our old key files:
    if os.path.exists('%s_pubkey.txt' % name) or os.path.exists('%s_privkey.txt' % name):
        sys.exit(
            'WARNING: The file %s_pubkey.txt or %s_privkey.txt already exists! Use a different name or delete these files and re-run this program.' % (
            name, name))

    publicKey, privateKey = generateKey(key_size)

    print()
    print('The public key is a %s and a %s digit number.' % (len(str(publicKey[0])), len(str(publicKey[1]))))
    print('Writing public key to file %s_pubkey.txt...' % name)
    fo = open('%s_pubkey.txt' % name, 'w')
    # 文件内容：<密钥大小整数>,<n整数>,<e或d整数>
    fo.write('%s,%s,%s' % (key_size, publicKey[0], publicKey[1]))
    fo.close()

    print()
    print('The private key is a %s and a %s digit number.' % (len(str(publicKey[0])), len(str(publicKey[1]))))
    print('Writing private key to file %s_privkey.txt...' % name)
    fo = open('%s_privkey.txt' % name, 'w')
    fo.write('%s,%s,%s' % (key_size, privateKey[0], privateKey[1]))
    fo.close()


# If makeRsaKeys.py is run (instead of imported as a module) call
# the main() function.
if __name__ == '__main__':
    main()
