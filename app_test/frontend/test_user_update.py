from seleniumbase import BaseCase
from app_test.conftest import base_url
from app.models import User
from app.models import db

"""
This file defines all integration tests for the frontend update_user.html page
"""


class FrontEndTest(BaseCase):

    def test_update_user_input(self, *_):
        """
        This is a frontend input partitioning test
        for updating user information.
        Possible inputs:
        R3-2: Valid/Invalid postal code
        R3-4: Valid/Invalid username
        R3-1: Valid/Invalid email
        Valid/Invalid Password
        """

        FrontEndTest.test_update_helper(self)

        # All invalid inputs
        FrontEndTest.clear_keys(self)
        self.type("#email", "a")
        self.type("#name", "a")
        self.type("#password", "a")
        self.type("#postal-code", "a")
        self.click('input[type="submit"]')
        self.assert_element("#message")
        self.assert_text("Update Failed!", "#message")

        # Just invalid email, no other updates
        self.open(base_url + "/update-user")
        self.find_element("#email").clear()
        self.type("#email", "a")
        self.click('input[type="submit"]')
        self.assert_element("#message")
        self.assert_text("Update Failed!", "#message")

        # Just invalid password, no other updates
        self.open(base_url + "/update-user")
        self.find_element('#password').clear()
        self.type("#password", "a")
        self.click('input[type="submit"]')
        self.assert_element("#message")
        self.assert_text("Update Failed!", "#message")

        # Just invalid username, no other updates
        self.open(base_url + "/update-user")
        self.find_element('#name').clear()
        self.type("#name", "a")
        self.click('input[type="submit"]')
        self.assert_element("#message")
        self.assert_text("Update Failed!", "#message")

        # Just invalid postal code, no other updates
        self.open(base_url + "/update-user")
        self.type("#postal-code", "a")
        self.click('input[type="submit"]')
        self.assert_element("#message")
        self.assert_text("Update Failed!", "#message")

        # No updates, should pass
        self.open(base_url + "/update-user")
        self.click('input[type="submit"]')
        # Should be redirected to home page
        self.assert_element("#welcome-header")
        self.assert_text("Welcome Test !", "#welcome-header")

        # Just valid email, no other updates
        self.open(base_url + "/update-user")
        self.find_element("#email").clear()
        self.type("#email", "newemail@gmail.com")
        self.click('input[type="submit"]')
        # If we update the email, the user must log back in
        self.assert_element("#message")
        self.assert_text("Please login to your account", "#message")
        # Delete existing record, re-register
        FrontEndTest.test_update_helper(self)

        # Just valid username, no other updates
        self.open(base_url + "/update-user")
        self.find_element("#name").clear()
        self.type("#name", "newusername")
        self.click('input[type="submit"]')
        self.assert_element("#welcome-header")
        self.assert_text("Welcome newusername !", "#welcome-header")

        # Just valid password, no other updates
        self.open(base_url + "/update-user")
        self.find_element("#password").clear()
        self.type("#password", "Mynewpw123!")
        self.click('input[type="submit"]')
        self.assert_element("#welcome-header")
        self.assert_text("Welcome newusername !", "#welcome-header")

        # Just valid postal code, no other updates
        self.open(base_url + "/update-user")
        self.type("#postal-code", "K7K 1N1")
        self.click('input[type="submit"]')
        self.assert_element("#welcome-header")
        self.assert_text("Welcome newusername !", "#welcome-header")

        # All valid updates
        FrontEndTest.clear_keys(self)
        self.type("#email", "validemail@gmail.com")
        self.type("#name", "validusername")
        self.type("#password", "Validpw123!")
        self.type("#postal-code", "")
        self.type("#billing-address", "")
        self.click('input[type="submit"]')
        # Goes back to login page since we updated email too
        self.assert_element("#message")
        self.assert_text("Please login to your account", "#message")

    def test_update_output(self, *_):
        """
        This is a frontend output partitioning test
        for updating user information.
        Possible outputs:
        - Valid update, redirect to home page
        - Invalid update, error message appears and no redirect occurs
        - Valid update, redirect to login page if email changed
        """

        FrontEndTest.test_update_helper(self)

        # No changes, valid update, redirect to home page
        self.open(base_url + "/update-user")
        self.click('input[type="submit"]')
        self.assert_element("#welcome-header")
        self.assert_text("Welcome Test !", "#welcome-header")

        # Invalid change, error message occurs and no redirect
        self.open(base_url + "/update-user")
        self.find_element("#email").clear()
        self.type("#email", "a")
        self.click('input[type="submit"]')
        self.assert_element("#message")
        self.assert_text("Update Failed!", "#message")

        # Email changes, valid update, redirect to login page
        self.open(base_url + "/update-user")
        self.type("#email", "validemail@gmail.com")
        self.type("#name", "validusername")
        self.click('input[type="submit"]')
        self.assert_element("#message")
        self.assert_text("Please login to your account", "#message")

    def test_update_boundaries(self, *_):
        """
        This is a frontend input boundary test
        for updating user information.
        Boundaries:
        - R1-1 Email and password cannot be empty
        - R1-4 Password length: min 6
        - R1-5 Username cannot be empty
        """

        FrontEndTest.test_update_helper(self)

        # Email cannot be empty
        self.open(base_url + "/update-user")
        self.find_element("#email").clear()
        self.type("#email", "a")
        self.click('input[type="submit"]')
        self.assert_element("#email")  # Remain on update page

        # Password cannot be empty
        self.open(base_url + "/update-user")
        self.find_element("#password").clear()
        self.click('input[type="submit"]')
        self.assert_element("#email")  # Remain on update page

        # Password with less than 6 characters:
        self.open(base_url + "/update-user")
        self.find_element("#password").clear()
        self.type("#password", "aA1!#")
        self.click('input[type="submit"]')
        self.assert_element("#message")
        self.assert_text("Update Failed!", "#message")

        # Password with exactly 6 characters:
        self.open(base_url + "/update-user")
        self.find_element("#password").clear()
        self.type("#password", "aA1!#A")
        self.click('input[type="submit"]')
        self.assert_element("#welcome-header")
        self.assert_text("Welcome Test !", "#welcome-header")

        # Empty username
        self.open(base_url + "/update-user")
        self.find_element("#name").clear()
        self.click('input[type="submit"]')
        self.assert_element("#email")  # Remain on update page

    def clear_keys(self, *_):
        """
        This helper method clears all fields
        of update-user to ensure fresh test inputs
        """
        self.open(base_url + "/update-user")
        self.find_element("#email").clear()
        self.find_element("#password").clear()
        self.find_element("#name").clear()
        self.find_element("#postal-code").clear()
        self.find_element("#billing-address").clear()

    def test_update_helper(self, *_):
        """
        This is a helper function to set up the database for the tests.
        We need to create a testing user, and to log in as this user.
        """

        User.query.delete()

        # Clear Database for the test user
        User.query.filter(User.email == "test2@test.com").delete()
        db.session.commit()

        # Create a new User
        self.open(base_url + "/register")
        # fill details
        self.type("#email", "test2@test.com")
        self.type("#real_name", "real username")
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
