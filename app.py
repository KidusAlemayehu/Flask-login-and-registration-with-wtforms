from flask import Flask, render_template, url_for, redirect, session, request, flash
from db import db
from forms import RegistrationForm, LoginForm
from model import User
from flask_migrate import Migrate
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
db.init_app(app)
migrate = Migrate(app, db)
app.config['SECRET_KEY'] = 'e581349e00c89fc8ffa0ae9f8e04828c8bc8b016359c99860255a11965134317'
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://postgres:'your_db_pwd'@localhost/Flask-Login-with-WTForms"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


@app.route("/")
def index(username):
    return render_template('index.html', username=username, title='Home')


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', form=form, title='Login')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            org_pwd = form.password.data
            if User.get_user_by_username(username=username):
                if User.get_user_by_email(email=email):
                    flash(f'User Already exists', 'danger')
                    return redirect(url_for('register'))
                else:
                    flash(
                        f'Welcome {form.username.data}!, You have registered successfully', 'success')
                    return redirect(url_for('login'))
            elif User.get_user_by_email(email=email):
                flash(f'Email is Already in use', 'danger')
                return redirect(url_for('register'))
            hs_pwd = generate_password_hash(org_pwd, method='pbkdf2:sha256')
            user = User(username=username, email=email, password=hs_pwd)
            user.save()
            flash(
                f'Welcome {form.username.data}!, You have registered successfully', 'success')
            return redirect(url_for('login'))
    elif request.method == 'GET':
        return render_template('register.html', form=form, title='Register')


if __name__ == '__main__':
    app.app_context().push()
    app.run(debug=True)
