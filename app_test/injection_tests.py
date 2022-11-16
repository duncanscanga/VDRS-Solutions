from app.models import create_listing, Listing
from app.models import register
'''
File to test SQL Injection handling for Register and Create Listing methods
'''


def test_sqli_register():
    '''
    Function to test SQL Injection handling for registration
    '''
    test_file = open('app_test/Generic_SQLI.txt', 'r')
    lines = test_file.readlines()
    print(lines)

    for line in lines:
        test_name_parameter(line)
        test_email_parameter(line)


def test_name_parameter(line):
    '''
    Function to test SQL Injection handling for registration
    parameter 'name'.
    '''
    assert register(line, 'realname@gmail.com',
                    'real_name', '12345Aa#') is False


def test_email_parameter(line):
    '''
    Function to test SQL Injection handling for registration
    parameter 'name'.
    '''
    assert register('user50', line, 'real_name', '12345Aa#') is False


def test_sqli_create_listing():
    '''
    Function to test SQL Injection handling for Create Listing methods
    '''
    test_file = open('app_test/Generic_SQLI.txt', 'r')
    lines = test_file.readlines()

    for line in lines:
        test_price_parameter(line)
        test_owner_id_parameter(line)


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
