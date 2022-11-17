from seleniumbase import BaseCase
from app_test.conftest import base_url
from app.models import User
from app.models import db

"""
This file defines all integration tests for the frontend login page.
"""


class FrontEndTest(BaseCase):

    def test_create_listing_input_success(self, *_):
        """
        This is a front end unit test to the login page using input
        partitioning tests.
        Possible inputs: valid/invalid email, valid/invalid password
        Requirements tested: R2-1
        """

        FrontEndTest.test_login_helper(self)

        # Invalid email, valid password
        self.open(base_url + "/login")
        self.type("#email", "InvalidEmail")
        self.type("#password", "User!123")
        self.click('input[type="submit"]')
        # Needs to return an error
        self.assert_element("#message")
        self.assert_text("Incorrect email or password.", "#message")

        # Valid email, invalid password
        self.type("#email", "test4@test.com")
        self.type("#password", "User!12")
        self.click('input[type="submit"]')
        # Needs to return an error
        self.assert_element("#message")
        self.assert_text("Incorrect email or password.", "#message")

        # Valid email, valid password
        self.type("#email", "test4@test.com")
        self.type("#password", "User!123")
        self.click('input[type="submit"]')
        # Needs to take the user to the home page
        self.assert_element("#welcome-header")

    def test_login_requirements_success(self, *_):
        """
        This is a front end unit test to the login page using requirements
        partitioning tests.
        Requirements tested: R1-3, R1-4
        """

        FrontEndTest.test_login_helper(self)

        # Password not long enough
        self.open(base_url + "/login")
        self.type("#email", "test4@test.com")
        self.type("#password", "Usr!1")
        self.click('input[type="submit"]')
        # Needs to return an error
        self.assert_element("#message")
        self.assert_text("Incorrect email or password.", "#message")

        # Passoword is long enough
        self.open(base_url + "/login")
        self.type("#email", "test4@test.com")
        self.type("#password", "User!123")
        self.click('input[type="submit"]')
        # Needs to take the user to the home page
        self.assert_element("#welcome-header")

        # Password doesnot have an upper case letter
        self.open(base_url + "/login")
        self.type("#email", "test4@test.com")
        self.type("#password", "user!123")
        self.click('input[type="submit"]')
        # Needs to return an error
        self.assert_element("#message")
        self.assert_text("Incorrect email or password.", "#message")

        # Password has an upper case letter
        self.open(base_url + "/login")
        self.type("#email", "test4@test.com")
        self.type("#password", "User!123")
        self.click('input[type="submit"]')
        # Needs to take the user to the home page
        self.assert_element("#welcome-header")

        # Password doesnot have a lower case letter
        self.open(base_url + "/login")
        self.type("#email", "test4@test.com")
        self.type("#password", "USER!123")
        self.click('input[type="submit"]')
        # Needs to return an error
        self.assert_element("#message")
        self.assert_text("Incorrect email or password.", "#message")

        # Password has a lower case letter
        self.open(base_url + "/login")
        self.type("#email", "test4@test.com")
        self.type("#password", "User!123")
        self.click('input[type="submit"]')
        # Needs to take the user to the home page
        self.assert_element("#welcome-header")

        # Password doesnot have a special character
        self.open(base_url + "/login")
        self.type("#email", "test4@test.com")
        self.type("#password", "user123")
        self.click('input[type="submit"]')
        # Needs to return an error
        self.assert_element("#message")
        self.assert_text("Incorrect email or password.", "#message")

        # Password has a special character
        self.open(base_url + "/login")
        self.type("#email", "test4@test.com")
        self.type("#password", "User!123")
        self.click('input[type="submit"]')
        # Needs to take the user to the home page
        self.assert_element("#welcome-header")

        # Invalid email
        # R1-3 is not valid
        self.open(base_url + "/login")
        self.type("#email", "test4@test...com")
        self.type("#password", "User123!")
        self.click('input[type="submit"]')
        # Needs to return an error
        self.assert_element("#message")
        self.assert_text("Incorrect email or password.", "#message")

        # Valid email
        self.open(base_url + "/login")
        self.type("#email", "test4@test.com")
        self.type("#password", "User!123")
        self.click('input[type="submit"]')
        # Needs to take the user to the home page
        self.assert_element("#welcome-header")

        # Password and email doesnot match, user doesnot exist
        self.open(base_url + "/login")
        self.type("#email", "test4@test.com")
        self.type("#password", "Password123!")
        self.click('input[type="submit"]')
        # Needs to return an error
        self.assert_element("#message")
        self.assert_text("Incorrect email or password.", "#message")

        # Password and email matches, user exists
        self.open(base_url + "/login")
        self.type("#email", "test4@test.com")
        self.type("#password", "User!123")
        self.click('input[type="submit"]')
        # Needs to take the user to the home page
        self.assert_element("#welcome-header")

    def test_login_output_success(self, *_):
        """
        This is a front end unit test to the login page using output
        partitioning tests.
        Possible Outputs: msg=Incorrect email or password,
        redirect to home page
        Requirements tested: R2-1
        """

        FrontEndTest.test_login_helper(self)

        # Invalid input
        self.open(base_url + "/login")
        self.type("#email", "test4@@test.com")
        self.type("#password", "Password123!")
        self.click('input[type="submit"]')
        # Needs to return an error
        self.assert_element("#message")
        self.assert_text("Incorrect email or password.", "#message")

        # Valid input, redirect to home page
        self.open(base_url + "/login")
        self.type("#email", "test4@test.com")
        self.type("#password", "User!123")
        self.click('input[type="submit"]')
        # Needs to take the user to the home page
        self.assert_element("#welcome-header")

    def test_login_helper(self, *_):
        """
        This is a helper function to set up the database for the tests.
        We need to register as a testing user.
        """

        User.query.delete()

        # Clear Database for the test user
        User.query.filter(User.email == "test4@test.com").delete()
        db.session.commit()

        # Create a new User
        self.open(base_url + "/register")
        # fill details
        self.type("#email", "test4@test.com")
        self.type("#real_name", "User4 Test")
        self.type("#name", "User4")
        self.type("#password", "User!123")
        self.type("#password2", "User!123")
        # click register button
        self.click('input[type="submit"]')
