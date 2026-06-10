type UserRecord = tuple[int, str, str, int, str]

def check_phone(phone: str) -> InvalidPhoneError:
    for number in str(phone).replace(" ", "").replace("-", ""):
        if number not in "+1234567890":
            return InvalidPhoneError("Некорректный номер телефона")
    return None
        
def check_age(age: int) -> InvalidAgeError:
    if age != None and age < 0:
        return InvalidAgeError("Возраст не может быть отрицательным")
    else:
        return None
    
def check_del_id(id: int, list: list[UserRecord]) -> DuplicateIDError:
    for record in list:
        if record[0] == id:
            return None
    return DuplicateIDError("Такого id не существует или оно уже удалено")

def check_create_id(id: int, list: list[UserRecord]) -> DuplicateIDError:
    flag = False
    for record in list:
        if record[0] == id:
            flag = True
            break
        else:
            flag = False
    if flag:
        return DuplicateIDError("Такое id уже существует")
    else:
        return None

class UserTableError(Exception):
    def __init__(self):
        self.message = ""

class InvalidAgeError(UserTableError):
    def __init__(self, message):
        self.message = message

class DuplicateIDError(UserTableError):
    def __init__(self, message):
        self.message = message

class InvalidPhoneError(UserTableError):
    def __init__(self, message):
        self.message = message

class StorageError(UserTableError):
    def __init__(self, message):
        self.message = message

class StorageReadError(StorageError):
    def __init__(self, message):
        self.message = message

class StorageWriteError(StorageError):
    def __init__(self, message):
        self.message = message

class CorruptDataError(StorageError):
    def __init__(self, message):
        self.message = message