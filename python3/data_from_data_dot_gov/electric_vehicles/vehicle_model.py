#!/usr/bin/python3
"""This module serves as a data scraper to get, create certain data
from the Electric_vehicle files
"""
import os
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class ElectricVehicleModel():
    """This class creates columns and their respective data types
    from the electric_vehicle_1.csv
    
    Args:
        __columns_dict - contains dictionary representation of the
        columns names and their data types
    """
    __columns_dict = {}

    def __init__(self):
        """creates instances to the path of the csv files
        assuming the csv scrapper has already been executed
        """
        self.file_1 = 'Electric_Vehicle_Population_Data_1.csv'
        self.file_2 = 'Electric_Vehicle_Population_Data_2.csv'

    def create_columns(self):
        """
        Creates columns from self.__columns_dict

        Returns:
            new_columns_dict - containing columns names and their
            data types
        """
        if self.__columns_dict:
            new_columns_dict = {}
            for cols, data_type in self.__columns_dict.items():
                clean_col = cols.replace(' ', '_').replace('(',
                        '').replace(')', '').replace('-', '_to_')
                new_columns_dict[clean_col] = data_type.__name__

            return new_columns_dict

    def pattern_seperator(self):
        """This function uses a pattern to read the lines from the
        csv files
        """
        columns_list = []
        data_list = []
        with open(self.file_1, 'r') as open_file1:
            # open file1 to read first line inside file1
            first_line = open_file1.readline()
            first_line = first_line.replace('\n', '')
            for words in first_line.split(','):
                columns_list.append(words)  # columns creation
            # open file to read second line inside file1
            # this allow me to get the type of each data
            first_line = open_file1.readlines()
            for items in first_line[1].split(','):
                try:
                    int_values = int(items)
                    data_list.append(int)
                except ValueError:
                    try:
                        float_val = float(items)
                        data_list.append(float)
                    except ValueError:
                        data_list.append(str)
        # dict containg columns name and their respective value
        self.__columns_dict = dict(zip(columns_list, data_list))
