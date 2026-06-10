from abc import ABC, abstractmethod

type UserRecord = tuple[int, str, str, int, str]


class UserTableInterface(ABC):
    @abstractmethod
    def create_record(
        self,
        id: int,
        first_name: str,
        second_name: str,
        age: int,
        phone: str,
    ) -> UserRecord:
        pass

    @abstractmethod
    def select_record(
        self,
        id: int | None = None,
        first_name: str | None = None,
        second_name: str | None = None,
        age: int | None = None,
        phone: str | None = None,
    ) -> list[UserRecord]:
        pass

    @abstractmethod
    def update_record(
        self,
        id: int | None = None,
        first_name: str | None = None,
        second_name: str | None = None,
        age: int | None = None,
        phone: str | None = None,
    ) -> UserRecord:
        pass

    @abstractmethod
    def delete_record(self, id: int) -> UserRecord:
        pass
