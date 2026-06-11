type UserRecord = tuple[int, str, str, int, str]

class UserTableError(Exception):
     def __init__(self, message=""):
        super().__init__(message)
        self.message = message

class Invaluser_idAgeError(UserTableError):
    def __init__(self, message):
        super().__init__(message)

class Duplicateuser_idError(UserTableError):
    def __init__(self, message):
        super().__init__(message)

class Invaluser_idPhoneError(UserTableError):
    def __init__(self, message):
        super().__init__(message)

class StorageError(UserTableError):
    def __init__(self, message):
        super().__init__(message)

class StorageReadError(StorageError):
    def __init__(self, message):
        super().__init__(message)

class StorageWriteError(StorageError):
    def __init__(self, message):
        super().__init__(message)

class CorruptDataError(StorageError):
    def __init__(self, message):
        super().__init__(message)

def check_phone(phone: str) -> Invaluser_idPhoneError:
    for number in str(phone).replace(" ", "").replace("-", ""):
        if number not in "+1234567890":
            return Invaluser_idPhoneError("Некорректный номер телефона")
    return None
        
def check_age(age: int) -> Invaluser_idAgeError:
    if age is not None and age < 0:
        return Invaluser_idAgeError("Возраст не может быть отрицательным")
    else:
        return None
    
def check_del_user_id(user_id: int, records: list[UserRecord]) -> Duplicateuser_idError:
    for record in records:
        if record[0] == user_id:
            return None
    return Duplicateuser_idError("Такого user_id не существует или оно уже удалено")

def check_create_user_id(user_id: int, records: list[UserRecord]) -> Duplicateuser_idError:
    flag = False
    for record in records:
        if record[0] == user_id:
            flag = True
            break
        else:
            flag = False
    if flag:
        return Duplicateuser_idError("Такое user_id уже существует")
    else:
        return None
