from app.models import alphanumeric_check, email_check, \
    create_listing, find_listing_by_id, find_listing_by_title, not_empty, \
    postal_code_check, unique_title_check, owner_check, length_check, \
    pw_check, range_check, register, login, description_length_check, \
    date_check, update_user, update_listing, find_listing
from datetime import date


def test_r1_7_user_register():

    # R1-1: Email cannot be empty. password cannot be empty.
    assert register('u00', '', 'real_u1', '') is False
    assert register('u10', 'test1@test.com', 'real_u1', '') is False
    assert register('u20', '', 'real_u3', '12345Aa#') is False

    # R1-3:The email has to follow addr-spec defined in RFC 5322
    assert register('u30', 'Invalid email', 'real_u4', '12345Aa#') is False

    # R1-4: Password has to meet the required complexity: minimum length 6,
    # at least one upper case, at least one lower case and at least one
    # special character.
    assert register('u40', 'test2@test.com', 'real_u4', '12') is False
    assert register('u50', 'test3@test.com', 'real_u5', '123456') is False
    assert register('u60', 'test4@test.com', 'real_u6', '123456A') is False
    assert register('u70', 'test5@test.com', 'real_u7', '123456a') is False
    assert register('u80', 'test6@test.com', 'real_u8', '123456a') is False

    # Valid register
    assert register('u90', 'test0@test.com', 'real_u9', '12345Aa#') is True

    # R1-5: User name has to be non-empty, alphanumeric-only, and space allowed
    # only if it is not as the prefix or suffix.
    assert register(' u', 'test8@test.com', 'real_u11', '123456a') is False
    assert register('u ', 'test9@test.com', 'real_u12', '123456a') is False

    # R1-6: User name has to be longer than 2 characters and less than
    # 20 characters.
    assert register('u', 'test7@test.com', 'real_u10', '123456Aa#') is False
    assert register('u100u100u100u100u100u100u100', 'test6@test.com', 'real_u',
                    '123456a') is False

    # R1-7: If the email has been used, the operation failed.
    assert register('u100', 'test0@test.com', 'real_u9', '12345Aa#') is False

    # R1-8: Shipping address is empty at the time of registration.
    user = login('test0@test.com', '12345Aa#')
    assert user.billing_address == ''

    # R1-9: Postal code is empty at the time of registration.
    assert user.postal_code == ''

    # R1-10:  Balance should be initialized as 100 at
    # the time of registration. (free $100 dollar signup bonus).
    assert user.balance == 100


def test_r2_1_login():
    '''
    Testing R2-1: A user can log in using her/his email address
      and the password.
    (will be tested after the previous test, so we already have u0,
      u1 in database)

      Also, the email and password inputs needs to meet the same email/password
      requirements in the email_check and pw_check functions
    '''

    user = login('test0@test.com', '12345Aa#')
    assert user is not None
    assert user.username == 'u90'

    user = login('test0@test.com', '123457Aa#')
    assert user is None

    user = login('InvalidEmail', '12345Aa#')   # Invalid email
    assert user is False

    user = login('test0@test.com', '12345')     # Password not long enough
    assert user is False


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
    text = "x" * 2000
    assert length_check(text, 20, 2000) is True
    text = "x" * 2002
    # Description that is more than 20 characters and greater than 2000
    assert length_check(text, 20, 2000) is False


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
    assert unique_title_check("Title", 0) is False
    # Title is unique
    assert unique_title_check("Unused Title", 0) is True


def test_r3_2_3_postal_check():
    '''
    R3-2: Postal code should be non-empty,
    alnum only, and no special characters.
    R3-3: Postal code has to be a valid Canadian postal code.
    '''
    assert postal_code_check("") is False
    assert postal_code_check("aaa") is False
    assert postal_code_check("aaa !aa") is False
    assert postal_code_check("k1k5m5") is False
    assert postal_code_check("aaaa aaa") is False
    assert postal_code_check("k1k 5m5") is True


def test_r3_1_update_user():
    '''
    R3-1: A user is only able to update his/her username,
    billing address, and postal code.
    '''
    # Start by registering a user
    assert register('original username', 'user@test.com',
                    'real_u1', '12345Aa#') is True

    # If curr_name does not exist, cannot update
    assert update_user('invalid_username', 'updated_username', 'new@test.com',
                       'address', 'K7L 3N6', '12345Aa#') is False

    # If new name does not have proper format, cannot update
    assert update_user('original username', '  my new name   ', 'new@test.com',
                       'address', 'K7L 3N6', '12345Aa#') is False
    assert update_user('original_username',
                       'aaaaaaaaaaaaaaaaaaaaa', 'new@test.com',
                       'address', 'K7L 3N6', '12345Aa#') is False

    # If new email does not have proper format, cannot update
    assert update_user('original username', 'new_user', '',
                       'address', 'K7L 3N6', '12345Aa#') is False

    # If new postal code does not have proper format, cannot update
    assert update_user('original username', 'new_user', 'new@test.com',
                       'address', 'K7L', '12345Aa#') is False

    # If the new username/email already exists from another user, cannot update
    assert update_user('original username',
                       'original username', 'test0@test.com',
                       'address', 'K7L 3N6') is False
    assert update_user('original username', 'u90', 'user@test.com',
                       'address', 'K7L 3N6', '12345Aa#') is False

    # Valid update
    assert update_user('original username', 'new username',
                       'new@test.com', 'address',
                       'K7L 3N5', '12345Aa#') is True

    # Ensure all fields were updated properly
    user = login('new@test.com', '12345Aa#')
    assert user is not None
    assert user.username == 'new username'


def test_r1_6_user_length():
    '''
    Testing R1-6: User name has to be longer than 2 characters
    and less than 20 characters.
    '''
    assert length_check("Lo", 3, 20) is False
    assert length_check("Lorem ipsum dolor s", 3, 20) is True
    assert length_check("Lorem ipsum dolor si", 3, 20) is True
    assert length_check("Lorem ipsum dolor sit", 3, 20) is False


def test_r1_1_empty():
    '''
    Testing R1-1: User name and password cannot be empty.
    '''
    assert not_empty('') is False
    assert not_empty('Lo') is True


def test_r5_1_update_listing():
    '''
    R5-1, R5-2, R5-4: One can only update title, description, and price.
    '''

    # First, create a listing
    create_listing("Titleunique", "This is a description.", 150, 1) is True

    # Cannot update if the owner_id does not exist
    assert update_listing(0, "Newesttitle", "This is a short description.",
                          150, 153, 123) is False

    # Cannot update if the title format is not correct
    assert update_listing(0, "The title is longer than the description",
                          "This is a short description.", 150, 153, 1) is False

    # Cannot update if the description format is not correct
    assert update_listing(0, "title", "too short", 150, 153, 1) is False

    # Cannot update if the new price is lower than the original price
    assert update_listing(0, "Newesttitle",
                          "This is a short description.", 150, 20, 1) is False

    # Update is successful if all the requirements are passed
    assert update_listing(0, "Newest Title",
                          "This is a short description. description",
                          150, 153, 1) is True

    # Check if the update is successful
    listing = find_listing(1)
    assert listing is not None
    assert listing.title == 'Newest Title'
    assert listing.description == 'This is a short description. description'
    assert listing.price == 153


def test_find_listing_by_id():
    '''
    Testing Listing: Testiing the retrieval of listing using title or id
    '''
    create_listing("Some Title", "Some Description here", 100, 1)
    assert find_listing_by_title("Some Title")[0].title == "Some Title"
    assert find_listing_by_id(find_listing_by_title("Some Title")
                              [0].id)[0].title == "Some Title"
    assert find_listing_by_title("Some Title")[0].title != "Title"
    assert find_listing_by_id(find_listing_by_title("Some Title")
                              [0].id)[0].title != "Title"
