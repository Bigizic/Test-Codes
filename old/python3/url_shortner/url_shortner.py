#!/usr/bin/python3
"""Creates a url shortner using an algorithm and generating unque id
for the long url
"""


import hashlib


def base62_encode(hash_int):
    """Implementation of base62 encoding
    """
    chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    temp_list = []

    while hash_int > 0:
        hash_int, r = divmod(hash_int, 62)
        temp_list.append(chars[r])

    return ''.join(reversed(temp_list))


def url_shortner():
    """Creates algoorithm to use
    """

    url = input("Enter url: ")
    sha_hash = hashlib.sha256(url.encode()).hexdigest()
    hash_int = int(sha_hash, 16) # convert the hex hash to an integer
    short_code = base62_encode(hash_int)
    # print(short_code)
    result = short_code[:7]
    print(result)
    """if database has result:
        result = short_code[-7:]"""


if __name__ == '__main__':
    url_shortner()
