from flask import Blueprint, redirect, render_template, flash, session, url_for#, request
from flask_login import login_user,login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from .db_models import db, User, UserStock
from . import login_manager
from .forms import RegisterForm, LoginForm, ChangePWForm

user_bp = Blueprint( 'user_bp', __name__)


@user_bp.route("/user_register", methods=["GET", "POST"])
def register():
    """Register user"""

    form = RegisterForm()
    if form.validate_on_submit():

        # check for exsting user
        user_exist = User.query.filter_by(email = form.email.data).first()
        if user_exist is None:  # if none then no user by that email exists
            new_user = User(firstname = form.firstname.data,
            lastname = form.lastname.data,
            email = form.email.data,
            password = generate_password_hash(form.password.data),
            created = datetime.now())
            db.session.add(new_user)
            db.session.commit()
            flash("Account successfully Registered; Please Log in", 'success')
            return redirect(url_for('user_bp.login'))
        flash("Email already in use", 'warning')
        return redirect(url_for("user_bp.register"))

    return render_template("user_register.html",form = form, title = 'User_Register')



@user_bp.route("/user_login", methods=["GET", "POST"])
def login():
    """ login users """
    form = LoginForm()

    if form.validate_on_submit():

        user_exist = User.query.filter_by(email = form.email.data).first()
        if user_exist:  # if none then no user by that email exists
            if check_password_hash(user_exist.password, form.password.data):
                login_user(user_exist)
                flash("Account successfully Logged In", 'success')
                return redirect(url_for('stock_bp.home'))
            flash('Incorrect Password','warning')
            return redirect(url_for('user_bp.login'))
        flash('Email does not exist','warning')
        return redirect(url_for('user_bp.login'))

    return render_template("user_login.html",form = form, title = 'User_Log-In')

@user_bp.route("/logout")
@login_required
def logout():
    """Log user out"""
    logout_user()
    # Forget any user_id
    session.clear()
    flash("Account successfully logged Out", 'success')
    return redirect(url_for('stock_bp.home'))


@login_manager.user_loader
def load_user(user_id):
    """Check if user is loggedin"""
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect to Login page."""
    flash('You must be logged in', 'warning')
    return redirect(url_for('user_bp.login'))

@user_bp.route("/user_changepw", methods=["GET", "POST"])
@login_required
def changepw():

    userid = current_user.id
    form = ChangePWForm()

    if form.validate_on_submit():

        user = User.query.filter_by(id = userid).first()

        if not check_password_hash(user.password, form.current_password.data):
            flash("Incorrect current password", 'warning')
            return redirect(url_for("user_bp.changepw"))

        new_password = form.new_password.data

        if new_password == form.current_password.data:
            flash("New password cannot match current password", 'warning')
            return redirect(url_for("user_bp.changepw"))

        user.password = generate_password_hash(new_password)

        db.session.commit()
        flash("Password successfully Changed", 'success')
        return redirect(url_for('stock_bp.dashboard'))


    return render_template("user_changepw.html",form=form, current_user=current_user)
