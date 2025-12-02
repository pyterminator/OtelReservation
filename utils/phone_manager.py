import re 

class PhoneChecker:

    @staticmethod 
    def check_phone(phone:str)->bool:
        pattern = r"^\+994-\d{2}-\d{3}-\d{2}-\d{2}$"
        if re.match(pattern, phone) and isinstance(phone, str): return True 
        return False 