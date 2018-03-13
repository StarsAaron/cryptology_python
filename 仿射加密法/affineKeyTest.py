# This program proves that the keyspace of the affine cipher is limited
# to len(SYMBOLS) ^ 2.

from 仿射加密法 import affineCipher, cryptomath
# 测试密钥是否具有“回调”效果，密钥A与密钥B同样具有“回调”效果，受限于符号集的大小
# 3与98加密效果一样 ，2和97一样等
message = 'Make things as simple as possible, but not simpler.'
for keyA in range(2, 100):
    key = keyA * len(affineCipher.SYMBOLS) + 1  # 密钥B统一为1

    if cryptomath.gcd(keyA, len(affineCipher.SYMBOLS)) == 1:
        print(keyA, affineCipher.encryptMessage(key, message))
