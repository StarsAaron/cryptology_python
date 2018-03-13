# Affine Cipher Hacker
# http://inventwithpython.com/hacking (BSD Licensed)

from 仿射加密法 import affineCipher, cryptomath, detectEnglish

SILENT_MODE = False


def main():
    # 密文
    my_message = """U&'<3dJ^Gjx'-3^MS'Sj0jxuj'G3'%j'<mMMjS'g{GjMMg9j{G'g"'gG'<3^MS'Sj<jguj'm'P^dm{'g{G3'%jMgjug{9'GPmG'gG'-m0'P^dm{LU'5&Mm{'_^xg{9"""

    hacked_message = hack_affine(my_message)

    if hacked_message is not None:
        print(hacked_message)
    else:
        print('Failed to hack encryption.')


def hack_affine(message):
    print('Hacking...')

    # Python programs can be stopped at any time by pressing Ctrl-C (on
    # Windows) or Ctrl-D (on Mac and Linux)
    print('(Press Ctrl-C or Ctrl-D to quit at any time.)')

    # brute-force by looping through every possible key
    for key in range(len(affineCipher.SYMBOLS) ** 2):  # **指数运算符
        key_a = affineCipher.getKeyParts(key)[0]
        if cryptomath.gcd(key_a, len(affineCipher.SYMBOLS)) != 1:
            continue

        decrypted_text = affineCipher.decryptMessage(key, message)
        if not SILENT_MODE:
            print('Tried Key %s... (%s)' % (key, decrypted_text[:40]))

        if detectEnglish.isEnglish(decrypted_text):
            # Check with the user if the decrypted key has been found.
            print()
            print('Possible encryption hack:')
            print('Key: %s' % (key))
            print('Decrypted message: ' + decrypted_text[:200])
            print()
            print('Enter D for done, or just press Enter to continue hacking:')
            response = input('> ')

            if response.strip().upper().startswith('D'):
                return decrypted_text
    return None


# If affineHacker.py is run (instead of imported as a module) call
# the main() function.
if __name__ == '__main__':
    main()
