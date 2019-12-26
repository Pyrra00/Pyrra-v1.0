import time
import string
import hashlib
ready = False
start = time.time()
chars = list(string.printable)[:95]
base = len(chars)
n = 0
hashmethod = 0
password = ""
solved = False
quit = ""
while ready != True:
    password = input("Enter a valid MD5 or SHA-1 hash:")

    if len(password) == 32:
        ready = True
    elif len(password) == 40:
        ready = True
        hashmethod = 2
    else:
        pass


def numberToBase(n, b):  # converts number N base 10 to a list of digits base b
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]


# check edge cases like empty, or 0
if password == '':
    print('Your password is empty')
    solved = True

# begin systematically checking passwords
while not solved:
    lst = numberToBase(n, base)
    word = ''
    for x in lst:
        word += str(chars[x])
    if hashmethod == 2:
        hashedGuess = hashlib.sha1(bytes(word, 'utf-8')).hexdigest()

    else:
        hashedGuess = hashlib.md5(bytes(word, 'utf-8')).hexdigest()
        print("[+] Trying password: " + word)
    if password == hashedGuess:
        solved = True
        print('-Stats-')
        print('Pass: ' + word)
        print('Attempts: ' + str(n))
        print('time: ' + str((time.time() - start)) + ' sec')
        while quit != "QUIT":
            quit = input('Type <QUIT> to quit: ')
    else:
        n += 1