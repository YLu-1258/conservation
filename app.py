from flask import render_template  # import render_template from "public" flask libraries

# import "packages" from "this" project
from flask_migrate import Migrate
from backend import app, db  # Definitions initialization
from backend.model.user import init_accounts
from backend.model.students import init_students
from backend.model.missions import init_missions

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

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/profile')
def profile():
    return render_template("profile.html")

@app.route('/about')
def about():
    return render_template("about .html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="8133")