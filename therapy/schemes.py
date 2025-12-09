from typing import List
from datetime import datetime
from pydantic import BaseModel, field_validator
from utils.mml_checker import title_checker, description_checker

class ValidateTherapy(BaseModel):
    title: str 
    description: str 

    @field_validator("title")
    def check_title(cls, title:str):
        try: return title_checker(title, min_=3, max_=255)
        except Exception as e: raise ValueError(str(e))

    @field_validator("description")
    def check_description(cls, description:str):
        try: return description_checker(description, min_=3, max_=1000)
        except Exception as e: raise ValueError(str(e))


class ShowTherapy(BaseModel):
    id: int
    title: str 
    description: str 
    img_file: str 
    img_size: str
    is_active: bool
    created_at: datetime 
    updated_at: datetime

class ShowAllTherapiesWithPagination(BaseModel):
    total: int 
    page: int 
    limit: int 
    items: List[ShowTherapy]