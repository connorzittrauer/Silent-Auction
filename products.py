from faker import Faker
from models import db, Items, User
import datetime

# here is where the fake auction items are generated and added to the database
def populate():
    fake = Faker()
    i = 0
    while i <= 10:
        product = Items(item_name=fake.address(), time_created=datetime.datetime.now())
        i += 1
        db.session.add(product)
    db.session.commit()

populate()

def admin():
    admin = User(role="Admin", username='admin',password="admin")
    bidder = User(role='Bidder', username='bidder', password='pass')
    auctioneer = User(role="Auctioneer", username='auct', password='pass')
    db.session.add(admin)
    db.session.add(bidder)
    db.session.add(auctioneer)
    db.session.commit()
