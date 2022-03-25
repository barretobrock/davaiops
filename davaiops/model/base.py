import re
from sqlalchemy import (
    Boolean,
    Column,
    func,
    TIMESTAMP
)
from sqlalchemy.ext.declarative import (
    declarative_base,
    declared_attr
)


class Base:

    @declared_attr
    def __tablename__(cls) -> str:
        """This names our tables automatically. It expects a table object class to begin with Table..
            and inserts an underscore between capital letters after that.

        Examples:
            TableThisThing -> this_thing
            TableHello -> hello
        """
        return '_'.join(x.lower() for x in re.findall(r'[A-Z][^A-Z]*', cls.__name__) if x != 'Table')

    @declared_attr
    def created_date(cls):
        return Column(TIMESTAMP, server_default=func.now())

    @declared_attr
    def last_updated(cls):
        return Column(TIMESTAMP, server_onupdate=func.now(), server_default=func.now())

    @declared_attr
    def is_deleted(cls):
        return Column(Boolean, default=False, nullable=False)

    @declared_attr
    def deleted_timestamp(cls):
        return Column(TIMESTAMP)


Base = declarative_base(cls=Base)
