import pytest

from src.backend.domain.funnel.value_objects.probability.errors import OutOfRangeProbabilityError, \
    UnsupportedProbabilityTypeError
from src.backend.domain.funnel.value_objects.probability.value_object import Probability

@pytest.fixture
def win_probability():
    return Probability(30)

@pytest.mark.parametrize(
    "value, expected",
    [
        (1, 1),
        (34, 34),
        (100, 100),
    ]
)
def test_valid_probability(value, expected):
    assert Probability(value).value == expected


@pytest.mark.parametrize(
    "value",
    [
        -1,
        100001,
        -30,
    ]
)
def test_out_of_range_probability(value):
    with pytest.raises(OutOfRangeProbabilityError):
        Probability(value)


@pytest.mark.parametrize(
    "value",
    [
        1.2,
        "1",
        {1},
        {"1": 1}
    ]
)
def test_unsupported_probability_type(value):
    with pytest.raises(UnsupportedProbabilityTypeError):
        Probability(value)