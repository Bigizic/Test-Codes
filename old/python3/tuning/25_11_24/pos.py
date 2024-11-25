#!/usr/bin/env python3

"""
solution
"""

class POS():

    def __init__(self):
        self.stack = []

    def push(self, value: int):
        """appends to stack
        """
        if value:
            self.stack.append(value)

    def pop(self):
        """Removes previous record and stores in the
        popped stack
        """
        new_stack = self.stack[:-1]
        self.stack = new_stack

    def double(self):
        """Gets the previous score then proceed to multiply it by 2
        i.e double the previous score
        """
        new_record = self.stack[-1] * 2
        self.push(new_record)

    def add(self):
        """sums up two prev records in the stack
        """
        self.push(self.stack[-1] + self.stack[-2])

    def get(self):
        return self.stack

    def add_all(self):
        res = 0
        for items in self.stack:
            res += items
        return res

    def negative_int(self, i: str):
        """
        changes a negative string like 
        "-3" to integer
        """
        if i[0] == '-':
            i = int(i[1:])
            self.push(i * -1)


def callPoints(ops) -> int:
    result = None

    try:
        op = POS()
        for i in ops:
            # not integer, probably ops[i]
            if i == "+":
                op.add()

            if i == "D":
                op.double()

            if i == "C":
                op.pop()

            if i.isdigit():
                op.push(int(i))

            # for negative integers
            if i[0] == '-':
                op.negative_int(i)

        result =  op.add_all()
        return result
    except Exception as e:
        print(e)

print(callPoints(["5", "2", "C", "D", "+"]))
print(callPoints(["1"]))
print(callPoints(["5", "-2", "4", "C", "D", "9", "+", "+"])) 
