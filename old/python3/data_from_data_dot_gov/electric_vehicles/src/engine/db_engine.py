#!/usr/bin/python3
"""A module that serves as the database engine
"""

from models.vehicle_model import ElectricVehicleModel, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

class DbEngine():
    """Database class that creates a connection to the database

    Args:
        __engine - private class attribute that creates the enigne
        __session - private class attribute that handles session
    """
    __engine = None
    __session = None

    @staticmethod
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

    def new(self, obj):
        """Adds new object to the database
        """
        self.__session.add(obj)

    def save(self):
        """Commit and saves all new changes to the database
        """
        self.__session.commit()

    def create_all(self):
        """creates a session, binds it to the engine and table
        """
        Base.metadata.create_all(self.__engine)
        tmp_session = sessionmaker(bind=self.__engine,
                                   expire_on_commit=False)
        Session = scopped_session(tmp_session)
        self.__session = Session()

    def close(self):
        """Ends session
        """
        self.__session.close()
