from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, FloatField, TelField, EmailField, FormField, IntegerField, SelectField, SubmitField, TextField, DatetimeField
from wtforms.validators import DataRequired, NumberRange, Length

class addstaff(FlaskForm):
    staff_name = StringField('Staff Name', validators=[DataRequired()])
    role = SelectField(u'Role', choices=[('broker', 'broker'), ('staff', 'staff')])
    email = EmailField('Email')
    phone = TelField('Telephone Number')
    staffsubmit = SubmitField('Save Changes')

class addentity(FlaskForm):
    contact_name = StringField('Staff Name', validators=[DataRequired()])
    company_name = StringField('Company Name', validators=[DataRequired()])
    entity_type = SelectField(u'Entity Type', choices=[('OTH', 'OTH'), ('Wholesale', 'Wholesale'), ('MJ', 'MJ')])
    email = EmailField('Email')
    phone = TelField('Telephone Number')
    notes = TextField('Notes')
    staffsubmit = SubmitField('Save Changes')

class addproduct(FlaskForm):
    prodname = StringField('Product Name', validators=[DataRequired()])
    prod_desc = TextField('Notes')
    prodsubmit = SubmitField('Save Changes')

class addintake(FlaskForm):
    
    datetime = DatetimeField('Intake Date', format='%Y-%m-%d %H:%M:%S')
    
    # Selling Info
    product_id = SelectField('Product Category', choices=[], coerce=int, validators=[DataRequired()]) #https://stackoverflow.com/questions/12850605/how-do-i-generate-dynamic-fields-in-wtforms/18324514
    sku = StringField('SKU', validators=[DataRequired()])
    selling_price = FloatField('Selling Price per Unit', validators=[DataRequired()])
    notes = TextField('Notes')
    
    #Purchase Info
    init_unitcount = IntegerField('Intake Amount', validators=[NumberRange(min=5, max=1000000),DataRequired()])
    cost_perunit = FloatField('$ Cost per Unit', validators=[DataRequired()])
    licensingfee = FloatField('Licensing Fee', validators=[DataRequired()])
    supplier = SelectField('Supplier', choices=[], coerce=int, validate_choice=True) #https://stackoverflow.com/questions/12850605/how-do-i-generate-dynamic-fields-in-wtforms/18324514
    intake_staff = SelectField('Intake Staff', choices=[], coerce=int, validate_choice=True) #https://stackoverflow.com/questions/12850605/how-do-i-generate-dynamic-fields-in-wtforms/18324514
    prodsubmit = SubmitField('Save Intake')

class additem(FlaskForm):
    sku = SelectField('Supplier', choices=[], coerce=int, validate_choice=True)
    quantity = IntegerField('Quantity', validators=[NumberRange(min=5, max=1000000),DataRequired()])

class addsale(FlaskForm):
    invoice_no = StringField('Invoice Number', validators=[DataRequired()])
    datetime = DatetimeField('Intake Date', format='%Y-%m-%d %H:%M:%S')
    prem_disc = FloatField('Licensing Fee')
    wiring_fee = FloatField('Licensing Fee')
    
    entity = SelectField('Customer', choices=[], coerce=int, validate_choice=True)
    
    seller_staff = SelectField('Seller/Staff', choices=[], coerce=int, validate_choice=True)
    broker_fee = FloatField('Broker Fee')
    
    sale_items = FieldList(FormField(additem), min_entries=1) #https://stackoverflow.com/questions/30121763/how-to-use-a-wtforms-fieldlist-of-formfields
    
    salesubmit = SubmitField('Save Sale')


class recordsample(FlaskForm):
    invoice_no = StringField('Invoice Number', validators=[DataRequired()])
    datetime = DatetimeField('Intake Date', format='%Y-%m-%d %H:%M:%S')
    
    entity = SelectField('Customer', choices=[], coerce=int, validate_choice=True)
    
    movement = SelectField(u'Sample Check Out or Sample Return?', choices=[('return', 'return'), ('checked-out', 'checked-out')])
    seller_staff = SelectField('Seller/Staff', choices=[], coerce=int, validate_choice=True)
    
    sample_items = FieldList(FormField(additem), min_entries=1) #https://stackoverflow.com/questions/30121763/how-to-use-a-wtforms-fieldlist-of-formfields
    
    salesubmit = SubmitField('Save Sale')