from . import errors
from .interface import UserRecord
from .interface import UserTableInterface


class UserTable(UserTableInterface):
    def __init__(self):
        self._user_table: list[UserRecord] = []

    def create_record(self,
                      user_id: int,
                      first_name: str,
                      second_name: str,
                      age: int,
                      phone: str) -> UserRecord:
        
        if errors.check_age(age) is not None:
            raise errors.check_age(age)
        
        if phone[0] != "+":
            phone = "+" + phone
        if errors.check_phone(phone) is not None:
            raise errors.check_phone(phone)
        
        if errors.check_create_user_id(user_id, self._user_table) is not None:
            raise errors.check_create_user_id(user_id, self._user_table)
        
        rec: UserRecord = (user_id, first_name, second_name, age, phone)
        self._user_table.append(rec)
        return rec
    
    def select_record(self,
                      user_id: int | None = None,
                      first_name: str | None = None,
                      second_name: str | None = None,
                      age: int | None = None,
                      phone: str | None = None) -> list[UserRecord]:
        selected_records: list[UserRecord] = []
        if (
            user_id is None
            and first_name is None
            and second_name is None
            and age is None
            and phone is None
        ):
            return self._user_table.copy()

        format_phone = ""
        if phone is not None and phone[0] != "+":
            format_phone = "+" + phone
        else:
          format_phone = phone

        for record in self._user_table:
            if user_id is not None and record[0] != user_id:
                continue
            if first_name is not None and record[1] != first_name:
                continue
            if second_name is not None and record[2] != second_name:
                continue
            if age is not None and record[3] != age:
                continue
            if format_phone is not None and record[4] != format_phone:
                continue
            selected_records.append(record)

        return selected_records
    
    def update_record(self,
                      user_id: int,
                      first_name: str | None = None,
                      second_name: str | None = None,
                      age: int | None = None,
                      phone: str | None = None):
        if user_id is not None: 
            i_check = errors.check_del_user_id(user_id, self._user_table)
            if i_check is not None:
                raise i_check
        
        a_check = errors.check_age(age) 
        if a_check is not None:         
            raise a_check
        
        n_check = errors.check_phone(phone) 
        if n_check is not None:         
            raise n_check
        format_phone = ""
        if phone is not None and phone[0] != "+":
            format_phone = "+" + phone
        else:
          format_phone = phone
        
        for i in range(len(self._user_table)):
                if self._user_table[i][0] == user_id:
                    if first_name is None:
                        upd_first_name = self._user_table[i][1]
                    else:
                        upd_first_name = first_name
                    if second_name is None:
                        upd_second_name = self._user_table[i][2]
                    else:
                        upd_second_name = second_name
                    if age is None:
                        upd_age = self._user_table[i][3]
                    else:
                        upd_age = age
                    if phone is None:
                        upd_phone = self._user_table[i][4]
                    else:
                        upd_phone = format_phone

        upd_record: UserRecord = (
            user_id,
            upd_first_name,
            upd_second_name,
            upd_age,
            upd_phone
        )
       

        for i in range(len(self._user_table)):
            if self._user_table[i][0] == user_id:
                self._user_table[i] = upd_record
                break
        return upd_record
    
    def delete_record(self, user_id: int) -> UserRecord:
        exc = errors.check_del_user_id(user_id, self._user_table)
        if exc is not None:
            raise exc
        for i in range(len(self._user_table)):
            if self._user_table[i][0] == user_id:
                deleted_rec = self._user_table[i]
                self._user_table.pop(i)
                return deleted_rec