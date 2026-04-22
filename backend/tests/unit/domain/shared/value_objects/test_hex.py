import pytest

from src.backend.domain.shared.value_objects.hex.errors import InvalidHexError, UnsupportedHexTypeError
from src.backend.domain.shared.value_objects.hex.value_object import HexCode


@pytest.fixture
def hex_code():
    return HexCode("#782078")

@pytest.mark.parametrize(
    "value, expected",
    [
        ("#F54927", "#F54927"),
        ("#94230D", "#94230D"),
        ("#201245", "#201245"),
    ]
)
def test_valid_hex(value, expected):
    assert HexCode(value).value == expected


@pytest.mark.parametrize(
    "value",
    [
        1,
        [1, 3, "dd"],
        {"5": 5},
    ]
)
def test_unsupported_hex_hex(value):
    with pytest.raises(UnsupportedHexTypeError):
        HexCode(value)


@pytest.mark.parametrize(
    "value",
    [
        "122",
        "JHJH",
        "hjhhghgkjjkjk",
    ]
)
def test_invalid_hex(value):
    with pytest.raises(InvalidHexError):
        HexCode(value)