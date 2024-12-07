from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    birth_date = Column(DateTime)
    phone_number = Column(String(20))

    bonuses = relationship('Bonus', back_populates='user')


# class Admin(Base):
#     __tablename__ = "admins"
#
#     id = Column(Integer, primary_key=True)
#     telegram_id = Column(Integer, unique=True, nullable=False)
#     #is_super_admin = Column(Boolean, default=False)




class Bonus(Base):
    __tablename__ = 'bonuses'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    coffees_count = Column(Integer, default=0)

    user = relationship('User', back_populates='bonuses')