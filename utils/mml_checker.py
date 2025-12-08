# MML - min, max, length
from string import ascii_lowercase, ascii_uppercase

def check_length(text: str, message: str, min_: int, max_: int) -> None:
    if len(text) < min_ or len(text) > max_: raise Exception(message)

def check_punct(text: str, message: str, space: bool = False, numbers: bool = False) -> None:
    abc = ascii_lowercase + "üçşıəöğ" + ascii_uppercase + "ÜÇŞİƏÖĞ"
    
    if space: abc += " "
    if numbers: abc += "0123456789"
    
    for ch in text:
        if ch not in abc:
            raise Exception(message)

def name_checker(name: str, min_:int = 3, max_: int=30) -> str | None:
    check_length(name, f"Ad minimum {min_}, maksimum {max_} simvoldan ibarət olmalıdır", min_, max_)
    name = name.strip().title()
    check_punct(name, f"Adın tərkibində yalnız hərf olmalıdır")
    return name

def surname_checker(surname: str, min_: int = 3, max_: int = 30) -> str | None:
    check_length(surname, f"Soyad minimum {min_}, maksimum {max_} simvoldan ibarət olmalıdır", min_, max_)
    surname = surname.strip().title()
    check_punct(surname, f"Soyadın tərkibində yalnız hərf olmalıdır")
    return surname

def title_checker(title: str, min_:int = 3, max_: int = 30) -> str | None:
    check_length(title, f"Başlıq minimum {min_}, maksimum {max_} simvoldan ibarət olmalıdır", min_, max_)
    title = title.strip().title()
    check_punct(title, f"Başlığın tərkibində yalnız hərf və boşluq olmalıdır", space=True)
    return title

def description_checker(description: str, min_:int = 3, max_: int = 1000) -> str | None:
    check_length(description, f"Açıqlama minimum {min_}, maksimum {max_} simvoldan ibarət olmalıdır", min_, max_)
    description = description.strip()
    check_punct(description, f"Açıqlamada yalnız hərflər, rəqəmlər və boşluq olmalıdır", space=True, numbers=True)
    return description

    