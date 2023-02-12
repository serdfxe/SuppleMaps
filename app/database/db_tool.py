from math import isnan
from app.database.session import Session
from app.database.unit_of_work import AlchemyUnitOfWork


class DBTool():
    session = Session()
    uow = AlchemyUnitOfWork(Session())

    @classmethod
    def filter(cls, *args, **kwargs):
        if not len(kwargs) and not len(args):
            return cls.session.query(cls)
        if len(args):
            return cls.session.query(cls).filter(*args)
        return cls.session.query(cls).filter_by(**kwargs)# .first() OR .all()

    @classmethod
    def all(cls, **kwargs):
        return cls.session.query(cls).all()

    @classmethod
    def new(cls, **kwargs):
        with cls.uow:
            new = cls(**kwargs)

            cls.uow.session.add(new)

            cls.uow.commit()

            cls.uow.session.refresh(new)
            cls.uow.session.expunge(new)
        
            return new

    @classmethod
    def update(cls, obj, **kwargs):
        with cls.uow:
            cls.uow.session.query(cls).filter_by(id=obj.id).update(kwargs)
            cls.uow.commit()

    @classmethod
    def delete_first(cls, **kwargs):
        with cls.uow:
            obj = cls.session.query(cls).filter_by(**kwargs).first()
            cls.session.delete(obj)
            cls.session.commit()

    @classmethod
    def delete_all(cls, **kwargs):
        with cls.uow:
            cls.uow.session.query(cls).filter_by(**kwargs).delete()
            cls.uow.commit()

    def as_dict(self):
        return {c.name: getattr(self, c.name) if not (isinstance(getattr(self, c.name), float) and isnan(getattr(self, c.name))) else None for c in self.__table__.columns}
