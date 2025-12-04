from contact import operations
from auth.models import User, UserRole
from utils.token_manager import TokenManager
from contact.schemes import ValidateData, ShowContactMessage, ShowContactMessageWithPagination
from fastapi import APIRouter, HTTPException, status, Depends, Query

router = APIRouter()

@router.post("", status_code=status.HTTP_200_OK, response_model=ShowContactMessage)
async def create_new(contact_form_data: ValidateData):
    result = await operations.create_new_contact_message(contact_form_data)
    if result: return result
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Əlaqə mesajı qeydə alınarkən xəta oldu")

# /messages?page=...&limit=10|50
@router.get("/messages", status_code=status.HTTP_200_OK, response_model=ShowContactMessageWithPagination)
async def get_contact_messages(
        user: User = Depends(TokenManager.get_current_user),
        limit: int = Query(10, ge=1, le=100),
        page: int = Query(1, ge=1)
    ):

    if limit not in (10, 50):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Pagination üçün limit 10 və ya 50 olmalıdır")

    if user.role != UserRole.ADMIN: 
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="İcazəsiz cəhd")

    offset = (page - 1) * limit
    items, total = await operations.get_all_contact_messages(limit=limit, offset=offset)

    return {"total": total, "page": page, "limit": limit, "items": items}
    

@router.get("/messages/{id}", status_code=status.HTTP_200_OK, response_model=ShowContactMessage)
async def get_contact_message(id: int, user: User = Depends(TokenManager.get_current_user)):
    if user.role != UserRole.ADMIN: raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="İcazəsiz cəhd")
    contact_message = await operations.get_contact_message(id=id)
    if contact_message: return contact_message
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tapılmadı")
