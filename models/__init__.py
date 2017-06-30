from datetime import datetime

from sqlalchemy import Column, BigInteger, DateTime, String
from sqlalchemy.ext.declarative import declarative_base

from lib.sqla import auto_manage_session, from_dict

_Base = declarative_base()


class Base(_Base):
    __abstract__ = True
    session = None

    id = Column(BigInteger, autoincrement=True, primary_key=True)
    created_on = Column(DateTime)
    modified_on = Column(DateTime)

    def __init__(self, allow_pk=False, **kwargs):
        from_dict(self, kwargs, allow_pk)

    @classmethod
    @auto_manage_session
    def find_by_id(cls, _id):
        return cls.session.query(cls).filter_by(id=_id).first()

    @classmethod
    @auto_manage_session
    def find_by_url(cls, url):
        return cls.session.query(cls).filter_by(url=url).first()

    @classmethod
    @auto_manage_session
    def create(cls, data_dict):
        obj = cls(**data_dict)
        obj.created_on = datetime.utcnow()
        cls.session.add(obj)
        cls.session.commit()
        return obj


class URL(Base):
    __tablename__ = "url"

    url = Column(String, unique=True)
