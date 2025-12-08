import os 
import aiofiles
from core.settings import STATIC_DIR
from fastapi import UploadFile, HTTPException

async def save_image(img_file: UploadFile, file_name: str, max_size: int = 5) -> tuple[str, float] | None:
    try:
        allowed_types = {
            "image/jpeg": [b"\xff\xd8\xff"],    # JPEG
            "image/png": [b"\x89PNG\r\n\x1a\n"], # PNG
            "image/webp": [b"RIFF"],             # WEBP (RIFF header)
        }

        if img_file.content_type not in allowed_types:
            raise ValueError("Şəkil formatı düzgün deyil (yalnız JPEG, PNG, WEBP)")

        file_bytes = await img_file.read()
        file_size_mb = round(len(file_bytes) / (1024 * 1024), 2)

        # Magic bytes yoxlaması
        valid = False
        for signature in allowed_types[img_file.content_type]:
            if file_bytes.startswith(signature):
                valid = True
                break

        if not valid:
            raise ValueError("Fayl real şəkil formatına uyğun deyil")

        if file_size_mb > max_size:
            raise ValueError(f"Şəkil maksimum {max_size}MB olmalıdır")

        file_path = os.path.abspath(os.path.join(STATIC_DIR, "images", file_name+img_file.content_type))

        async with aiofiles.open(file_path, "wb") as f:
            await f.write(file_bytes)

        return file_path, file_size_mb

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception:
        raise HTTPException(status_code=500, detail="Server xətası (Şəkil saxlanmadı)")

async def delete_image(file_path: str) -> bool:
    try:
        os.remove(file_path)
        return True
    except:
        return False