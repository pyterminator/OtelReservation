# from typing import List
# from contact.models import Contact

# def decode_contact_obj(obj: Contact) -> dict:
#     return {
#         "_id": obj._id,
#         "name": obj.name,
#         "surname": obj.surname,
#         "fullname": obj.surname,
#         "email": obj.email,
#         "phone": obj.phone,
#         "message": obj.message,
#         "is_active": obj.is_active,
#         "created_at": obj.created_at,
#         "updated_at": obj.updated_at
#     }


# def decode_contact_objects(objects: List[Contact]) -> List[dict]:
#     return [
#         decode_contact_obj(obj) for obj in objects
#     ]