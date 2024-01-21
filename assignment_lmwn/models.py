from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Users(Base):
    __tablename__ = "users_tb"
    user_id = Column(String(255), primary_key=True)
    for i in range(1000):
        locals()[f'feature_{i}'] = Column(Float)

class Restaurants(Base):
    __tablename__ = "restaurants_tb"
    restaurant_id = Column(String(255), primary_key=True)
    latitude = Column(Float)
    longitude = Column(Float)