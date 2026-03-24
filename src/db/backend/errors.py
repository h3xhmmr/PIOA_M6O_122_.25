type UserRecord = tuple[int, str, str, int, str]

def check_num(phone: str) -> ValueError:
    for number in phone.replace(" ", "").replace("-", ""):
        if number not in "+1234567890":
            return ValueError("Некорректный номер телефона")
        else:
            return None
        
def check_age(age: int) -> ValueError:
    if age != None and age < 0:
        return ValueError("Возраст не может быть отрицательным")
    else:
        return None
    
def check_id(id: int, list: list[UserRecord]) -> ValueError:
    for record in list:
        if record[0] == id:
            return None
    return ValueError("Такого id не существует или оно уже удалено")