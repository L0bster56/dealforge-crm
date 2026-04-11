from datetime import datetime
import uuid
from dataclasses import dataclass, field

from backend.domain.shared.value_objects.email.value_object import Email
from backend.domain.shared.value_objects.name.value_object import Name
from backend.domain.user.value_objects.username.value_object import Username


@dataclass
class User:
    """
    Главаная Сущность Пользователя
    """
    id: uuid.UUID
    first_name: Name
    last_name: Name
    username: Username
    email: Email
    password_hash: str
    last_interaction: datetime | None = None
    is_active: bool = field(default=True)
    created_at: datetime = field(default_factory=datetime.now)
    update_at: datetime = field(default_factory=datetime.now)

    @property
    def full_name(self) -> str:
        """
        Свойство, которое возвращает Полное Имя Пользователя
        :return:
        """
        return f"{self.first_name} {self.last_name}"

    def touch(self) -> None:
        """
        Будет фиксировать время изменения
        :return:
        """
        self.update_at = datetime.now()

    def interact(self):
        """
        Будет фиксировать время последней активности
        :return:
        """
        self.last_interaction = datetime.now()

    def ensure_active(self):
        """
        Будет проверять что пользователь наш активен
        :return:
        """
        if self.is_active:
            raise

    @classmethod
    def create(
            cls,
            id: uuid.UUID,
            first_name: str,
            last_name: str,
            username: str,
            email: str,
            password_hash: str,
    ):
        """
        Создает Объект Пользователя
        :param id: Уникальный Идентификатор
        :param first_name: Имя Пользователя
        :param last_name: Фамилия Пользователя
        :param username: Юзернейм
        :param email: Электронная Почта
        :param password_hash: 3aхешированный Пароль
        :return: Объект Пользователя
        """
        return cls(
            id=id,
            first_name=Name(first_name),
            last_name=Name(last_name),
            username=Username(username),
            email=Email(email),
            password_hash=password_hash,
        )

    def __hash__(self):
        return hash(self.id)

    def change_password(
            self,
            new_password: str,
    ):
        self.password_hash = new_password
        self.touch()
