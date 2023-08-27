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

    def __init__(self, file_1, file_2):
        """creates instances to the path of the csv files
        """
        self.file_1 = file_1
        self.file_2 = file_2
        self.connector()

    def connector(self):
        """creates a connection to mysql databse
        """
        pass_wd = os.getenv('PWD')
        d_b = "ElectricVehicle"
        host = "localhost"
        self.__engine = create_engine(
                        'mysql+mysqldb://root:{}@{}:3306/{}'
                        .format(pass_wd, host, d_b),
                        pool_pre_ping=True)
        Session = sessionmaker(bind=self.__engine)
        self.__session = Session()

    def alter_database(self):
        """Creates tables
        """
        query = ""
        self.__session.execute(query)

    def pattern_seperator(self):
        """This function uses a pattern to read the lines from the
        csv files
        """
        with open(self.file_1, 'r') as open_file1:
            first_line = open_file1.readline()
            pattern = first_line.split(',')
            for words in pattern:
                print(words)


if __name__ == '__main__':
    main = ElectricVehicle('Electric_Vehicle_Population_Data_1.csv', 'Electric_Vehicle_Population_Data_1.csv')
    main.pattern_seperator()
