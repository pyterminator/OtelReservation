from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, TIMESTAMP, Integer, Boolean

BASE = declarative_base()

class Contact(BASE):
    __tablename__ = "contact_form"

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String(30))
    surname = Column(String(30))

    fullname = Column(String(60), nullable=True)

    email = Column(String(255))
    phone = Column(String(17))

    message = Column(String(255))

    is_active = Column(Boolean, default=True)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.timezone('UTC', func.now()))
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.timezone('UTC', func.now()))

    def __init__(self, name, surname, fullname, email, phone, message):
        self.name = name 
        self.surname = surname 
        self.fullname = fullname 
        self.email = email 
        self.phone = phone
        self.message = message
