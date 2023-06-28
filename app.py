from flask import render_template, request, session, redirect, url_for, make_response  # import render_template from "public" flask libraries

from functools import wraps

from backend import app, db  # Definitions initialization
from backend.model.user import init_accounts
from backend.model.students import init_students
from backend.model.missions import init_missions

from backend.model.user import User
from backend.model.students import Student
from backend.model.missions import Missions

from backend.api.api import users_bp
from backend.api.api import points_bp
from backend.api.api import missions_bp

app.register_blueprint(users_bp)
app.register_blueprint(points_bp)
app.register_blueprint(missions_bp)

@app.before_first_request
def init_db():
    with app.app_context():
        db.create_all()
        init_accounts()
        init_students()
        init_missions()

@app.after_request
def add_cache_control(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' in session:
            # User is logged in, proceed with the decorated function
            return func(*args, **kwargs)
        else:
            # User is not logged in, redirect to login page or return an error response
            return redirect('/login')
    return wrapper

@app.route('/')
@login_required
def home():
    return render_template("home.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    # If we receive a form input from the frontend
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Perform authentication logic using the provided credentials

        try:
            user = User.query.filter_by(_username = username).all()[0]
        except:
            return render_template('login.html', error="Invalid Credentials")


        if user and user.is_password(password):
            # Authentication successful, store user ID in the session
            session['user_id'] = user.id
            response = make_response(redirect('/'))
            response.set_cookie('user_id', str(user.id))
            return response
        else:
            # Authentication failed
            
            return render_template('login.html', error="Invalid Credentials")
    else:
        # GET request, render the login page
        return render_template('login.html')
    
@app.route('/logout')
def logout():
    # Clear the user's session data
    response = make_response(redirect('/login'))
    response.set_cookie('user_id', '', expires=0)
    session.clear()
    # Redirect to the login page or any other desired page
    return response

@app.route('/profile')
def profile():
    return render_template("profile.html")

@app.route('/about')
def about():
    return render_template("about .html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="8133")