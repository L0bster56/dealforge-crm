import pytest

from src.backend.domain.shared.value_objects.email.errors import InvalidEmailError
from src.backend.domain.shared.value_objects.email.value_object import Email


@pytest.fixture
def test_email():
    return Email("testuser@gmail.com")

@pytest.mark.parametrize(
    "value, expected",
    [
        ("test.user@gmail.com", "test.user@gmail.com"),
        ("example123@yahoo.com", "example123@yahoo.com"),
        ("user_name@outlook.com", "user_name@outlook.com"),
        ("my-email@mail.ru", "my-email@mail.ru"),
        ("hello.world@company.org", "hello.world@company.org"),
        ("user2025@test.net", "user2025@test.net"),
        ("first.last@domain.co", "first.last@domain.co"),
        ("simple@mail.com", "simple@mail.com"),
        ("name.surname123@service.io", "name.surname123@service.io"),
        ("x_y-z@sub.domain.com", "x_y-z@sub.domain.com"),
    ]
)
def test_valid_email(value, expected):
    assert Email(value).value == expected


@pytest.mark.parametrize(
    "value",
    [
        "plainaddress",  # нет @
        "@no-local-part.com",  # нет имени до @
        "user@",  # нет домена
        "user@.com",  # домен начинается с точки
        "user@com",  # нет точки в домене
        "user@domain..com",  # двойная точка
        "user@@domain.com",  # два @
        "user domain@domain.com",  # пробел внутри
        "user#domain.com",  # нет @ вообще
        "user@domain,com"  # запятая вместо точки
    ]
)
def test_invalid_email(value):
    with pytest.raises(InvalidEmailError):
        Email(value)