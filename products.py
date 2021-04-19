from faker import Faker
from models import db, Items, User


# here is where the fake auction items are generated and added to the database
def populate():
    fake = Faker()
    i = 0
    while i <= 10:
        product = Items(item_name=fake.address())
        i += 1
        db.session.add(product)
    db.session.commit()

populate()

def admin():
    admin = User(role="Admin", username='admin',password="admin")
    db.session.add(admin)
    db.session.commit()
