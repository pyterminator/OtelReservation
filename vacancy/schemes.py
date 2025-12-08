from fastapi import HTTPException, status
from utils.mml_checker import name_checker, surname_checker
from utils.email_manager import EmailChecker
from utils.phone_manager import PhoneChecker
from pydantic import BaseModel, EmailStr, field_validator

class ValidateApplyVacancy(BaseModel):
    name: str 
    surname: str 
    email: EmailStr
    phone: str 

    # Name Validator
    @field_validator("name")
    def check_name(cls, name:str):
        try: name = name_checker(name)
        except Exception as e: raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")
        return name

    # Surname Validator
    @field_validator("surname")
    def check_surname(cls, surname:str):
        try: surname = surname_checker(surname)
        except Exception as e: raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")
        return surname

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