"""Script to seed database."""

import json
from datetime import datetime
import sqlalchemy.exc as sq

import flaskinventory.model as m
import server


def get_entities():
    """Load dummy users from dataset into database."""

    # Load dummy user data from JSON file
    with open("flaskinventory/data/entity.json") as f:
        dummy_entities = json.loads(f.read())
    # print (dummy_entities)
    # Create dummy users, store them in list so we can use them
    dummies_in_db = []
    for entity, details in dummy_entities[0].items():
        contact_name, company_name, entity_role, entity_type, email, phone, notes = (
            details["contact_name"],
            details["company_name"],
            details["entity_role"],
            details["entity_type"],
            details["email"],
            details["phone"],
            details["notes"]
        )
        # print(contact_name, company_name, entity_type, email, phone, notes)
        db_entity = m.Entity(
            contact_name, entity_role, company_name, entity_type, email, phone, notes
        )
        m.db.session.add(db_entity)

        try:
            m.db.session.commit()
        except sq.IntegrityError:
            m.db.session.rollback()
            print("entity already exists")

def get_staff():
    """Load dummy users from dataset into database."""

    # Load dummy user data from JSON file
    with open("flaskinventory/data/staff.json") as f:
        dummy_staff = json.loads(f.read())

    # Create dummy users
    for staff, details in dummy_staff[0].items():
        staff_name, role, email, phone = (
            details["staff_name"],
            details["role"],
            details["email"],
            details["phone"]
        )

        db_staff = m.Staff(
            staff_name, role, email, phone)
        m.db.session.add(db_staff)
    
        try:
            m.db.session.commit()
        except sq.IntegrityError:
            m.db.session.rollback()
            print("staff already exists")

def get_products():
    """Load dummy users from dataset into database."""

    # Load dummy user data from JSON file
    with open("flaskinventory/data/product.json") as f:
        dummy_product = json.loads(f.read())

    # Create dummy users
    for prod, details in dummy_product[0].items():
        product_name, description = (
            details["product_name"],
            details["description"]
        )

        db_product = m.Product(product_name, description) 
        m.db.session.add(db_product)
        
        try:
            m.db.session.commit()
        except sq.IntegrityError:
            m.db.session.rollback()
            print("prod already exists")

if __name__ == "__main__":

    m.connect_to_db(server.app)

    print(
        "************************ CHECK IF DB CREATED ********************"
    )

    get_entities()

    print(
        "************************ DUMMY ENTITIES ADDED TO DB ********************"
    )

    get_staff()

    print(
        "************************ DUMMY STAFF ADDED TO DB ********************"
    )

    get_products()

    print(
        "************************ DUMMY PRODUCTS ADDED TO DB ********************"
    )


    m.db.session.commit()

