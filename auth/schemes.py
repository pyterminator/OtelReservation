from string import ascii_lowercase
from fastapi import status, HTTPException
from utils.email_manager import EmailChecker
from utils.password_manager import PasswordChecker
from pydantic import BaseModel, EmailStr, field_validator
from auth.models import UserRole
from datetime import datetime

class ValidateUser(BaseModel):

    username: str 
    email: EmailStr 
    password: str 
    role: UserRole = UserRole.USER

    @field_validator("password")
    def check_password(cls, password):
        if not PasswordChecker.check_password(password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Şifrə minimum 8 simvoldan ibarət olmalıdır. Tərkibində ən az bir böyük hərf, 1 kiçik hərf, 1 rəqəm və nöqtə olmalıdır")
        return password
    
    @field_validator("email")
    def check_email(cls, email):
        if not EmailChecker.check_email(email): 
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="E-poçt doğru formada daxil edilməyib!")
        return email 

    @field_validator("username")
    def check_username(cls, username):
        for ch in username:
            if ch not in ascii_lowercase:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="İstifadəçi adında yalnız 26 kiçik ingilis hərfi olmalıdır!")
        return username


class ShowUser(BaseModel):
    id: int 
    username: str 
    email: str 
    role: UserRole
    is_active: bool 
    created_at: datetime 
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }

class TokenFormat(BaseModel): 
    access_token: str 
    refresh_token: str 
    token_type: str 

class LoginData(BaseModel):
    email: str 
    password: str

    @field_validator("password")
    def check_password(cls, password):
        if not PasswordChecker.check_password(password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Şifrə formatı səhvdir")
        return password
    
    @field_validator("email")
    def check_email(cls, email):
        if not EmailChecker.check_email(email): 
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="E-poçt formatı səhvdir")
        return email 

class ValidateRefreshToken(BaseModel):
    refresh_token: str