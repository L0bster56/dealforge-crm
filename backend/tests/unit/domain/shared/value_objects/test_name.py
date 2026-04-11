import pytest

from src.backend.domain.shared.value_objects.name.errors import UnSupportedNameTypeError, InvalidNameLengthError, \
    InvalidNameFormatError
from src.backend.domain.shared.value_objects.name.value_object import Name

@pytest.fixture
def test_name():
    return Name("test")

@pytest.mark.parametrize(
    "value, expected",
    [
        ("Alex", "Alex"),
        ("john", "john"),
        ("USERNAME", "USERNAME"),
        ("TestName", "TestName"),
        ("Алексей", "Алексей"),
    ]
)
def test_valid_name(value, expected):
    assert Name(value).value == expected


@pytest.mark.parametrize(
    "value",
    [
        1.2,
        [1, 2, 3],
        {1},
        {"name": "alice"}
    ]
)
def test_unsupported_name_type(value):
    with pytest.raises(UnSupportedNameTypeError):
        Name(value)


@pytest.mark.parametrize(
    "value",
    [
        "a",
        "a" * 256
    ]
)
def test_invalid_name_length(value):
    with pytest.raises(InvalidNameLengthError):
        Name(value)


@pytest.mark.parametrize(
    "value",
    [
        "alex123"     # есть цифры
        "user_name"   # есть _
        "john doe"    # пробел
        "123"         # только цифры
    ]
)
def test_invalid_name_format(value):
    with pytest.raises(InvalidNameFormatError):
        Name(value)