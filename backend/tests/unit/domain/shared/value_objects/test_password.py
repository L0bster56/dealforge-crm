import pytest

from src.backend.application.auth.dtos.change_password import ChangePasswordCommand


@pytest.fixture()
def change_password_command(user_id):
    return ChangePasswordCommand(
        user_id=user_id
    )