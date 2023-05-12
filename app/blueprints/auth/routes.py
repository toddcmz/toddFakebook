from flask import render_template, flash, redirect, url_for
from . import bp
from app.forms import RegisterForm
from app.forms import SigninForm
from app.models import User
from app import db
from flask_login import login_user, logout_user, login_required, current_user

@bp.route('/signin', methods=['GET', 'POST'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('main.home')) # this is saying you can't visit this page if you're already signed in
    form = SigninForm()
    if form.validate_on_submit():
        thisUser = User.query.filter_by(username=form.username.data).first()
        if thisUser and thisUser.check_password(form.password.data):
            flash(f'{form.username.data} signed in', 'success')
            login_user(thisUser)
            return redirect(url_for('main.home'))
        else:
            flash(f'{form.username.data} does not exist or incorrect password', 'warning')
    return render_template('signin.jinja', title='Sign In', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated: # this is saying you can't visit this page if you're already signed in
        return redirect(url_for('main.home'))
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        checkUser = User.query.filter_by(username=username).first()
        checkEmail = User.query.filter_by(email=email).first()
        if not checkUser and not checkEmail:
            thisUser = User(username=username, email=email)
            thisUser.password = thisUser.hash_password(form.password.data)
            thisUser.add_token()
            thisUser.commit()
            flash(f"Username '{username}' submitted a sign up request", 'success')
            return redirect(url_for('main.home'))
        elif checkUser:
            flash(f'{username} already taken, try again', 'warning')
        else:
            flash(f'{email} already taken, try again', 'warning')
    return render_template('register.jinja', title='Register', form = form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))