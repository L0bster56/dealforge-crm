import pytest

from src.backend.domain.user.value_objects.username.errors import UnSupportedUsernameTypeError, \
    InvalidUsernameLengthError, InvalidUsernameFormatError
from src.backend.domain.user.value_objects.username.value_object import Username


@pytest.fixture
def test_username():
    return Username("testuser")

@pytest.mark.parametrize(
    "value, expected",
    [
        ("user123", "user123"),
        ("alex_dev", "alex_dev"),
        ("boburbek", "boburbek"),
        ("python_senior", "python_senior"),
        ("admin_99", "admin_99"),
        ("my_super_login", "my_super_login"),
        ("uzb_developer", "uzb_developer"),
        ("test_user_account", "test_user_account"),
        ("it_specialist", "it_specialist"),
        ("fastapi_master", "fastapi_master")
    ]
)
def test_valid_username(value, expected):
    assert Username(value).value == expected


@pytest.mark.parametrize(
    "value",
    [
        1,
        [1, 2],
        True,
        1.6,
    ]
)
def test_unsupported_username(value):
    with pytest.raises(UnSupportedUsernameTypeError):
        Username(value)


@pytest.mark.parametrize(
    "value",
    [
        "a",
        "a1",
        "aa",
        "a" * 256,
        "username" * 100
    ]
)
def test_invalid_username_length(value):
    with pytest.raises(InvalidUsernameLengthError):
        Username(value)


@pytest.mark.parametrize(
    "value",
    [
        "1username",
        "_user123",
        "777python",
        "user.name",
        "alex-dev",
        "hello world",
        "user@name",
        "admin!",
        "dev#ops",
        "user_тест",
        "my-name-123",
        "user/name",
        "active.user",
    ]
)
def test_invalid_username_format(value):
    with pytest.raises(InvalidUsernameFormatError):
        Username(value)