from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
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
# Helper Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def sku_get_intake_quantity(sku):
    """quantity from intake"""

    return Intake.query.filter(Intake.sku == sku).first()

def sku_get_sale_quantity(sku):
    """add quantity of all sales"""
    
    items_with_sku = Item.query.filter(Item.sku == sku).all()
    return_data = {"quantity_total": 0, "sale_records":[]}
    
    for item in items_with_sku:
        return_data["quantity_total"] += item.quantity
        return_data["sale_records"].append(item)
        
    return return_data     

def sku_get_sample_quantity(sku):   
    """add quantity of all samples out"""
    
    sampleitems_with_sku = SampleItem.query.filter(SampleItem.sku == sku).all()
    return_data = {"sampleout":{"quantity_total": 0, "sample_records":[]}, "returned": {"quantity_total": 0, "sample_records":[]}}
    
    for sampleitem in sampleitems_with_sku:
        
        sample_record = Sample.query.filter(Sample.id == sampleitem.sale_id).first()
        if sample_record.movement == "sampleout":
            return_data["sampleout"]["quantity_total"] += sampleitem.quantity
            return_data["sampleout"]["sample_records"].append(sampleitem.id)
        if sample_record.movement == "samplereturn":
            return_data["returned"]["quantity_total"] += sampleitem.quantity
            return_data["returned"]["sample_records"].append(sampleitem.id)

    return return_data  

def calculate_quantity_instock(sku):
    """quantity left = intake minus sales, minus samples out, add sample returned"""

    quant_intake = sku_get_intake_quantity(sku)
    quant_sold = sku_get_sale_quantity(sku)
    quant_dict = sku_get_sample_quantity(sku)
    quant_sample_out = quant_dict["sampleout"]
    quant_sample_returned = quant_dict["returned"]
    
    quant_instock = quant_intake - quant_sold["quantity_total"] - quant_sample_out["quantity_total"] + quant_sample_returned["quantity_total"]
    
    return quant_instock

# By Product ~~~~~~~~~~~~~~

def prod_get_intake_quantity(product_id):
    """all intake with given product id"""
    
    intake_quant = 0
    intake_with_id = Intake.query.filter(Intake.product_id == product_id).all()
    
    for intake in intake_with_id:
            intake_quant += intake.quantity
    
    return intake_quant
   
def prod_get_sale_quantity(product_id):
    """from sales - add quantity with given product id"""

    sale_quant = 0
    items_with_id = Item.query.filter(Item.product_id == product_id).all()
    
    for item in items_with_id:
            sale_quant += item.quantity
    
    return sale_quant
    
def prod_get_sample_quantity(product_id): 
    """from samples - add quantity with given product id"""

    sampleitems_with_id = SampleItem.query.filter(SampleItem.product_id == product_id).all()
    return_data = {"sampleout":{"quantity_total": 0, "sample_records":[]}, "returned": {"quantity_total": 0, "sample_records":[]}}
    
    for sampleitem in sampleitems_with_id:
        
        sample_record = Sample.query.filter(Sale.id == sampleitem.sale_id).first()
        if sample_record.movement == "sampleout":
            return_data["sampleout"]["quantity_total"] += sampleitem.quantity
            return_data["sampleout"]["sample_records"].append(sampleitem.sample_record_id)
        if sample_record.movement == "samplereturn":
            return_data["returned"]["quantity_total"] += sampleitem.quantity
            return_data["returned"]["sample_records"].append(sampleitem.sample_record_id)

    return return_data  

def prod_calculate_quantity_instock(product_id):
    """quantity left = intake minus sales, minus samples out, add sample returned"""

    quant_intake = prod_get_intake_quantity(product_id)
    quant_sold = prod_get_sale_quantity(product_id)
    quant_dict = prod_get_sample_quantity(product_id)
    quant_sample_out = quant_dict["sampleout"]
    quant_sample_returned = quant_dict["returned"]
    
    quant_instock = quant_intake - quant_sold["quantity_total"] - quant_sample_out["quantity_total"] + quant_sample_returned["quantity_total"]
    
    return quant_instock


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~           
# Money Calculations
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Item Instance Calc ~~~~~~~~~~~~~~

def calc_sub_total(quantity, item_instance):
    
    prem_disc = item_instance.sale.prem_disc_percentage
    prem_disc = (100 + prem_disc) / 100
    new_price = item_instance.intake_instance.selling_price *  prem_disc
    
    print("premium or discount: ", prem_disc)
    print("quantity: ", quantity)
    print("new price per item: ", new_price)
    
    sub_total = quantity * new_price

    print("subtotal: ", sub_total)

    return sub_total

def calc_cogs(quantity, item_instance):
    
    cost_per_unit = item_instance.intake_instance.cost_per_unit
    licensing_per_unit = item_instance.intake_instance.licensing_fee
    
    cogs_of_item = quantity * (cost_per_unit + licensing_per_unit)
    
    return cogs_of_item


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# People models
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
class User(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80), unique=True)
    
    def __repr__(self):
        return f'< ID = {self.id} User = {self.username} >'

    def __init__(self, username, email, password):
        self.username, self.email, self.password = (username, email, password)

class Staff(db.Model):
    """An staff member."""
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    staff_name = db.Column(db.String(150), unique=True, nullable=False)
    role = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String)
    notes = db.Column(db.Text)
   
    def __repr__(self):
        return f'< Staff = {self.staff_name} Role = {self.role} >'

    def __init__(self, staff_name, role="staff", email=None, phone=None, notes="N/A"):
        self.staff_name, self.role, self.notes, self.email, self.phone = (staff_name, role, notes, email, phone)
        
class Entity(db.Model):
    """An entity."""
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    contact_name = db.Column(db.String(150), unique=True, nullable=False)
    company_name = db.Column(db.String(150), nullable=False)
    entity_role = db.Column(db.String(150), nullable=False)
    entity_type = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(255))
    phone = db.Column(db.String)
    notes = db.Column(db.Text)
    
    intakes = db.relationship("Intake", backref='entity')
    sales = db.relationship("Sale", backref='entity')
    payments = db.relationship("Payment", backref='entity')
    samples = db.relationship("Sample", backref='entity')

        
    def __repr__(self):
        return f'< Contact = {self.contact_name} Company = {self.company_name} >'

    def __init__(self, contact_name, entity_role, company_name=None, entity_type="MJ", email=None, phone=None, notes="N/A"):
        if company_name == None:
            company_name = contact_name
        self.contact_name, self.company_name, self.entity_type, self.entity_role, self.notes, self.email, self.phone = (contact_name, company_name, entity_type, entity_role, notes, email, phone)       

    def get_sum_of_sales(self):
        
        sale_sum = 0
        
        for sale in self.sales:
            sale_sum += sale.get_receipt_total()
            
        return sale_sum
    
    def get_sum_of_payments(self):
        
        payment_sum = 0
        
        for payment in self.payments:
            payment_sum += payment.amount_received
            
        return payment_sum
    
    def get_outstanding_total(self):
        
        sale_sum = self.get_sum_of_sales()
        payment_sum = self.get_sum_of_payments()
        
        return sale_sum - payment_sum     
    
    def get_total_samples_out(self):
        
        sample_items = SampleItem.query.filter(SampleItem.sample.entity == self).all()
        
        sample_dict = {"checkedout": {"count": 0, "items": []}, "returned": {"count": 0, "item": []}}
        
        for item in sample_items:
            if item.sample.movement == "sampleout":
                sample_dict["checkedout"]["count"] += item.quantity
                sample_dict["checkedout"]["items"].append(item)
            elif item.sample.movement == "samplereturn":
                sample_dict["returned"]["count"] += item.quantity
                sample_dict["returned"]["items"].append(item)
        
        return sample_dict
    
    def get_samples_out(self):
        
        sample_items = SampleItem.query.filter(SampleItem.sample.entity == self).all()
        
        sample_dict = {}
        
        for item in sample_items:
            
            if item.intake_instance not in sample_dict:
                sample_dict[item.intake_instance] = 0
            
            if item.sample.movement == "sampleout":
                sample_dict[item.intake_instance] += item.quantity
            
            elif item.sample.movement == "samplereturn":
                sample_dict[item.intake_instance] -= item.quantity
        
        return sample_dict
        
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
    notes = db.Column(db.Text)
    description = db.Column(db.Text)
    
    intake_variants = db.relationship("Intake", backref='product')
    sale_items = db.relationship("Item", backref='product')
    sample_items = db.relationship("SampleItem", backref='product')
    
    def __repr__(self):
        return f'{self.product_name}'

    def __init__(self, name, description="N/A", notes="N/A"):
        self.product_name, self.description, self.notes = (name, description, notes)            
            
class Intake(db.Model):
    """A lower-level category of product, identified by sku."""
    
    date = db.Column(db.Date, nullable=False)
    
     # REF: Product table
    product_id = db.Column(db.Integer(), db.ForeignKey(Product.id), nullable=False)
    
    # REF: Product Info
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    type_key = db.Column(db.String(18), nullable=False)
    sku = db.Column(db.String(20), nullable=False)
    notes = db.Column(db.Text)
    
    # REF: Intake Info
    initial_unit_count = db.Column(db.Integer, nullable=False)  # intial amount; managed in a separate form
    cost_per_unit = db.Column(db.Float(10), nullable=False)
    entity_id = db.Column(db.Integer(), db.ForeignKey(Entity.id))
    
    items = db.relationship("Item", backref='intake_instance')
    sample_items = db.relationship("SampleItem", backref='intake_instance')
    addons = db.relationship("AddOns", backref='intake_instance')
    brokers = db.relationship ("StaffRelations", backref='intake_instance')
    
    def __repr__(self):
        return f'{self.sku}'

    def __init__(self, date, sku, product_id, type_key, initial_unit_count, cost_per_unit, entity_id, notes="N/A"):
        self.date, self.sku, self.product_id, self.type_key, self.initial_unit_count, self.cost_per_unit, self.entity_id, self.notes = (date, sku, product_id, type_key, initial_unit_count, cost_per_unit, entity_id, notes)

    def calculate_subtotal(self):
        
        total = self.cost_per_unit * self.initial_unit_count
            
        return total
    
    def calculate_addon_total(self):
        
        total = 0
        for item in self.addons:
            total += item.amount
            
        return total
    
    def calculate_brokers_total(self):
        
        total = 0
        for item in self.brokers:
            total += item.broker_rate
            
        return total
    
    def get_intake_cog(self):
        """Returns intake cog related to SKU"""
        
        addon_total = self.calculate_addon_total()
        broker_total = self.calculate_brokers_total()
        sub_total = self.calculate_subtotal()
        
        total_cog = addon_total + broker_total + sub_total
        
        return total_cog
    

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
    date = db.Column(db.Date, nullable=False)
    
    #REF: Customer Info
    entity_id = db.Column(db.Integer(), db.ForeignKey(Entity.id)) 
    
    # wiring_fee = db.Column(db.Float(10), nullable=False)
    
    notes = db.Column(db.Text)
    
    items = db.relationship("Item", backref='sale')
    
    # def __repr__(self):
    #     return f'<Customer = {self.name} Invoice = {self.invoice_no} Date = {self.date} >'
    
    def __init__(self, invoice_no, date, entity_id, notes="N/A"):
        self.invoice_no,self.date, self.entity_id, self.notes = (invoice_no, date, entity_id, notes)
    
    def get_cogs_sum(self):
        """internal - returns cog sum of all cart items from given sale"""
        
        cog_sum = 0
        for item in self.items:
            cog_sum += item.cogs
        
        return cog_sum 
    
    def get_subtotal_sum(self):
        """external - sum of all item total"""
        
        sub_sum = 0
        for item in self.items:
            sub_sum += item.subtotal
        
        return sub_sum
            
    def get_receipt_total(self):
        """internal - return total receipt amount to be charged to client"""
        
        return self.get_subtotal_sum() + self.wiring_fee      
    
class Item(db.Model):
    
    #Item info
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    product_id = db.Column(db.Integer(), db.ForeignKey(Product.id), nullable=False)
    intake_id = db.Column(db.Integer(), db.ForeignKey(Intake.id))
    sale_price = db.Column(db.Float(10), nullable=False)
    quantity = db.Column(db.Integer(), nullable = False)
    
    notes = db.Column(db.Text)
    
    cogs = db.Column(db.Integer())
    subtotal = db.Column(db.Integer())

    #REF: Sale Info
    sale_id = db.Column(db.Integer(), db.ForeignKey(Sale.id))
    
    def __repr__(self):
        return f'SKU { self.intake_instance } ({ self.product })'

    def __init__(self, product_id, intake_id, quantity, sale_price, sale_id, notes="N/A"):
        cogs = self.calculate_item_cogs(quantity, intake_id)
        subtotal = self.calculate_subtotal(quantity, sale_price)
        self.product_id, self.intake_id, self.quantity, self.sale_id, self.notes, self.sale_price, self.cogs, self.subtotal, self.notes = (product_id, intake_id, quantity, sale_id, notes, sale_price, cogs, subtotal, notes)
    
    def calculate_item_cogs(self, quantity, intake_id):
        
        intake_instance = Intake.query.filter(Intake.id == intake_id).first()
        
        cost_per_unit = intake_instance.cost_per_unit
        
        print(cost_per_unit)
        
        licensing_per_unit = intake_instance.licensing_fee
        
        cogs_of_item = quantity * (cost_per_unit + licensing_per_unit)
        
        return cogs_of_item
    
        
    def calculate_subtotal(self, quantity, price):

        sub_total = quantity * price
        
        return sub_total

class AddOns(db.Model):  
    
    #Item info
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    transaction_type = db.Column(db.String(20), nullable=False)
    add_on_type = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Float(10), nullable=False)

    notes = db.Column(db.Text)
    
    #REF: Sale Info
    sale_id = db.Column(db.Integer(), db.ForeignKey(Sale.id), nullable=True)
    intake_id = db.Column(db.Integer(), db.ForeignKey(Intake.id), nullable=True)
    
    def __repr__(self):
        return f'SKU { self.id } ({ self.transaction_type })'

    def __init__(self, transaction_type, add_on_type, amount, sale_id, intake_id, notes="N/A"):
        self.transaction_type, self.add_on_type, self.amount, self.sale_id, self.intake_id, self.notes= (transaction_type, add_on_type, amount, sale_id, intake_id, notes)

class Sample(db.Model):
    """TO DO"""
    
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    record_no = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.now)
    movement = db.Column(db.String, nullable=False)
    notes = db.Column(db.Text)
    
    #REF: Customer Info
    entity_id = db.Column(db.Integer(), db.ForeignKey(Entity.id))
    
    items = db.relationship("SampleItem", backref='sample')
    
    def __init__(self, record_no, date, movement, entity_id, notes="N/A"):
        self.record_no, self.date, self.movement, self.entity_id, self.notes = (record_no, date, movement, entity_id, notes)

class SampleItem(db.Model):
    
    #Item info
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    product_id = db.Column(db.Integer(), db.ForeignKey(Product.id), nullable=False)
    intake_id = db.Column(db.Integer(), db.ForeignKey(Intake.id))
    quantity = db.Column(db.Integer(), nullable = False)
    notes = db.Column(db.Text)

    #REF: Sale Info
    sample_record_id = db.Column(db.Integer(), db.ForeignKey(Sample.id))

    def __repr__(self):
        return f'SKU { self.sku } ({ self.product })'

    def __init__(self, product_id, intake_id, quantity, sample_record_id, notes="N/A"):
        self.product_id, self.intake_id, self.quantity, self.sample_record_id, self.notes = (product_id, intake_id, quantity, sample_record_id, notes)


class Payment(db.Model):
    
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    
    #REF: Customer Info
    entity_id = db.Column(db.Integer(), db.ForeignKey(Entity.id))
    
    #REF: Staff Info
    amount_received = db.Column(db.Float(10), nullable=False)
    
    notes = db.Column(db.Text)
    
    
    # def __repr__(self):
    #     return f'<Customer = {self.name} Invoice = {self.invoice_no} Date = {self.date} >'
    
    def __init__(self, date, entity_id, amount_received, notes="N/A"):
        self.date, self.entity_id, self.amount_received, self.notes = (date, entity_id, amount_received, notes)

class StaffRelations(db.Model):
    
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    staff_id = db.Column(db.Integer(), db.ForeignKey(Staff.id))
    broker_rate = db.Column(db.Float(10), nullable=True)
    broker_fee_paid = db.Column(db.Boolean, default=None)
    notes = db.Column(db.Text)
    
    intake_id = db.Column(db.Integer(), db.ForeignKey(Intake.id))
    sale_id = db.Column(db.Integer(), db.ForeignKey(Sale.id))
    sample_id = db.Column(db.Integer(), db.ForeignKey(Sample.id))
    payment_id = db.Column(db.Integer(), db.ForeignKey(Payment.id))
    
    staff_person = db.relationship("Staff", backref='transactions')
    
    sale = db.relationship("Sale", backref='staff_relations')
    sample = db.relationship("Sample", backref='staff_relations')
    payment = db.relationship("Payment", backref='staff_relations')
    intake = db.relationship("Intake", backref='staff_relations')
    
    def __repr__(self):
        return f'SKU { self.id } ({ self.staff })'

    def __init__(self, staff_id, broker_rate, broker_fee_paid, intake_id=None, sale_id=None, sample_id=None, payment_id=None, notes="N/A"):
        self.staff_id, self.broker_rate, self.broker_fee_paid, self.intake_id, self.sale_id, self.sample_id, self.payment_id, self.notes = (staff_id, broker_rate, broker_fee_paid, intake_id, sale_id, sample_id, payment_id, notes)
    
    # def calculate_broker_subtotal(self):
    #     if self.intake_id:
    #         broker_subtotal = self.broker_rate * self.intake.initial_unit_count
    #         return broker_subtotal
    #     elif self.sale_id:
    #         broker_subtotal = self.broker_rate * self.sale.initial_unit_count
    #         return broker_subtotal

            
class StaffInvolvement(db.Model):  
    
    #Item info
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    transaction_type = db.Column(db.String(20), nullable=False)
    staff_person = db.Column(db.String(30), nullable=False)

    notes = db.Column(db.Text)
    
    #REF: Sale Info
    sale_id = db.Column(db.Integer(), db.ForeignKey(Sale.id))
    intake_id = db.Column(db.Integer(), db.ForeignKey(Intake.id))
    
    def __repr__(self):
        return f'SKU { self.id } ({ self.staff_person })'

    def __init__(self, transaction_type, staff_person, sale_id, intake_id, notes="N/A"):
        self.transaction_type, self.add_on_type, self.amount, self.staff_person, self.notes= (transaction_type, staff_person, sale_id, intake_id, notes)

  

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
    Bootstrap(app)
    db.create_all()
    db.session.commit()
            
            