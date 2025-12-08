import uuid
from vacancy import operations
from vacancy.schemes import ValidateApplyVacancy
from utils.pdf_manager import save_pdf, delete_pdf
from fastapi import UploadFile, APIRouter, HTTPException, status, File, Form

router = APIRouter()

@router.post('/apply', status_code=201)
async def apply_cv_vacancy(
        name: str = Form(...),
        surname: str = Form(...),
        email: str = Form(...),
        phone: str = Form(...),
        cv_file: UploadFile = File()
    ):

    data = ValidateApplyVacancy( name=name, surname=surname, email=email, phone=phone )
    
    unique_id = uuid.uuid4().hex
    file_name = f"{data.name}{data.surname}_CV.{unique_id}.pdf"

    result = await save_pdf(cv_file, file_name)
    
    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Fayl saxlamaq mümkün olmadı")
    
    file_path, file_size_mb = result

    try:
        new_apply = await operations.create_new( data.name, data.surname, data.email, data.phone, file_path, str(file_size_mb) )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")
    
    if not new_apply:
        try: await delete_pdf(file_path)
        except: raise HTTPException(status_code=400, detail="Fayl silmə xətası")

    return new_apply
    
    

    
    

    



    

    

    



    