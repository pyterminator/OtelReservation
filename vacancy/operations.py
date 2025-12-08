from typing import List
from sqlalchemy import select, func
from vacancy.models import VacancyApplication
from core.database import AsyncSessionLocal

async def create_new(
    name:str,
    surname:str,
    email:str,
    phone:str,
    cv_filename:str,
    cv_filesize:str 
) -> VacancyApplication | None:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            try:
                new_apply = VacancyApplication(
                    name=name,
                    surname=surname,
                    fullname=name+" "+surname,
                    email=email,
                    phone=phone,
                    cv_filename=cv_filename,
                    cv_filesize=cv_filesize
                )
                session.add(new_apply)
                await session.flush()
                await session.refresh(new_apply)
                return new_apply
            except Exception as e:
                await session.rollback()
                raise e

async def get_all_career_applications(limit: int, offset: int)-> List[VacancyApplication]:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            total_result = await session.execute(select(func.count(VacancyApplication.id)))
            total_count = total_result.scalar()

            stmt = (
                select(VacancyApplication)
                .order_by(VacancyApplication.id.desc())
                .limit(limit)
                .offset(offset)
            )

            result = await session.execute(stmt)
            applications = result.scalars().all()

            return applications, total_count
        
async def get_career_application(id: int) -> VacancyApplication | None:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            stmt = select(VacancyApplication).where((VacancyApplication.id == id))
            result = await session.execute(stmt)
            existing_career_application = result.scalar_one_or_none()

            if existing_career_application:
                return existing_career_application
            
            return None
