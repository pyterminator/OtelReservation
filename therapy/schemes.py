from pydantic import BaseModel, field_validator
from utils.mml_checker import title_checker, description_checker

class ValidateTherapy(BaseModel):
    title: str 
    description: str 

    @field_validator("title")
    def check_name(cls, title:str):
        try: return title_checker(title, min_=3, max_=255)
        except Exception as e: raise ValueError(str(e))

    @field_validator("description")
    def check_name(cls, description:str):
        try: return description_checker(description, min_=3, max_=1000)
        except Exception as e: raise ValueError(str(e))