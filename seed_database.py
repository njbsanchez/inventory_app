"""Script to seed database."""

import json
from datetime import datetime

import flaskinventory.model as m
import server


def get_entities():
    """Load dummy users from dataset into database."""

    # Load dummy user data from JSON file
    with open("flaskinventory/data/entity.json") as f:
        dummy_entities = json.loads(f.read())

    # Create dummy users, store them in list so we can use them
    dummies_in_db = []
    for entity in dummy_entities:
        customer_name, company_name, entity_type, email, phone, notes = (
            user["customer_name"],
            user["company_name"],
            user["entity_type"],
            user["email"],
            user["phone"],
            user["notes"]
        )

        db_entity = m.Entity(
            customer_name, company_name, entity_type, email, phone, notes
        )

    m.db.session.commit()

def get_staff():
    """Load dummy users from dataset into database."""

    # Load dummy user data from JSON file
    with open("flaskinventory/data/staff.json") as f:
        dummy_staff = json.loads(f.read())

    # Create dummy users
    for user in dummy_staff:
        staff_name, role, email, phone = (
            user["staff_name"],
            user["role"],
            user["email"],
            user["phone"]
        )

        db_staff = m.Staff(
            staff_name, role, email, phone
        )

    m.db.session.commit()

def get_products():
    """Load dummy users from dataset into database."""

    # Load dummy user data from JSON file
    with open("flaskinventory/data/product.json") as f:
        dummy_product = json.loads(f.read())

    # Create dummy users
    for user in dummy_product:
        product_name, description = (
            user["product_name"],
            user["description"]
        )

        db_product = m.Product(product_name, description) 
        
    m.db.session.commit()

if __name__ == "__main__":

    m.connect_to_db(server.app)
    m.db.create_all()

    print(
        "************************ CHECK IF TRACKIFY DB CREATED ********************"
    )

    get_entities()

    print(
        "************************ DUMMY USERS ADDED TO DB ********************"
    )

    get_staff()

    print(
        "************************ DUMMY ARTISTS ADDED TO DB ********************"
    )

    get_products()

    print(
        "************************ DUMMY ARTISTS ADDED TO DB ********************"
    )


    m.db.session.commit()
