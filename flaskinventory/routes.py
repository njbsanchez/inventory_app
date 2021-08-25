
from flask import render_template,url_for,redirect,flash,request,jsonify
from flaskinventory.forms import AddStaff, AddEntity, addproduct, addintake, additem, addsale, recordsample, LoginForm, RegisterForm
from flaskinventory.model import db, User, Staff, Entity, Product, Intake, Sale, Item, get_all_staff
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from flaskinventory.app import app
from wtforms import StringField, FieldList, FloatField, FormField, BooleanField, DateField, IntegerField, SelectField, SubmitField, TextField
from wtforms.fields.html5 import TelField, EmailField
from wtforms.validators import InputRequired, NumberRange, Length, Email
from flask_bootstrap import Bootstrap
import time, datetime
import sqlalchemy.exc as sq

bootstrap = Bootstrap(app)

@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        # return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user.password == form.password.data:
                return redirect(url_for('show_staff'))
        
        return '<h1> Username or Password is incorrect. <h1>'
    return render_template("login.html", form=form)


@app.route("/admin_new_user", methods=['GET','POST'])
def signup():
    form = RegisterForm()
    
    if form.validate_on_submit():
        # return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'
        new_user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        
        return '<h1> New user has been created!</h1>'
        
    return render_template("signup.html", form=form)


@app.route("/")
def coming_soon():
    """dummy development page"""
    return render_template("coming_soon.html")


@app.route("/intake", methods = ['GET', 'POST'])
def show_intake():
    """list staff/add staff."""
    p_form = addproduct(csrf_enabled=True)
    i_form = addintake(csrf_enabled=True)
    p_details = Product.query.all()
    i_details = Intake.query.all()
    p_exists = bool(Product.query.all())
    i_exists = bool(Intake.query.all())
    
    if p_exists == False and request.method == 'GET':
        flash(f'Add product to view', 'info')
    
    if i_exists == False and request.method == 'GET':
        flash(f'Add intake to view', 'info')
        
    if p_form.validate_on_submit():
        
        prodname = p_form.prodname.data
        prod_desc = p_form.prod_desc.data
    
        new_prod = Product(product_name=prodname, description=prod_desc)
        db.session.add(new_prod)
        
        try:
            db.session.commit()
            print('added!')
            flash(f'{p_form.prodname} has been added!','success')
            return redirect(url_for('staff'))
        except sq.IntegrityError:
            db.session.rollback()
            flash(f'This product already exists.', 'danger')
            return redirect('/staff')
        
    if i_form.validate_on_submit():
        
        prod_categories = [(p.id, p.product_name) for p in Product.query.all()]
        prodname = p_form.prodname.data
        prod_desc = p_form.prod_desc.data
    
        new_prod = Product(prodname, prod_desc)
        db.session.add(new_prod)
        
        try:
            db.session.commit()
            print('added!')
            flash(f'{p_form.prodname} has been added!','success')
            return redirect(url_for('staff'))
        except sq.IntegrityError:
            db.session.rollback()
            flash(f'This productalready exists.', 'danger')
            return redirect('/staff')
        
    return render_template("staff.html", i_details=i_details, p_details=p_details, form=form)

@app.route("/staff/", methods = ['GET', 'POST'])
def show_staff():
    """list staff/add staff."""
    form = AddStaff()
    details = Staff.query.all()
    exists = bool(Staff.query.all())
    # exists = bool(Staff.query.all())
    if exists == False and request.method == 'GET':
        flash(f'Add staff to view', 'info')
        
    if form.validate_on_submit():
        
        # return '<h1>' + form.staff_name.data + ' ' + form.role.data + ' ' + form.email.data + ' ' + form.notes.data + '</h1>'

        new_staff = Staff(staff_name=form.staff_name.data, 
                          role=form.role.data, 
                          email = form.email.data,
                          phone = form.phone.data,
                          notes = form.notes.data)
        
        print(new_staff)
        db.session.add(new_staff)
        
        try:
            db.session.commit()
            print('added!')
            flash(f'Staff has been added!','success')
            return redirect(url_for('show_staff'))
        except sq.IntegrityError:
            db.session.rollback()
            flash(f'This staff member already exists.', 'danger')
            return redirect('/staff')
          
    return render_template("staff.html", details=details, form=form)

@app.route("/entity/", methods = ['GET', 'POST'])
def show_entity():
    """list staff/add staff."""
    form = AddEntity()
    details = Entity.query.all()
    exists = bool(Entity.query.all())
    # exists = bool(Staff.query.all())
    if exists == False and request.method == 'GET':
        flash(f'Add an entity to view', 'info')
        
    if form.validate_on_submit():
  
        new_entity = Entity(contact_name = form.contact_name.data,
                           company_name = form.company_name.data,
                           entity_type = form.entity_type.data,
                           email = form.email.data,
                           phone = form.phone.data,
                           notes = form.notes.data)
        
        print(new_entity)
        db.session.add(new_entity)
        
        try:
            db.session.commit()
            print('added!')
            flash(f'Entity has been added!','success')
            return redirect(url_for('show_entity'))
        except sq.IntegrityError:
            db.session.rollback()
            flash(f'This staff member already exists.', 'danger')
            return redirect('/entity')
          
    return render_template("entity.html", details=details, form=form)