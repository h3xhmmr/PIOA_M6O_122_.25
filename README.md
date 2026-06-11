## М6О-122БВ-25

## Саенко Михаил Александрович

## База данных пользователей

Консольное приложение для CRUD-операций над записями пользователей. Поддерживаются три варианта хранения: in-memory, JSON-файл и CSV-файл.

### Основной функционал

- CRUD-операции через единый интерфейс `UserTableInterface`
- Проверка ошибок: отрицательный возраст, некорректный номер телефона, дублирующийся id
- Обработка ошибок чтения, записи и повреждённых файловых данных
- Консольный интерфейс с выбором типа базы данных при запуске

### Структура проекта

```
task_python_1/
├── src/
│   ├── data/                  
│   └── db/
│       ├── backend/
│       │   ├── __init__.py
│       │   ├── errors.py # типы ошибок,их обработка
│       │   ├── interface.py # интерфейс для работы с БД
│       │   ├── memory.py # in-memory логика
│       │   ├── file.py # json логика
│       │   └── csv_file.py # csv логика
│       └── endpoints/ # интерфейс
│           ├── __init__.py
│           ├── __main__.py    
│           └── tui.py         
└── test/ # тесты
    ├── __init__.py
    ├── test_memory.py
    ├── test_file.py
    └── test_csv_file.py
```


### Реализации хранения


| Тип       | Класс              | Файл по умолчанию     |
| --------- | ------------------ | --------------------- |
| In-memory | `UserTable`        | —                     |
| JSON      | `FileUserTable`    | `src/data/users.json` |
| CSV       | `CsvFileUserTable` | `src/data/users.csv`  |


Запись пользователя: `(id, first_name, second_name, age, phone)`.

CSV-файл содержит заголовок `id,first_name,second_name,age,phone` и строки данных. При ошибках чтения/записи выбрасываются `StorageReadError` / `StorageWriteError`, при некорректном содержимом — `CorruptDataError`.

### Запуск

Требуется Python 3.14.3 и выше.

```bash
python -m src.db.endpoints
```

При старте выберите тип базы:

1. In-memory — данные только в оперативной памяти
2. Файловая (JSON) — сохранение в `src/data/users.json`
3. Файловая (CSV) — сохранение в `src/data/users.csv`

### Тесты

```bash
pytest --cov=src --cov-report=term-missing
```

Тесты покрывают in-memory, JSON и CSV реализации, включая сценарии с повреждёнными файлами и ошибками ввода-вывода.
![image.png]()