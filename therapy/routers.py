import uuid
from therapy import operations
from auth.models import User, UserRole
from therapy.schemes import ValidateTherapy, ShowAllTherapiesWithPagination, ShowTherapy
from utils.token_manager import TokenManager
from utils.img_manager import save_image, delete_image
from fastapi import APIRouter, Form, UploadFile, File, HTTPException, Depends, status, Query

router = APIRouter()

@router.post('/')
async def create_new_therapy(
    title: str = Form(...),
    description: str = Form(...),
    image: UploadFile = File(...),
    user: User = Depends(TokenManager.get_current_user)
):
    
    if user.role != UserRole.ADMIN: 
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="İcazəsiz cəhd")

    try:
        data = ValidateTherapy(title=title, description=description)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    unique_id = uuid.uuid4().hex 
    file_name = f"{data.title.lower()}.{unique_id}"

    result = await save_image(image, file_name,max_size = 10)

    if not result:
        raise HTTPException(status_code=400, detail="Faylı saxlamaq mümkün olmadı")

    file_path, file_size_mb = result

    try:
        new_therapy = await operations.create_new_therapy(data.title, data.description, file_path, str(file_size_mb))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    if not new_therapy:
        try: await delete_image(file_path)
        except: raise HTTPException(status_code=400, detail="Fayl silmə xətası")
    
    return new_therapy

@router.get('/', status_code=200, response_model=ShowAllTherapiesWithPagination)
async def get_therapies(
    user: User = Depends(TokenManager.get_current_user),
    limit: int = Query(10, ge=1, le=100),
    page: int = Query(1, ge=1)
):
    if limit not in (10, 50):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Pagination üçün limit 10 və ya 50 olmalıdır")

    if user.role != UserRole.ADMIN: 
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="İcazəsiz cəhd")

    offset = (page - 1) * limit
    items, total = await operations.get_all_therapies(limit=limit, offset=offset)

    return {"total": total, "page": page, "limit": limit, "items": items}


# @router.put('/{id}')
# async def update_therapy():
#     ...

# @router.delete('/{id}')
# async def delete_therapy():
#     ...