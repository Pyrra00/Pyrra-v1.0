from hashlib import md5
from time import time
from string import printable
from itertools import product, count


def passwords(encoding):
    chars = [c.encode(encoding) for c in printable]
    for length in count(start=1):
        for pwd in product(chars, repeat=length):
            yield b''.join(pwd)


def crack(search_hash, encoding):
    for pwd in passwords(encoding):
        if md5(pwd).digest() == search_hash:
            return pwd.decode(encoding)


if __name__ == "__main__":
    encoding = 'ascii'  # utf-8 for unicode support
    password = input('password: ')
    password_hash = md5(password.encode(encoding)).digest()

    start = time()
    cracked = crack(password_hash, encoding)
    end = time()
    print(f"Password cracked: {cracked}")
    print(f"Time: {end - start} seconds.")