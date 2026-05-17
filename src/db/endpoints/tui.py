from src.db.backend.memory import UserTable

class Application:
    def __init__(self):
        self._user_base = UserTable()

    def print_menu(self) -> None:
        print("\n====== База пользователей ======")
        print("1. Добавить запись")
        print("2. Обновить данные пользователя")
        print("3. Найти запись по id")
        print("4. Показать все записи")
        print("5. Удалить пользователя")
        print("6. Найти запись по фильтру")
        print("0. Выйти")

    def read_int(self, prompt: str) -> int:
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

    def add_user(self) -> None:
        print("\n Добавление записи")

        user_id = self.read_int("id: ")
        name = input("first_name: ").strip()
        sec_name = input("second_name: ").strip()
        age = self.read_int("age: ")
        phone_num = input("phone_number: ").strip()

        try:
            record = self._user_base.create_record(user_id, name, sec_name, age, phone_num)
            print(f"Запись добавлена: {record}")

        except ValueError as exc:
            print(f"Ошибка: {exc}, проверьте корректность вводимых данных")

    def _update_user(self) -> None:
        user_id = self.read_int("id: ")
        name = input("first_name: ").strip()
        sec_name = input("second_name: ").strip()
        age = self.read_optional_int("age: ")
        phone_num = input("phone_number: ").strip()

        try:
            self._user_base.update_record(id = user_id, 
                        first_name = name, 
                        second_name = sec_name, 
                        age = age, 
                        phone = phone_num)
            print(f"Запись с номером {user_id} обновлена")
        except ValueError as exc:
            print(f"Ошибка: {exc}, проверьте корректность вводимых данных")

    def print_records(self, records: list[tuple[int, str, str, int, str]]) -> None:
        if not records:
            print("Записи не найдены.")
            return

        for record in records:
            print(record)

    def _find_users_by_filter(self) -> None:
        print("\n Поиск по фильтру (Enter = пропустить поле)")

        user_id = self.read_optional_int("id: ")
        name = input("first_name: ").strip() or None
        sec_name = input("second_name: ").strip() or None
        age = self.read_optional_int("age: ")
        phone_num = input("phone_number: ").strip() or None

        try:
            records = self._user_base.select_record(
                id=user_id,
                first_name=name,
                second_name=sec_name,
                age=age,
                phone=phone_num,
            )
            self.print_records(records)
        except ValueError as exc:
            print(f"Ошибка: {exc}, проверьте корректность вводимых данных")

    def _find_user(self) -> None:
        user_id = self.read_int("id: ")
        try:
            record = self._user_base.select_record(id = user_id)
            print(record)
        except ValueError as exc:
            print(f"Ошибка: {exc}, проверьте корректность вводимых данных")

    def _show_all_users(self) -> None:
        print("\n Список записей")
        try:
            self.print_records(self._user_base.select_record())
        except ValueError as exc:
            print(f"Ошибка: {exc}")

    def _find_user(self) -> None:
        user_id = self.read_int("id: ")
        try:
            record = self.select_record(id = user_id)
            print(record)
        except ValueError as exc:
            print(f"Ошибка: {exc}, проверьте корректность вводимых данных")

    def _delete_user(self):
        user_id = self.read_optional_int("id: ")
        try:
            lst = self._user_base.delete_record(user_id)
            print(f"Запись с номером {lst} удалена")
        except ValueError as exc:
            print(f"Ошибка: {exc}, проверьте корректность вводимых данных")

    def run(self):
        while True:
            self.print_menu()

            action = input("Выберите действие: ").strip()

            if action == "1":
                self.add_user()

            elif action == "2":
                self.update_user()

            elif action == "3":
                self.find_user()

            elif action == "4":
                self.show_all_users()

            elif action == "5":
                self.delete_user()

            elif action == "6":
                self.find_users_by_filter()

            elif action == "0":
                print("Выход из программы.")
                break

            else:
                print("Неизвестная команда. Повторите ввод.")