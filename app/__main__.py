from app import app
from app.models import *
from app.controllers import *

"""
This file runs the server on port 8081
"""

FLASK_PORT = 8081

if __name__ == "__main__":
    app.run(debug=True, port=FLASK_PORT)
