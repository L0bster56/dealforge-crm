from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv
from starlette import status

from src.backend.application.user.dtos.create_user import CreateUserCommand, CreateUserResult
from src.backend.application.user.dtos.delete_user import DeleteUserCommand
from src.backend.application.user.dtos.get_user_by_id import GetUserByIdCommand, GetUserByIdResult
from src.backend.application.user.dtos.update_user import UpdateUserCommand
from src.backend.application.user.use_cases.create_user import CreateUserUseCase
from src.backend.application.user.use_cases.delete_user import DeleteUserUseCase
from src.backend.application.user.use_cases.get_user_by_id import GetUserByIdUseCase
from src.backend.application.user.use_cases.update_user import UpdateUserUseCase
from src.backend.domain.shared.specification import Specification
from src.backend.domain.user.entity import User
from src.backend.infrastracture.db.sqlalchemy.core.uow import SqlAlchemyUnitOfWork
from src.backend.infrastracture.security.argon2.hasher import Argon2Hasher
from src.backend.presentation.api.v1.auth.dependencies import get_current_user, get_hasher, get_password_spec
from src.backend.presentation.api.v1.core.dependencies import get_uow

router= APIRouter(
    prefix="/users",
    tags=["user"]
)

@cbv(router)
class UserRouter:
    uow: SqlAlchemyUnitOfWork = Depends(get_uow)
    user: User = Depends(get_current_user)

    @router.post(
        "/",
        name="Создание пользователя",
        status_code=status.HTTP_201_CREATED,
        response_model=CreateUserResult,
    )
    async def create_user(
            self,
            request: CreateUserCommand,
            hasher: Argon2Hasher = Depends(get_hasher),
            password_spec: Specification[str] = Depends(get_password_spec),
    ):
        uc = CreateUserUseCase(
            uow=self.uow,
            hasher=hasher,
            password_spec=password_spec,
            actor=self.user
        )
        response = await uc.execute(
            cmd=request
        )
        return response


    @router.delete(
        "/{user_id}",
        name="Удаление пользователя",
        status_code=status.HTTP_200_OK,
    )
    async def delete_user(
            self,
            user_id: UUID,
    ):
        uc = DeleteUserUseCase(
            uow=self.uow,
            actor=self.user
        )
        cmd = DeleteUserCommand(user_id=user_id)
        await uc.execute(cmd=cmd)


    @router.get(
        "/{user_id}",
        name="Получение пользователя по ИД",
        status_code=status.HTTP_200_OK,
        response_model=GetUserByIdResult
    )
    async def get_user_by_id(
            self,
            user_id: UUID
    ):
        uc = GetUserByIdUseCase(
            uow=self.uow,
        )
        cmd = GetUserByIdCommand(user_id=user_id)
        response = await uc.execute(cmd=cmd)
        return response


    @router.patch(
        "/{user_id}",
        name="Изменение пользователя",
        status_code=status.HTTP_200_OK,
    )
    async def update_user(
            self,
            user_id: UUID,
            request: UpdateUserCommand,
    ):
        uc = UpdateUserUseCase(
            uow=self.uow,
            actor=self.user
        )
        response = await uc.execute(
            user_id=user_id,
            cmd=request
        )