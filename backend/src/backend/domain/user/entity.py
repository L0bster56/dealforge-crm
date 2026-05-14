import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum

from backend.domain.shared.entity import BaseEntity
from backend.domain.shared.mixins import TimeActionMixin
from src.backend.domain.shared.value_objects.email.value_object import Email
from src.backend.domain.shared.value_objects.name.value_object import Name
from src.backend.domain.user.value_objects.username.value_object import Username


class UserRole(StrEnum):
    """
    Роли пользователя в системе.

    Attributes:
        consultant: обычный пользователь (по умолчанию)
        sales_manager: менеджер продаж
        director: руководитель
        admin: администратор системы
    """
    consultant = "consultant"
    sales_manager = "sales_manager"
    director = "director"
    admin = "admin"


@dataclass
class User(BaseEntity, TimeActionMixin):
    """
    Домашняя (domain) сущность пользователя.

    Содержит основную информацию о пользователе:
    идентификацию, профиль, роль и состояние активности.

    Attributes:
        id: уникальный идентификатор пользователя
        first_name: имя (Value Object)
        last_name: фамилия (Value Object)
        username: уникальный username (Value Object)
        email: email пользователя (Value Object)
        password_hash: захешированный пароль
        last_interaction: время последней активности
        is_active: активен ли пользователь
        role: роль пользователя
        created_at: дата создания
        updated_at: дата обновления
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

    @property
    def full_name(self) -> str:
        """
        Возвращает полное имя пользователя.

        Returns:
            строка вида "Имя Фамилия"
        """
        return f"{self.first_name} {self.last_name}"

    def interact(self) -> None:
        """
        Обновляет время последней активности пользователя.
        """
        self.last_interaction = datetime.now()

    def is_active_user(self) -> bool:
        """
        Проверяет, активен ли пользователь.

        Returns:
            True если активен, иначе False
        """
        return self.is_active

    @classmethod
    def create(
        cls,
        first_name: str,
        last_name: str,
        username: str,
        email: str,
        password_hash: str,
        role: UserRole = UserRole.consultant
    ) -> "User":
        """
        Фабричный метод создания пользователя.

        Args:
            first_name: имя пользователя
            last_name: фамилия пользователя
            username: уникальный username
            email: email
            password_hash: уже захешированный пароль
            role: роль пользователя

        Returns:
            объект User
        """
        return cls(
            id=uuid.uuid4(),
            first_name=Name(first_name),
            last_name=Name(last_name),
            username=Username(username),
            email=Email(email),
            password_hash=password_hash,
            role=role
        )

    def change_password(self, new_password: str) -> None:
        """
        Изменяет пароль пользователя.

        Args:
            new_password: новый захешированный пароль
        """
        self.password_hash = new_password
        self._touch()

    def change_first_name(self, first_name: str) -> None:
        """
        Изменяет имя пользователя.

        Args:
            first_name: новое имя
        """
        self.first_name = Name(first_name)
        self._touch()

    def change_last_name(self, last_name: str) -> None:
        """
        Изменяет фамилию пользователя.

        Args:
            last_name: новая фамилия
        """
        self.last_name = Name(last_name)
        self._touch()

    def change_email(self, email: str) -> None:
        """
        Изменяет email пользователя.

        Args:
            email: новый email
        """
        self.email = Email(email)
        self._touch()

    def change_username(self, username: str) -> None:
        """
        Изменяет username пользователя.

        Args:
            username: новый username
        """
        self.username = Username(username)
        self._touch()