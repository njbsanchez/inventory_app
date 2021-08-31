
from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, FloatField, FormField, BooleanField, DateField, IntegerField, SelectField, SubmitField, TextField, validators
from wtforms.fields.html5 import TelField, EmailField
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
    
    date = DateField('Intake Date', format='%Y-%m-%d')
    
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

# class additem(FlaskForm):
#     sku = SelectField('Supplier', choices=[], coerce=int, validate_choice=True)
#     quantity = IntegerField('Quantity', [validators.NumberRange(min=5, max=1000000),validators.DataRequired()])

# class addsale(FlaskForm):
#     invoice_no = StringField('Invoice Number', [validators.DataRequired()])
#     date = DateField('Intake Date', format='%Y-%m-%d')
#     prem_disc = FloatField('Licensing Fee')
#     wiring_fee = FloatField('Licensing Fee')
    
#     entity = SelectField('Customer', choices=[], coerce=int, validate_choice=True)
    
#     seller_staff = SelectField('Seller/Staff', choices=[], coerce=int, validate_choice=True)
#     broker_fee = FloatField('Broker Fee')
    
#     sale_items = FieldList(FormField(additem), min_entries=1) #https://stackoverflow.com/questions/30121763/how-to-use-a-wtforms-fieldlist-of-formfields
    
#     salesubmit = SubmitField('Save Sale')


# class recordsample(FlaskForm):
#     invoice_no = StringField('Invoice Number', [validators.DataRequired()])
#     date = DateField('Intake Date', format='%Y-%m-%d')
    
#     entity = SelectField('Customer', choices=[], coerce=int, validate_choice=True)
    
#     movement = SelectField(u'Sample Check Out or Sample Return?', choices=[('return', 'return'), ('checked-out', 'checked-out')])
#     seller_staff = SelectField('Seller/Staff', choices=[], coerce=int, validate_choice=True)
    
#     sample_items = FieldList(FormField(additem), min_entries=1) #https://stackoverflow.com/questions/30121763/how-to-use-a-wtforms-fieldlist-of-formfields
    
#     salesubmit = SubmitField('Save Sale')