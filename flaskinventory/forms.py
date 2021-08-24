from flask_wtf import FlaskForm, Form
from wtforms import form, StringField, FieldList, FloatField, FormField, BooleanField, DateField, IntegerField, SelectField, SubmitField, TextField
from wtforms.fields.html5 import TelField, EmailField
from wtforms.validators import InputRequired, NumberRange, Length, Email

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = StringField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember me')
    
class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message="Invalid Email")])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = StringField('Password', validators=[InputRequired(), Length(min=8, max=80)]) 

class AddStaff(FlaskForm):
    staff_name = StringField('Staff Name', validators=[InputRequired()])
    role = SelectField(u'Role', choices=[('broker', 'broker'), ('staff', 'staff')])
    email = EmailField('Email')
    phone = TelField('Telephone Number')
    notes = TextField('Notes')
    staffsubmit = SubmitField('Save Changes')

class editstaff(FlaskForm):
    staff_name = StringField('Staff Name', validators=[InputRequired()])
    role = SelectField(u'Role', choices=[('broker', 'broker'), ('staff', 'staff')])
    email = EmailField('Email')
    phone = TelField('Telephone Number')
    staffsubmit = SubmitField('Save Changes')

class addentity(FlaskForm):
    contact_name = StringField('Staff Name', validators=[InputRequired()])
    company_name = StringField('Company Name', validators=[InputRequired()])
    entity_type = SelectField(u'Entity Type', choices=[('OTH', 'OTH'), ('Wholesale', 'Wholesale'), ('MJ', 'MJ')])
    email = EmailField('Email')
    phone = TelField('Telephone Number')
    notes = TextField('Notes')
    staffsubmit = SubmitField('Save Changes')

class addproduct(FlaskForm):
    prodname = StringField('Product Name', validators=[InputRequired()])
    prod_desc = TextField('Notes')
    prodsubmit = SubmitField('Save Changes')

class addintake(FlaskForm):
    
    date = DateField('Intake Date', format='%Y-%m-%d')
    
    # Selling Info
    product_id = SelectField('Product Category', choices=[], coerce=int, validators=[InputRequired()]) #https://stackoverflow.com/questions/12850605/how-do-i-generate-dynamic-fields-in-wtforms/18324514
    sku = StringField('SKU', validators=[InputRequired()])
    selling_price = FloatField('Selling Price per Unit', validators=[InputRequired()])
    notes = TextField('Notes')
    
    #Purchase Info
    init_unitcount = IntegerField('Intake Amount', validators=[NumberRange(min=5, max=1000000),InputRequired()])
    cost_perunit = FloatField('$ Cost per Unit', validators=[InputRequired()])
    licensingfee = FloatField('Licensing Fee', validators=[InputRequired()])
    supplier = SelectField('Supplier', choices=[], coerce=int, validate_choice=True) #https://stackoverflow.com/questions/12850605/how-do-i-generate-dynamic-fields-in-wtforms/18324514
    intake_staff = SelectField('Intake Staff', choices=[], coerce=int, validate_choice=True) #https://stackoverflow.com/questions/12850605/how-do-i-generate-dynamic-fields-in-wtforms/18324514
    prodsubmit = SubmitField('Save Intake')

class additem(FlaskForm):
    sku = SelectField('Supplier', choices=[], coerce=int, validate_choice=True)
    quantity = IntegerField('Quantity', validators=[NumberRange(min=5, max=1000000),InputRequired()])

class addsale(FlaskForm):
    invoice_no = StringField('Invoice Number', validators=[InputRequired()])
    date = DateField('Intake Date', format='%Y-%m-%d')
    prem_disc = FloatField('Licensing Fee')
    wiring_fee = FloatField('Licensing Fee')
    
    entity = SelectField('Customer', choices=[], coerce=int, validate_choice=True)
    
    seller_staff = SelectField('Seller/Staff', choices=[], coerce=int, validate_choice=True)
    broker_fee = FloatField('Broker Fee')
    
    sale_items = FieldList(FormField(additem), min_entries=1) #https://stackoverflow.com/questions/30121763/how-to-use-a-wtforms-fieldlist-of-formfields
    
    salesubmit = SubmitField('Save Sale')


class recordsample(FlaskForm):
    invoice_no = StringField('Invoice Number', validators=[InputRequired()])
    date = DateField('Intake Date', format='%Y-%m-%d')
    
    entity = SelectField('Customer', choices=[], coerce=int, validate_choice=True)
    
    movement = SelectField(u'Sample Check Out or Sample Return?', choices=[('return', 'return'), ('checked-out', 'checked-out')])
    seller_staff = SelectField('Seller/Staff', choices=[], coerce=int, validate_choice=True)
    
    sample_items = FieldList(FormField(additem), min_entries=1) #https://stackoverflow.com/questions/30121763/how-to-use-a-wtforms-fieldlist-of-formfields
    
    salesubmit = SubmitField('Save Sale')