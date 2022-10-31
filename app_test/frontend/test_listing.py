from seleniumbase import BaseCase

from app_test.conftest import base_url
from app.models import Booking, Listing, User
from app.models import db

"""
This file defines all integration tests for the frontend create listing page.
"""


class FrontEndTest(BaseCase):

    def test_create_listing_input_success(self, *_):
        """
        This is a front end unit test to the create listing page using input
        partitioning tests.
        Possible inputs: valid/invalid title, valid/invalid description,
        valid/invalid price
        Requirements tested: R4-1, R4-3, R4-4, R4-8
        """

        FrontEndTest.test_listing_helper(self)

        # Clear Database for the test title
        user = User.query.filter(User.email == "test2@test.com").all()
        ownerId = user[0].id
        Listing.query.filter(Listing.owner_id == ownerId).delete()
        db.session.commit()

        # Invalid Title, Valid description, Valid price
        # R4-1 is not valid
        self.open(base_url + "/create-listing")
        self.type("#title", "Test Title ")
        self.type("#description", "This is a test description")
        self.type("#price", "110.00")
        self.click('input[type="submit"]')
        # Should return an error
        self.assert_element("#message")
        self.assert_text("Creation Failed!", "#message")

        # Valid Title, Invalid description, Valid price
        self.type("#title", "Test Title ")
        # R4-3 is not valid
        self.type("#description", "This")
        self.type("#price", "110.00")
        self.click('input[type="submit"]')
        # Should return an error
        self.assert_element("#message")
        self.assert_text("Creation Failed!", "#message")

        # Valid Title, Valid description, Invalid price
        self.type("#title", "Test Title")
        self.type("#description", "This is a test description")
        # R4-5 is not valid
        self.type("#price", "9.00")
        self.click('input[type="submit"]')
        # Should return an error
        self.assert_element("#message")
        self.assert_text("Creation Failed!", "#message")

        # Valid Title, Valid description, Valid price
        self.type("#title", "Test Title")
        self.type("#description", "This is a test description")
        self.type("#price", "11.50")
        self.click('input[type="submit"]')
        # Should redirect to the home page
        self.assert_element("#welcome-header")
        self.assert_text("Welcome Test !", "#welcome-header")
        self.assert_element("#listings")
        self.assert_element("#listingTitle")
        self.assert_text("Test Title", "#listingTitle")
        self.assert_element("#listingPrice")
        self.assert_text("11.5", "#listingPrice")

    def test_create_listing_boundary_success(self, *_):
        """
        This is a front end unit test to the create listing page using input
        boundary tests.
        Price has to be in range [10,10000]
        Possible inputs: 9.99, 10.00,10000.01, 10000.00
        Requirements tested: R4-5
        """

        FrontEndTest.test_listing_helper(self)

        # Clear Database for the test title
        user = User.query.filter(User.email == "test2@test.com").all()
        ownerId = user[0].id
        Listing.query.filter(Listing.owner_id == ownerId).delete()
        db.session.commit()

        # 9.99 (invalid)
        self.open(base_url + "/create-listing")
        self.type("#title", "Testing Title")
        self.type("#description", "This is a test description")
        self.type("#price", "9.99")
        self.click('input[type="submit"]')
        # Should return an error
        self.assert_element("#message")
        self.assert_text("Creation Failed!", "#message")

        # 10.00 (valid)
        self.open(base_url + "/create-listing")
        self.type("#title", "Testing Title")
        self.type("#description", "This is a test description")
        self.type("#price", "10.00")
        self.click('input[type="submit"]')
        # Should redirect to the home page
        self.assert_element("#welcome-header")
        self.assert_text("Welcome Test !", "#welcome-header")
        self.assert_element("#listings")
        self.assert_element("#listingTitle")
        self.assert_text("Testing Title", "#listingTitle")
        self.assert_element("#listingPrice")
        self.assert_text("10.0", "#listingPrice")

        # Clear Database for the test title
        Listing.query.filter(Listing.owner_id == ownerId).delete()
        db.session.commit()

        # 10000.01 (invalid)
        self.open(base_url + "/create-listing")
        self.type("#title", "Testing Title 2")
        self.type("#description", "This is a test description")
        self.type("#price", "10000.01")
        self.click('input[type="submit"]')
        # Should return an error
        self.assert_element("#message")
        self.assert_text("Creation Failed!", "#message")

        # 10000.00 (valid)
        self.open(base_url + "/create-listing")
        self.type("#title", "Testing Title 2")
        self.type("#description", "This is a test description")
        self.type("#price", "10000.00")
        self.click('input[type="submit"]')
        # Should redirect to the home page
        self.assert_element("#welcome-header")
        self.assert_text("Welcome Test !", "#welcome-header")
        self.assert_element("#listings")
        self.assert_element("#listingTitle")
        self.assert_text("Testing Title 2", "#listingTitle")
        self.assert_element("#listingPrice")
        self.assert_text("10000.0", "#listingPrice")

        # Clear Database for the test title
        Listing.query.filter(Listing.owner_id == ownerId).delete()
        db.session.commit()

    def test_create_listing_output_success(self, *_):
        """
        This is a front end unit test to the create listing page using output
        partitioning tests.
        Possible Outputs: msg=Creation Failed!, redirect to home page
        Requirements tested: R4-2, R4-4
        """

        FrontEndTest.test_listing_helper(self)

        # Clear Database for the test title
        user = User.query.filter(User.email == "test2@test.com").all()
        ownerId = user[0].id
        Listing.query.filter(Listing.owner_id == ownerId).delete()
        db.session.commit()

        self.open(base_url + "/create-listing")

        self.type("#title", "Test Title Two. This is a test description" +
                  "Test Title Two. This is a test description")
        self.type("#description", "This is a test description")
        self.type("#price", "50.00")
        self.click('input[type="submit"]')
        # Should return an error
        self.assert_element("#message")
        self.assert_text("Creation Failed!", "#message")

        # redirect to home page if all three are valid
        self.type("#title", "Test Title Two")
        self.type("#description", "This is a test description")
        self.type("#price", "50.00")
        self.click('input[type="submit"]')
        # Should redirect to the home page
        self.assert_element("#welcome-header")
        self.assert_text("Welcome Test !", "#welcome-header")
        self.assert_element("#listings")
        self.assert_element("#listingTitle")
        self.assert_text("Test Title Two", "#listingTitle")
        self.assert_element("#listingPrice")
        self.assert_text("50.0", "#listingPrice")

        # Clear Database for the test title
        Listing.query.filter(Listing.owner_id == ownerId).delete()
        db.session.commit()

    def test_update_listing_input_success(self, *_):
        """
        This is a front end unit test to the update listing page using input
        partitioning.
        Possible inputs: valid/invalid title, valid/invalid description,
        valid/invalid price
        Requirements tested: R5-1, R5-4
        """

        FrontEndTest.test_listing_helper(self)

        # Create a test listing
        self.open(base_url + "/create-listing")
        self.type("#title", "Test Title")
        self.type("#description", "This is a test description")
        self.type("#price", "10.00")
        self.click('input[type="submit"]')

        listing = Listing.query.filter(Listing.title == "Test Title").all()
        listing_id = listing[0].id
        self.open(base_url + "/update-listing/" + str(listing_id))

        # Invalid Title, Valid description, Valid price
        # R4-1 is not valid
        self.type("#title", "Test Title ")
        self.type("#description", "This is a test description")
        self.type("#price", "110.00")
        self.click('input[type="submit"]')
        # Should return an error
        self.assert_element("#message")
        self.assert_text("Update Failed!", "#message")

        # Valid Title, Invalid description, Valid price
        self.type("#title", "Test Title ")
        # R4-3 is not valid
        self.type("#description", "This")
        self.type("#price", "110.00")
        self.click('input[type="submit"]')
        # Should return an error
        self.assert_element("#message")
        self.assert_text("Update Failed!", "#message")

        # Valid Title, Valid description, Invalid price
        self.type("#title", "Test Title")
        self.type("#description", "This is a test description")
        # R4-5 is not valid
        self.type("#price", "9.00")
        self.click('input[type="submit"]')
        # Should return an error
        self.assert_element("#message")
        self.assert_text("Update Failed!", "#message")

        # Valid Title, Valid description, Valid price
        self.type("#title", "Test Title")
        self.type("#description", "This is a test description")
        self.type("#price", "13.50")
        self.click('input[type="submit"]')
        # Should redirect to the home page
        self.assert_element("#welcome-header")
        self.assert_text("Welcome Test !", "#welcome-header")
        self.assert_element("#listings")
        self.assert_element("#listingTitle")
        self.assert_text("Test Title", "#listingTitle")
        self.assert_element("#listingPrice")
        self.assert_text("13.5", "#listingPrice")

    def test_update_listing_boundary_success(self, *_):
        """
        This is a front end unit test to the update listing page using input
        boundary tests.
        Price has to be in range [10,10000]
        Possible inputs: 9.99, 10.00,10000.01, 10000.00
        Requirements tested: R5-2, R5-4
        """

        FrontEndTest.test_listing_helper(self)

        # Create a test listing
        self.open(base_url + "/create-listing")
        self.type("#title", "Test Title")
        self.type("#description", "This is a test description")
        self.type("#price", "10.00")
        self.click('input[type="submit"]')

        listing = Listing.query.filter(Listing.title == "Test Title").all()
        listing_id = listing[0].id

        user = User.query.filter(User.email == "test2@test.com").all()
        ownerId = user[0].id
        Listing.query.filter(Listing.owner_id == ownerId).delete()
        db.session.commit()

        # Navigate to the Create Listing Page
        self.open(base_url + "/create-listing")
        # Create a new listing
        self.type("#title", "Test Title")
        self.type("#description", "This is a test description")
        self.type("#price", "10.00")
        self.click('input[type="submit"]')

        listing = Listing.query.filter(Listing.title == "Test Title").all()
        listing_id = listing[0].id

        # 9.99 (invalid)
        self.open(base_url + "/update-listing/" + str(listing_id))
        self.type("#title", "Testing Title")
        self.type("#description", "This is a test description")
        self.type("#price", "9.99")
        self.click('input[type="submit"]')
        # Should return an error
        self.assert_element("#message")
        self.assert_text("Update Failed!", "#message")

        # 10.00 (valid)
        self.open(base_url + "/update-listing/" + str(listing_id))
        self.type("#title", "Testing Title")
        self.type("#description", "This is a test description")
        self.type("#price", "10.00")
        self.click('input[type="submit"]')
        # Should redirect to the home page
        self.assert_element("#welcome-header")
        self.assert_text("Welcome Test !", "#welcome-header")
        self.assert_element("#listings")
        self.assert_element("#listingTitle")
        self.assert_text("Testing Title", "#listingTitle")
        self.assert_element("#listingPrice")
        self.assert_text("10.0", "#listingPrice")

        # 10000.01 (invalid)
        self.open(base_url + "/update-listing/" + str(listing_id))
        self.type("#title", "Testing Title 2")
        self.type("#description", "This is a test description")
        self.type("#price", "10000.01")
        self.click('input[type="submit"]')
        # Should return an error
        self.assert_element("#message")
        self.assert_text("Update Failed!", "#message")

        # 10000.00 (valid)
        self.open(base_url + "/update-listing/" + str(listing_id))
        self.type("#title", "Testing Title 2")
        self.type("#description", "This is a test description")
        self.type("#price", "10000.00")
        self.click('input[type="submit"]')
        # Should redirect to the home page
        self.assert_element("#welcome-header")
        self.assert_text("Welcome Test !", "#welcome-header")
        self.assert_element("#listings")
        self.assert_element("#listingTitle")
        self.assert_text("Testing Title 2", "#listingTitle")
        self.assert_element("#listingPrice")
        self.assert_text("10000.0", "#listingPrice")

    def test_update_listing_output_success(self, *_):
        """
        This is a front end unit test to the create listing page using output
        partitioning tests.
        Possible Outputs: msg=Update Failed!, redirect to home page
        Requirements tested: R5-4
        """

        FrontEndTest.test_listing_helper(self)

        # Create a test listing
        self.open(base_url + "/create-listing")
        self.type("#title", "Test Title")
        self.type("#description", "This is a test description")
        self.type("#price", "10.00")
        self.click('input[type="submit"]')

        listing = Listing.query.filter(Listing.title == "Test Title").all()
        listing_id = listing[0].id

        user = User.query.filter(User.email == "test2@test.com").all()
        ownerId = user[0].id
        Listing.query.filter(Listing.owner_id == ownerId).delete()
        db.session.commit()

        # Navigate to the Create Listing Page
        self.open(base_url + "/create-listing")
        # Create a new listing
        self.type("#title", "Test Title")
        self.type("#description", "This is a test description")
        self.type("#price", "11.50")
        self.click('input[type="submit"]')

        listing = Listing.query.filter(Listing.title == "Test Title").all()
        listing_id = listing[0].id

        self.open(base_url + "/update-listing/" + str(listing_id))
        # show error message if one of the three are invalid
        # R4-4 is not valid
        self.type("#title", "Test Title Two. This is a test description")
        self.type("#description", "This is a test description")
        self.type("#price", "50.00")
        self.click('input[type="submit"]')
        # Should return an error
        self.assert_element("#message")
        self.assert_text("Update Failed!", "#message")

        # redirect to home page if all three are valid
        self.type("#title", "Test Title Two")
        self.type("#description", "This is a test description")
        self.type("#price", "50.00")
        self.click('input[type="submit"]')
        # Should redirect to the home page
        self.assert_element("#welcome-header")
        self.assert_text("Welcome Test !", "#welcome-header")
        self.assert_element("#listings")
        self.assert_element("#listingTitle")
        self.assert_text("Test Title Two", "#listingTitle")
        self.assert_element("#listingPrice")
        self.assert_text("50.0", "#listingPrice")

    def test_listing_helper(self, *_):
        """
        This is a helper function to set up the database for the tests.
        We need to create a testing user, and to log in as this user.
        """

        User.query.delete()
        Listing.query.delete()
        Booking.query.delete()

        # Clear Database for the test user
        User.query.filter(User.email == "test2@test.com").delete()
        db.session.commit()

        # Create a new User
        self.open(base_url + "/register")
        # fill details
        self.type("#email", "test2@test.com")
        self.type("#real_name", "Test Test")
        self.type("#name", "Test")
        self.type("#password", "Test!123")
        self.type("#password2", "Test!123")
        # click register button
        self.click('input[type="submit"]')

        # Login as the new User
        self.open(base_url + "/login")
        # fill email and password
        self.type("#email", "test2@test.com")
        self.type("#password", "Test!123")
        # click enter button
        self.click('input[type="submit"]')
