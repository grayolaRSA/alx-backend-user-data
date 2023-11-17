#!/usr/bin/env python3
"""
module for DB class to create and add users to DB
"""


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import NoResultFound, InvalidRequestError
from typing import Union, Callable, List, Dict


from user import Base
from user import User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        method to add new user to database
        """
        user = User(email=email, hashed_password=hashed_password)

        self._session.add(user)
        self._session.commit()

        return user

    def find_user_by(self, **kwargs: Dict[Union[str, int],
                                          Union[str, int]]) -> User:
        """
        method to find user based on key-value argument
        """
        if kwargs:
            for key, value in kwargs.items():
                if not hasattr(User, key):
                    raise InvalidRequestError

                found_user = self._session.query(User).filter_by(
                    **kwargs).first()
                if found_user is None:
                    raise NoResultFound
                return found_user

    def update_user(self, user_id: int, **kwargs:
                    Dict[Union[str, int], Union[str, int]]) -> None:
        """
        method that updates user details in the database
        """
        found_user = self.find_user_by(id=user_id)

        if kwargs:
            for key, value in kwargs.items():
                if not hasattr(User, key):
                    raise ValueError

        setattr(found_user, key, value)

        self._session.commit()
