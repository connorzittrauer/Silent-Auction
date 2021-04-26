from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from models import User, Items
import datetime


# Define a Login Form to allow users to login
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


# Define a Logout Form to allow users to logout
class RegistrationForm(FlaskForm):
    user_type = SelectField('types', choices=[('bidder', 'Bidder'), ('auctioneer', 'Auctioneer')])
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots or '
               'underscores')])
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class NewAuctionItem(FlaskForm):
    address = StringField("Home: ", validators=[DataRequired()])
    submit = SubmitField("Post Listing")


def current_time():
    return datetime.datetime.now()


class NewBid(FlaskForm):
    bid = StringField("Enter a bid: ", validators=[DataRequired()])
    submit = SubmitField("Place")

    def validate_bid(self, field):
        #right now this is a list, need to be just the time_created column of the current auction item
        expiration = Items.query.with_entities(Items.time_created).all()

        #checks difference between current time and item creation time
        difference = (current_time() - expiration) / 60
        if difference > 5.0:
            raise ValidationError('This bid has expired!')

    # def validate_bid(form, field):
    #     bid = int(field.data)
    #     bid_index = [0, bid]
    #     if not bid > bid_index.index[bid - 1]:
    #         raise ValidationError('Bid must be higher than the previous bid')


class UpdateUser(FlaskForm):
    role = SelectField('types', choices=[('Bidder', 'Bidder'), ('Auctioneer', 'Auctioneer')])
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots or '
               'underscores')])
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Update')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class Logout(FlaskForm):
    logout = SubmitField('Logout')
