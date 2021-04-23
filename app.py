import flask
from flask import Flask, render_template, Blueprint, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from models import db, Items, User, Bids
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from forms import LoginForm, RegistrationForm, NewAuctionItem, NewBid, UpdateUser
from random import randint
import os

app = Flask(__name__)
boostrap = Bootstrap(app)

# Set the login manager's login view to login route function
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'app.login'


# configure the login manager so it knows how to identify a user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# set up useful variables
basedir = os.path.abspath(os.path.dirname(__file__))

# configure Flask options
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,
                                                                    'data.sqlite')  # the sqlite:/// needs an extra / for linux systems
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'SDF#$DSFLKSDFJG$#LKJDFS$%LKJS'

# after the app object was created and configured
db.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/items-index")
def items_index():
    # query the database for a list of the addresses
    data = Items.query.all()
    return render_template("items-index.html", data=data)


@app.route('/items-index/<item_id>', methods=['GET', 'POST'])
def item_page(item_id):
    form = NewBid()
    id = randint(100000, 999999)
    item = Items.query.get(int(item_id))
    data = Bids.query.filter_by(item_id=item_id)
    if form.validate_on_submit():
        bid = Bids(bid_id=id, item_id=item_id, user_id=current_user.user_id, bid_price=form.bid.data)
        db.session.add(bid)
        db.session.commit()
        flash('Bid Received!')
        return redirect(url_for("item_page", item_id=item_id))
    return render_template('item-page.html', form=form, data=data)


@app.route("/bidder")
def bidder():
    return render_template("bidder.html")


@app.route("/auctioneer", methods=['GET', 'POST'])
def auctioneer():
    form = NewAuctionItem()
    if form.validate_on_submit() and current_user.role == 'Auctioneer':
        item = Items(item_name=form.address.data)
        db.session.add(item)
        db.session.commit()
        flash('Auctioneer Item Created.')
        return redirect(url_for("auctioneer"))
    return render_template("auctioneer.html", form=form)


@app.route("/admin", methods=['GET', 'POST'])
def admin():
    data = User.query.all()
    form = RegistrationForm()
    print("before validation")
    if form.validate_on_submit():
        print("after validation")
        # create a new user from the Form fields
        user = User(role=dict(form.user_type.choices).get(form.user_type.data),
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account Created.')
        return redirect(url_for('admin'))
    return render_template("admin.html", data=data, form=form)


@app.route("/admin/<username>" + "<user_id>", methods=['GET', 'POST'])
def user_index(username, user_id):
    username = User.query.get(username)
    data = User.query.get(int(user_id))
    form = UpdateUser()
    if form.validate_on_submit():
        data.role = form.role.data
        data.username = form.username.data
        data.password = form.password.data
        db.session.add(data)
        db.session.commit()
        flash("User updated")
    return render_template('user-index.html', form=form, data=data)


@app.route("/new-bidder")
def new_bidder():
    return render_template("new-bidder.html")


# set up the login view and handle login logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # create a user variable set with a query of the first item that matches the provided email
        user = User.query.filter_by(username=form.username.data.lower()).first()
        if user is not None and user.verify_password(form.password.data):
            # using the login_user function with the user and remember me data
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                if current_user.role == "Bidder":
                    next = url_for('items_index')
                    return redirect(next)
                elif current_user.role == 'Auctioneer':
                    next = url_for('auctioneer')
                    return redirect(next)
                else:
                    next = url_for('admin')
                    return redirect(next)
        flash('Invalid username or password.')
    return render_template('login.html', form=form)


# set up the logout view and logic
@app.route('/logout')
@login_required
def logout():
    # using the logout_user method to log out the user
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))


# set up the registration view and registration logic
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    print("before validation")
    if form.validate_on_submit():
        print("after validation")
        # create a new user from the Form fields
        user = User(role=dict(form.user_type.choices).get(form.user_type.data),
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account Created.')
        flash('You can now login')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
