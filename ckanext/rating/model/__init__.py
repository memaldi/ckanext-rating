from ckan import model
from ckan.model.domain_object import DomainObject
from ckan.model.meta import metadata, mapper, Session

from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import types

import logging
log = logging.getLogger(__name__)

rating_table = None


def setup():
    if rating_table is None:
        define_rating_table()
        log.debug('Rating table defined in memory')

    if model.package_table.exists() and model.user_table.exists():
        if not rating_table.exists():
            rating_table.create()
            log.debug('Rating table create')
        else:
            log.debug('Rating table already exists')
    else:
        log.debug('Rating table creation deferred')


class Rating(DomainObject):

    @classmethod
    def filter(cls, **kwargs):
        return Session.query(cls).filter_by(**kwargs)

    @classmethod
    def exists(cls, **kwargs):
        if cls.filter(**kwargs).first():
            return True
        else:
            return False

    @classmethod
    def get(cls, **kwargs):
        instance = cls.filter(**kwargs).first()
        return instance

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        Session.add(instance)
        Session.commit()
        return instance.as_dict()


def define_rating_table():
    global rating_table

    rating_table = Table('rating', metadata,
                         Column('package_id', types.UnicodeText,
                                ForeignKey('package.id',
                                           ondelete='CASCADE',
                                           onupdate='CASCADE'),
                                primary_key=True, nullable=False),
                         Column('user_id', types.UnicodeText,
                                ForeignKey('user.id',
                                           ondelete='CASCADE',
                                           onupdate='CASCADE'),
                                primary_key=True, nullable=False)
                         )
    mapper(Rating, rating_table)
