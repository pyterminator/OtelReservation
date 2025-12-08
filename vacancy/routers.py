import uuid
from vacancy import operations
from auth.models import User, UserRole
from utils.token_manager import TokenManager
from utils.pdf_manager import save_pdf, delete_pdf
from vacancy.schemes import ValidateApplyVacancy, ShowAllApplicationsWithPagination, ShowApplication
from fastapi import UploadFile, APIRouter, HTTPException, status, File, Form, Depends, Query

router = APIRouter()

@router.post('/apply', status_code=201)
async def apply_cv_vacancy(
        name: str = Form(...),
        surname: str = Form(...),
        email: str = Form(...),
        phone: str = Form(...),
        cv_file: UploadFile = File(...)
    ):
    try:
        data = ValidateApplyVacancy( name=name, surname=surname, email=email, phone=phone )
    except Exception as e:
        raise HTTPException(status_code=400, detail = str(e))
    
    unique_id = uuid.uuid4().hex
    file_name = f"{data.name}{data.surname}_CV.{unique_id}.pdf"

    result = await save_pdf(cv_file, file_name)
    
    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Faylı saxlamaq mümkün olmadı")

    file_path, file_size_mb = result

    try:
        new_apply = await operations.create_new( data.name, data.surname, data.email, data.phone, file_path, str(file_size_mb) )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")
    
    if not new_apply:
        try: await delete_pdf(file_path)
        except: raise HTTPException(status_code=400, detail="Fayl silmə xətası")

    return new_apply

@router.get('/applications', status_code=200, response_model=ShowAllApplicationsWithPagination)
async def get_career_applications(
        user: User = Depends(TokenManager.get_current_user),
        limit: int = Query(10, ge=1, le=100),
        page: int = Query(1, ge=1)
    ):
    if limit not in (10, 50):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Pagination üçün limit 10 və ya 50 olmalıdır")

    if user.role != UserRole.ADMIN: 
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="İcazəsiz cəhd")

    offset = (page - 1) * limit
    items, total = await operations.get_all_career_applications(limit=limit, offset=offset)

    return {"total": total, "page": page, "limit": limit, "items": items}

@router.get('/applications/{id}', status_code=200, response_model=ShowApplication) 
async def get_career_application(id: int, user: User = Depends(TokenManager.get_current_user)):
    if user.role != UserRole.ADMIN: raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="İcazəsiz cəhd")
    career_application = await operations.get_career_application(id=id)
    if career_application: return career_application
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tapılmadı")

