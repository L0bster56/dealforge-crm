import pytest

from src.backend.domain.shared.value_objects.id.errors import UnsupportedTypeIdError, NegativeIntIdError
from src.backend.domain.shared.value_objects.id.value_object import Id


@pytest.mark.parametrize(
    "value, expected",
    [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
    ]
)
def test_valid_id(value, expected):
    assert Id(value).value == expected


@pytest.mark.parametrize(
    "value",
    [
        1.6,
        "1",
        {1},
    ]
)
def test_unsupported_type_id(value):
    with pytest.raises(UnsupportedTypeIdError):
        Id(value)


@pytest.mark.parametrize(
    "value",
    [
        0,
        -2,
        -100
    ]
)
def test_negative_int_id(value):
    with pytest.raises(NegativeIntIdError):
        Id(value)
