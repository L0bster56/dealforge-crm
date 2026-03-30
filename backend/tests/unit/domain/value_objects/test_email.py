import pytest

from backend.domain.shared.value_objects.email.errors import InvalidEmailError
from backend.domain.shared.value_objects.email.value_object import Email


@pytest.mark.parametrize(
    "value, expected",
    [
        ("user1@example.com", "user1@example.com"),
        ("john.doe@gmail.com", "john.doe@gmail.com"),
        ("alice_smith@yahoo.com", "alice_smith@yahoo.com"),
        ("test.user123@outlook.com", "test.user123@outlook.com"),
        ("dev-team@company.org", "dev-team@company.org"),
        ("first.last@sub.domain.com", "first.last@sub.domain.com"),
        ("simple@mail.net", "simple@mail.net"),
        ("contact_us@service.co", "contact_us@service.co"),
        ("myemailfilter@gmail.com", "myemailfilter@gmail.com"),
        ("info123@business.io", "info123@business.io"),
    ]
)
def test_valid_email(value, expected):
    assert Email(value).value == expected


@pytest.mark.parametrize(
    "value",
    [
        "plainaddress",
        "@no-local-part.com",
        "user@",
        "user@.com",
        "user@com",
        "user@domain..com",
        "user.name@gmailcom",
        "user#domain.com",
        "user@domain,com",
        "user@domain com"
        " user@gmail.com",
        "user@gmail.com ",
        "user@-domain.com",
        "user@domain-.com",
        "user@domain.c",
    ]
)
def test_invalid_email(value):
    with pytest.raises(InvalidEmailError):
        Email(value)
