from . import errors

type UserRecord = tuple[int, str, str, int, str]

Users: list[UserRecord] = []


def create_record(user_id: int, 
                  name: str, 
                  sec_name: str, 
                  age: int, 
                  phone_num: str) -> UserRecord:
    
    a_check = errors.check_age(age)
    if a_check != None:
        raise a_check
    
    for record in Users:
        if record[0] == user_id:
            raise ValueError("Запись с таким номером пользователя({user_id}) уже существует")

    
    n_check = errors.check_num(phone_num)
    if n_check != None:
        raise n_check

    if phone_num[0] != "+":
        phone_num = "+" + phone_num
    
    new_record: UserRecord = (
        user_id,
        name,
        sec_name,
        age,
        phone_num
    )

    Users.append(new_record)

    return new_record

def delete_record(user_id: int) -> UserRecord:
    i_check = errors.check_id(user_id)
    if i_check != None:
        raise i_check
    del_record = Users.pop(user_id)
    return del_record

def select_record(user_id: int | None = None, 
                  name: str | None = None, 
                  sec_name: str | None = None, 
                  age: int | None = None, 
                  phone_num: str | None = None) -> list[UserRecord]:
    selected_records: list[UserRecord] = []

    #тут проверяю корректность ввода данных пользователя, чтобы 
    #сразу сказать ему в tui, что он ничего по ним не найдет
    #ошибки отловятся в tui и вызовется новый интерфейс по типу
    #"вы уверенны в корректности данных? да/нет"
    a_check = errors.check_age(age) 
    if a_check != None:         
        raise a_check
    
    i_check = errors.check_id(user_id)
    if i_check != None:
        raise i_check

    if (
        user_id is None
        and name is None
        and sec_name is None
        and age is None
        and phone_num is None
    ):
        return Users.copy()

    for record in Users:
        if user_id == None or record[0] != user_id:
            continue
        if name == None or record[1] != name:
            continue
        if sec_name == None or record[2] != sec_name:
            continue
        if age == None or record[3] != age:
            continue
        if phone_num == None or record[4] != phone_num:
            continue

        selected_records.append(record)

        return selected_records

def update_record(user_id: int | None = None, 
                  name: str | None = None, 
                  sec_name: str | None = None, 
                  age: int | None = None, 
                  phone_num: str | None = None) -> UserRecord:
    #тут тоже дальнейший отлов ошибок ввода
    i_check = errors.check_id(user_id)
    if i_check != None:
        raise i_check
    
    a_check = errors.check_age(age) 
    if a_check != None:         
        raise a_check
    
    n_check = errors.check_num(phone_num) 
    if n_check != None:         
        raise n_check
    
    upd_record: UserRecord = (
        user_id,
        name,
        sec_name,
        age,
        phone_num
    )

    for i in range(len(Users)):
        if Users[i][0] == user_id:
            Users[i] = upd_record
            break
    return upd_record