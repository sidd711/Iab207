from flask import (
    Blueprint, flash, render_template, request, url_for, redirect
)
from werkzeug.security import generate_password_hash, check_password_hash
#from .models import User
from .forms import LoginForm, RegisterForm
from flask_login import login_user, login_required, logout_user
from . import db
from .models import User
# JRD COMMENT


# create a blueprint
bp = Blueprint('auth', __name__)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        # get the info input into the form
        inputname = form.user_name.data
        inputpass = form.password.data

        u1 = User.query.filter_by(name=inputname).first()

        if u1 is None:
            error = "Incorrect user name"
        elif not check_password_hash(u1.password_hash, inputpass):
            error = "Incorrect password"
        if error is None:
            login_user(u1)
            print(
                f'Successfully logged in\nUser: {u1.name} \nID: {u1.id}')
            flash('You logged in successfully')
            return redirect(url_for('main.index'))
    return render_template('forms.html', form=form,  heading='Login')


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        print('Register form submitted')
        uname = form.user_name.data
        pwd = form.password.data
        email = form.password.data

        # generate a hashed pwd for security
        pwd_hash = generate_password_hash(pwd)
        # Create a new user object
        new_user = User(name=uname,
                        emailid=email,
                        password_hash=pwd_hash)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created sucessfully.')
        return redirect(url_for('auth.login'))
    return render_template('forms.html', form=form, heading="Register Form")
