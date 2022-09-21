from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Setting up SQLAlchemy and data models so we can map data models 
# into database tables.
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)


# A class to represent a qB&B property.
class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Stores the street address (in the format of: 1209 King St W Suite 201).
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

    def __repr__(self):
        return '<Property %r>' % self.id
