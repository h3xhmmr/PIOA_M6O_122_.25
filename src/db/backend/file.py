import json
from pathlib import Path

from . import errors
from .interface import UserRecord
from .interface import UserTableInterface
from .memory import UserTable

DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "users.json"

COLUMNS = ["user_id", "first_name", "second_name", "age", "phone"]


class FileUserTable(UserTableInterface):
    def __init__(self, file_path: str | Path | None = None):
        self._file_path = Path(file_path) if file_path is not None else DEFAULT_DB_PATH
        self._storage = UserTable()
        self._load()

    def _is_valuser_id_record(self, item: object) -> bool:
        return (
            isinstance(item, (list, tuple))
            and len(item) == 5
            and isinstance(item[0], int)
            and isinstance(item[1], str)
            and isinstance(item[2], str)
            and isinstance(item[3], int)
            and isinstance(item[4], str)
        )

    def _load(self) -> None:
        if not self._file_path.exists():
            return

        try:
            raw = self._file_path.read_text(encoding="utf-8")
        except OSError as exc:
            raise errors.StorageReadError(
                f"Не удалось прочитать файл базы данных: {exc}"
            ) from exc

        if not raw.strip():
            return

        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise errors.CorruptDataError(
                f"Повреждённые данные в файле базы данных: {exc}"
            ) from exc

        if not isinstance(data, dict):
            raise errors.CorruptDataError(
                "Некорректная запись"
            )
        if "columns" not in data or "records" not in data:
            raise errors.CorruptDataError(
                "Некорректный формат данных"
            )
        if data["columns"] != COLUMNS:
            raise errors.CorruptDataError(
                f"Несовместимый набор столбцов: ожидается {COLUMNS}, получено {data['columns']}"
            )
        if not isinstance(data["records"], list):
            raise errors.CorruptDataError("Поле 'records' должно быть списком")

        records: list[UserRecord] = []
        for idx, record_dict in enumerate(data["records"]):
            if not isinstance(record_dict, dict):
                raise errors.CorruptDataError(
                    f"Запись {idx} не является объектом JSON"
                )
            try:
                record_tuple = tuple(record_dict[col] for col in COLUMNS)
            except KeyError as e:
                raise errors.CorruptDataError(
                    f"В записи {idx} отсутствует поле {e}"
                ) from e
            if not self._is_valuser_id_record(record_tuple):
                raise errors.CorruptDataError(
                    f"Запись {idx} содержит некорректные типы данных"
                )
            records.append(record_tuple)

        validate_error = errors.validate_table(records)
        if validate_error is not None:
            raise validate_error
        self._storage = UserTable()
        self._storage._user_table.extend(records)

    def _save(self) -> None:
        """Сохраняет текущие записи в JSON-файл в формате {"columns": [...], "records": [...]}."""
        try:
            self._file_path.parent.mkdir(parents=True, exist_ok=True)
            records = self._storage.select_record()  # список кортежей
            records_as_dicts = [dict(zip(COLUMNS, record)) for record in records]
            data_to_save = {"columns": COLUMNS, "records": records_as_dicts}
            self._file_path.write_text(
                json.dumps(data_to_save, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        except OSError as exc:
            raise errors.StorageWriteError(
                f"Не удалось записать файл базы данных: {exc}"
            ) from exc

    def create_record(
        self,
        user_id: int,
        first_name: str,
        second_name: str,
        age: int,
        phone: str,
    ) -> UserRecord:
        record = self._storage.create_record(user_id, first_name, second_name, age, phone)
        self._save()
        return record

    def select_record(
        self,
        user_id: int | None = None,
        first_name: str | None = None,
        second_name: str | None = None,
        age: int | None = None,
        phone: str | None = None,
    ) -> list[UserRecord]:
        return self._storage.select_record(
            user_id=user_id,
            first_name=first_name,
            second_name=second_name,
            age=age,
            phone=phone,
        )

    def update_record(
        self,
        user_id: int | None = None,
        first_name: str | None = None,
        second_name: str | None = None,
        age: int | None = None,
        phone: str | None = None,
    ) -> UserRecord:
        record = self._storage.update_record(
            user_id=user_id,
            first_name=first_name,
            second_name=second_name,
            age=age,
            phone=phone,
        )
        self._save()
        return record

    def delete_record(self, user_id: int) -> UserRecord:
        record = self._storage.delete_record(user_id)
        self._save()
        return record