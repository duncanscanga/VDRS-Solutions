from app.models import register, login


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
