#!/usr/bin/python3
"""This module sets the id for each row
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer
import uuid
from models.vehicle_model import Base, ElectricVehicleModel
from src import db_storage


class EvData(ElectricVehicleModel, Base):
    """Proceeds to create a new table and create columns for it
    """
    __tablename__ = 'Evehicles'
    id = Column(String(60), primary_key=True, nullable=False)
    my_dict = ElectricVehicleModel()
    #res = my_dict.create_columns()
    #print(res)
    db_storage.save()

    """
    if my_dict:
        for name, d_type in my_dict.items():
            if d_type == 'int':
                setattr(EvData, name, Column(Integer))
            else:
                setattr(EvData, name, Column(String))
    """


    def __init__(self):
        """Constructor to create unique id
        """
        super().__init__()
        # self.id = str(uuid.uuid4())
