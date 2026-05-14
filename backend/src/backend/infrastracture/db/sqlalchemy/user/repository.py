from uuid import UUID

from sqlalchemy import select, exists, delete, and_

from backend.infrastracture.db.sqlalchemy.core.repository import SQLAlchemyRepository
from src.backend.application.user.repository import UserRepository
from src.backend.domain.shared.value_objects.email.value_object import Email
from src.backend.domain.shared.value_objects.name.value_object import Name
from src.backend.domain.user.entity import User
from src.backend.domain.user.value_objects.username.value_object import Username
from src.backend.infrastracture.db.sqlalchemy.user.models import UserModel


def to_model(user: User) -> UserModel:
    return UserModel(
        id=user.id,
        first_name=str(user.first_name),
        last_name=str(user.last_name),
        email=str(user.email),
        username=str(user.username),
        password_hash=user.password_hash,
        last_interaction=user.last_interaction,
        created_at=user.created_at,
        updated_at=user.updated_at,
        is_active=user.is_active,
        role=user.role
    )


def to_entity(user: UserModel) -> User:
    return User(
        id=user.id,
        first_name=Name(user.first_name),
        last_name=Name(user.last_name),
        email=Email(user.email),
        username=Username(user.username),
        password_hash=user.password_hash,
        last_interaction=user.last_interaction,
        created_at=user.created_at,
        updated_at=user.updated_at,
        is_active=user.is_active,
        role=user.role
    )


class SqlAlchemyUserRepository(SQLAlchemyRepository, UserRepository):

    async def get_by_id(self, user_id: UUID) -> User:
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        return to_entity(user) if user else None

    async def get_by_username(self, username: str) -> User:
        stmt = select(UserModel).where(UserModel.username == username.lower())
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
        await self.session.merge(user)
        await self.session.flush()

    async def delete(self, user: User) -> None:
        stmt = delete(UserModel).where(UserModel.id == user.id)
        await self.session.execute(stmt)
        await self.session.flush()

    async def exists_username(self, username: str, user_id: UUID = None) -> bool:
        condition = UserModel.username == username
        if user_id:
            condition = and_(condition, UserModel.id != user_id)
        stmt = select(exists().where(condition))
        result = await self.session.execute(stmt)
        return result.scalar()

    async def exists_email(self, email: str, user_id: UUID = None) -> bool:
        condition = UserModel.email == email
        if user_id:
            condition = and_(condition, UserModel.id != user_id)
        stmt = select(exists().where(condition))
        result = await self.session.execute(stmt)
        return result.scalar()
