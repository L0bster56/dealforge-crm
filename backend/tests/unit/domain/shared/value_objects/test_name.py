import pytest

from backend.domain.shared.value_objects.name.errors import UnsupportedNameTypeError, InvalidNameLengthError, \
    InvalidNameFormatError
from backend.domain.shared.value_objects.name.value_object import Name




@pytest.mark.parametrize(
    'value, expected',
    [
        ("Sanjar", "Sanjar"),
        ("Санжар", "Санжар")
    ]
)
def test_valid_name(value, expected):
    assert Name(value).value == expected


@pytest.mark.parametrize(
    "value",
    [
        123,
        1.5,
        ["Sanjar"],
        {"name": "Sanjar"},
    ]
)
def test_name_invalid_type(value):
    with pytest.raises(UnsupportedNameTypeError):
        Name(value)


@pytest.mark.parametrize(
    "value",
    [
        "Sa",
        "Sa" * 101
    ]
)
def test_name_invalid_length(value):
    with pytest.raises(InvalidNameLengthError):
        Name(value)


@pytest.mark.parametrize(
    "value",
    [
        "Sanjar123",
        "Sanjar@",
        "San_jar",
        "Sanjar--Sa",
        "Sanjar  sa",
    ]
)
def test_name_invalid_format(value):
    with pytest.raises(InvalidNameFormatError):
        Name(value)
