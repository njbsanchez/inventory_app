from _typeshed import OpenTextModeUpdating
from inventory.flaskinventory.routes import show_sales
from flaskinventory.forms import AddStaff, AddEntity, addproduct, addintake, LoginForm, RegisterForm, additem, addsample, addsampleitem
from flaskinventory.model import db, User, Staff, Entity, Product, Intake, Sale, Item, Sample, SampleItem
from flaskinventory.app import app
import sqlalchemy.exc as sq

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~           
# Inventory calculations
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# By SKU ~~~~~~~~~~~


quantity from intake

add quantity of all sales 

add quantity of all samples out 

add quantity of all samples returned

add quantity of all 

def calc_quantity_used():
    """Create and return a new user."""

    user = User(email=email, name=name, s_id=s_id, latitude=latitude, longitude=longitude, recent_activity=recent_activity)

    db.session.add(user)
    db.session.commit()

    return user

# By Product ~~~~~~~~~~~~~~

def calc_quantity_used():
    """Create and return a new user."""

    user = User(email=email, name=name, s_id=s_id, latitude=latitude, longitude=longitude, recent_activity=recent_activity)

    db.session.add(user)
    db.session.commit()

    return user

def calc_quantity_left():

def calc_():

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~           
# Money Calculations
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~