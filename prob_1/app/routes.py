from flask import render_template, url_for, flash, redirect, request
from app import app, db
from app.models import User, Restaurant, Reservation
from app.forms import RegistrationForm, LoginForm, BookingForm
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/')
@app.route('/index')
def index():
    restaurants = Restaurant.query.all()
    print(restaurants) 
    for restaurant in restaurants:
        print(restaurant.name)  # Wyświetl nazwę każdej restauracji
    return render_template('index.html', restaurants=restaurants)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    reservations = Reservation.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', reservations=reservations)

@app.route('/book/<int:restaurant_id>', methods=['GET', 'POST'])
@login_required
def book(restaurant_id):
    form = BookingForm()
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    if form.validate_on_submit():
        reservation = Reservation(
            date=form.date.data,
            guests=form.guests.data,
            menu_choice=form.menu_choice.data,
            user_id=current_user.id,
            restaurant_id=restaurant.id
        )
        db.session.add(reservation)
        db.session.commit()
        flash('Your reservation has been created!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('booking.html', title='Book', form=form, restaurant=restaurant)

@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        flash('You are not authorized to view this page.', 'danger')
        return redirect(url_for('index'))
    reservations = Reservation.query.all()
    return render_template('admin.html', reservations=reservations)