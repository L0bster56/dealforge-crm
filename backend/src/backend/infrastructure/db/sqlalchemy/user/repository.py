from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.application.user.repository import UserRepository
from src.backend.domain.shared.value_objects.email.value_object import Email
from src.backend.domain.shared.value_objects.name.value_object import Name
from src.backend.domain.user.entity import User
from src.backend.domain.user.value_objects.username.value_object import Username
from src.backend.infrastructure.db.sqlalchemy.user.models import UserModel


# User -> UserModel
def to_model(user: User) -> UserModel:  # new *
    return UserModel(
        id=user.id,
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        password_hash=user.password_hash,
        last_interaction=user.last_interaction,
        created_at=user.created_at,
        updated_at=user.updated_at,
        is_active=user.is_active,
    )


# UserModel -> User
def to_entity(user: UserModel) -> User:  # new *
    return User(
        id=user.id,
        username=Username(user.username),
        email=Email(user.email),
        first_name=Name(user.first_name),
        last_name=Name(user.last_name),
        password_hash=user.password_hash,
        last_interaction=user.last_interaction,
        created_at=user.created_at,
        updated_at=user.updated_at,
        is_active=user.is_active,
    )


class SqlalchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: UUID) -> User:
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        return to_entity(user) if user else None

    async def get_by_username(self, username: str) -> User:
        stmt = select(UserModel).where(UserModel.username == username)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        return to_entity(user) if user else None

    async def get_by_email(self, email: str) -> User:
        stmt = select(UserModel).where(UserModel.email == email)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        return to_entity(user) if user else None

    async def create(self, user: User) -> User:
        user = to_model(user)
        self.session.add(user)
        await self.session.flush()
        return to_entity(user)

    async def update(self, user: User) -> None:
        user = to_model(user)
        self.session.add(user)
        await self.session.flush()

    async def delete(self, user: User) -> None:
        user = to_model(user)
        await self.session.delete(user)
        await self.session.flush()
