from model import db, Intake, Sale, Item, Sample, SampleItem
from app import app
import sqlalchemy.exc as sq


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~           
# Inventory calculations
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# By SKU ~~~~~~~~~~~

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
        
        sample_record = Sample.query.filter(Sale.id == sampleitem.sale_id).first()
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
    
    sub_total = quantity * item_instance.intake_instance.selling_price

def calc_cogs(quantity, item_instance):
    
    cost_per_unit = item_instance.intake_instance.cost_per_unit
    licensing_per_unit = item_instance.intake_instance.licensing_fee
    
    cogs_of_item = quantity * (cost_per_unit + licensing_per_unit)
    
    return cogs_of_item

# Sale Instance Calc ~~~~~~~~~~~~~~

def add_subtotals(sale_id):
    """
    - query for items with sale_id
    - loop through items
        - using item.quantity and item.quantity"""
    
    subtotal_dict = {}
    total = 0
    
    sale_instance = Sale.query.filter(Sale.id == sale_id).first()
    
    for i, item in enumerate(sale_instance.items, 1):
        price = item.intake_instance.selling_price
        quantity = item.quantity
        sub_total = item.subtotal
        subtotal_dict[(i, item)] = (price, quantity, sub_total)
        total += sub_total
        
    subtotal_data = {"total": total, "sub_dict": subtotal_dict}
        
    return subtotal_data

def get_items_cogs(sale_id):
    """
    - query for items with sale_id
    - loop through items
        - using item.quantity and item.quantity"""
    
    cogs_dict = {}
    total_cogs = 0
    
    sale_instance = Sale.query.filter(Sale.id == sale_id).first()
    
    for i, item in enumerate(sale_instance.items, 1):
        cost_per_unit = item.intake_instance.cost_per_unit
        quantity = item.quantity
        item_cogs = item.cogs
        cogs_dict[(i, item)] = (cost_per_unit, quantity, item_cogs)
        total_cogs += item_cogs
        
    cogs_data = {"total": total_cogs, "cogs_dict": cogs_dict}
        
    return cogs_data



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~           
# Broker Calculations
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def broker_pay_out(broker):
    broker_dict = {"fee_total": 0, "fee_paid": 0, "fee_unpaid": 0}
    sales_list = broker.sales
    for sale_instance in sales_list:
        broker_dict["fee_total"] += sale_instance.broker_fee
        if sale_instance.broker_fee_paid == False:
            broker_dict["fee_unpaid"] += sale_instance.broker_fee
        elif sale_instance.broker_fee_paid == True:
            broker_dict["fee_paid"] += sale_instance.broker_fee
    print( broker_dict["fee_total"] == broker_dict["fee_unpaid"] + broker_dict["fee_paid"])
    
    return broker_dict

def sale_by_broker(broker):
     Entity.query.filter(Entity.id = broker.id).first()