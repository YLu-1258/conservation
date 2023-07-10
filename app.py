from flask import render_template, request, session, redirect, make_response

from functools import wraps

from conservation import app, db
from conservation.model.user import init_accounts
from conservation.model.students import init_students
from conservation.model.history import init_entrys

from conservation.model.user import User
from conservation.model.students import Student

from conservation.api.api import users_bp
from conservation.api.api import points_bp
from conservation.api.api import missions_bp
from conservation.api.api import history_bp

app.register_blueprint(users_bp)
app.register_blueprint(points_bp)
app.register_blueprint(missions_bp)
app.register_blueprint(history_bp)

@app.before_first_request
def init_db():
    with app.app_context():
        db.create_all()
        init_accounts()
        init_students()
        # init_missions()
        init_entrys()

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
        
        user = User.query.filter_by(_username = username).all()

        if user:
            if user[0].verify_password(password):
                # Authentication successful, store user ID in the session   
                session['user_id'] = user[0].id
                response = make_response(redirect('/'))
                response.set_cookie('user_id', str(user[0].id))
                return response
        return render_template('login.html', error="Invalid Credentials")
    else:
        # GET request, render the login page
        return render_template('login.html')
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    # If we receive a form input from the frontend
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Perform authentication logic using the provided credentials
        
        exist = User.query.filter_by(_username = username).all()

        if exist:
             return render_template('register.html', error="Username Exists")
        
        user = User(username, password, 2)
        user.create()
        uuid = user = User.query.filter_by(_username = username).all()[0].id
        print(uuid)
        student = Student(uuid, username, None, 0, 0)
        student.create()
        return render_template('login.html', notif=f'Standard User "{username}" created')
    else:
        # GET request, render the login page
        return render_template('register.html')
    
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
    return render_template("about.html")

@app.route('/history')
def history():
    return render_template("history.html")

@app.route('/leaderboard')
def leaderboard():
    return render_template("leaderboard.html")

@app.route('/tutorial')
def tutorial():
    return render_template("tutorial.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="8133")