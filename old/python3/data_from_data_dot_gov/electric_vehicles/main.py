#!/usr/bin/python3
from evdata import EvData
from db_engine import DbEngine
from vehicle_model import ElectricVehicleModel

if __name__ == '__main__':
    my_dict = ElectricVehicleModel()
    my_dict.pattern_seperator()
    man = my_dict.create_columns()

    session = DbEngine().__session

    
