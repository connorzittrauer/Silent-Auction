from apt.auth import unicode
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

#association table
bids = db.Table('bids',
        db.Column('item_id', db.Integer, db.ForeignKey('items.item_id')),
        db.Column('user_id', db.Integer, db.ForeignKey('user.user_id')))

class Items(db.Model):
    item_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(64), unique=True, nullable=False)
    item_price = db.Column(db.String(64), unique=True)

#many-to-many relationship, bidders/auctioneers can have multiple items
class User(UserMixin, db.Model):
    role = db.Column(db.String(32), nullable=False)
    user_id = db.Column(db.Integer, primary_key=True)
    offers = db.relationship('Items', secondary=bids, backref=db.backref('bids', lazy='dynamic'))
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

    def is_authenticated(self):
        return True
    # not really sure what this does but it prevents an error
    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return int(self.user_id)

    def get_username(self):
        return str(self.username)


