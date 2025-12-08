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
