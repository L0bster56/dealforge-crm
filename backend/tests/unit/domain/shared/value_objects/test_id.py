import pytest

from src.backend.domain.shared.value_objects.id.errors import UnsupportedTypeIdError, NegativeIntIdError
from src.backend.domain.shared.value_objects.id.value_object import Id

@pytest.mark.parametrize(
    "value, expected",
    [
        (1, 1),
        (100, 100),
        (10000, 10000),
    ]
)
def test_valid_id(value, expected):
    assert Id(value).value == expected


@pytest.mark.parametrize(
    "value",
    [
        1.2,
        "1",
        {1},
        {"id": 1}
    ]
)
def test_unsupported_type_id(value):
    with pytest.raises(UnsupportedTypeIdError):
        Id(value)


@pytest.mark.parametrize(
    "value",
    [
        0,
        -1,
        -100
    ]
)
def test_negative_int_id(value):
    with pytest.raises(NegativeIntIdError):
        Id(value)