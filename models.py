from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime

Base = declarative_base()


class KarmaReason(Base):
    __table__ = 'karma_reasons'

    karma_id = Column(Integer, ForeignKey('karma.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    added = Column(DateTime, nullable=False, default=datetime.now())
    reason = Column(String(length=1024), nullable=True)
    change = Column(Integer, nullable=False)
    score = Column(Integer, nullable=False)

    karma = relationship('Karma', back_populates='karma')
    user = relationship('User', back_populates='user')


class User(Base):
    __table__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    user_uid = Column(String(length=250), nullable=False)
    is_super = Column(Boolean, nullable=False)
    can_alias = Column(Boolean, nullable=False)

    karma_reasons = relationship('KarmaReason', back_populates='karma_reasons')


class Karma(Base):
    __table__ = 'karma'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(length=1024), nullable=False)
    added = Column(DateTime, nullable=False, default=datetime.now())
    altered = Column(DateTime, nullable=False, default=datetime.now())
    score = Column(Integer, nullable=False)
    pluses = Column(Integer, nullable=False, default=0)
    minuses = Column(Integer, nullable=False, default=0)
    neutrals = Column(Integer, nullable=False, default=0)
