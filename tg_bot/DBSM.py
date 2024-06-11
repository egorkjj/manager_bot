from sqlalchemy import create_engine, Column, Integer, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime


DATABASE_URL = f"sqlite:///db.sqlite3"

# Создание объекта Engine
engine = create_engine(DATABASE_URL)

# Создание базового класса для моделей
Base = declarative_base()

# Определение модели User
class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer, autoincrement=True, primary_key=True)
    worker = Column(Text, nullable=True)
    worker_id = Column(Text, nullable=True)
    manager = Column(Text, nullable=True)
    add_time = Column(Text, nullable=True)
    buyer_phone = Column(Text, nullable=True)
    adress = Column(Text, nullable=True)
    comment = Column(Text, nullable=True)
    category = Column(Integer, nullable=True)
    is_order = Column(Boolean, nullable=True)

def add_order_metadata(manager, phone, adress, comment, category):
    Session = sessionmaker()
    session = Session(bind = engine)
    new_order = Order(manager = manager, buyer_phone = phone, adress = adress, comment = comment, category = category, is_order = False)
    session.add(new_order)
    session.commit()
    id = new_order.id
    session.close()
    return id


Base.metadata.create_all(engine)
