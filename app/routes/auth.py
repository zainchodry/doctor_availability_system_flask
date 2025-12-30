from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.extenshions import db
from app.models import User
from app.forms import *

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Email address already registered')
            return redirect(url_for('auth.register'))
        
        if form.password.data != form.confirm_password.data:
            flash('Passwords do not match')
            return redirect(url_for('auth.register'))
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data),
            role=form.role.data
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form = form)

@auth_bp.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Logged in successfully.')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid email or password')
            return redirect(url_for('auth.login'))
    return render_template('login.html', form = form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('auth.login'))
