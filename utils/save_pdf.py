import os
import uuid
from fastapi import UploadFile, HTTPException, status

async def save_pdf(cv_file: UploadFile, file_name: str) -> tuple[str, str] | None:
    ...
