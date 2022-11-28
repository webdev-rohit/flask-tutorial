from flask import Flask, render_template, url_for, flash, redirect, request
from main import app, db, bcrypt
from main.forms import RegistrationForm, LoginForm
from main.models import User, Post
from flask_login import login_user, logout_user, current_user, login_required

posts = [
    {
        "blog": "Blog 1",
        "author": "Rohit Vishwakarma",
        "dated": "13th, Sept, 2022",
        "content": "Some content by Rohit."
    },
    {
        "blog": "Blog 2",
        "author": "Jane Doe",
        "dated": "14th, Sept, 2022",
        "content": "Some content by Jane."
    }
]

@app.route("/")
@app.route("/home")  # / and /home will redirect to the same page
def home():
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated: # this condition is to check if a user is already logged in.
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():  # this validate_on_submit fxn will tell if our form validated or not on submit
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') # while regostration of a new user, whatever the user might enter as a password, that is being hashed here using flask_bcrypt module and will be stored in db in hashed form only.
        user = User(username=form.username.data, email=form.email.data, password=hashed_password) # creation of the user with username, email and password fields
        db.session.add(user) # pylint: disable=no-member
        db.session.commit() # pylint: disable=no-member
        flash(f'Account successfully created for {form.username.data}! You can now log in.', 'success')  # on successful validation we want to show a flash message which will be shown as an alert by tweaking the frontend code. flash is just imported in the first line of this file. 'success' is the bootstrap class which will show the message in green.
        return redirect(url_for('login'))  # also, on successful validation after submit, we want to be redirected to the home page.
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: # this condition is to check if a user is already logged in.
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() # this line checks if the entered email exists or not in our db.
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            # return redirect(next_page) if next_page else redirect(url_for('home'))
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')