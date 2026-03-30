import pytest

from backend.domain.user.value_objects.username.errors import InvalidUsernameFormatError, UnSupportedUsernameTypeError, \
    InvalidUsernameLengthError
from backend.domain.user.value_objects.username.value_object import Username


@pytest.mark.parametrize(
    "value, expected",
    [
        ("John", "john"),
        ("Alice123", "alice123"),
        ("user_name", "user_name"),
        ("DevUser_1", "devuser_1"),
        ("TestUser999", "testuser999"),
    ]
)
def test_valid_username(value, expected):
    assert Username(value).value == expected


@pytest.mark.parametrize(
    "value",
    [
        1,
        ["sa"],
        True,
        1.6
    ]
)
def test_unsupported_type_username(value):
    with pytest.raises(UnSupportedUsernameTypeError):
        Username(value)


@pytest.mark.parametrize(
    "value",
    [
        "a",
        "user" * 70,
    ]
)
def test_username_too_long(value):
    with pytest.raises(InvalidUsernameLengthError):
        Username(value)


import pytest


@pytest.mark.parametrize(
    "value",
    [
        "1username",
        "_username",
        " user",
        "user ",
        "user name",
        "user-name",
        "user.name",
        "user@name",
        "user!",
        "user#",
    ]
)
def test_invalid_username_format(value):
    with pytest.raises(InvalidUsernameFormatError):
        Username(value)
