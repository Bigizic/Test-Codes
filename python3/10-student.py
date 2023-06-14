#!/usr/bin/python3
"""A class Student that defines a student by:

Parameters:
    first_name (str)
    last_name (str)
    age (int)

Raises:
    void

Return:
    a dictionary representation of a Student instance
"""
import sys


class Student:
    """Class Implementation
    """

    def __init__(self, first_name, last_name, age):
        """Constructor
        """
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.input_list = []

    def read_input(self):
        """A function that reads user input and stores it in a list
        """
        while (1):
            read_input = input("Enter attribute or (q to quit): ")
            if read_input == 'q':
                break
            self.input_list.append(user_input)

    def to_json(self, attrs=None):
        attrs = self.input_list
        """Description:
            this function checks if the attrs is a list, if yes it return
            items as a dict, by iterating through attrs and storing each
            iterated element in items then it check if the class (self)
            has an attribute in the items variable if yes it proced to
            get the attribute of that particular item from the class
            Student(self) and store it in items then it returns the
            attribute
            """
        if attrs is not None and type(attrs) is list:
            return {items: getattr(self, items) for items in attrs
                    if hasattr(self, items)}
        else:
            return vars(self)

first_name = input("Enter first name: ")
last_name = input("Enter last name: ")
age = int(input("Enter age: "))
my_object = Student(first_name, last_name, age)
my_object.read_input()

print(my_object.to_json())
