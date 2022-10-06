from app import app
from flask_sqlalchemy import SQLAlchemy
from validate_email import validate_email
from datetime import date


'''
This file defines data models and related business logics
'''


db = SQLAlchemy(app)


class Property(db.Model):
    """A class to represent a qB&B property."""

    id = db.Column(db.Integer, primary_key=True)
    # Stores the street address (format: 1209 King St W Suite 201).
    address = db.Column(db.String(120), nullable=False)
    # Stores the size of the property (in square feet).
    size = db.Column(db.Integer, nullable=False)
    # Stores the number of guests the property can house.
    guests = db.Column(db.Integer, nullable=False)
    # Stores the name of the city.
    city = db.Column(db.String(80), nullable=False)
    # Stores the name of the country.
    country = db.Column(db.String(80), nullable=False)
    # Stores the name of the state/province.
    state = db.Column(db.String(80), nullable=False)
    # Stores the postal/zip code.
    zip_code = db.Column(db.String(80), nullable=False)
    # Stores the user who created the property
    owner_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<Property %r>" % self.id


class Listing(db.Model):
    """A class to represent a qB&B Listing."""

    # Stores the corresponding property's id
    id = db.Column(db.Integer, primary_key=True)
    # Stores the title
    title = db.Column(db.String(80), nullable=False)
    # Stores the description
    description = db.Column(db.String(200), nullable=False)
    # Stores the corresponding home owner's id
    owner_id = db.Column(db.Integer, nullable=False)
    # Stores decimal cost of listing
    price = db.Column(db.Float, nullable=False)
    # Stores the last modified date
    last_modified_date = db.Column(db.Date, nullable=False)
    # Stores the corresponding property id (not required)
    property_id = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return "<Listing %r>" % self.id


class Booking(db.Model):
    """A class to represent a qB&B Booking."""

    id = db.Column(db.Integer, primary_key=True)
    # Stores the corresponding listing ID
    listing_id = db.Column(db.Integer, nullable=False)
    # Stores decimal cost of listing
    price = db.Column(db.Float, nullable=False)
    # Stores booking date of the listing
    date = db.Column(db.Date, nullable=False)
    # Stores the corresponding renter ID
    user_id = db.Column(db.Integer, nullable=False)
    # Stores the corresponding owner ID (not required)
    owner_id = db.Column(db.Integer, nullable=True)
    # Stores the id of the review of the guest (not required)
    review_id = db.Column(db.Integer, nullable=True)
    # Stores start date of the listing (not required)
    start_date = db.Column(db.Date, nullable=True)
    # Stores end date of the listing (not required)
    end_date = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return "<Booking %r>" % self.id


class User(db.Model):
    """A class to represent the User Entity."""

    # Stores the id
    id = db.Column(db.Integer, primary_key=True)
    # Stores the username
    username = db.Column(db.String(80), nullable=False)
    # Stores the email
    email = db.Column(db.String(120), unique=True, nullable=False)
    # Stores the amount of balance
    balance = db.Column(db.Integer, nullable=False)
    # Stores the password
    password = db.Column(db.String(80), nullable=False)
    # Stores the billing address
    billing_address = db.Column(db.String(200), nullable=False)
    # Stores the postal code
    postal_code = db.Column(db.String(100), nullable=False)
    # Stores the real name (not required)
    real_name = db.Column(db.String(80), unique=False, nullable=True)

    def __repr__(self):
        return "<User %r>" % self.id


class Review(db.Model):
    """A class to represent the Review Entity."""

    # Stores the id
    id = db.Column(db.Integer, primary_key=True)
    # Stores the corresponding reviewers id
    user_id = db.Column(db.Integer, nullable=False)
    # Stores the corresponding listing id
    listing_id = db.Column(db.Integer, nullable=False)
    # Stores the review of the guest in paragraph form
    review_text = db.Column(db.String(200), nullable=False)
    # Stores date of the review
    date = db.Column(db.Date, nullable=False)
    # Stores the number 1-5 rating (not required)
    review_score = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return "<Review %r>" % self.id


# create all tables
db.create_all()


def register(name, email, real_name, password, billing_address, postal_code):
    '''
    Register a new user
      Parameters:
        name (string):     user name
        email (string):    user email
        password (string): user password
      Returns:
        True if registration succeeded otherwise False
    '''
    # check if the email has been used:
    existed = User.query.filter_by(email=email).all()
    if len(existed) > 0:
        return False

    # create a new user
    user = User(username=name, email=email, real_name=real_name, balance=0,
                password=password, billing_address=billing_address,
                postal_code=postal_code)
    # add it to the current database session
    db.session.add(user)
    # actually save the user object
    db.session.commit()

    return True


def login(email, password):
    '''
    Check login information:
      First, email and password inputs needs to meet the same email/
      password requiremnts in the email_check and pw_check functions

      Parameters:
        email (string):    user email
        password (string): user password
      Returns:
        The user object if login succeeded otherwise None
    '''
    # The email and password inputs need to meet the requirements
    # specified in email_check and pw_check
    if email_check(email) and pw_check(password) is True:
        # compare email/password with the originally registered email/password
        valids = User.query.filter_by(email=email, password=password).all()
        if len(valids) != 1:
            return None
        return valids[0]
    else:
        return False


def pw_check(password):
    '''
    Ensure the password is valid
      Parameters:
        password (string):     user password
      Returns:
        True if password is valid otherwise False
    '''
    # Needs to be at least 6 characters
    if len(password) < 6:
        return False

    has_upper = False
    has_lower = False
    has_special = False

    # For each character, update upper, lower,
    # and special flags if char matches the requirement
    for c in password:
        if c.isupper():
            has_upper = True
        elif c.islower():
            has_lower = True
        elif not c.isalnum():
            has_special = True

    # Only return true if all the flags got set to True at least once
    return has_upper and has_lower and has_special


# Uses the validate_email library to ensure the email is valid.
# We can use this single line inside the methods that need it
# instead of leaving it as its own function.
def email_check(email):
    return validate_email(email)


def create_listing(title, description, price, owner_id):
    '''
    Create a new listing object
      Parameters:
        title (string):       title of the listing
        description (string): description of listing
        price (float):        price of listing
        owner_id (int):       id of the owner
      Returns:
        True if the listing can be created, otherwise False
    '''
    # check the requirements
    if (alphanumeric_check(title) and
            length_check(title, 0, 80) and length_check(description, 20, 2000)
            and description_length_check(description, title) and
            range_check(price, 10, 10000) and
            date_check(date.today(), date(2021, 1, 2), date(2025, 1, 2))
            and owner_check(owner_id) and unique_title_check(title)):
        # create a new listing
        listing = Listing(title=title, description=description, price=price,
                          last_modified_date=date.today(), owner_id=owner_id)
        # add it to the current database session
        db.session.add(listing)
        # actually save the user object
        db.session.commit()
        return True
    return False


def alphanumeric_check(title):
    '''
    Check if the given title satisfies:
    R4-1: The title of the product has to be alphanumeric-only,
    and space allowed only if it is not as prefix and suffix.
    Parameters:
        title (string):       title of the listing
    Returns:
        True if the requirements are meant, otherwise False
    '''
    if title[0] == " " or title[-1] == " ":
        return False
    for element in range(0, len(title)):
        if not (title[element].isalnum() or title[element] == " "):
            return False
    return True


def length_check(str, min, max):
    '''
    Check if the length of the string is valid
    Parameters:
        str (string):         string to be checked
        min (int):            minimum bound
        max (int):            maximum bound
    Returns:
        True if the requirements are meant, otherwise False
    '''
    if len(str) <= max and len(str) >= min:
        return True
    return False


def unique_title_check(title):
    '''
    Check if the given title of a listing has already been used.
    Parameters:
        title (string):        title of the listing
    Returns:
        True if the requirements are meant, otherwise False
    '''
    # R4-8: A user cannot create products that have the same title.
    existed = Listing.query.filter_by(title=title).all()
    if len(existed) > 0:
        return False
    return True


def range_check(num, min, max):
    '''
    Check if the num is in the given range
    Parameters:
        num (float):        price to be checked
        min (int):            minimum bound
        max (int):            maximum bound
    Returns:
        True if the requirements are meant, otherwise False
    '''
    if num <= max and num >= min:
        return True
    return False


def description_length_check(description, title):
    '''
    Check if the description is longer than the title
    Parameters:
        description (string):      listing description
        title (string):            listing title
    Returns:
        True if the requirements are meant, otherwise False
    '''
    if len(description) > len(title):
        return True
    return False


def date_check(date, min, max):
    '''
    Check if the date is in the given range
    Parameters:
        date (Date):        date to be checked
        min (Date):         start date
        max (Date):         end date
    Returns:
        True if the requirements are meant, otherwise False
    '''
    if date > min and date < max:
        return True
    return False


def owner_check(owner_id):
    '''
    Check if the given owner id exists in the User table.
    Parameters:
        owner_id (int):        id of the owner of the listing
    Returns:
        True if the requirements are meant, otherwise False
    '''
    existed = User.query.filter_by(id=owner_id).all()
    if len(existed) > 0:
        return True
    return False
