from abc import ABC, abstractmethod

from app.database.session import Session


class UnitOfWork(ABC):
    def __init__(self, session):
        # self.repository = repository(Session())
        self.session = session

    @abstractmethod
    def begin(self):
        pass

    @abstractmethod
    def rollback(self):
        pass

    @abstractmethod
    def commit(self):
        pass

    def __enter__(self):
        self.begin()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.rollback()
        self.session.close()


class AlchemyUnitOfWork(UnitOfWork):
    def begin(self):
        self.session.begin()

    def rollback(self):
        self.session.rollback()

    def commit(self):
        self.session.commit()
