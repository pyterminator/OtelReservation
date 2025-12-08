from typing import List
from sqlalchemy import select, func
from therapy.models import Therapy
from core.database import AsyncSessionLocal

async def create_new_therapy(
    title:str,
    description:str,
    img_file:str,
    img_size:str
) -> Therapy | None:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            try:
                new_therapy = Therapy(
                    title=title,
                    description=description,
                    img_file=img_file,
                    img_size=img_size
                )
                
                session.add(new_therapy)
                await session.flush()
                await session.refresh(new_therapy)
                return new_therapy
            except Exception as e:
                await session.rollback()
                raise e