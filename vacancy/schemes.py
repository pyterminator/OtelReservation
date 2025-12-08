from utils.email_manager import EmailChecker
from utils.phone_manager import PhoneChecker
from pydantic import BaseModel, EmailStr, field_validator
from utils.mml_checker import name_checker, surname_checker

class ValidateApplyVacancy(BaseModel):
    name: str 
    surname: str 
    email: EmailStr
    phone: str 

    # Name Validator
    @field_validator("name")
    def check_name(cls, name:str):
        try: return  name_checker(name)
        except Exception as e: raise ValueError(str(e))

    # Surname Validator
    @field_validator("surname")
    def check_surname(cls, surname:str):
        try: return surname_checker(surname)
        except Exception as e: raise ValueError(str(e))

    # Email validator
    @field_validator("email")
    def check_email(cls, email):
        if not EmailChecker.check_email(email):
            raise ValueError("Yanlış e-poçt formatıdır")
        return email
    
    
    # Phone Validator
    @field_validator("phone")
    def check_phone(cls, phone):
        if not PhoneChecker.check_phone(phone):
            raise ValueError("Yanlış telefon formatıdır")
        return phone