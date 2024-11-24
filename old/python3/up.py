#!/usr/bin/env python3

def sn(n: int):
    if n < 5:
        return 0

    count = 0
    a_list = []
    for i in range(1, n + 1):
        a_list.append(i**2)
    b_list = a_list

    for i in range(n):
        count += itera(n, i, a_list, b_list)
    return count

def itera(n: int, i: int, a_list: list, b_list: list):
    count = 0
    for it in range(0, n):
        if a_list[i] + b_list[it] in b_list:
            count += 1
    return count

print(sn(10))
print(sn(5))
print(sn(100))
# lesser than 5
for i in range(6):
    print(sn(i))

