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
