# Simple Substitution Cipher Hacker
# http://inventwithpython.com/hacking (BSD Licensed)

import copy
import os
import pprint
from Toolslib import pyperclip
import re

from 简单替代加密法 import simpleSubCipher, makeWordPatterns

if not os.path.exists('wordPatterns.py'):
    makeWordPatterns.main()  # create the wordPatterns.py file
import wordPatterns

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
nonLettersOrSpacePattern = re.compile('[^A-Z\s]')  # 无字母或空格正则


def main():
    message = 'Sy l nlx sr pyyacao l ylwj eiswi upar lulsxrj isr sxrjsxwjr, ia esmm rwctjsxsza sj wmpramh, lxo txmarr jia aqsoaxwa sr pqaceiamnsxu, ia esmm caytra jp famsaqa sj. Sy, px jia pjiac ilxo, ia sr pyyacao rpnajisxu eiswi lyypcor l calrpx ypc lwjsxu sx lwwpcolxwa jp isr sxrjsxwjr, ia esmm lwwabj sj aqax px jia rmsuijarj aqsoaxwa. Jia pcsusx py nhjir sr agbmlsxao sx jisr elh. -Facjclxo Ctrramm'

    # Determine the possible valid ciphertext translations.
    print('Hacking...')
    letterMapping = hackSimpleSub(message)

    # Display the results to the user.
    print('Mapping:')
    pprint.pprint(letterMapping)
    print()
    print('Original ciphertext:')
    print(message)
    print()
    print('Copying hacked message to clipboard:')
    hackedMessage = decryptWithCipherletterMapping(message, letterMapping)
    pyperclip.copy(hackedMessage)
    print(hackedMessage)


# 获取一个空的字母映射表
def getBlankCipherletterMapping():
    # Returns a dictionary value that is a blank cipherletter mapping.
    return {'A': [], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [], 'H': [], 'I': [], 'J': [], 'K': [], 'L': [],
            'M': [], 'N': [], 'O': [], 'P': [], 'Q': [], 'R': [], 'S': [], 'T': [], 'U': [], 'V': [], 'W': [], 'X': [],
            'Y': [], 'Z': []}


# 添加字母到映射表
def addLettersToMapping(letterMapping, cipherword, candidate):
    # The letterMapping parameter is a "cipherletter mapping" dictionary
    # value that the return value of this function starts as a copy of.
    # The cipherword parameter is a string value of the ciphertext word.
    # The candidate parameter is a possible English word that the
    # cipherword could decrypt to.

    # This function adds the letters of the candidate as potential
    # decryption letters for the cipherletters in the cipherletter
    # mapping.

    letterMapping = copy.deepcopy(letterMapping)
    for i in range(len(cipherword)):
        if candidate[i] not in letterMapping[cipherword[i]]:
            letterMapping[cipherword[i]].append(candidate[i])
    return letterMapping


# 求两个密字映射的交集
def intersectMappings(mapA, mapB):
    # To intersect two maps, create a blank map, and then add only the
    # potential decryption letters if they exist in BOTH maps.
    intersectedMapping = getBlankCipherletterMapping()
    for letter in LETTERS:

        # An empty list means "any letter is possible". In this case just
        # copy the other map entirely.
        # 空跟不空的交集是不空的内容，区别数学意义上的交集
        if mapA[letter] == []:
            intersectedMapping[letter] = copy.deepcopy(mapB[letter])
        elif mapB[letter] == []:
            intersectedMapping[letter] = copy.deepcopy(mapA[letter])
        else:
            # If a letter in mapA[letter] exists in mapB[letter], add
            # that letter to intersectedMapping[letter].
            for mappedLetter in mapA[letter]:
                if mappedLetter in mapB[letter]:
                    intersectedMapping[letter].append(mappedLetter)

    return intersectedMapping


# 从密字映射移除已经破译的字母
# 思路：
# （1）先用solvedLetters保存映射表中只存在一个字母映射的字母，表示已经破译的字母
# （2）遍历26个字母的映射表，遍历solvedLetters中的字母跟里面多个映射字母比对，如果
# 存在跟solvedLetters中字母一样的字母进行删除，逐渐缩小映射的范围
# （3）最后当把缩小范围的字母映射长度变为1时，表示该字母找到破译的字母了

# 详细过程Debug模式中可以看的很清楚，letterMapping中字母的映射表会逐渐变短
def removeSolvedLettersFromMapping(letterMapping):
    # Cipher letters in the mapping that map to only one letter are
    # "solved" and can be removed from the other letters.
    # For example, if 'A' maps to potential letters ['M', 'N'], and 'B'
    # maps to ['N'], then we know that 'B' must map to 'N', so we can
    # remove 'N' from the list of what 'A' could map to. So 'A' then maps
    # to ['M']. Note that now that 'A' maps to only one letter, we can
    # remove 'M' from the list of letters for every other
    # letter. (This is why there is a loop that keeps reducing the map.)
    letterMapping = copy.deepcopy(letterMapping)
    loopAgain = True
    while loopAgain:
        # First assume that we will not loop again:
        loopAgain = False

        # solvedLetters will be a list of uppercase letters that have one
        # and only one possible mapping in letterMapping
        solvedLetters = []
        for cipherletter in LETTERS:
            # 如果当前字母的映射结果只有一个，就认为已经破译了，从列表中移除
            if len(letterMapping[cipherletter]) == 1:
                solvedLetters.append(letterMapping[cipherletter][0])

        # If a letter is solved, than it cannot possibly be a potential
        # decryption letter for a different ciphertext letter, so we
        # should remove it from those other lists.
        for cipherletter in LETTERS:
            # 把映射的字母数不为1的字母中移除已经破译的字母
            for s in solvedLetters:
                if len(letterMapping[cipherletter]) != 1 and s in letterMapping[cipherletter]:
                    letterMapping[cipherletter].remove(s)
                    # 如果移除后长度变成1，可以认为该字母找到破译的字母了
                    if len(letterMapping[cipherletter]) == 1:
                        # A new letter is now solved, so loop again.
                        loopAgain = True
    return letterMapping


# 获取密字映射表
def hackSimpleSub(message):
    intersectedMap = getBlankCipherletterMapping()  # 生成空的密字映射表
    cipherwordList = nonLettersOrSpacePattern.sub('', message.upper()).split()  # 分割成单词列表
    # 循环遍历每个单词，添加字母映射
    for cipherword in cipherwordList:
        # Get a new cipherletter mapping for each ciphertext word.
        newMap = getBlankCipherletterMapping()

        wordPattern = makeWordPatterns.getWordPattern(cipherword)  # 获取单词模式
        # 判断该单词模式是否在单词模式列表中
        if wordPattern not in wordPatterns.allPatterns:
            continue  # This word was not in our dictionary, so continue.

        # Add the letters of each candidate to the mapping.
        for candidate in wordPatterns.allPatterns[wordPattern]:
            newMap = addLettersToMapping(newMap, cipherword, candidate)  # 添加字母到映射表

        # Intersect the new mapping with the existing intersected mapping.
        intersectedMap = intersectMappings(intersectedMap, newMap)  # 两个映射表的交集

    # Remove any solved letters from the other lists.
    return removeSolvedLettersFromMapping(intersectedMap)


# 使用密字映射表创建密钥
def decryptWithCipherletterMapping(ciphertext, letterMapping):
    # Return a string of the ciphertext decrypted with the letter mapping,
    # with any ambiguous decrypted letters replaced with an _ underscore.

    # First create a simple sub key from the letterMapping mapping.
    key = ['x'] * len(LETTERS)
    for cipherletter in LETTERS:
        if len(letterMapping[cipherletter]) == 1:
            # If there's only one letter, add it to the key.
            keyIndex = LETTERS.find(letterMapping[cipherletter][0])
            key[keyIndex] = cipherletter
        else:
            ciphertext = ciphertext.replace(cipherletter.lower(), '_')
            ciphertext = ciphertext.replace(cipherletter.upper(), '_')
    key = ''.join(key)

    # With the key we've created, decrypt the ciphertext.
    return simpleSubCipher.decryptMessage(key, ciphertext)


if __name__ == '__main__':
    main()
