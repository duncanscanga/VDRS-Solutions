from flask import render_template, request, session, redirect
from app.models import create_listing, login, User, register, update_listing, \
    update_user, find_listings, find_listing_by_id

from app import app


def authenticate(inner_function):
    """
    :param inner_function: any python function that accepts a user object
    Wrap any python function and check the current session to see if
    the user has logged in. If login, it will call the inner_function
    with the logged in user object.
    To wrap a function, we can put a decoration on that function.
    Example:
    @authenticate
    def home_page(user):
        pass
    """

    def wrapped_inner():

        # check did we store the key in the session
        if 'logged_in' in session:
            email = session['logged_in']
            try:
                user = User.query.filter_by(email=email).one_or_none()
                if user:
                    # if the user exists, call the inner_function
                    # with user as parameter
                    return inner_function(user)
            except Exception:
                pass
        else:
            # else, redirect to the login page
            return redirect('/login')

    # return the wrapped version of the inner_function:
    # Changed: ensure unique wrapper by using function name
    # to avoid overwriting error.
    wrapped_inner.__name__ = inner_function.__name__
    return wrapped_inner


@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html', message='Please login')


@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    user = login(email, password)
    if user:
        session['logged_in'] = user.email
        """
        Session is an object that contains sharing information
        between a user's browser and the end server.
        Typically it is packed and stored in the browser cookies.
        They will be past along between every request the browser made
        to this services. Here we store the user object into the
        session, so we can tell if the client has already login
        in the following sessions.
        """
        # success! go back to the home page
        # code 303 is to force a 'GET' request
        return redirect('/', code=303)
    else:
        return render_template('login.html', message='login failed')


@app.route('/')
@authenticate
def home(user):
    # authentication is done in the wrapper function
    # see above.
    # by using @authenticate, we don't need to re-write
    # the login checking code all the time for other
    # front-end portals

    listings = find_listings(user.id)
    return render_template('index.html', user=user, listings=listings)


@app.route('/register', methods=['GET'])
def register_get():
    # templates are stored in the templates folder
    return render_template('register.html', message='')


@app.route('/register', methods=['POST'])
def register_post():
    email = request.form.get('email')
    name = request.form.get('name')
    real_name = request.form.get('real_name')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    error_message = None

    if password != password2:
        error_message = "The passwords do not match"
    else:
        # use backend api to register the user
        success = register(name, email, real_name, password)
        if not success:
            error_message = "Registration failed."
    # if there is any error messages when registering new user
    # at the backend, go back to the register page.
    if error_message:
        return render_template('register.html', message=error_message)
    else:
        return redirect('/login')


@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in', None)
    return redirect('/')


# Route to send the user update template
@app.route('/update-user', methods=['GET'])
@authenticate
def get_update_user(user):
    # Return the template with the user's current information
    return render_template(
        'update_user.html',
        user=user,
        msg="Please modify the information you want to update below.")


# Route to receive the updated user information
@app.route('/update-user', methods=['POST'])
@authenticate
def post_update_user(user):
    # First grab form data
    curr_name = user.username
    new_name = request.form.get('name')
    new_email = request.form.get('email')
    new_addr = request.form.get('billing-address')
    new_postal = request.form.get('postal-code')

    # Evaluate if the update was successful:
    success = update_user(curr_name, new_name, new_email, new_addr, new_postal)
    # If so, return to home page
    # If not, stay on update_user.html with error msg
    if success:
        return redirect('/')
    else:
        return render_template(
            'update_user.html',
            user=user,
            msg="Update Failed!")


# Route to send the listing update template
@app.route('/update-listing/<int:listing_id>', methods=['GET'])
def get_update_listing(listing_id):
    listing = find_listing_by_id(listing_id)
    # Return the template with the listing's current information
    return render_template(
        'update_listing.html',
        listing=listing[0],
        msg="Please modify the information you want to update below.")


# Route to receive the updated listing information
@app.route('/update-listing/<int:listing_id>', methods=['POST'])
def post_update_listing(listing_id):
    listing = find_listing_by_id(listing_id)
    # First grab form data
    new_title = request.form.get('title')
    new_description = request.form.get('description')
    new_price = request.form.get('price')

    # Evaluate if the update was successful:
    success = update_listing(listing[0].id, new_title, new_description,
                             listing[0].price, float(new_price),
                             listing[0].owner_id)
    # If so, return to home page
    # If not, stay on update_listing.html with error msg
    if success:
        return redirect('/')
    else:
        return render_template(
            'update_listing.html',
            listing=listing[0],
            msg="Update Failed!")


# Route to create a new listing
@app.route('/create-listing', methods=['GET'])
@authenticate
def get_create_listing(user):
    return render_template(
        'create_listing.html',
        user=user,
        msg="Please modify the information you want to update below.")


# Route to receive the updated listing information
@app.route('/create-listing', methods=['POST'])
@authenticate
def post_create_listing(user):
    # First grab form data
    new_title = request.form.get('title')
    new_description = request.form.get('description')
    new_price = request.form.get('price')

    # Evaluate if the update was successful:
    success = create_listing(new_title, new_description, float(new_price),
                             user.id)
    # If so, return to home page
    # If not, stay on create_listing.html with error msg
    if success:
        return redirect('/')
    return render_template(
        'create_listing.html',
        user=user,
        msg="Creation Failed!")
