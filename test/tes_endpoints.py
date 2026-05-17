import unittest
from src.db.endpoints.tui import Application

class TestApplication(unittest.TestCase):
    def setUp(self):
        self.Application = Application()
        self.assertIsInstance(self.Application, Application)

    def test_print_menu(self):
        message = """\n====== База пользователей ======
        1. Добавить запись
        2. Обновить данные пользователя
        3. Найти запись по id
        4. Показать все записи
        5. Удалить пользователя
        6. Найти запись по фильтру
        0. Выйти"""
        self.assertEqual(message, self.Application.print_menu())

    def test_create_user(self):
        cases = [
            (1, "Loh", "Lohov", 69, "+4201488"),
            (2, "Tupac", "Shakur", 25, "+1312"),
            (3, "Pasha", "Tehnik", 40, "+228"),
            (4, "Marik", "Marrakesh", 35, "+375")
        ]

        for test_case in cases:
            with self.subTest(test_data = test_case):
                record = self.Application.create_user(*test_case)
                self.assertEqual(record, test_case)

    def test_create_user_negative_age(self):
        cases = [
            (1, "Loh", "Lohov", -23, "+1234567890"),
            (2, "Tupac", "Shakur", -25, "+1312"),
            (3, "Pasha", "Tehnik", -40, "+228"),
            (4, "Marik", "Marrakesh", -35, "+375")
        ]

        err_mesage = "Возраст не может быть отрицательным"

        for test_case in cases:
            self.assertEqual(self.Application.create_user(*test_case), err_mesage)
