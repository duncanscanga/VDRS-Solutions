from app import app
from app.models import *        # noqa: F403,F401
from app.controllers import *   # noqa: F403,F401

"""
This file runs the server on port 8081
"""

FLASK_PORT = 8081

if __name__ == "__main__":
    app.run(debug=True, port=FLASK_PORT)
