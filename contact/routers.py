from typing import List
from contact import operations
from fastapi import APIRouter, HTTPException, status
from contact.schemes import ValidateData, ShowContactMessage

router = APIRouter()

#
##
### ---> Endpoints for "contact form" 
##
#

@router.post("", status_code=status.HTTP_200_OK)
def create_new(contact_form_data: ValidateData):
    is_saved = operations.create_new(
        name=contact_form_data.name,
        surname=contact_form_data.surname,
        fullname=contact_form_data.name + " " + contact_form_data.surname,
        email=contact_form_data.email,
        phone=contact_form_data.phone,
        message=contact_form_data.message
    )
    
    if is_saved: return { "detail" : "Əlaqə mesajı qeydə alındı" }

    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Əlaqə mesajı qeydə alınarkən xəta oldu")

@router.get("/messages", status_code=status.HTTP_200_OK, response_model=List[ShowContactMessage])
def get_contact_messages():
    data = operations.get_all_as_objects()
    if data: return data 
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Xəta oldu")
