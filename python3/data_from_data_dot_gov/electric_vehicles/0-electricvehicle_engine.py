#!/usr/bin/python3
"""This module serves as a data scraper to get, create certain data
from the Electric_vehicle files
"""
import os
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class ElectricVehicle():
    """ """
    __engine = None
    __session = None
    __columns_dict = {}

    def __init__(self, file_1, file_2):
        """creates instances to the path of the csv files
        """
        self.file_1 = file_1
        self.file_2 = file_2
        self.connector()

    def connector(self):
        """creates a connection to mysql databse
        """
        # pass_wd = os.getenv('pwd', 'password')
        d_b = "ElectricVehicle"
        host = "localhost"
        self.__engine = create_engine(
            'mysql+mysqldb://user_1738:groot@{}:3306/{}'
            .format(host, d_b), pool_pre_ping=True)
        Session = sessionmaker(bind=self.__engine)
        self.__session = Session()

    def create_columns(self):
        """Creates columns from self.__columns_dict
        """
        if self.__columns_dict:
            columns = []
            for cols, data_type in self.__columns_dict.items():
                columns.append(f"{cols} {data_type.__name__}")
            query = f"CREATE TABLE IF NOT EXISTS EV_DATA ({', '.join(columns)})"
            self.__session.execute(query)
            self.__session.commit()

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


if __name__ == '__main__':
    main = ElectricVehicle('Electric_Vehicle_Population_Data_1.csv',
                           'Electric_Vehicle_Population_Data_1.csv')
    main.pattern_seperator()
    main.create_columns()
