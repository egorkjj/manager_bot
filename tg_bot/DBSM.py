from sqlalchemy import create_engine, Column, Integer, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import pytz

categories = {
    "0": "Окна и двери ПВХ",
    "1": "Металлические двери",
    "2": "Межкомнатные двери",
    "3": "Ворота",
    "4": "Рольшторы, жалюзи"
}

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
    add_time = Column(Text, nullable=True)
    buyer_phone = Column(Text, nullable=True)
    buyer_name = Column(Text, nullable=True)
    adress = Column(Text, nullable=True)
    comment = Column(Text, nullable=True)
    category = Column(Integer, nullable=True)
    is_order = Column(Boolean, nullable=True)
    is_photo_zamer = Column(Boolean, nullable=True)

class Reclamation(Base):
    __tablename__ = 'recl'
    id = Column(Integer, autoincrement=True, primary_key=True)
    worker_id = Column(Text, nullable=True)
    buyer_phone = Column(Text, nullable=True)
    buyer_name = Column(Text, nullable=True)
    adress = Column(Text, nullable=True)
    comment = Column(Text, nullable=True)
    category = Column(Integer, nullable=True)
    done = Column(Boolean, nullable=True)

def add_order_metadata(phone, adress, comment, category, name):
    Session = sessionmaker()
    session = Session(bind = engine)
    moscow_time = datetime.now(pytz.timezone('Europe/Moscow'))
    moscow_time = datetime.strftime(moscow_time, "%Y.%m.%d %H:%m")
    print(moscow_time)
    new_order = Order(buyer_phone = phone, adress = adress, comment = comment, category = category, is_order = False, buyer_name = name, add_time = moscow_time, is_photo_zamer = False)
    session.add(new_order)
    session.commit()
    id = new_order.id
    session.close()
    return id

def get_order_data(id, worker_id, worker):
    Session = sessionmaker()
    session = Session(bind = engine)
    current = session.query(Order).filter(Order.id == id).first()
    phone = current.buyer_phone
    adress = current.adress
    comm = current.comment
    name = current.buyer_name
    cat = categories[f"{current.category}"]
    current.worker = worker
    current.worker_id = worker_id
    session.commit()
    session.close()
    return [phone, adress, comm, cat, name]


def decline_order(id):
    Session = sessionmaker()
    session = Session(bind = engine)
    current = session.query(Order).filter(Order.id == id).first()
    if current == None:
        session.close()
        return False
    id_w = current.worker_id
    session.query(Order).filter(Order.id == id).delete()
    session.commit()
    session.close()
    return id_w


def yes_order(id):
    Session = sessionmaker()
    session = Session(bind = engine)
    current = session.query(Order).filter(Order.id == id).first()
    if current == None:
        session.close()
        return False
    current.is_order = True
    session.commit()
    user = current.worker_id
    adress = current.adress
    name = current.buyer_name
    phone = current.buyer_phone
    cat = current.category
    id = current.id
    session.close()
    return [user, adress, name, phone, categories[f"{cat}"], id]

def yes_zamer(id):
    Session = sessionmaker()
    session = Session(bind = engine)
    current = session.query(Order).filter(Order.id == id).first()
    current.is_photo_zamer = True
    session.commit()
    session.close()
    

def fetchall() -> list[dict]:
    result = []
    Session = sessionmaker()
    session = Session(bind = engine)
    all_order = session.query(Order).all()
    for i in all_order:
        js = {
            "id": i.id,
            "cat": categories[f"{i.category}"],
            "worker": i.worker if i.worker != None else "❌",
            "phone": i.buyer_phone,
            "name": i.buyer_name,
            "adress": i.adress,
            "comment": i.comment if i.comment != "отсутствует" else "❌",
            "zamer": "✅" if i.is_photo_zamer else "❌",
            "order": "✅" if i.is_order else "❌",
            "date": i.add_time
        }
        result.append(js)
    session.close()
    return result

def add_recl_metadata(phone, adress, comment, category, name):
    Session = sessionmaker()
    session = Session(bind = engine)
    new_order = Reclamation(buyer_phone = phone, adress = adress, comment = comment, category = category, buyer_name = name, done=False)
    session.add(new_order)
    session.commit()
    id = new_order.id
    session.close()
    return id

def get_recl_data(id, worker_id):
    Session = sessionmaker()
    session = Session(bind = engine)
    current = session.query(Reclamation).filter(Reclamation.id == id).first()
    phone = current.buyer_phone
    adress = current.adress
    comm = current.comment
    name = current.buyer_name
    cat = categories[f"{current.category}"]
    current.worker_id = worker_id
    session.commit()
    session.close()
    return [phone, adress, comm, cat, name]

Base.metadata.create_all(engine)
