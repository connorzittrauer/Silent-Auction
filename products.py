from faker import Faker
from models import db, Items


# here is where the fake auction items are generated and added to the database
def populate():
    fake = Faker()
    i = 0
    while i <= 100:
        product = Items(item_name=fake.address())
        i += 1
        db.session.add(product)
    db.session.commit()

populate()
