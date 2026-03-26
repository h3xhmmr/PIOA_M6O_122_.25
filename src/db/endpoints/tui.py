from src.db.backend.memory import create_record, select_record, delete_record, update_record
def _print_menu() -> None:
    print("\n====== База пользователей ======")
    print("1. Добавить запись")
    print("2. Обновить данные пользователя")
    print("3. Найти запись по id")
    print("4. Показать все записи")
    print("5. Удалить пользователя")
    print("6. Найти запись по фильтру")
    print("0. Выйти")

def _read_int(prompt: str) -> int:
    while True:
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            print("Ошибка: введите целое число.")

def _add_user() -> None:
    print("\nДобавление записи")

    user_id = _read_int("id: ")
    name = input("first_name: ").strip()
    sec_name = input("second_name: ").strip()
    age = _read_int("age: ")
    phone_num = input("phone_number: ").strip()

    try:
        record = create_record(user_id, name, sec_name, age, phone_num)
        print(f"Запись добавлена: {record}")

    except ValueError as exc:
        print(f"Ошибка: {exc}, проверьте корректность вводимых данных")

def _update_user() -> None:
    user_id = _read_int("id: ")
    name = input("first_name: ").strip()
    sec_name = input("second_name: ").strip()
    age = _read_optional_int("age: ")
    phone_num = input("phone_number: ").strip()

    try:
        update_record(user_id = user_id, 
                      name = name, 
                      sec_name = sec_name, 
                      age = age, 
                      phone_num = phone_num)
        print(f"Запись с номером {user_id} обновлена")
    except ValueError as exc:
        print(f"Ошибка: {exc}, проверьте корректность вводимых данных")

def _print_records(records: list[tuple[int, str, str, int, str]]) -> None:
    if not records:
        print("Записи не найдены.")
        return

    for record in records:
        print(record)

def _show_all_users() -> None:
    print("\nСписок записей")
    try:
        _print_records(select_record())
    except ValueError as exc:
        print(f"Ошибка: {exc}")

def _read_optional_int(prompt: str) -> int | None:
    while True:
        raw = input(prompt).strip()

        if raw == "":
            return None

        try:
            return int(raw)
        except ValueError:
            print("Ошибка: введите целое число или оставьте поле пустым.")

def _find_user() -> None:
    user_id = _read_int("id: ")
    try:
        record = select_record(user_id = user_id)
        print(record)
    except ValueError as exc:
        print(f"Ошибка: {exc}, проверьте корректность вводимых данных")

def _find_users_by_filter() -> None:
    print("\nПоиск по фильтру (Enter = пропустить поле)")

    user_id = _read_optional_int("id: ")
    name = input("first_name: ").strip() or None
    sec_name = input("second_name: ").strip() or None
    age = _read_optional_int("age: ")
    phone_num = input("phone_number: ").strip() or None

    try:
        records = select_record(
            user_id=user_id,
            name=name,
            sec_name=sec_name,
            age=age,
            phone_num=phone_num,
        )
        _print_records(records)
    except ValueError as exc:
        print(f"Ошибка: {exc}, проверьте корректность вводимых данных")

def _delete_user():
    user_id = _read_optional_int("id: ")
    try:
        lst = delete_record(user_id)
        print(f"Запись с номером {lst} удалена")
    except ValueError as exc:
        print(f"Ошибка: {exc}, проверьте корректность вводимых данных")

def run() -> None:
    while True:
        _print_menu()

        action = input("Выберите действие: ").strip()

        if action == "1":
            _add_user()

        elif action == "2":
            _update_user()

        elif action == "3":
            _find_user()

        elif action == "4":
            _show_all_users()

        elif action == "5":
           _delete_user()

        elif action == "6":
           _find_users_by_filter

        elif action == "0":
            print("Выход из программы.")
            break

        else:
            print("Неизвестная команда. Повторите ввод.")
