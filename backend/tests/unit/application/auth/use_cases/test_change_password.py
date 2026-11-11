import pytest

from src.backend.application.auth.dtos.change_password import ChangePasswordCommand
from tests.unit.domain.user.test_entity import user_id


# @pytest.fixture
# def change_password_command(user_id):
#     return ChangePasswordCommand(
#         user_id=user_id,
#
#     )
