type UserRecord = tuple[int, str, str, int, str]


class UserTableError(Exception):
     def __init__(self, message=""):
        super().__init__(message)
        self.message = message


class InvalidAgeError(UserTableError):
    def __init__(self, message):
        super().__init__(message)


class DuplicateIdError(UserTableError):
    def __init__(self, message):
        super().__init__(message)


class InvalidPhoneError(UserTableError):
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


def check_phone(phone: str) -> InvalidPhoneError:
    if phone == "":
        return InvalidPhoneError("Некорректный номер телефона")
    for number in str(phone).replace(" ", "").replace("-", ""):
        if number not in "+1234567890":
            return InvalidPhoneError("Некорректный номер телефона")
    return None
        
def check_age(age: int) -> InvalidAgeError:
    if age is not None and age < 0:
        return InvalidAgeError("Возраст не может быть отрицательным")
    else:
        return None
    
def check_del_user_id(user_id: int, records: list[UserRecord]) -> DuplicateIdError:
    for record in records:
        if record[0] == user_id:
            return None
    return DuplicateIdError("Такого user_id не существует или оно уже удалено")

def check_create_user_id(user_id: int, records: list[UserRecord]) -> DuplicateIdError:
    flag = False
    for record in records:
        if record[0] == user_id:
            flag = True
            break
        else:
            flag = False
    if flag:
        return DuplicateIdError("Такое user_id уже существует")
    else:
        return None

def validate_table(records: list[UserRecord]) -> CorruptDataError:
    for i in range(len(records)):
            if check_age(records[i][3]) is not None:
                return CorruptDataError(
                    f"Некорректная запись возраста в файле(строка {i + 1})"
                )
            if check_phone(records[i][4]) is not None:
                return CorruptDataError(
                    f"Некорректная запись номера телефона в файле(строка {i + 1})"
                )