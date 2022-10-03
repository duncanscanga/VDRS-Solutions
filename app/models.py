from app import app
from flask_sqlalchemy import SQLAlchemy


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
    property_id = db.Column(db.Integer, nullable=False)

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
    owner_id = db.Column(db.Integer, nullable=False)
    # Stores the id of the review of the guest (not required)
    review_id = db.Column(db.Integer, nullable=False)
    # Stores start date of the listing (not required)
    start_date = db.Column(db.Date, nullable=False)
    # Stores end date of the listing (not required)
    end_date = db.Column(db.Date, nullable=False)

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
    real_name = db.Column(db.String(80), unique=False, nullable=False)

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
    review_score = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<User %r>" % self.id


# create all tables
db.create_all()


def register(name, email, real_name, password, b, p):
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
                password=password, billing_address=b,
                postal_code=p)
    # add it to the current database session
    db.session.add(user)
    # actually save the user object
    db.session.commit()

    return True


def login(email, password):
    '''
    Check login information
      Parameters:
        email (string):    user email
        password (string): user password
      Returns:
        The user object if login succeeded otherwise None
    '''
    valids = User.query.filter_by(email=email, password=password).all()
    if len(valids) != 1:
        return None
    return valids[0]
