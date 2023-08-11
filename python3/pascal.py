#!/usr/bin/python3
"""A representation of the pascal triangle
"""


def pascal_triangle():
    """implementation
    """
    prompt = input("Enter a number: ")

    if (prompt == "exit"):
        return
    prompt = int(prompt)
    result = []

    for r in range(prompt):
        temp = []
        for c in range(r + 1):
            if c == 0 or c == r:
                temp.append(1)
            else:
                temp.append(result[r-1][c-1] + result[r-1][c])
        result.append(temp)

    for i in range(prompt):
        for j in range(prompt - i - 1):
            print(" ", end="")
        for j in range(i + 1):
            print(result[i][j], end=" ")
        print()

pascal_triangle()
