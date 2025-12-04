import os, uuid
from vacancy import operations
from vacancy.schemes import ValidateApplyVacancy
from fastapi import UploadFile, File, Form, APIRouter, Depends, HTTPException, status


router = APIRouter()

@router.post('/apply')
async def apply_cv_vacancy(
        name: str = Form(...),
        surname: str = Form(...),
        email: str = Form(...),
        phone: str = Form(...),
        cv_file: UploadFile = File()
    ):

    try: data = ValidateApplyVacancy(name=name, surname=surname, email=email, phone=phone)
    except Exception as e: raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")


    if cv_file.content_type != "application/pdf": raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Yalnız PDF faylı göndərilə bilər")


    file_name = data.name + "_" + data.surname + "_cv_" + f"{uuid.uuid4()}" + ".pdf"
    file_path = os.path.join(os.getcwd(), "static_files", file_name)

    

    
    with open(file_path, "wb+") as f:
        f.write(file_bytes)

    