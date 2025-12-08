import os 
import aiofiles
from core.settings import STATIC_DIR
from fastapi import UploadFile, HTTPException, status


async def save_pdf(cv_file: UploadFile, file_name: str, max_size: int = 10) -> tuple[str, str] | None:
    try:
        if cv_file.content_type != "application/pdf": 
            raise ValueError("Fayl PDF formatında deyil")

        file_bytes = await cv_file.read()
        file_size_mb = round(len(file_bytes) / (1024 * 1024), 2)

        if not file_bytes.startswith(b"%PDF"): 
            raise ValueError("Fayl PDF formatında deyil")

        if file_size_mb > max_size: 
            raise ValueError(f"PDF faylın həcmi maksimum {max_size}MB olmalıdır")

        file_path = os.path.join(STATIC_DIR, file_name)

        async with aiofiles.open(file_path, "wb") as f:
            await f.write(file_bytes)

        return file_path, file_size_mb

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Server xətası (PDF saxlanmadı)")


async def delete_pdf(file_path: str) -> bool:
    try:
        os.remove(file_path)
        return True
    except:
        return False
