import os
from fastapi import UploadFile, HTTPException, status


async def save_pdf(cv_file: UploadFile, file_name: str) -> tuple[str, str] | None:
    try:
        if cv_file.content_type != "application/pdf": 
            raise Exception("Yalnız PDF faylı göndərilə bilər")

        file_bytes = await cv_file.read()
        file_size_mb = round(len(file_bytes) / (1024 * 1024), 2)

        if file_size_mb > 10:
            raise Exception("PDF faylın həcmi maksimum 10MB olmalıdır")

        file_path = os.path.join(os.getcwd(), "static_files", file_name)

        with open(file_path, "wb+") as f:
            f.write(file_bytes)

        return file_path, file_size_mb

    except Exception as e:
        raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")


async def delete_pdf(file_path: str) -> bool:
    try:
        os.remove(file_path)
        return True
    except:
        return False
