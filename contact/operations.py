# from typing import List
# from contact.models import Contact 
# from core.database import db_session
# import contact.decoder as DataDecoder

# #
# ##
# ### ---> CRUD operations for 'contact form'
# ##
# #

# # Create new
# def create_new(
#         name: str,
#         surname: str,
#         fullname: str,
#         email:str,
#         phone:str,
#         message:str,
#     ) -> bool:
#     try:
#         new_contact_message = Contact()
#         new_contact_message.name = name 
#         new_contact_message.surname = surname 
#         new_contact_message.fullname = fullname 
#         new_contact_message.email = email 
#         new_contact_message.phone = phone 
#         new_contact_message.message = message

#         db_session.add(new_contact_message)
#         db_session.commit()
#         return True
#     except Exception as e:
#         return False

# # Get all as obj
# def get_all_as_objects() -> List[Contact] | None:
#     try:
#         data = db_session.query(Contact).all()
#         return data 
#     except: return None

# # Get all as dict
# def get_all_as_dict() -> List[dict] | None:
#     try:
#         data = get_all_as_objects()
#         data = DataDecoder.decode_contact_objects(data)
#         return data 
#     except: return None

# # Get one as obj
# def get_one_as_obj(id:int)-> Contact | None:
#     try:
#         criteria = {"_id": id}
#         obj = db_session.query(Contact).filter_by(**criteria).first()
#         if obj:
#             return obj
#         return None
#     except: return None

# # Get one as dict
# def get_one_as_dict(id:int)-> dict | None:
#     try:
#         obj = get_one_as_obj(id)
#         if obj:
#             obj_to_dict = DataDecoder.decode_contact_obj(obj) 
#             return obj_to_dict
#         return None
#     except: return None

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
