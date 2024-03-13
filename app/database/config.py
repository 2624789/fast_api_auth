from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from app.config import settings

Base = declarative_base()


class ModelBase(Base):
    __abstract__ = True

    def to_dict(self):
        return {
            field.name:getattr(self, field.name) for field in self.__table__.c
        }


engine = create_engine(settings.database_url, connect_args={})
