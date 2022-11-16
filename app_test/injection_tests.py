from app.models import create_listing, Listing, User, register
'''
File to test SQL Injection handling for Register and Create Listing methods
'''


def test_sqli_register():
    '''
    Function to test SQL Injection handling for Register method
    '''
    injection_file = open('app_test/Generic_SQLI.txt', 'r')
    lines = injection_file.readlines()

    for line in lines:
        real_name_register(line)
        password_register(line)


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
