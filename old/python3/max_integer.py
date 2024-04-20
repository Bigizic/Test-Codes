#!/usr/bin/python3


def max_int(my_list=[]):
    """
    Description: functiions that checks if a list only contains integers
    if the list is empty it returns None otherwise it gets the first number
    of the list, iterate through the list and check if the current number is
    greater than the first number if yes it updates the first number to the
    current number on the list, it continues to iterate through the whole list
    and check if the current number is greater than the first number. It then
    procced to return the index of the biggest number by iterating the list and
    checking if the current number is not equal to the biggest number in most cases
    it will return true until it meet the biggest number in the iteration, it keeps a
    count that keeps adding up if the biggest number is not equal to the current number
    in the list it prints the count as the count serves as the index of the biggest number
    """
    if my_list:
        first_int = my_list[0]
        count = 0
        for i in my_list:
            if isinstance(i, int):
                if i > first_int:
                    first_int = i
        for x in my_list:
            if first_int != x:
                count +=1
            else:
                break
        print("Maximum number is: {}, and the index is {}".format(first_int, count))

    return None

max_int([1, 900, 2, 13, 344, 5, -13, 3])
