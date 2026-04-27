import unittest

from db.backend.memory import UserTableError, InvalidAgeError, InvalidPhoneNumberError, DuplicateIDError
from db.backend.memory import DB, UserTable

class TestUserTable(unittest.TestCase):
    def setUp(self):
        self.user_table = UserTable()
        self.assertIsInstance(self.user_table, UserTable)

    def test_create_record(self):
        cases = [
            (1, "Loh", "Lohov", 69, "+4201488"),
            (2, "Tupac", "Shakur", 25, "+1312"),
            (3, "Pasha", "Tehnik", 40, "+228"),
            (4, "Marik", "Marrakesh", 35, "+375")
        ]

        for test_case in cases:
            with self.subTest(test_data = test_case):
                record = self.user_table.create_record(*test_case)
                self.assertEqual(record, test_case)

    def test_create_record_negative_age(self):
        cases = [
            (1, "Loh", "Lohov", -23, "+1234567890"),
            (2, "Tupac", "Shakur", -25, "+1312"),
            (3, "Pasha", "Tehnik", -40, "+228"),
            (4, "Marik", "Marrakesh", -35, "+375")
        ]

        err_mesage = "Возраст не может быть отрицательным"

        for test_case in cases:
            with self.subTest(test_data = test_case):
                with self.assertRaises(InvalidAgeError) as context:
                    self.user_table.create_record(*test_case)
        self.assertEqual(str(context.exception), err_mesage)

    def test_create_record_invalid_phone_number(self):
        cases = [
            (1, "Loh", "Lohov", 23, "+1b3456a890"),
            (2, "Tupac", "Shakur", 25, "*ACAB"),
            (3, "Pasha", "Tehnik", 40, "ti po-moemu pereputal"),
            (4, "Marik", "Marrakesh", 35, "YHHB!")
        ]

        err_mesage = "Некорректный номер телефона"

        for test_case in cases:
            with self.subTest(test_data = test_case):
                with self.assertRaises(InvalidPhoneNumberError) as context:
                    self.user_table.create_record(*test_case)
        self.assertEqual(str(context.exception), err_mesage)

    def test_create_record_duplicate_id(self):
        test_case_1 = (1, "Sanya", "Pushkin", 18, "1234567890")
        test_case_2 = (1, "Serega", "Colotushkin", 81, "0987654321")

        err_message = "Запись с id = 1 уже существует"
        self.user_table.create_user(*test_case_1)

        with self.assertRaises(DuplicateIDError) as context:
                self.user_table.create_record(*test_case_2)
        self.assertEqual(str(context.exception), err_message)