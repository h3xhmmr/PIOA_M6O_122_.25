from . import memory
def check_num(phone: str) -> ValueError:
    for number in "+1234567890":
        if number not in phone.replace(" ", "").replace("-", "") or number != phone[0]:
            return ValueError("Некорректный номер телефона")
        else:
            return None
        
def check_age(age: int) -> ValueError:
    if age < 0:
        return ValueError("Возраст не может быть отрицательным")
    else:
        return None
    
def check_id(id: int, list: list[memory.UserRecord]) -> ValueError:
    for record in list:
        if record[0] == id:
            return None
    return ValueError("Такого id не существует или оно уже удалено")