#!/usr/bin/python3

import re

file_path = "file1"

with open(file_path, "r") as file:
    lines = file.readlines()

pattern = r'x === (\d+) && y === (\d+)'

#x_positions = []
#y_positions = []
new_arr = []
for line in lines:
    matches = re.findall(pattern, line)
    for match in matches:
        #x_positions.append(int(match[0]))
        #y_positions.append(int(match[1]))
        x = (int(match[0]))
        y = (int(match[1]))
        new_arr.append([x, y])

#[for i in x_positions new_arr.append(i), for j in y_positons new_arr.append(j)]

print(new_arr)

#print(len(x_positions))

print()
print(len(new_arr))

#print(len(y_positions))
