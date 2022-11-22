from flask import render_template, request, session, redirect
from app.models import create_listing, login, User, register, update_listing, \
    update_user, find_listings, find_listing_by_id, browse_listings, \
    find_bookings, create_booking, find_booked_listing

from app import app
from datetime import datetime


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
    return render_template('login.html',
                           message='Please login to your account')


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
        return render_template('login.html',
                               message='Incorrect email or password.')


@app.route('/')
@authenticate
def home(user):
    # authentication is done in the wrapper function
    # see above.
    # by using @authenticate, we don't need to re-write
    # the login checking code all the time for other
    # front-end portals
    listings = find_listings(user.id)
    bookings = find_bookings(user.id)
    bookedListings = find_booked_listing(user.id)

    return render_template('index.html', user=user, listings=listings,
                           bookings=bookings, bookedListings=bookedListings)


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
        error_message = "The passwords do not match."
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
    curr_email = user.email
    new_name = request.form.get('name')
    new_email = request.form.get('email')
    new_addr = request.form.get('billing-address')
    new_postal = request.form.get('postal-code')
    new_pw = request.form.get('password')

    # Evaluate if the update was successful:
    success = update_user(curr_name, new_name, new_email,
                          new_addr, new_postal, new_pw)
    # If so, return to home page
    # If not, stay on update_user.html with error msg
    if success:
        # We prompt the user to log back in to
        # restore session with valid new email
        if curr_email != new_email:
            return redirect('/logout')
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
    success = create_listing(new_title, new_description, str(new_price),
                             str(user.id))
    # If so, return to home page
    # If not, stay on create_listing.html with error msg
    if success:
        return redirect('/')
    return render_template(
        'create_listing.html',
        user=user,
        msg="Creation Failed!")


# Route to browse all listings
@app.route('/browse-listings', methods=['GET'])
@authenticate
def get_browse_listings(user):
    listings = browse_listings(user.id)
    return render_template(
        'browse_listings.html',
        user=user,
        listings=listings)


# Route to send the booking template
@app.route('/book-listing/<int:listing_id>/<int:user_id>', methods=['GET'])
def get_book_listing(listing_id, user_id):
    listing = find_listing_by_id(listing_id)
    # Return the template with the listing's current information
    return render_template(
        'book_listing.html',
        listing=listing[0],
        msg="Please enter the dates you would like to book.")


# Route to receive the updated booking information
@app.route('/book-listing/<int:listing_id>/<int:user_id>', methods=['POST'])
def post_book_listing(listing_id, user_id):
    listing = find_listing_by_id(listing_id)
    # First grab form data
    start = request.form.get('start')
    end = request.form.get('end')

    start = datetime.strptime(start, '%Y-%m-%d')
    end = datetime.strptime(end, '%Y-%m-%d')

    # Evaluate if the update was successful:
    success = create_booking(listing_id, user_id, start, end)
    # If so, return to home page
    # If not, stay on update_listing.html with error msg
    if success:
        return redirect('/')
    else:
        return render_template(
            'book_listing.html',
            listing=listing[0],
            msg="Booking Failed!")
