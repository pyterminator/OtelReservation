from typing import List
from fastapi import HTTPException, status
from utils.email_manager import EmailChecker
from utils.phone_manager import PhoneChecker
from pydantic import BaseModel, EmailStr, field_validator

class ValidateData(BaseModel):
    name: str 
    surname: str 

    email: EmailStr 
    phone: str

    message: str 

    # Name Validator
    @field_validator("name")
    def check_name(cls, name:str):
        if len(name) < 3 or len(name) > 30:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ad minimum 3, maksimum 30 simvoldan ibarət olmalıdır")
        return name.strip().title()

    # Surname Validator
    @field_validator("surname")
    def check_surname(cls, surname:str):
        if len(surname) < 3 or len(surname) > 30:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Soyad minimum 3, maksimum 30 simvoldan ibarət olmalıdır")
        return surname.strip().title()

    # Email validator
    @field_validator("email")
    def check_email(cls, email):
        if not EmailChecker.check_email(email): 
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Yanlış e-poçt formatıdır")
        return email
    
    # Phone Validator
    @field_validator("phone")
    def check_phone(cls, phone):
        if not PhoneChecker.check_phone(phone): 
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Yanlış telefon formatıdır")
        return phone
    
    # Message Validator
    @field_validator("message")
    def check_message(cls, message:str):
        if len(message) < 3 or len(message) > 255: 
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Mesaj minimum 3, maksimum 255 simvoldan ibarət olmalıdır")
        return message.strip()

class ShowContactMessage(BaseModel):
    id: int
    fullname: str
    email: str
    phone: str
    message: str
    is_active: bool

class ShowContactMessageWithPagination(BaseModel):
    total: int
    page: int 
    limit: int
    items: List[ShowContactMessage]