from app.models import alphanumeric_check, email_check, create_listing, \
    unique_title_check, owner_check, length_check, pw_check, \
    range_check, register, login, description_length_check, date_check
from datetime import date
from app import app
import pytest
@pytest.fixture
def app_context():
    with app.app_context():
        yield


def test_r1_7_user_register():
    '''
    Testing R1-7: If the email has been used, the operation failed.
    '''

    assert register('u0', 'test0@test.com', 'real_u1', '123456',
                    '1209 King St W Suite 201', 'K7L 3N6') is True
    assert register('u1', 'test1@test.com', 'real_u2', '123456',
                    '1209 King St W Suite 201', 'K7L 3N6') is True
    assert register('u2', 'test1@test.com', 'real_u3', '123456',
                    '1209 King St W Suite 201', 'K7L 3N6') is False


def test_r2_1_login():
    '''
    Testing R2-1: A user can log in using her/his email address
      and the password.
    (will be tested after the previous test, so we already have u0,
      u1 in database)
    '''

    user = login('test0@test.com', 123456)
    assert user is not None
    assert user.username == 'u0'

    user = login('test0@test.com', 1234567)
    assert user is None


def test_r1_4_pw_check():
    '''
    Testing R1-4: Password has to meet the required complexity:
    - minimum length 6
    - At least one upper case
    - At least one lower case
    - At least one special character
    '''

    assert pw_check("12345") is False     # Not long enough
    assert pw_check("123456") is False
    # Long enough, missing alpha and special
    assert pw_check("12345a") is False    # Missing upper case and special
    assert pw_check("12345A") is False    # Missing lower and special
    assert pw_check("12345Aa") is False   # Missing special
    assert pw_check("12345Aa#") is True   # Satisfies all requirements


def test_r1_3_email_check():
    '''
    Testing R1-3: The email has to follow add-spec defined in RFC 5322
    '''
    assert email_check("hello@gmail.com") is True
    assert email_check("firstname.lastname@example.com") is True
    assert email_check("email@example.co.jp") is True
    assert email_check("InvalidEmail") is False
    assert email_check("email..email@example.com") is False


def test_r4_1_title_alnum_check():
    '''
    R4-1: The title of the product has to be alphanumeric-only,
    and space allowed only if it is not as prefix and suffix.
    '''
    assert alphanumeric_check("Title") is True
    assert alphanumeric_check("Title With Space") is True
    assert alphanumeric_check("Title ") is False
    assert alphanumeric_check(" Title") is False
    assert alphanumeric_check(" Title ") is False
    assert alphanumeric_check("Title With Space ") is False
    assert alphanumeric_check(" Title With Space ") is False
    assert alphanumeric_check("Title_") is False
    assert alphanumeric_check(" ") is False


def test_r4_2_title_length_check():
    '''
    R4-2: The title of the product is no longer than 80 characters.
    '''
    # Title that is less than 80 characters
    assert length_check("Lorem ipsum dolor sit amet, consectetuer ad" +
                        "ipiscing elit. Aenean commodo ligula", 0, 80) is True
    # Title that is equal to 80 characters
    assert length_check("Lorem ipsum dolor sit amet, consectetuer ad" +
                        "ipiscing elit. Aenean commodo ligula.", 0, 80) is True
    # Title that is more than 80 characters
    assert length_check("Lorem ipsum dolor sit amet, consectetuer ad" +
                        "ipiscing elit. Aenean commodo ligula.1", 0,
                        80) is False


def test_r4_3_description_length_check():
    '''
    R4-3: The description of the product can be arbitrary characters,
    with a minimum length of 20 characters and a maximum of 2000 characters.
    '''
    # Description that is less than 20 characters
    assert length_check("Lorem ipsum dolor s", 20, 2000) is False
    # Description that is equal to 20 characters
    assert length_check("Lorem ipsum dolor si", 20, 2000) is True
    # Description that is more than 20 characters and less than 2000
    assert length_check("Lorem ipsum dolor sit.", 20, 2000) is True
    # Description that is more than 20 characters and equal to 2000
    assert length_check("Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer",
                        20, 2000) is True
    # Description that is more than 20 characters and greater than 2000
    assert length_check("Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci" +
                        "Lorem ipsum dolor sit amet, consectetuer adipisci",
                        20, 2000) is False


def test_r4_4_description_length_check():
    '''
    R4-4: Description has to be longer than the product's title.
    '''
    # Title is longer than description
    assert description_length_check("Description", "This is the title"
                                    ) is False
    # Title is shorter than description
    assert description_length_check("Description", "Title") is True
    # Title and description are the same length
    assert description_length_check("Test", "Test") is False


def test_r4_5_price_check():
    '''
    R4-5: Price has to be of range [10, 10000].
    '''
    # Price is less than 10
    assert range_check(9.99, 10, 10000) is False
    # Price is equal to 10
    assert range_check(10, 10, 10000) is True
    # Price is less than 10000 and greater than 10
    assert range_check(50.51, 10, 10000) is True
    # Price is equal to 10000
    assert range_check(10000, 10, 10000) is True
    # Price is greather than 10000
    assert range_check(10000.50, 10, 10000) is False


def test_r4_6_date_check():
    '''
    R4-6: last_modified_date must be after 2021-01-02 and before 2025-01-02.
    '''
    # Date is before 2021-01-02
    assert date_check(date(2021, 1, 1),
                      date(2021, 1, 2), date(2025, 1, 2)) is False
    # Date is 2021-01-02
    assert date_check(date(2021, 1, 2),
                      date(2021, 1, 2), date(2025, 1, 2)) is False
    # Date is between 2021-01-02 and  2025-01-02
    assert date_check(date(2022, 1, 1),
                      date(2021, 1, 2), date(2025, 1, 2)) is True
    # Date is 2025-01-02
    assert date_check(date(2025, 1, 2),
                      date(2021, 1, 2), date(2025, 1, 2)) is False
    # Date is after 2025-01-02
    assert date_check(date(2025, 1, 3),
                      date(2021, 1, 2), date(2025, 1, 2)) is False


def test_r4_7_owner_check():
    '''
    R4-7: owner_email cannot be empty. The owner of the corresponding
    product must exist in the database.
    NOTE: Since owner_email is not stored in the listing model,
    I will check if the owner's corresponding id exists. If the owner's
    email is empty, it would not be allowed in the database on creation.
    '''
    # Owner does exist
    assert owner_check(1) is True
    # Owner does not exist
    assert owner_check(-1) is False


def test_r4_8_unique_title():
    '''
    R4-8: A user cannot create products that have the same title.
    '''
    # Title is already used
    create_listing("Title", "This is a description.", 100, 1)
    assert unique_title_check("Title") is False
    # Title is unique
    assert unique_title_check("Unused Title") is True
