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

async def get_all_therapies(limit: int, offset: int) -> List[Therapy]:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            total_result = await session.execute(select(func.count(Therapy.id)))
            total_count = total_result.scalar()

            stmt = (
                select(Therapy)
                .order_by(Therapy.id.desc())
                .limit(limit)
                .offset(offset)
            )

            result = await session.execute(stmt)
            therapies = result.scalars().all()

            return therapies, total_count
