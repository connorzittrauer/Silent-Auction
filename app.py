import flask
from flask import Flask, render_template, Blueprint
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from models import db, Items, Bidder, Auctioneer, login_manager
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from forms import LoginForm, RegistrationForm, NewAuctionItem, NewBid
import os

app = Flask(__name__)
boostrap = Bootstrap(app)

#Set the login manager's login view to login route function
login_manager.login_view = 'app.login'


#set up useful variables
basedir = os.path.abspath(os.path.dirname(__file__))

#configure Flask options
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite') #the sqlite:/// needs an extra / for linux systems
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'SDF#$DSFLKSDFJG$#LKJDFS$%LKJS'

#after the app object was created and configured
db.init_app(app)

#$initialize extensions
db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/items-index")
def items_index():
    # query the database for a list of the addresses
    data = Items.query.all()
    return render_template("items-index.html", data=data)


#not updating database record!
@app.route('/items-index/<item_id>', methods=['GET', 'POST'])
def item_page(item_id):
    data = Items.query.get(int(item_id))
    form = NewBid()
    if form.validate_on_submit() and flask.request.method == 'POST':
        data.item_price = form.bid.data
        db.session.commit()
        flash('Bid Received!')
        # return redirect(url_for("items_index"))
    return render_template('item-page.html',form=form, data=data)

@app.route("/bidder")
def bidder():
    return render_template("bidder.html")

@app.route("/auctioneer", methods=['GET', 'POST'])
def auctioneer():
    form = NewAuctionItem()
    if form.validate_on_submit():
        item = Items(item_name=form.address.data)
        db.session.add(item)
        db.session.commit()
        flash('Auctioneer Item Created.')
        return redirect(url_for("auctioneer"))
    return render_template("auctioneer.html", form=form)


@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/new-bidder")
def new_bidder():
    return render_template("new-bidder.html")


#set up the login view and handle login logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #create a user variable set with a query of the first item that matches the provided email
        bidder = Bidder.query.filter_by(email=form.email.data.lower()).first()
        if bidder is not None and bidder.verify_password(form.password.data):
            #using the login_user function with the user and remember me data
            login_user(bidder, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid email or password.')
    return render_template('login.html', form=form)


#set up the logout view and logic
@app.route('/logout')
@login_required
def logout():
    #using the logout_user method to log out the user
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

#set up the registration view and registration logic
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    print("before validation")
    if form.validate_on_submit():
        print("after validation")
        #create a new user from the Form fields
        user = Bidder(email=form.email.data.lower(),
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