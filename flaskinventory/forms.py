
from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, FloatField, FormField, BooleanField, IntegerField, SelectField, SubmitField, TextField, validators
from wtforms.fields.html5 import TelField, EmailField, DateField
# from wtforms.validators import DataRequired, NumberRange, Length, Email, validators
from flask_bootstrap import Bootstrap

class LoginForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired(), validators.Length(min=4, max=20)])
    password = StringField('Password', [validators.DataRequired(),validators.Length(min=8, max=80)])
    remember = BooleanField('Remember me')
    
class RegisterForm(FlaskForm):
    email = StringField('Email', [validators.DataRequired(), validators.Email(message="Invalid Email")])
    username = StringField('Username', [validators.DataRequired(),validators.Length(min=4, max=20)])
    password = StringField('Password', [validators.DataRequired(),validators.Length(min=8, max=80)]) 

class AddStaff(FlaskForm):
    staff_name = StringField('Name', [validators.DataRequired()])
    role = StringField('Role (broker or staff)',[validators.DataRequired()])
    email = EmailField('Email')
    phone = TelField('Telephone Number')
    notes = TextField('Notes')
    staffsubmit = SubmitField('Save Changes')

class editstaff(FlaskForm):
    staff_name = StringField('Staff Name', [validators.DataRequired()])
    role = StringField('role')
    email = EmailField('Email')
    phone = TelField('Telephone Number')
    staffsubmit = SubmitField('Save Changes')

class AddEntity(FlaskForm):
    contact_name = StringField('Entity Name', [validators.DataRequired()])
    company_name = StringField('Company Name', [validators.DataRequired()])
    entity_type = StringField('Entity Type: (OTH, Wholesale, MJ)',[validators.DataRequired()])
    email = EmailField('Email')
    phone = TelField('Telephone Number')
    notes = TextField('Notes')
    staffsubmit = SubmitField('Save Changes')

class addproduct(FlaskForm):
    prodname = StringField('Product Name', [validators.DataRequired()])
    prod_desc = TextField('Notes')
    prodsubmit = SubmitField('Save Changes')

class addintake(FlaskForm):
    
    date = DateField('Intake Date (format: 12-24-2000)', format='%Y-%m-%d')
    
    # Selling Info
    product_id = SelectField('Product Category', choices=[], coerce=int, option_widget=None) #https://stackoverflow.com/questions/12850605/how-do-i-generate-dynamic-fields-in-wtforms/18324514
    sku = StringField('SKU', [validators.DataRequired()])
    selling_price = FloatField('Selling Price per Unit', [validators.DataRequired()])
    notes = TextField('Notes')
    
    #Purchase Info
    init_unitcount = IntegerField('Intake Amount', [validators.NumberRange(min=5, max=1000000), validators.DataRequired()])
    cost_perunit = FloatField('$ Cost per Unit', [validators.DataRequired()])
    licensingfee = FloatField('Licensing Fee', [validators.DataRequired()])
    supplier = SelectField('Supplier', choices=[], coerce=int, option_widget=None, validate_choice=True) #https://stackoverflow.com/questions/12850605/how-do-i-generate-dynamic-fields-in-wtforms/18324514
    staff_id = SelectField('Intake Staff', choices=[], coerce=int, option_widget=None, validate_choice=True) #https://stackoverflow.com/questions/12850605/how-do-i-generate-dynamic-fields-in-wtforms/18324514
    intakesubmit = SubmitField('Save Intake')

class additem(FlaskForm):
    
    sku = SelectField('SKU Number', choices=[], coerce=int, validate_choice=True)
    product_id = SelectField('Product Category', choices=[], coerce=int, option_widget=None) #https://stackoverflow.com/questions/12850605/how-do-i-generate-dynamic-fields-in-wtforms/18324514
    quantity = IntegerField('Quantity', [validators.NumberRange(min=5, max=1000000),validators.DataRequired()])
    itemsubmit = SubmitField('Add Item')
    
class addsale(FlaskForm):
    invoice_no = StringField('Sample Number', [validators.DataRequired()])
    date = DateField('Intake Date', format='%Y-%m-%d')
    prem_disc = FloatField('Premium/Discount Percentage')
    wiring_fee = FloatField('Wiring Fee')

    entity = SelectField('Customer', choices=[], coerce=int, option_widget=None, validate_choice=True)
    
    staff_id = SelectField('Staff/Sales Associate', choices=[], coerce=int, option_widget=None, validate_choice=True)
    broker_fee = FloatField('Broker Fee')
    broker_fee_paid = BooleanField('Has Broker Fee been paid out?')
    notes = TextField('Notes')
    
    salesubmit = SubmitField('Proceed to Add Items')


class addsample(FlaskForm):
    record_no = StringField('Record Number', [validators.DataRequired()])
    date = DateField('Intake Date', format='%Y-%m-%d')
    
    entity = SelectField('Customer', choices=[], coerce=int, validate_choice=True)
    
    movement = SelectField(u'Sample Check Out or Sample Return?', choices=[('samplereturn', 'sample return'), ('sampleout', 'sample out')])
    staff_id = SelectField('Seller/Staff', choices=[], coerce=int, validate_choice=True)
    
    # sample_items = FieldList(FormField(additem), min_entries=1) #https://stackoverflow.com/questions/30121763/how-to-use-a-wtforms-fieldlist-of-formfields
    notes = TextField('Notes')
    
    samplesubmit = SubmitField('Save Sample')
    
class addsampleitem(FlaskForm):
    
    sku = SelectField('SKU Number', choices=[], coerce=int, validate_choice=True)
    product_id = SelectField('Product Category', choices=[], coerce=int, option_widget=None) #https://stackoverflow.com/questions/12850605/how-do-i-generate-dynamic-fields-in-wtforms/18324514
    quantity = IntegerField('Quantity', [validators.NumberRange(min=5, max=1000000),validators.DataRequired()])
    
    notes = TextField('Notes')
    
    itemsubmit = SubmitField('Add Sample Item')
    