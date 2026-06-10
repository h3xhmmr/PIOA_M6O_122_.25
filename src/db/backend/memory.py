from . import errors

type UserRecord = tuple[int, str, str, int, str]


class UserTable:
    def __init__(self):
        self._user_table: list[UserRecord] = []

    def create_record(self,
                      id: int,
                      first_name: str,
                      second_name: str,
                      age: int,
                      phone: str) -> UserRecord:
        
        if errors.check_age(age) != None:
            raise errors.check_age(age)
        
        if phone[0] != "+":
            phone = "+" + phone
        if errors.check_phone(phone) != None:
            raise errors.check_phone(phone)
        
        if errors.check_create_id(id, self._user_table) != None:
            raise errors.check_create_id(id, self._user_table)
        
        rec: UserRecord = (id, first_name, second_name, age, phone)
        self._user_table.append(rec)
        return rec
    
    def select_record(self,
                      id: int | None = None,
                      first_name: str | None = None,
                      second_name: str | None = None,
                      age: int | None = None,
                      phone: str | None = None) -> list[UserRecord]:
        selected_records: list[UserRecord] = []
        if (
            id is None
            and first_name is None
            and second_name is None
            and age is None
            and phone is None
        ):
            return self._user_table.copy()

        format_phone = ""
        if phone != None and phone[0] != "+":
            format_phone = "+" + phone
        else:
          format_phone = phone

        for record in self._user_table:
            if id != None and record[0] != id:
                continue
            if first_name != None and record[1] != first_name:
                continue
            if second_name != None and record[2] != second_name:
                continue
            if age != None and record[3] != age:
                continue
            if format_phone != None and record[4] != format_phone:
                continue
            selected_records.append(record)

        return selected_records
    
    def update_record(self,
                      id: int | None = None,
                      first_name: str | None = None,
                      second_name: str | None = None,
                      age: int | None = None,
                      phone: str | None = None):
        if id != None: 
            i_check = errors.check_del_id(id, self._user_table)
            if i_check != None:
                raise i_check
        
        a_check = errors.check_age(age) 
        if a_check != None:         
            raise a_check
        
        n_check = errors.check_phone(phone) 
        if n_check != None:         
            raise n_check
        format_phone = ""
        if phone != None and phone[0] != "+":
            format_phone = "+" + phone
        else:
          format_phone = phone
        
        for i in range(len(self._user_table)):
                if self._user_table[i][0] == id:
                    if first_name == None:
                        upd_first_name = self._user_table[i][1]
                    else:
                        upd_first_name = first_name
                    if second_name == None:
                        upd_second_name = self._user_table[i][2]
                    else:
                        upd_second_name = second_name
                    if age == None:
                        upd_age = self._user_table[i][3]
                    else:
                        upd_age = age
                    if phone == None:
                        upd_phone = self._user_table[i][4]
                    else:
                        upd_phone = format_phone

        upd_record: UserRecord = (
            id,
            upd_first_name,
            upd_second_name,
            upd_age,
            upd_phone
        )
       

        for i in range(len(self._user_table)):
            if self._user_table[i][0] == id:
                self._user_table[i] = upd_record
                break
        return upd_record
    
    def delete_record(self, id: int) -> UserRecord:
        exc = errors.check_del_id(id, self._user_table)
        if exc != None:
            raise exc
        for i in range(len(self._user_table)):
            if self._user_table[i][0] == id:
                deleted_rec = self._user_table[i]
                self._user_table.pop(i)
                return deleted_rec