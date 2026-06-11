import unittest

import src.db.backend.errors as errors
from src.db.backend.memory import UserTable

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
                with self.assertRaises(errors.Invaluser_idAgeError) as context:
                    self.user_table.create_record(*test_case)
        self.assertEqual(str(context.exception), err_mesage)

    def test_create_record_invaluser_id_phone_number(self):
        cases = [
            (1, "Loh", "Lohov", 23, "+1b3456a890"),
            (2, "Tupac", "Shakur", 25, "*ACAB"),
            (3, "Pasha", "Tehnik", 40, "ti po-moemu pereputal"),
            (4, "Marik", "Marrakesh", 35, "+YHHB")
        ]

        err_mesage = "Некорректный номер телефона"

        for test_case in cases:
            with self.subTest(test_data = test_case):
                with self.assertRaises(errors.Invaluser_idPhoneError) as context:
                    self.user_table.create_record(*test_case)
        self.assertEqual(str(context.exception), err_mesage)

    def test_create_record_duplicate_user_id(self):
        test_case_1 = (1, "Sanya", "Pushkin", 18, "1234567890")
        test_case_2 = (1, "Serega", "Colotushkin", 81, "0987654321")

        err_message = "Такое user_id уже существует"
        self.user_table.create_record(*test_case_1)

        with self.assertRaises(errors.Duplicateuser_idError) as context:
                self.user_table.create_record(*test_case_2)
        self.assertEqual(str(context.exception), err_message)

    def test_select_record(self):
        test_datas = [
            (1, "Ja", "Morant", 26, "+12"),
            (2, "Giannis", "Freak", 31, "+34"),
            (3, "Kobe", "Bryant", 41, "+13"),
            (4, "James", "Harden", 36, "+1"),
            (5, "Artem", "Apchihba", 26, "+34"),
        ]

        for test_data in test_datas:
            self.user_table.create_record(*test_data)

        cases = [
            {
                "name": "Выбор без фильтров",
                "filters": [None, None, None, None, None],
                "expected": test_datas,
            },
            {
                "name": "Фильтр по user_id",
                "filters": [1, None, None, None, None],
                "expected": [test_datas[0]],
            },
            {
                "name": "Фильтр по имени",
                "filters": [None, "Giannis", None, None, None],
                "expected": [test_datas[1]],
            },
            {
                "name": "Фильтр по фамилии",
                "filters": [None, None, "Bryant", None, None],
                "expected": [test_datas[2]],
            },
            {
                "name": "Фильтр по возрасту",
                "filters": [None, None, None, 26, None],
                "expected": [test_datas[0], test_datas[4]],
            },
            {
                "name": "Фильтр по номеру телефона",
                "filters": [None, None, None, None, "+34"],
                "expected": [
                    test_datas[1],
                    test_datas[4],
                ],
            },
        ]

        for case in cases:
            with self.subTest(
                case=case["name"], filters=case["filters"], expected=case["expected"]
            ):
                records = self.user_table.select_record(*case["filters"])
                self.assertEqual(records, case["expected"])
    
    def test_delete_record(self):
        case_1 = (1, "Ja", "Morant", 26, "+12")
        case_2 = (2, "Giannis", "Freak", 31, "+34")
        result = [(1, "Ja", "Morant", 26, "+12")]

        self.user_table.create_record(*case_1)
        self.user_table.create_record(*case_2)

        with self.subTest(test_data = case_1):
            self.user_table.delete_record(2)
            remain = self.user_table.select_record()
            self.assertEqual(result, remain)

    def test_delete_incorrect_user_id(self):
        case_1 = (1, "Ja", "Morant", 26, "+12")
        case_2 = (2, "Giannis", "Freak", 31, "+34")

        self.user_table.create_record(*case_1)
        self.user_table.create_record(*case_2)
        err_message = "Такого user_id не существует или оно уже удалено"

        with self.assertRaises(errors.Duplicateuser_idError) as context:
            self.user_table.delete_record(3)
        self.assertEqual(str(context.exception), err_message)

    def test_update_record(self):
        case_1 = (1, "Ja", "Morant", 26, "+12")
        case_2 = (2, "Ja", "Morant", 26, "+12")
        test_cases = [{
                        "upd": (1, "Giannis", "Freak", 31, "+34"),
                        "res": (1, "Giannis", "Freak", 31, "+34")
                       },
                       {
                        "upd": (2, None, None, 31, "+34"),
                        "res": (2, "Ja", "Morant", 31, "+34")
                       }]

        self.user_table.create_record(*case_1)
        self.user_table.create_record(*case_2)

        for test in test_cases:
            with self.subTest(test_data = test):
                rec = self.user_table.update_record(*test["upd"])
            self.assertEqual(test["res"], rec)

    def test_invaluser_id_update_record(self):
        case = (1, "Ja", "Morant", 26, "+12")
        test_cases = [{
                        "upd": (2, "Giannis", "Freak", 31, "+34"),
                        "err": "Такого user_id не существует или оно уже удалено",
                        "err_type": errors.Duplicateuser_idError
                       },
                       {
                        "upd": (1, "Giannis", "Freak", -31, "+34"),
                        "err": "Возраст не может быть отрицательным",
                        "err_type": errors.Invaluser_idAgeError
                       },
                       {
                        "upd": (1, "Giannis", "Freak", 31, "ACAB"),
                        "err": "Некорректный номер телефона",
                        "err_type": errors.Invaluser_idPhoneError
                       }]

        self.user_table.create_record(*case)

        for case in test_cases:
            with self.assertRaises(case["err_type"]) as context:
                rec = self.user_table.update_record(*case["upd"])
        self.assertEqual(str(context.exception), case["err"])