import csv
from io import StringIO
from pathlib import Path

from . import errors
from .interface import UserRecord
from .interface import UserTableInterface
from .memory import UserTable

DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "users.csv"
CSV_FIELDNAMES = ("id", "first_name", "second_name", "age", "phone")


class CsvFileUserTable(UserTableInterface):
    def __init__(self, file_path: str | Path | None = None):
        self._file_path = Path(file_path) if file_path is not None else DEFAULT_DB_PATH
        self._storage = UserTable()
        self._load()

    def _parse_record(self, row: dict[str, str], line_number: int) -> UserRecord:
        missing_fields = [field for field in CSV_FIELDNAMES if field not in row]
        if missing_fields:
            raise errors.CorruptDataError(
                f"Некорректная запись в CSV-файле (строка {line_number}): "
                f"отсутствуют поля {', '.join(missing_fields)}"
            )

        try:
            record_id = int(row["id"])
            age = int(row["age"])
        except ValueError as exc:
            raise errors.CorruptDataError(
                f"Некорректная запись в CSV-файле (строка {line_number}): "
                f"неверный тип данных"
            ) from exc

        first_name = row["first_name"]
        second_name = row["second_name"]
        phone = row["phone"]

        if not isinstance(first_name, str) or not isinstance(second_name, str):
            raise errors.CorruptDataError(
                f"Некорректная запись в CSV-файле (строка {line_number})"
            )
        if not isinstance(phone, str):
            raise errors.CorruptDataError(
                f"Некорректная запись в CSV-файле (строка {line_number})"
            )

        return (record_id, first_name, second_name, age, phone)

    def _load(self) -> None:
        if not self._file_path.exists():
            return

        try:
            raw = self._file_path.read_text(encoding="utf-8")
        except OSError as exc:
            raise errors.StorageReadError(
                f"Не удалось прочитать CSV-файл базы данных: {exc}"
            ) from exc

        if not raw.strip():
            return

        try:
            reader = csv.DictReader(StringIO(raw))
        except csv.Error as exc:
            raise errors.CorruptDataError(
                f"Повреждённые данные в CSV-файле базы данных: {exc}"
            ) from exc

        if reader.fieldnames is None:
            raise errors.CorruptDataError("Некорректный формат данных в CSV-файле базы данных")

        normalized_fieldnames = [name.strip() for name in reader.fieldnames if name is not None]
        if normalized_fieldnames != list(CSV_FIELDNAMES):
            raise errors.CorruptDataError(
                "Некорректный формат заголовка в CSV-файле базы данных"
            )

        records: list[UserRecord] = []
        for line_number, row in enumerate(reader, start=2):
            if not any(value.strip() for value in row.values() if value is not None):
                continue
            records.append(self._parse_record(row, line_number))

        self._storage = UserTable()
        self._storage._user_table.extend(records)

    def _save(self) -> None:
        try:
            self._file_path.parent.mkdir(parents=True, exist_ok=True)
            buffer = StringIO()
            writer = csv.DictWriter(buffer, fieldnames=CSV_FIELDNAMES, lineterminator="\n")
            writer.writeheader()
            for record in self._storage.select_record():
                writer.writerow(
                    {
                        "id": record[0],
                        "first_name": record[1],
                        "second_name": record[2],
                        "age": record[3],
                        "phone": record[4],
                    }
                )
            self._file_path.write_text(buffer.getvalue(), encoding="utf-8")
        except OSError as exc:
            raise errors.StorageWriteError(
                f"Не удалось записать CSV-файл базы данных: {exc}"
            ) from exc

    def create_record(
        self,
        id: int,
        first_name: str,
        second_name: str,
        age: int,
        phone: str,
    ) -> UserRecord:
        record = self._storage.create_record(id, first_name, second_name, age, phone)
        self._save()
        return record

    def select_record(
        self,
        id: int | None = None,
        first_name: str | None = None,
        second_name: str | None = None,
        age: int | None = None,
        phone: str | None = None,
    ) -> list[UserRecord]:
        return self._storage.select_record(
            id=id,
            first_name=first_name,
            second_name=second_name,
            age=age,
            phone=phone,
        )

    def update_record(
        self,
        id: int | None = None,
        first_name: str | None = None,
        second_name: str | None = None,
        age: int | None = None,
        phone: str | None = None,
    ) -> UserRecord:
        record = self._storage.update_record(
            id=id,
            first_name=first_name,
            second_name=second_name,
            age=age,
            phone=phone,
        )
        self._save()
        return record

    def delete_record(self, id: int) -> UserRecord:
        record = self._storage.delete_record(id)
        self._save()
        return record
