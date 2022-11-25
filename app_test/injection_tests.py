from app.models import create_listing, create_booking, \
    Listing, User, Booking, register, db
from datetime import date

'''
File to test SQL Injection handling for Register and Create Listing methods
'''


def test_sqli_register():
    '''
    Function to test SQL Injection handling for registration
    '''
    injection_file = open('app_test/Generic_SQLI.txt', 'r')
    lines = injection_file.readlines()

    for line in lines:
        test_name_parameter(line)
        test_email_parameter(line)
        real_name_register(line)
        password_register(line)


def test_name_parameter(line):
    '''
    Function to test SQL Injection handling for registration
    parameter 'name'.
    '''
    assert register(line, 'realname@gmail.com',
                    'real name', '12345Aa#') is False


def test_email_parameter(line):
    '''
    Function to test SQL Injection handling for registration
    parameter 'name'.
    '''
    assert register('user50', line, 'real name', '12345Aa#') is False


def test_sqli_create_listing():
    '''
    Function to test SQL Injection handling for Create Listing methods
    '''
    test_file = open('app_test/Generic_SQLI.txt', 'r')
    lines = test_file.readlines()

    for line in lines:
        test_price_parameter(line)
        test_owner_id_parameter(line)
        test_listing_title_parameter(line)
        test_listing_description_parameter(line)


def test_price_parameter(line):
    '''
    Function to test SQL Injection handling for Create Listing methods
    parameter 'price'.
    '''
    Listing.query.filter(Listing.title == "Test Title").delete()
    assert create_listing("Test Title", "This is a description.",
                          line, 1) is False


def test_owner_id_parameter(line):
    '''
    Function to test SQL Injection handling for Create Listing methods
    parameter 'owner_id'.
    '''
    Listing.query.filter(Listing.title == "Test Title").delete()
    assert create_listing("Test Title", "This is a description.",
                          150, line) is False


def test_listing_title_parameter(line):
    '''
    Function to test SQL Injection handling for Create Listing method
    parameter 'title'.
    '''

    Listing.query.filter(Listing.title == "Test Title").delete()
    assert create_listing(line, "This is a description.",
                          150, 1) is False


def test_listing_description_parameter(line):
    '''
    Function to test SQL Injection handling for Create Listing method
    parameter 'description'.
    '''

    Listing.query.filter(Listing.title == "Test Title").delete()
    assert create_listing("Test Title", line, 150, 1) is False


def real_name_register(line):
    '''
    Function to test SQL Injection handling for Register method
    for the 'real_name' parameter.
    '''
    User.query.filter(User.email == "test0@test.com").delete()
    assert register('u90', 'test0@test.com', line, '12345Aa#') is False


def password_register(line):
    '''
    Function to test SQL Injection handling for Register method
    for the 'password' parameter.
    '''
    User.query.filter(User.email == "test0@test.com").delete()
    assert register('u90', 'test0@test.com', 'real_u9', line) is False


def test_sqli_booking():
    '''
    Function to test SQL Injection handling for booking
    '''
    injection_file = open('app_test/Generic_SQLI.txt', 'r')
    lines = injection_file.readlines()

    User.query.delete()
    Listing.query.delete()
    Booking.query.delete()
    db.session.commit()

    # Start by registering a host user
    assert register('u586', 'host546@test.com',
                    'real username235', '12345Aa#') is True
    # Then create a listing
    assert create_listing("ListingTitle", "This is a description.",
                        10, 1) is True

    # Register a buyer
    assert register('u586', 'buyer@test.com',
                    'real username235', '12345Aa#') is True

    for line in lines:
        listing_id_booking(line)
        uid_booking(line)
        start_date_booking(line)
        end_date_booking(line)
        User.query.delete()
        Listing.query.delete()
        Booking.query.delete()
        db.session.commit()

        # Start by registering a host user
        assert register('u586', 'host546@test.com',
                        'real username235', '12345Aa#') is True
        # Then create a listing
        assert create_listing("ListingTitle", "This is a description.",
                              10, 1) is True

        # Register a buyer
        assert register('u586', 'buyer@test.com',
                        'real username235', '12345Aa#') is True


def listing_id_booking(line):
    '''
    Function to test SQL Injection handling for booking method
    for the 'listing_id' parameter.
    '''
    # Book the listing
    assert create_booking(line, 2, date(2022, 12, 1),
                          date(2022, 12, 3)) is False


def uid_booking(line):
    '''
    Function to test SQL Injection handling for booking method
    for the 'listing_id' parameter.
    '''
    # Book the listing
    assert create_booking(1, line, date(2022, 12, 1),
                          date(2022, 12, 3)) is False


def start_date_booking(line):
    '''
    Function to test SQL Injection handling for booking method
    for the 'listing_id' parameter.
    '''

    # Book the listing
    assert create_booking(1, 2, line, date(2022, 12, 3)) is False


def end_date_booking(line):
    '''
    Function to test SQL Injection handling for booking method
    for the 'listing_id' parameter.
    '''

    # Book the listing
    assert create_booking(1, 2, date(2022, 12, 1), line) is False
