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

    id = db.Column(db.Integer, primary_key=True)
    # Stores the corresponding property's id
    property_id = db.Column(db.Integer, nullable=False)
    # Stores the corresponding home owner's id
    owner_id = db.Column(db.Integer, nullable=False)
    # Stores decimal cost of listing
    price = db.Column(db.Float, nullable=False)
    # Stores start and end datetime.date() object
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return "<Listing %r>" % self.id


class Booking(db.Model):
    """A class to represent a qB&B Booking."""

    id = db.Column(db.Integer, primary_key=True)
    # Stores the corresponding listing ID
    listing_id = db.Column(db.Integer, nullable=False)
    # Stores the corresponding renter ID
    renter_id = db.Column(db.Integer, nullable=False)
    # Stores the review of the guest in paragraph form
    review = db.Column(db.String(200), nullable=False)
    # Stores the number 1-5 rating
    review_score = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<Booking %r>" % self.id


class User(db.Model):
    """A class to represent the User Entity."""

    id = db.Column(db.Integer, primary_key=True)
    # Stores the id
    username = db.Column(db.String(80), unique=True, nullable=False)
    # Stores the username
    email = db.Column(db.String(120), unique=True, nullable=False)
    # Stores the email
    real_name = db.Column(db.String(80), unique=True, nullable=False)
    # Stores the real name
    money = db.Column(db.Integer)
    # Stores the amount of money
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return "<User %r>" % self.id


# create all tables
db.create_all()


def register(name, email, password):
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
    user = User(username=name, email=email, password=password)
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
