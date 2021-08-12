from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

def connect_to_db(flask_app, dbname='inventory_psql', echo=False):  
    
    #organization info
    flask_app.config['ORG_NAME'] = 'MJ'
    flask_app.config['APP_TITLE'] = 'Sales & Inventory DB'
    flask_app.config['APP_DESC'] = 'An extremely simple way to track the sales and inventory of cannabis products.'

    #database
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql:///' + dbname
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    #Flask-Admin config
    flask_app.config['DEBUG'] = True
    flask_app.config['HOST'] = 'localhost'
    flask_app.config['PORT'] = 8000
    
    db.app = flask_app
    db.init_app(flask_app)
    
    print('Connected to the db!')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# People models
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Staff(db.Model):
    """An staff member."""
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    staff_name = db.Column(db.String(150), unique=True, nullable=False)
    role = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(255))
    phone = db.Column(db.String)
    
    intakes = db.relationship("Intake", backref='staff')
    sales = db.relationship("Sale", backref='staffer')
    
    def __repr__(self):
        return f'< Staff = {self.staff_name} Role = {self.role} >'

    def __init__(self, staff_name, role="staff", email=None, phone=None, notes="N/A"):
        self.contact_name, self.notes, self.email, self.phone = (staff_name, notes, email, phone)
        
class Entity(db.Model):
    """An entity."""
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    contact_name = db.Column(db.String(150), unique=True, nullable=False)
    company_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(255))
    phone = db.Column(db.String)
    notes = db.Column(db.Text)
    
    supplier = db.relationship("Intake", backref='entity')
    customer = db.relationship("Sale", backref='entity')
    
    def __repr__(self):
        return f'< Contact = {self.countact_name} Company = {self.company_name} >'

    def __init__(self, contact_name, company_name=None, email=None, phone=None, notes="N/A",):
        self.contact_name, self.notes, self.email, self.phone = (contact_name, notes, email, phone)
        if company_name == None:
            self.company_name = contact_name

def get_all_staff():
    """Returns intake related to SKU"""
    return Staff.query.all()

def get_all_entities():
    """Returns intake related to SKU"""
    return Entity.query.all()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~           
# Inventory models
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Product(db.Model):
    """A high-level category of product."""
    
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    product_name = db.Column(db.String(255), unique=True)
    description = db.Column(db.Text)
    
    variants = db.relationship("Intake", backref='product')
    
    def __repr__(self):
        return f'<Product ID = {self.id} Product name = {self.name} >'

    def __init__(self, name, description="N/A"):
        self.name, self.description = (name, description)            
            
class Intake(db.Model):
    """A lower-level category of product, identified by sku."""
    
    
    date = db.Column(db.DateTime, default=datetime.datetime.now)
    
     # REF: Product table
    product_id = db.Column(db.Integer(), db.ForeignKey(Product.id), nullable=False)
    
    # REF: Product Info
    sku = db.Column(db.String(12), primary_key=True, nullable=False)
    selling_price = db.Column(db.Float(10), nullable=False)
    notes = db.Column(db.Text)
    
    # REF: Intake Info
    initial_unit_count = db.Column(db.Integer, nullable=False)  # intial amount; managed in a separate form
    cost_per_unit = db.Column(db.Float(10), nullable=False)
    licensing_fee = db.Column(db.Float(10), nullable=False)
    entity_id = db.Column(db.Integer(), db.ForeignKey(Entity.id))
    
    sale_instance = db.relationship("Item", backref='variant')
    
    #REF: Staff Info
    staff_name = db.Column(db.String(), db.ForeignKey(Staff.staff_name))
    

    def __repr__(self):
        return f'< Product name = {self.get_by_product} SKU = {self.sku} >'

    def __init__(self, sku, product_id, selling_price, initial_unit_count, cost_per_unit, licensing_fee, entity_id, staff_name, notes="N/A"):
        self.sku, self.product_id, self.selling_price, self.initial_unit_count, self.cost_per_unit, self.licensing_fee, self.entity_id, self.staff_name,  self.notes = (sku, product_id, selling_price, initial_unit_count, cost_per_unit, licensing_fee, entity_id, staff_name, notes)

def get_all_products():
    """Returns intake related to SKU"""
    return Product.query.all()

def get_intake_by_sku(sku):
    """Returns intake related to SKU"""
    return Intake.query.filter(Intake.sku==sku).first()

def get_all_intakes_by_source(entity):
    """TO DO"""
    return Intake.query.filter(Intake.entity_id==entity.id).all()

def get_all_intakes_by_purchaser(staff):
    """TO DO"""
    return Intake.query.filter(Intake.staff_name==staff.staff_name).all()

def get_all_skus_by_product(self, product):
    """TO DO"""
    return Intake.query.filter(Intake.product_id==product.id).all()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~           
# Activity Models
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Sale(db.Model):
    
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    invoice_no = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.now)
    prem_disc_percentage =  db.Column(db.Integer, nullable=False)
    wiring_fee = db.Column(db.Float(10), nullable=False)
    
    #REF: Customer Info
    entity_id = db.Column(db.Integer(), db.ForeignKey(Entity.id))
    
    #REF: Staff Info
    seller_name = db.Column(db.String(), db.ForeignKey(Staff.staff_name))
    broker_fee = db.Column(db.Float(10), nullable=False)
    
    items = db.relationship("Item", backref='sale')
    
    def __repr__(self):
        return f'<Customer = {self.name} Invoice = {self.invoice_no} Date = {self.date} >'
    
    def __init__(self, invoice_receipt_no, prem_disc_percentage, wiring_fee, entity_id, staff_name, broker_fee, ):
        self.invoice_receipt_no, self.prem_disc_percentage, self.wiring_fee, self.entity_id, self.staff_name, self.broker_fee = (invoice_receipt_no, prem_disc_percentage, wiring_fee, entity_id, staff_name, broker_fee)
    
    def get_cart(self):
        """returns all cart items from given sale"""
        
        return Item.query.filter(Item.sale_id==self.id).all()

class Item(db.Model):
    
    #Item info
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    sku = db.Column(db.String(), db.ForeignKey(Intake.sku))
    quantity = db.Column(db.Integer(), nullable = False)

    #REF: Sale Info
    sale_id = db.Column(db.Integer(), db.ForeignKey(Sale.id))

# class Sample(db.Model):
#     """TO DO"""
    
#     id = db.Column(db.Integer, auto_increment=True, primary_key=True)
#     invoice_no = db.Column(db.String, nullable=False)
#     date = db.Column(db.DateTime, default=datetime.datetime.now)
#     prem_disc_percentage =  db.Column(db.Integer, nullable=False)
#     wiring_fee = db.Column(db.Float(10), nullable=False)
    
#     #REF: Customer Info
#     entity_id = db.Column(db.Integer(), db.ForeignKey(Entity.id))
    
#     #REF: Staff Info
#     seller_name = db.Column(db.String(), db.ForeignKey(Staff.staff_name))
#     broker_fee = db.Column(db.Float(10), nullable=False)
    
#     items = db.relationship("Item", backref='sale')

def get_sale_by_id(id):
    """Return sale with given ID."""
    
    return Sale.query.filter(Sale.id==id).first()

def get_sale_by_invoice(invoice_no):
    """Return sale with given invoice number."""
    
    return Sale.query.filter(Sale.invoice_no==invoice_no).first()

def get_sales_by_customer(entity):
    """Returns all sales related to given entity instance."""
    
    return Sale.query.filter(Sale.entity_id==entity.id).all().order_by("date")

def get_sales_by_seller(seller):
    """Returns all sales related to given staff member/seller."""
    
    return Sale.query.filter(Sale.seller_name==seller.seller_name).all().order_by("date")

def get_sales_from_date(date):
    """Returns all sales related from given date."""
    
    return Sale.query.filter(Sale.date==date).all().order_by("date")


if __name__ == '__main__':
    from app import app
    
    connect_to_db(app)
    db.create_all()
    db.session.commit()
            
            