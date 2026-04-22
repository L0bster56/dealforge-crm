import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime

from enum import StrEnum

from src.backend.domain.shared.value_objects.email.value_object import Email
from src.backend.domain.shared.value_objects.name.value_object import Name
from src.backend.domain.user.value_objects.username.value_object import Username


class UserRole(StrEnum):
    consultant = "consultant"
    sales_manager = "sales_manager"
    director = "director"
    admin = "admin"


@dataclass
class User:
    """
    Главная сущность пользователя
    """
    id: uuid.UUID
    first_name: Name
    last_name: Name
    username: Username
    email: Email
    password_hash: str
    last_interaction: datetime | None = None
    is_active: bool = field(default=True)
    role: UserRole = field(default=UserRole.consultant)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    @property
    def full_name(self) -> str:
        """
        Свойство которое возвращает полное имя пользователя
        """
        return f"{self.first_name} {self.last_name}"

    def touch(self) -> None:
        """
        Будет фиксировать время изменения
        """
        self.updated_at = datetime.now()

    def interact(self):
        """
        Будет фиксировать время последней активности
        """
        self.last_interaction = datetime.now()

    def endure_active(self):
        """
        Будет проверять что пользователь активен
        """
        return self.is_active

    @classmethod
    def create(
            cls,
            id: uuid.UUID,
            first_name: str,
            last_name: str,
            username: str,
            email: str,
            password_hash: str,
            role: UserRole = UserRole.consultant
    ):
        """
        Создает объект
        :param id: уникальный идентификатор
        :param first_name: имя пользователя
        :param last_name: фамилия пользователя
        :param username: юзернейм
        :param email: электронная почта
        :param password_hash: захешированный пароль
        :param role: роль пользователя
        :return: объект пользователя
        """
        return cls(
            id=id,
            first_name=Name(first_name),
            last_name=Name(last_name),
            username=Username(username),
            email=Email(email),
            password_hash=password_hash,
            role=role
        )

    def change_password(self, new_password: str):
        self.password_hash = new_password
        self.touch()


    def change_first_name(self, first_name: str):
        self.first_name = Name(first_name)
        self.touch()

    def change_last_name(self, last_name: str):
        self.last_name = Name(last_name)
        self.touch()

    def change_email(self, email: str):
        self.email = Email(email)
        self.touch()

    def change_username(self, username: str):
        self.username = Username(username)
        self.touch()

    def __hash__(self):
        return hash(self.id)


