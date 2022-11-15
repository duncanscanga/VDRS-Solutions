from app.models import create_listing, Listing
import os
'''
File to test SQL Injection handling for Register and Create Listing methods
'''


def test_sqli_register():
    pass


def test_sqli_create_listing():
    test_file = open('app_test/Generic_SQLI.txt', 'r')
    lines = test_file.readlines()
    print(lines)

    for line in lines:    
        test_price_parameter(line)
        test_owner_id_parameter(line)

def test_price_parameter(line):
    Listing.query.filter(Listing.title == "Test Title").delete()
    print(line)
    assert create_listing("Test Title", "This is a description.", line, 1) is False


def test_owner_id_parameter(line):
    Listing.query.filter(Listing.title == "Test Title").delete()
    print(line)
    assert create_listing("Test Title", "This is a description.", 150, line) is False

