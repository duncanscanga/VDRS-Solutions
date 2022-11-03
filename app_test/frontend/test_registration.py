from seleniumbase import BaseCase
from app_test.conftest import base_url


class FrontEndTest(BaseCase):
    def test_register_input_success(self, *_):
        """
        This is a front end unit test to the register page using input
        partitioning tests.
        Possible inputs: valid/invalid email, valid/invalid full name,
        valid/invalid name, valid/invalid password, valid,invalid
        confirm password
        Requirements tested: R1-1, R1-3, R1-5
        The R1 tests don't give an error message,
        instead a prompt appears on the registration
        page asking you to input the email or password
        you left empty.
        """

        # empty email, valid full name, valid name,
        # valid password, valid confirm password
        # R1-1 not valid
        self.open(base_url + "/register")
        self.type("#real_name", "real_u10")
        self.type("#name", "u10")
        self.type("#password", "12345Aa#")
        self.type("#password2", "12345Aa#")
        self.click('input[type="submit"]')
        # stay on the register page
        self.assert_element("#email")

        # valid email, valid full name, valid name,
        # empty password, valid confirm password
        # R1-1 not valid
        self.open(base_url + "/register")
        self.type("#email", "valid@gmail.com")
        self.type("#real_name", "real_u10")
        self.type("#name", "u10")
        self.type("#password2", "12345Aa#")
        self.click('input[type="submit"]')
        # stay on the register page
        self.assert_element("#password")

        # invalid email, valid full name, valid name,
        # valid password, valid confirm password
        self.open(base_url + "/register")
        # R1-3 not valid
        self.type("#email", "Invalid email")
        self.type("#real_name", "real_u10")
        self.type("#name", "u10")
        self.type("#password", "12345Aa#")
        self.type("#password2", "12345Aa#")
        self.click('input[type="submit"]')
        # should return an error
        self.assert_element("#message")
        self.assert_text("Registration failed.", "#message")

        # valid email, valid full name, invalid name,
        # valid password, valid confirm password
        self.open(base_url + "/register")
        self.type("#email", "valid@gmail.com")
        self.type("#real_name", "real_u10")
        # R1-5 not valid
        self.type("#name", " u10")
        self.type("#password", "12345Aa#")
        self.type("#password2", "12345Aa#")
        self.click('input[type="submit"]')
        # should return an error
        self.assert_element("#message")
        self.assert_text("Registration failed.", "#message")

        # valid email, valid full name, valid name
        # valid password, valid confirm password
        self.open(base_url + "/register")
        self.type("#email", "valid@gmail.com")
        self.type("#real_name", "real_person")
        self.type("#name", "real")
        self.type("#password", "12345Aa#")
        self.type("#password2", "12345Aa#")
        self.click('input[type="submit"]')
        # takes the user to the login page
        self.assert_element("#message")
        self.assert_text("Please login to your account", "#message")

    def test_register_boundary_success(self, *_):
        """
        This is a front end unit test for the register page using
        input boundary tests.
        Password has to be longer than 5 characters.
        The password also has to have one uppercase, lowercase
        and special character.
        Inputs of strings with length: 5,6

        Username has to be longer than 2 but less than 20 characters.
         Inputs of strings with length: 2,3,19,20

        Requirements tested: R1-4,R1-6
        """

        # valid email, valid full name, valid name
        # invalid password, valid confirm password
        self.open(base_url + "/register")
        self.type("#email", "valid2@gmail.com")
        self.type("#real_name", "real_u10")
        self.type("#name", "u10")
        # R1-4 not valid
        self.type("#password", "12Aa#")
        self.type("#password2", "12Aa#")
        self.click('input[type="submit"]')
        # should return an error
        self.assert_element("#message")
        self.assert_text("Registration failed.", "#message")

        # valid email, valid full name, valid name
        # valid password, valid confirm password
        self.open(base_url + "/register")
        self.type("#email", "valid2@gmail.com")
        self.type("#real_name", "real_u10")
        self.type("#name", "u10")
        self.type("#password", "123Aa#")
        self.type("#password2", "123Aa#")
        self.click('input[type="submit"]')
        # takes the user to the login page
        self.assert_element("#message")
        self.assert_text("Please login to your account", "#message")

        # invalid name length less than 3
        self.open(base_url + "/register")
        self.type("#email", "valid3@gmail.com")
        self.type("#real_name", "real_u10")
        # R1-6 not valid
        self.type("#name", "u1")
        self.type("#password", "12345Aa#")
        self.type("#password2", "12345Aa#")
        self.click('input[type="submit"]')
        # should return an error
        self.assert_element("#message")
        self.assert_text("Registration failed.", "#message")

        # valid name length 3
        self.open(base_url + "/register")
        self.type("#email", "valid3@gmail.com")
        self.type("#real_name", "real_u10")
        self.type("#name", "u10")
        self.type("#password", "12345Aa#")
        self.type("#password2", "12345Aa#")
        self.click('input[type="submit"]')
        # takes the user to the login page
        self.assert_element("#message")
        self.assert_text("Please login to your account", "#message")

        # valid name length 19
        self.open(base_url + "/register")
        self.type("#email", "valid4@gmail.com")
        self.type("#real_name", "real_u10")
        self.type("#name", "u101111111111111111")
        self.type("#password", "12345Aa#")
        self.type("#password2", "12345Aa#")
        self.click('input[type="submit"]')
        # takes the user to the login page
        self.assert_element("#message")
        self.assert_text("Please login to your account", "#message")

        # valid name length 20
        self.open(base_url + "/register")
        self.type("#email", "valid5@gmail.com")
        self.type("#real_name", "real_u10")
        self.type("#name", "u1011111111111111111")
        self.type("#password", "12345Aa#")
        self.type("#password2", "12345Aa#")
        self.click('input[type="submit"]')
        # takes the user to the login page
        self.assert_element("#message")
        self.assert_text("Please login to your account", "#message")

    def test_register_output_success(self, *_):
        """
        This is a front end unit test for the register page
        using output partitioning tests.
        Possible Outputs: "Registration failed." ,"The passwords do not match."
        Requirements tested: R1-7
        Also tests if the passwords do not match
        """

        # valid email, valid full name, valid name
        # valid password, invalid confirm password
        self.open(base_url + "/register")
        self.type("#email", "valid6@gmail.com")
        self.type("#real_name", "real_u10")
        self.type("#name", "u10")
        self.type("#password", "123Aa#")
        # passwords do not match
        self.type("#password2", "123")
        self.click('input[type="submit"]')
        # should return an error
        self.assert_element("#message")
        self.assert_text("The passwords do not match.", "#message")

        # valid email, valid full name, valid name
        # valid password, valid confirm password
        self.open(base_url + "/register")
        self.type("#email", "valid6@gmail.com")
        self.type("#real_name", "real_u10")
        self.type("#name", "u10")
        self.type("#password", "123Aa#")
        self.type("#password2", "123Aa#")
        self.click('input[type="submit"]')
        # takes the user to the login page
        self.assert_element("#message")
        self.assert_text("Please login to your account", "#message")

        # invalid email (repeated), valid full name, valid name
        # valid password, valid confirm password
        self.open(base_url + "/register")
        # violates R1-7
        self.type("#email", "valid6@gmail.com")
        self.type("#real_name", "real_u10")
        self.type("#name", "u10")
        self.type("#password", "123Aa#")
        self.type("#password2", "123Aa#")
        self.click('input[type="submit"]')
        # should return an error
        self.assert_element("#message")
        self.assert_text("Registration failed.", "#message")
