import pytest

from tests.unit.domain.user.specifications.password import (
    PasswordLengthSpecification,
    PasswordUpperLetterSpecification,
    PasswordLowerLetterSpecification,
    PasswordSpecialCharacterSpecification,
    PasswordDigitSpecification, PasswordDifferenceSpecification
)


@pytest.fixture
def password_length_spec()-> PasswordLengthSpecification:
    return PasswordLengthSpecification()

@pytest.fixture
def password_upper_letter_spec()-> PasswordUpperLetterSpecification:
    return PasswordUpperLetterSpecification()

@pytest.fixture
def password_lower_letter_spec() -> PasswordLowerLetterSpecification:
    return PasswordLowerLetterSpecification()

@pytest.fixture
def password_digit_spec() -> PasswordDigitSpecification:
    return PasswordDigitSpecification()

@pytest.fixture
def password_special_character_spec() -> PasswordSpecialCharacterSpecification:
    return PasswordSpecialCharacterSpecification()


@pytest.fixture
def password_spec(
        password_length_spec: PasswordLengthSpecification,
        password_upper_letter_spec:PasswordUpperLetterSpecification,
        password_lower_letter_spec:PasswordLowerLetterSpecification,
        password_digit_spec:PasswordDigitSpecification,
        password_special_character_spec:PasswordSpecialCharacterSpecification,
):
    return (
        password_length_spec &
        password_upper_letter_spec &
        password_lower_letter_spec &
        password_digit_spec &
        password_special_character_spec
    )

import pytest

@pytest.mark.parametrize(
    "password, expected",
    [
        ("Malika", False),
        ("Jaxanqin123", False),
        ("Visola@123", True),
    ]
)
def test_password_spec(
    password_spec,
    password: str,
    expected: bool
):
    assert password_spec.is_satisfied_by(password) == expected

@pytest.mark.parametrize(
    "password, expected",
    [
        ("Malika", False),
        ("Jaxangir", True)
    ]
)
def test_password_length_spec(
        password_length_spec: PasswordLengthSpecification,
        password: str,
        expected: bool
):
    assert password_length_spec.is_satisfied_by(password) == expected

import pytest

@pytest.mark.parametrize(
    "password, expected",
    [
        ("Malika", True),
        ("sanjac", False),
    ]
)
def test_password_upper_letter_spec(
    password_upper_letter_spec: PasswordUpperLetterSpecification,
    password: str,
    expected: bool
):
    assert password_upper_letter_spec.is_satisfied_by(password) == expected


@pytest.mark.parametrize(
    "password, expected",
    [
        ("malika", True),
        ("MALIKA", False),
    ]
)
def test_password_lower_letter_spec(
    password_lower_letter_spec: PasswordLowerLetterSpecification,
    password: str,
    expected: bool
):
    assert password_lower_letter_spec.is_satisfied_by(password) == expected


@pytest.mark.parametrize(
    "password, expected",
    [
        ("abc123", True),
        ("abcdef", False),
    ]
)
def test_password_digit_spec(
    password_digit_spec: PasswordDigitSpecification,
    password: str,
    expected: bool
):
    assert password_digit_spec.is_satisfied_by(password) == expected


@pytest.mark.parametrize(
    "password, expected",
    [
        ("abc!def", True),
        ("abcdef", False),
    ]
)
def test_password_special_character_spec(
    password_special_character_spec: PasswordSpecialCharacterSpecification,
    password: str,
    expected: bool
):
    assert password_special_character_spec.is_satisfied_by(password) == expected


@pytest.fixture()
def password_diff_spec()-> PasswordDifferenceSpecification:
    return PasswordDifferenceSpecification()

@pytest.mark.parametrize(
    "passwords, expected",
    [
        (("Malika", "Malika"), False,),

        (("Jaxangir", "Jaxangir123"),True,)
    ]
)
def test_password_diff_spec(
        password_diff_spec: PasswordDifferenceSpecification,
        passwords: tuple[str,str],
        expected: bool
):
    assert password_diff_spec.is_satisfied_by(passwords) == expected