import uuid
from therapy.schemes import ValidateTherapy
from fastapi import APIRouter, Form, UploadFile, File, HTTPException
from utils.img_manager import save_image, delete_image
from therapy import operations

router = APIRouter()

@router.post('/')
async def create_new_therapy(
    title: str = Form(...),
    description: str = Form(...),
    image: UploadFile = File(...)
):
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

@router.get('/')
async def get_therapies():
    ...

@router.put('/{id}')
async def update_therapy():
    ...

@router.delete('/{id}')
async def delete_therapy():
    ...