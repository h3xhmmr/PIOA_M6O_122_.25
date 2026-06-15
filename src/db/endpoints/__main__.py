from src.db.backend.csv_file import CsvFileUserTable
from src.db.backend.file import FileUserTable
from src.db.backend.memory import UserTable

from .tui import Application


def _choose_user_base():
    print("\n====== Выбор базы данных ======")
    print("1. In-memory")
    print("2. Файловая (JSON)")
    print("3. Файловая (CSV)")

    while True:
        choice = input("Выберите тип базы данных: ").strip()

        if choice == "1":
            return UserTable()

        if choice == "2":
            return FileUserTable()

        if choice == "3":
            return CsvFileUserTable()

        print("Неизвестная команда. Повторите ввод.")


def main():
    app = Application(user_base=_choose_user_base())
    app.run()


if __name__ == "__main__":
    main()
