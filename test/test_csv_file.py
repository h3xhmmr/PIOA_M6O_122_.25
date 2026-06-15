import unittest
from pathlib import Path

import src.db.backend.errors as errors
from src.db.backend.csv_file import CsvFileUserTable

TEST_DB_PATH = Path(__file__).parent / "test_db.csv"
CSV_HEADER = "user_id,first_name,second_name,age,phone\n"


class TestCsvFileUserTable(unittest.TestCase):
    def setUp(self):
        if TEST_DB_PATH.exists():
            TEST_DB_PATH.unlink()
        self.user_table = CsvFileUserTable(TEST_DB_PATH)
        self.assertIsInstance(self.user_table, CsvFileUserTable)

    def tearDown(self):
        if TEST_DB_PATH.exists():
            TEST_DB_PATH.unlink()

    def test_create_record(self):
        cases = [
            (1, "Loh", "Lohov", 69, "+4201488"),
            (2, "Tupac", "Shakur", 25, "+1312"),
            (3, "Pasha", "Tehnik", 40, "+228"),
            (4, "Marik", "Marrakesh", 35, "+375"),
        ]

        for test_case in cases:
            with self.subTest(test_data=test_case):
                record = self.user_table.create_record(*test_case)
                self.assertEqual(record, test_case)

    def test_create_record_negative_age(self):
        cases = [
            (1, "Loh", "Lohov", -23, "+1234567890"),
            (2, "Tupac", "Shakur", -25, "+1312"),
            (3, "Pasha", "Tehnik", -40, "+228"),
            (4, "Marik", "Marrakesh", -35, "+375"),
        ]

        err_message = "Возраст не может быть отрицательным"

        for test_case in cases:
            with self.subTest(test_data=test_case):
                with self.assertRaises(errors.InvalidAgeError) as context:
                    self.user_table.create_record(*test_case)
        self.assertEqual(str(context.exception), err_message)

    def test_create_record_invaluser_id_phone_number(self):
        cases = [
            (1, "Loh", "Lohov", 23, "+1b3456a890"),
            (2, "Tupac", "Shakur", 25, "*ACAB"),
            (3, "Pasha", "Tehnik", 40, "ti po-moemu pereputal"),
            (4, "Marik", "Marrakesh", 35, "+YHHB"),
        ]

        err_message = "Некорректный номер телефона"

        for test_case in cases:
            with self.subTest(test_data=test_case):
                with self.assertRaises(errors.InvalidPhoneError) as context:
                    self.user_table.create_record(*test_case)
        self.assertEqual(str(context.exception), err_message)

    def test_create_record_duplicate_user_id(self):
        test_case_1 = (1, "Sanya", "Pushkin", 18, "1234567890")
        test_case_2 = (1, "Serega", "Colotushkin", 81, "0987654321")

        err_message = "Такое user_id уже существует"
        self.user_table.create_record(*test_case_1)

        with self.assertRaises(errors.DuplicateIdError) as context:
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
                "expected": [test_datas[1], test_datas[4]],
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

        with self.subTest(test_data=case_1):
            self.user_table.delete_record(2)
            remain = self.user_table.select_record()
            self.assertEqual(result, remain)

    def test_delete_incorrect_user_id(self):
        case_1 = (1, "Ja", "Morant", 26, "+12")
        case_2 = (2, "Giannis", "Freak", 31, "+34")

        self.user_table.create_record(*case_1)
        self.user_table.create_record(*case_2)
        err_message = "Такого user_id не существует или оно уже удалено"

        with self.assertRaises(errors.DuplicateIdError) as context:
            self.user_table.delete_record(3)
        self.assertEqual(str(context.exception), err_message)

    def test_update_record(self):
        case_1 = (1, "Ja", "Morant", 26, "+12")
        case_2 = (2, "Ja", "Morant", 26, "+12")
        test_cases = [
            {
                "upd": (1, "Giannis", "Freak", 31, "+34"),
                "res": (1, "Giannis", "Freak", 31, "+34"),
            },
            {
                "upd": (2, None, None, 31, "+34"),
                "res": (2, "Ja", "Morant", 31, "+34"),
            },
        ]

        self.user_table.create_record(*case_1)
        self.user_table.create_record(*case_2)

        for test in test_cases:
            with self.subTest(test_data=test):
                rec = self.user_table.update_record(*test["upd"])
            self.assertEqual(test["res"], rec)

    def test_invaluser_id_update_record(self):
        case = (1, "Ja", "Morant", 26, "+12")
        test_cases = [
            {
                "upd": (2, "Giannis", "Freak", 31, "+34"),
                "err": "Такого user_id не существует или оно уже удалено",
                "err_type": errors.DuplicateIdError,
            },
            {
                "upd": (1, "Giannis", "Freak", -31, "+34"),
                "err": "Возраст не может быть отрицательным",
                "err_type": errors.InvalidAgeError,
            },
            {
                "upd": (1, "Giannis", "Freak", 31, "ACAB"),
                "err": "Некорректный номер телефона",
                "err_type": errors.InvalidPhoneError,
            },
        ]

        self.user_table.create_record(*case)

        for case in test_cases:
            with self.assertRaises(case["err_type"]) as context:
                self.user_table.update_record(*case["upd"])
        self.assertEqual(str(context.exception), case["err"])

    def test_load_from_file(self):
        record = (1, "Ja", "Morant", 26, "+12")
        self.user_table.create_record(*record)

        reloaded = CsvFileUserTable(TEST_DB_PATH)
        self.assertEqual(reloaded.select_record(), [record])

    def test_save_to_file(self):
        self.assertFalse(TEST_DB_PATH.exists())
        self.user_table.create_record(1, "Ja", "Morant", 26, "+12")
        self.assertTrue(TEST_DB_PATH.exists())

        content = TEST_DB_PATH.read_text(encoding="utf-8")
        self.assertIn(CSV_HEADER.strip(), content)
        self.assertIn("Ja,Morant,26,+12", content)

    def test_empty_file(self):
        TEST_DB_PATH.write_text("", encoding="utf-8")
        table = CsvFileUserTable(TEST_DB_PATH)
        self.assertEqual(table.select_record(), [])

    def test_missing_file(self):
        missing_path = Path(__file__).parent / "missing_db.csv"
        table = CsvFileUserTable(missing_path)
        self.assertEqual(table.select_record(), [])
        if missing_path.exists():
            missing_path.unlink()

    def test_invaluser_id_header(self):
        TEST_DB_PATH.write_text("user_user_id,name,surname,years,tel\n", encoding="utf-8")

        with self.assertRaises(errors.CorruptDataError) as context:
            CsvFileUserTable(TEST_DB_PATH)

        self.assertIn("Некорректный формат заголовка", str(context.exception))

    def test_invaluser_id_record_type(self):
        TEST_DB_PATH.write_text(
            CSV_HEADER + "1,Ja,Morant,twenty-six,+12\n",
            encoding="utf-8",
        )

        with self.assertRaises(errors.CorruptDataError) as context:
            CsvFileUserTable(TEST_DB_PATH)

        self.assertIn("неверный тип данных", str(context.exception))

    def test_invaluser_id_record_missing_field(self):
        TEST_DB_PATH.write_text(
            "user_id,first_name,second_name,age\n1,Ja,Morant,26\n",
            encoding="utf-8",
        )

        with self.assertRaises(errors.CorruptDataError) as context:
            CsvFileUserTable(TEST_DB_PATH)

        self.assertIn("Некорректный формат заголовка", str(context.exception))

    def test_read_error(self):
        dir_path = Path(__file__).parent / "test_db_csv_dir"
        dir_path.mkdir(exist_ok=True)

        try:
            with self.assertRaises(errors.StorageReadError) as context:
                CsvFileUserTable(dir_path)
            self.assertIn("Не удалось прочитать CSV-файл", str(context.exception))
        finally:
            dir_path.rmdir()

    def test_write_error(self):
        dir_path = Path(__file__).parent / "test_db_csv_dir"
        dir_path.mkdir(exist_ok=True)

        try:
            self.user_table._file_path = dir_path
            with self.assertRaises(errors.StorageWriteError) as context:
                self.user_table.create_record(1, "Ja", "Morant", 26, "+12")
            self.assertIn("Не удалось записать CSV-файл", str(context.exception))
        finally:
            dir_path.rmdir()

    def test_delete_persists_to_file(self):
        self.user_table.create_record(1, "Ja", "Morant", 26, "+12")
        self.user_table.create_record(2, "Giannis", "Freak", 31, "+34")
        self.user_table.delete_record(2)

        reloaded = CsvFileUserTable(TEST_DB_PATH)
        self.assertEqual(
            reloaded.select_record(),
            [(1, "Ja", "Morant", 26, "+12")],
        )

    def test_update_persists_to_file(self):
        self.user_table.create_record(1, "Ja", "Morant", 26, "+12")
        self.user_table.update_record(1, "Giannis", "Freak", 31, "+34")

        reloaded = CsvFileUserTable(TEST_DB_PATH)
        self.assertEqual(
            reloaded.select_record(),
            [(1, "Giannis", "Freak", 31, "+34")],
        )
