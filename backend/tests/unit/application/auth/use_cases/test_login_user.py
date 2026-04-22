import pytest

from src.backend.application.auth.dtos.login_user import LoginUserCommand
from src.backend.application.auth.errors import AuthUserNotFoundError, InvalidPasswordError, InActiveUserError
from src.backend.application.auth.use_cases.login_user import LoginUserUseCase
from src.backend.domain.user.entity import User
from tests.unit.application.auth.interfaces.security.fake_hasher import FakeHasher
from tests.unit.application.auth.interfaces.security.fake_token import FakeTokenService
from tests.unit.application.shared.interfaces.fake_uow import FakeUnitOfWork
from tests.unit.domain.shared.value_objects.test_email import test_email
from tests.unit.domain.shared.value_objects.test_name import test_name
from tests.unit.domain.user.test_entity import valid_user, password_hash, user_id
from tests.unit.domain.user.value_objects.test_username import test_username


@pytest.fixture()
def login_user_command() -> LoginUserCommand:
    return LoginUserCommand(
        username="username",
        password="password"
    )

def make_use_case(user: User=None, password_match: bool = True) -> LoginUserUseCase:
    return LoginUserUseCase(
        uow=FakeUnitOfWork(user=user),
        tokens=FakeTokenService(),
        hasher=FakeHasher(result=password_match)
    )

# @pytest.mark.asyncio
# async def test_successful_login_user(login_user_command: LoginUserCommand, valid_user: User):
#     use_case = make_use_case(user=valid_user)
#     result = await use_case.execute(login_user_command)
#     assert result.access_token == f"token: {valid_user.id}"
#     assert result.refresh_token == f"token: {valid_user.id}"
#     assert result.token_type == "Bearer"


@pytest.mark.asyncio
async def test_login_user_not_found(login_user_command: LoginUserCommand):
    use_case = make_use_case(user=None)

    with pytest.raises(AuthUserNotFoundError):
        await use_case.execute(login_user_command)


@pytest.mark.asyncio
async def test_login_user_invalid_password(login_user_command: LoginUserCommand, valid_user: User):
    use_case = make_use_case(user=valid_user, password_match=False)

    with pytest.raises(InvalidPasswordError):
        await use_case.execute(login_user_command)


@pytest.mark.asyncio
async def test_login_user_inactive_user(login_user_command: LoginUserCommand, valid_user: User):
    valid_user.is_active = False
    use_case = make_use_case(user=valid_user)

    with pytest.raises(InActiveUserError):
        await use_case.execute(login_user_command)