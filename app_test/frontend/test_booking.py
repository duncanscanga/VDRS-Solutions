from seleniumbase import BaseCase
from app_test.conftest import base_url
from app.models import User, Booking, Listing
from app.models import db

"""
This file defines all integration tests for the frontend booking page.
"""


class FrontEndTest(BaseCase):

    def test_create_booking_input_success(self, *_):
        """
        This is a front end unit test to the booking page using
        input partitioning tests.
        Possible inputs: valid/invalid start date, valid/invalid end date,
        low user balance
        Requirements tested: Booking Requirement 1, 3, 4
        """

        FrontEndTest.test_booking_helper(self)

        user = User.query.filter(User.email == "user202@test.com").all()
        user_id = user[0].id
        listing = Listing.query.filter(Listing.title == "First Listing").all()
        listing_id = listing[0].id
        self.open(base_url + "/book-listing/" + str(listing_id) +
                  "/" + str(user_id))

        # Valid start date, valid end date, balance is enough
        self.type("#start", "2022\t1215")
        self.type("#end", "2022\t1220")
        self.click('input[type="submit"]')
        # Needs to take the user to the home page
        self.assert_element("#welcome-header")

        self.open(base_url + "/book-listing/" + str(listing_id) +
                  "/" + str(user_id))

        # Invalid start date, valid end date, balance is enough
        self.type("#start", "2022\t1218")
        self.type("#end", "2022\t1225")
        self.click('input[type="submit"]')
        # Needs to return an error
        self.assert_element("#message")
        self.assert_text("Booking Failed!", "#message")

        # Valid start date, invalid end date, balance is enough
        self.type("#start", "2022\t1226")
        self.type("#end", "2022\t1216")
        self.click('input[type="submit"]')
        # Needs to return an error
        self.assert_element("#message")
        self.assert_text("Booking Failed!", "#message")

        listing = Listing.query.filter(Listing.title == "Second Listing").all()
        listing_id = listing[0].id
        self.open(base_url + "/book-listing/" + str(listing_id) +
                  "/" + str(user_id))

        # Valid start date, valid end date, balance is less than the cost
        self.type("#start", "2022\t1210")
        self.type("#end", "2022\t1212")
        self.click('input[type="submit"]')
        # Needs to return an error
        self.assert_element("#message")
        self.assert_text("Booking Failed!", "#message")

    def test_create_booking_boundary_success(self, *_):
        """
        This is a front end unit test to the booking page using input
        boundary tests.
        Cannot double book a listing.
        Possible inputs for invalid start date: middle of the first booking,
        at least one day before the booking end date.
        Requirements tested: Booking Requirement 4
        """

        FrontEndTest.test_booking_helper(self)

        user = User.query.filter(User.email == "user202@test.com").all()
        user_id = user[0].id
        listing = Listing.query.filter(Listing.title == "First Listing").all()
        listing_id = listing[0].id
        self.open(base_url + "/book-listing/" + str(listing_id) +
                  "/" + str(user_id))

        # book the first listing for test
        self.type("#start", "2022\t1215")
        self.type("#end", "2022\t1220")
        self.click('input[type="submit"]')

        self.open(base_url + "/book-listing/" + str(listing_id) +
                  "/" + str(user_id))

        # start date - in the middle of the first booking (invalid)
        self.type("#start", "2022\t1218")
        self.type("#end", "2022\t1225")
        self.click('input[type="submit"]')
        # Needs to return an error
        self.assert_element("#message")
        self.assert_text("Booking Failed!", "#message")

        # start date - a day before the first booking ends (invalid)
        self.type("#start", "2022\t1219")
        self.type("#end", "2022\t1225")
        self.click('input[type="submit"]')
        # Needs to return an error
        self.assert_element("#message")
        self.assert_text("Booking Failed!", "#message")

    def test_booking_output_success(self, *_):
        """
        This is a front end unit test to the booking page using output
        partitioning tests.
        Possible Outputs: msg=Booking Failed,
        redirect to home page
        Requirements tested: Booking Requirement 1, 4, 5
        """

        FrontEndTest.test_booking_helper(self)

        user = User.query.filter(User.email == "user202@test.com").all()
        user_id = user[0].id
        listing = Listing.query.filter(Listing.title == "First Listing").all()
        listing_id = listing[0].id
        self.open(base_url + "/book-listing/" + str(listing_id) +
                  "/" + str(user_id))

        # Valid input, redirect to homepage with booked listings
        self.type("#start", "2022\t1215")
        self.type("#end", "2022\t1220")
        self.click('input[type="submit"]')
        # Needs to take the user to the home page
        self.assert_element("#welcome-header")
        # Shows booked listings
        self.assert_element("#bookedListings")
        self.assert_text("First Listing", "#listingTitle")

        self.open(base_url + "/book-listing/" + str(listing_id) +
                  "/" + str(user_id))

        # Invalid input
        self.type("#start", "2022\t1217")
        self.type("#end", "2022\t1220")
        self.click('input[type="submit"]')
        # Needs to return an error
        self.assert_element("#message")
        self.assert_text("Booking Failed!", "#message")

    def test_booking_helper(self, *_):
        """
        This is a helper function to set up the database for the tests.
        Create two testing users, and create listings.
        """

        User.query.delete()
        Listing.query.delete()
        Booking.query.delete()

        # Clear Database for the test user
        User.query.filter(User.email == "user101@test.com").delete()
        db.session.commit()

        # Create a new User
        self.open(base_url + "/register")
        # fill details
        self.type("#email", "user101@test.com")
        self.type("#real_name", "User Test")
        self.type("#name", "User")
        self.type("#password", "User!123")
        self.type("#password2", "User!123")
        # click register button
        self.click('input[type="submit"]')

        # Login as the first User
        self.open(base_url + "/login")
        # fill email and password
        self.type("#email", "user101@test.com")
        self.type("#password", "User!123")
        # click enter button
        self.click('input[type="submit"]')

        # Create a new listing #1
        self.open(base_url + "/create-listing")
        self.type("#title", "First Listing")
        self.type("#description", "This is the first test description")
        self.type("#price", "10.00")
        self.click('input[type="submit"]')

        # Create a new listing #2
        self.open(base_url + "/create-listing")
        self.type("#title", "Second Listing")
        self.type("#description", "This is the second test description")
        self.type("#price", "120.00")
        self.click('input[type="submit"]')

        # Logout as the first user
        self.open(base_url + "/logout")

        # Create a second User
        self.open(base_url + "/register")
        # fill details
        self.type("#email", "user202@test.com")
        self.type("#real_name", "Second User")
        self.type("#name", "Second")
        self.type("#password", "User!123")
        self.type("#password2", "User!123")
        # click register button
        self.click('input[type="submit"]')

        # Login as the second User
        self.open(base_url + "/login")
        # fill email and password
        self.type("#email", "user202@test.com")
        self.type("#password", "User!123")
        # click enter button
        self.click('input[type="submit"]')
