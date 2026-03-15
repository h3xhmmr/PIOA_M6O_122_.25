type UserRecord = tuple[int, str, str, int, str]

Users: list[UserRecord] = []

def create_record(user_id: int, 
                  name: str, 
                  sec_name: str, 
                  age: int, 
                  phone_num: str) -> UserRecord:
    
    if age < 0:
        raise ValueError("Возраст не может быть отрицательным")
    
    for record in Users:
        if record[0] == user_id:
            raise ValueError("Запись с таким номером пользователя({user_id}) уже существует")

    

    for number in "+1234567890":
        if number not in phone_num.replace(" ", "").replace("-", "") or number != phone_num[0]:
            raise ValueError("Некорректный номер телефона")

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

def delete_record():
    pass

def select_record():
    pass

def update_record():
    pass