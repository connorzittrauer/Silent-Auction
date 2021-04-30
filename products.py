from faker import Faker
from app import db, app
from models import Items, User
import datetime
from dotenv import dotenv_values

config = dotenv_values(".env")


# here is where the fake auction items are generated and added to the database
def populate():
    fake = Faker()
    i = 0
    while i <= 10:
        product = Items(item_name=fake.address(), time_created=datetime.datetime.now())
        i += 1
        db.session.add(product)
    db.session.commit()


def admin():
    admin = User(role="Admin", username= config.get('USERNAME1'),password= config.get('PASSWORD1'))
    bidder = User(role='Bidder', username=config.get('USERNAME2'), password=config.get('PASSWORD2'))
    auctioneer = User(role="Auctioneer", username=config.get('USERNAME3'), password=config.get('PASSWORD3'))
    db.session.add(admin)
    db.session.add(bidder)
    db.session.add(auctioneer)
    db.session.commit()

with app.app_context():
    db.create_all()
    admin()
    populate()