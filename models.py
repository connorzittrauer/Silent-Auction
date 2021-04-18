from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

login_manager = LoginManager()
# #Set the login manager's login view to login route function
# login_manager.login_view = 'app.login'

#association table
bids = db.Table('bids',
        db.Column('item_id', db.Integer, db.ForeignKey('items.item_id')),
        db.Column('bidder_id', db.Integer, db.ForeignKey('bidder.bidder_id')),
        db.Column('auctioneer_id', db.Integer, db.ForeignKey('auctioneer.auctioneer_id')))




class Items(db.Model):
    item_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(64), unique=True, nullable=False)
    item_price = db.Column(db.String(64), unique=True)

#many-to-many relationship, bidders can have multiple items
class Bidder(db.Model):
    bidder_id = db.Column(db.Integer, primary_key=True)
    bidder_name = db.Column(db.String(20))
    items = db.relationship('Items', secondary=bids, backref=db.backref('bidder'))

    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    #Creating the password property
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    #Defining a password setter
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    #Defining the verify_password method
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    #not really sure what this does but it prevents an error
    def is_active(self):
       return True

    # configure the login manager so it knows how to identify a user
    @login_manager.user_loader
    def load_user(bidder_id):
        return Bidder.query.get(int(bidder_id))

#many-to-many relationship, auctioneers can have multiple items
class Auctioneer(db.Model):
    auctioneer_id = db.Column(db.Integer, primary_key=True)
    auctioneer_name = db.Column(db.String(20))
    items = db.relationship('Items', secondary=bids, backref=db.backref('auctioneer'))
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    #Creating the password property
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    #Defining a password setter
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    #Defining the verify_password method
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    #not really sure what this does but it prevents an error
    def is_active(self):
       return True

    # configure the login manager so it knows how to identify a user
    @login_manager.user_loader
    def load_user(auctioneer_id):
        return Auctioneer.query.get(int(auctioneer_id))

