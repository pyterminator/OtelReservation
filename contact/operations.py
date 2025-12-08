from typing import List
from contact.models import Contact
from sqlalchemy import select, func
from contact.schemes import ValidateData
from core.database import AsyncSessionLocal 


async def create_new_contact_message(data: ValidateData) -> Contact | None:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            try:
               new_contact_message = Contact(
                   name = data.name,
                   surname = data.surname,
                   fullname = data.name + " " + data.surname,
                   email = data.email,
                   phone = data.phone,
                   message = data.message
               )
               session.add(new_contact_message)
               return new_contact_message
            except:
                await session.rollback()
                return None


async def get_all_contact_messages(limit: int, offset: int) -> List[Contact]:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            total_result = await session.execute(select(func.count(Contact.id)))
            total_count = total_result.scalar()

            stmt = (
                select(Contact)
                .order_by(Contact.id.desc())
                .limit(limit)
                .offset(offset)
            )

            result = await session.execute(stmt)
            contacts = result.scalars().all()

            return contacts, total_count


async def get_contact_message(id: int) -> Contact | None:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            stmt = select(Contact).where((Contact.id == id))
            result = await session.execute(stmt)
            existing_contact_message = result.scalar_one_or_none()
            if existing_contact_message:
                return existing_contact_message
            return None


# # Update contact message
# def update_message(
#         id:int,
#         name:str|None=None,
#         surname:str|None=None,
#         fullname:str|None=None,
#         email:str|None=None,
#         phone:str|None=None,
#         message:str|None=None,
#         is_active:bool|None=None
#     ) -> bool:

#     try:
#         obj = get_one_as_obj(id)
#         if obj:
#             obj.name = name if name else obj.name
#             obj.surname = surname if surname else obj.surname 
#             obj.fullname = fullname if fullname else obj.fullname 
#             obj.email = email if email else obj.email
#             obj.phone = phone if phone else obj.phone 
#             obj.message = message if message else obj.message
#             obj.is_active = is_active if is_active else obj.is_active
#             db_session.commit()
#             return True
#         return False
#     except: return False


# # Permanently delete contact message
# def delete_message(id: int) -> bool:
#     try:
#         obj = get_one_as_obj(id)
#         if obj:
#             db_session.delete(obj)
#             db_session.commit()
#             return True
#         return False
#     except: return False
