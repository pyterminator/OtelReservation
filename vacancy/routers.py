from vacancy import operations
from utils.pdf_manager import save_pdf, delete_pdf
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

    try: 
        data = ValidateApplyVacancy(
            name=name, 
            surname=surname, 
            email=email, 
            phone=phone
        )

    except Exception as e: 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"{e}"
        )
    
    result = await save_pdf(cv_file, data)
    
    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Fayl saxlamaq mümkün olmadı")
    
    file_path, file_size_mb = result

    try:
        new_apply = await operations.create_new(
            name=data.name,
            surname=data.surname,
            email=data.email,
            phone=data.phone,
            cv_filename=file_path,
            cv_filesize=f"{file_size_mb}"
        )
        return {
            "message": "CV uğurla yükləndi, müraciət qeydə alındı",
            "data": {
                "name": new_apply.name,
                "surname": new_apply.surname,
                "email": new_apply.email,
                "phone": new_apply.phone,
                "cv_filename": new_apply.cv_filename,
                "cv_filesize": f"{new_apply.cv_filesize} MB",
            }
        }
    except:
        try:
            await delete_pdf(file_path)
        except:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="PDF save/delete proses xətası")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Müraciət qeydə alınmadı")
    
    

    



    

    

    



    