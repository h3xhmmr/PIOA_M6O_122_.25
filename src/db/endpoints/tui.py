from src.db.backend.interface import UserTableInterface
from src.db.backend.memory import UserTable
import src.db.backend.errors as errors


class Application:
    def __init__(self, user_base: UserTableInterface | None = None):
        self._user_base = user_base if user_base is not None else UserTable()

    def _print_menu(self) -> None:
        print("\n====== База пользователей ======")
        print("1. Добавить запись")
        print("2. Обновить данные пользователя")
        print("3. Найти запись по user_id")
        print("4. Показать все записи")
        print("5. Удалить пользователя")
        print("6. Найти запись по фильтру")
        print("0. Выйти")

    def _read_int(self, prompt: str) -> int:
        while True:
            raw = input(prompt).strip()
            try:
                return int(raw)
            except ValueError:
                print("Ошибка: введите целое число.")

    def _read_optional_int(self, prompt: str) -> int | None:
        while True:
            raw = input(prompt).strip()

            if raw == "":
                return None

            try:
                return int(raw)
            except ValueError:
                print("Ошибка: введите целое число или оставьте поле пустым.")

    def _add_user(self) -> None:
        print("\n Добавление записи")

        user_user_id = self._read_int("user_id: ")
        name = input("first_name: ").strip()
        sec_name = input("second_name: ").strip()
        age = self._read_int("age: ")
        phone_num = input("phone_number: ").strip()

        try:
            record = self._user_base.create_record(user_user_id, name, sec_name, age, phone_num)
            print(f"Запись добавлена: {record}")

        except (errors.Invaluser_idPhoneError, errors.Invaluser_idAgeError, errors.Duplicateuser_idError) as exc:
            print(f"Ошибка: {exc}")

    def _update_user(self) -> None:
        user_user_id = self._read_int("user_id: ")
        name = input("first_name: ").strip()
        sec_name = input("second_name: ").strip()
        age = self._read_optional_int("age: ")
        phone_num = input("phone_number: ").strip()

        try:
            self._user_base.update_record(user_id = user_user_id, 
                        first_name = name, 
                        second_name = sec_name, 
                        age = age, 
                        phone = phone_num)
            print(f"Запись с номером {user_user_id} обновлена")
        except (errors.Invaluser_idPhoneError, errors.Invaluser_idAgeError, errors.Duplicateuser_idError) as exc:
            print(f"Ошибка: {exc}")

    def _print_records(self, records: list[tuple[int, str, str, int, str]]) -> None:
        if not records:
            print("Записи не найдены.")
            return

        for record in records:
            print(record)

    def _find_users_by_filter(self) -> None:
        print("\n Поиск по фильтру (Enter = пропустить поле)")

        user_user_id = self._read_optional_int("user_id: ")
        name = input("first_name: ").strip() or None
        sec_name = input("second_name: ").strip() or None
        age = self._read_optional_int("age: ")
        phone_num = input("phone_number: ").strip() or None
        
        records = self._user_base.select_record(
            user_id=user_user_id,
            first_name=name,
            second_name=sec_name,
            age=age,
            phone=phone_num,
        )
        self._print_records(records)

    def _find_user(self) -> None:
        user_user_id = self._read_int("user_id: ")
        record = self._user_base.select_record(user_id = user_user_id)
        print(record)
        
    def _show_all_users(self) -> None:
        print("\n Список записей")
        self._print_records(self._user_base.select_record())

    def _delete_user(self):
        user_user_id = self._read_int("user_id: ")
        try:
            lst = self._user_base.delete_record(user_user_id)
            print(f"Запись {lst} удалена")
        except errors.Duplicateuser_idError as exc:
            print(f"Ошибка: {exc}")

    def run(self):
        while True:
            self._print_menu()

            action = input("Выберите действие: ").strip()

            if action == "1":
                self._add_user()

            elif action == "2":
                self._update_user()

            elif action == "3":
                self._find_user()

            elif action == "4":
                self._show_all_users()

            elif action == "5":
                self._delete_user()

            elif action == "6":
                self._find_users_by_filter()

            elif action == "0":
                print("Выход из программы.")
                break

            else:
                print("Неизвестная команда. Повторите ввод.")
