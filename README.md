# VDRS-Solutions - CMPE 327 Software Quality Assurance Project
[![Pytest - All Tests](https://github.com/duncanscanga/VDRS-Solutions/actions/workflows/pytest.yml/badge.svg)](https://github.com/duncanscanga/VDRS-Solutions/actions/workflows/pytest.yml)
[![PEP8 Format Test](https://github.com/duncanscanga/VDRS-Solutions/actions/workflows/style_check.yml/badge.svg)](https://github.com/duncanscanga/VDRS-Solutions/actions/workflows/style_check.yml)
# Setting up local development environment
The most efficient way to develop Flask projects locally is to create a virtual environment to install Flask and other dependencies. Here's a quick guide to get started.

Each local machine will have its own virtual environment, since they contain files that we don't really want to push up to the repository. So, the `.gitignore` file includes common virtual environment folder names to ensure that this doesn't happen. By following the naming conventions here, the environment won't be added to your commits:
- Head to the root of the project `/VDRS-Solutions` and run: `python -m venv venv`, depending on the Python installation, you might have to replace `python` with `python3`. This creates a virtual environment in the folder `/VDRS-Solutions/venv`.
-  To hop into this environment, run `source venv/Scripts/activate` or `venv\Scripts\activate` in Windows CMD. In the terminal, you should now see an indication that you're now using the virtual environment.
- VSCode often needs to be told to use the virtual environment as the Python interpreter, to specify this, type `ctrl+shift+p`, and search `select interpreter`. From there, you can add the path of your venv's python.exe file, for example: `VDRS-Solutions/venv/Scripts/python.exe`.
- The first time you start the environment, you have to download the dependencies that the project uses. All of these should be added to the `requirements.txt` file. So in the terminal: `pip install -r requirements.txt`. This will download all the dependencies onto the virtual environment.
- We're almost ready to start the Flask app. We also need to specify which file contains the Flask app, so in the terminal: `export FLASK_APP=__init__.py` or `set FLASK_APP=__init__.py`.
- By default, Flask does not reload the server whenever a change is made, which means we have to manually restart it everytime we add a new feature. Instead, when developing, we can turn on debugging mode: `export FLASK_DEBUG=1`. Now, everytime the file is saved, the server will hot-reload.
- To start the app, `flask run` will start the server @ http://localhost:5000 . 
- To test formatting, head to the directory of the files that should be tested, and run `flake8`. Ensure to fix any warnings that show up before suggesting changes through a PR.
