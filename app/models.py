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


def register(name, email, real_name, password):
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

    # check if the email and password are not empty:
    if not not_empty(email) and not not_empty(password):
        return False

    # Check that the email has to follow addr-spec defined in RFC 5322
    if not email_check(email):
        return False

    # Check that the password has to meet the required complexity:
    # minimum length 6, at least one upper case, at least one lower
    # case, and at least one special character.
    if not pw_check(password):
        return False

    # Check that has to be non-empty, alphanumeric-only,
    # and space allowed only if it is not as the prefix or suffix
    if not alphanumeric_check(name):
        return False

    # Check that user name is longer than 2 but less than 20
    if not length_check(name, 3, 20):
        return False

    '''
    R1-8: Shipping address is empty at the time of registration.
    R1-9: Postal code is empty at the time of registration.
    R1-10: Balance should be initialized as 100 at the time of registration.
    (free $100 dollar signup bonus).
    '''
    # create a new user
    user = User(username=name, email=email, real_name=real_name, balance=100,
                password=password, billing_address='',
                postal_code='')
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
            and owner_check(owner_id) and unique_title_check(title, 0)):
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


def unique_title_check(title, listing_id):
    '''
    Check if the given title of a listing has already been used.
    Parameters:
        title (string):        title of the listing
    Returns:
        True if the requirements are meant, otherwise False
    '''
    # R4-8: A user cannot create products that have the same title.
    existed = Listing.query.filter_by(title=title).all()
    # Checking if the title was unchanged
    if len(existed) == 1 and existed[0].id == listing_id:
        return True
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


def update_user(curr_name, new_name, new_email, new_addr, new_postal, new_pw):
    '''
    R3-1, R3-4: Allow user to update username, password, email,
    billing addr, and postal code.
    Parameters:
        curr_name   (String):     current username
        new_name    (String):     updated username
        new_email   (String):     updated email
        new_addr    (String):     updated billing address
        new_postal  (String):     updated postal code
        new_pw      (String):     updated password
    Returns:
        True if the transaction is successful, False otherwise
    '''
    # If the current user exists
    valid = User.query.filter_by(username=curr_name).all()
    if len(valid) == 1:
        # We check if the new information is of a valid format
        if (
            (postal_code_check(new_postal) or len(new_postal) == 0) and
            email_check(new_email) and
            alphanumeric_check(new_name) and
            length_check(new_name, 3, 19) and
            pw_check(new_pw)
        ):

            # We then check if the new username and email are unique:
            # If the user didn't update their existing names/passwords,
            # the query will return 1, which is ok (it's their record),
            # so ensure that the name and email have indeed been updated.
            if (
                ((len(User.query.filter_by(username=new_name).all()) > 0)
                    and valid[0].username != new_name) or
                ((len(User.query.filter_by(email=new_email).all()) > 0)
                    and valid[0].email != new_email)
            ):
                return False
            # If they're unique, update all the fields
            else:
                valid[0].username = new_name
                valid[0].email = new_email
                valid[0].billing_address = new_addr
                valid[0].postal_code = new_postal
                valid[0].password = new_pw
                db.session.commit()
                return True
        else:
            # If any of the fields are not formatted properly, return False
            return False
    else:
        # If the current user does not exist, return False right away
        return False


def postal_code_check(postal_code):
    '''
    R3-2, R3-3: Ensures postal code is a valid Canadian postal code.
    Parameters:
        postal_code (String):   new or updated code
    Returns:
        True if the postal code is valid, False otherwise
    '''
    if len(postal_code) != 7:
        return False

    if (
        (not postal_code[0].isalpha()) or
        (not postal_code[1].isnumeric()) or
        (not postal_code[2].isalpha()) or
        (not postal_code[3] == " ") or
        (not postal_code[4].isnumeric()) or
        (not postal_code[5].isalpha()) or
        (not postal_code[6].isnumeric())
    ):
        return False
    else:
        return True


def not_empty(word):
    '''
    Checks R1-1 if the email
    or password is empty
    '''
    if len(word) == 0:
        return False
    return True


def update_listing(listing_id, new_title, new_desc, curr_price, new_price,
                   owner_id):
    '''
    R5-1, R5-2, R5-4: Can only update title, desc, and price
    Parameters:
        listing_id  (int):      listing id
        new_title   (String):   updated title
        new_desc    (String):   updated description
        curr_price  (float):    original price
        new_price   (float):    updated price
        owner_id    (int):      owner id
    Returns:
        True if the update is successful, False otherwise
    '''

    # Check if the listing exists using the id or the owner_id
    if listing_id != 0:
        listing = Listing.query.filter_by(id=listing_id).all()
    else:
        listing = Listing.query.filter_by(owner_id=owner_id).all()
    if len(listing) > 0:
        # Check if the format of the new information is correct
        if (alphanumeric_check(new_title) and
                length_check(new_title, 0, 80) and
                length_check(new_desc, 20, 2000)
                and description_length_check(new_desc, new_title) and
                range_check(new_price, curr_price, 10000) and
                unique_title_check(new_title, listing_id) and
                listing[0].owner_id == owner_id):
            # Update title, description and price
            listing[0].title = new_title
            listing[0].description = new_desc
            listing[0].price = new_price

            # When the update operations are successful,
            # update the modified date
            # Check if the new date format is correct
            if (date_check(date.today(), date(2021, 1, 2), date(2025, 1, 2))):
                # Update the modified date
                listing[0].last_modified_date = date.today()
                db.session.commit()
                return True

            # Modified date does not follow requirements
            else:
                return False

        # New information does not follow required format
        else:
            return False

    # Listing does not exist
    return False


# Returns the listing when the owner id is passed in
def find_listing(owner_id):
    listing = Listing.query.filter_by(owner_id=owner_id).all()
    if len(listing) > 0:
        return listing[0]
    return False


def find_listings(owner_id):
    '''
    Find listings of a certain owner
    Parameters:
        owner_id    (int):      owner id
    Returns:
        All listings with given owner id
    '''
    listings = Listing.query.filter_by(owner_id=owner_id).all()
    return listings


def find_listing_by_id(listing_id):
    '''
    Find listing of a certain id
    Parameters:
        listing_id    (int):      listing id
    Returns:
        The listing with given id
    '''
    listing = Listing.query.filter_by(id=listing_id).all()
    return listing


def find_listing_by_title(title):
    '''
    Find listing of a certain title
    Parameters:
        title    (string):      listing title
    Returns:
        The listing with given title
    '''
    listing = Listing.query.filter_by(title=title).all()
    return listing
