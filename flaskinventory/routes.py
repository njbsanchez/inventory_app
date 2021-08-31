
from flask import render_template,url_for,redirect,flash,request,jsonify
from flaskinventory.forms import AddStaff, AddEntity, addproduct, addintake, LoginForm, RegisterForm #additem, addsale, recordsample,
from flaskinventory.model import db, User, Staff, Entity, Product, Intake, Sale, Item, get_all_staff
from flask_bootstrap import Bootstrap
from flaskinventory.app import app
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


@app.route("/product", methods = ['GET', 'POST'])
def show_product():
    """list staff/add staff."""
    p_form = addproduct(csrf_enabled=True)
    p_details = Product.query.all()
    p_exists = bool(Product.query.all())
    
    if p_exists == False and request.method == 'GET':
        flash(f'Add product to view', 'info')
        
    if p_form.validate_on_submit():
        
        prodname = p_form.prodname.data
        prod_desc = p_form.prod_desc.data
    
        new_prod = Product(prodname, prod_desc)
        db.session.add(new_prod)
        
        try:
            db.session.commit()
            print('added!')
            flash(f'{p_form.prodname} has been added!','success')
            return redirect(url_for('show_product'))
        except sq.IntegrityError:
            db.session.rollback()
            flash(f'This product already exists.', 'danger')
            return redirect('/product')
        
    return render_template("product.html", details=p_details, form=p_form)


@app.route("/intake", methods = ['GET', 'POST'])
def show_intake():
    """list staff/add staff."""
    i_form = addintake()
    
    i_form.product_id.choices = [(product.id, product.product_name) for product in Product.query.all()]
    i_form.supplier.choices = [(entity.id, entity.contact_name) for entity in Entity.query.all()]
    i_form.staff_id.choices = [(staff.id, staff.staff_name) for staff in Staff.query.all()]
    
    i_details = Intake.query.all()
    i_exists = bool(Intake.query.all())

    if i_exists == False and request.method == 'GET':
        flash(f'Add intake to view', 'info')
        
    if i_form.validate_on_submit():
        
        date = i_form.date.data
        product_id = i_form.product_id.data
        sku = i_form.sku.data
        selling_price = i_form.selling_price.data
        notes = i_form.notes.data
        initial_unit_count = i_form.init_unitcount.data
        cost_per_unit = i_form.cost_perunit.data
        licensing_fee = i_form.licensingfee.data
        entity_id = i_form.supplier.data
        staff_id = i_form.staff_id.data
        
        return '<h1>' + date + sku + ' ' + product_id + ' ' +  selling_price + ' ' + initial_unit_count  + ' ' +  '</h1>'

        # new_prod = Intake(date, sku, product_id, selling_price, initial_unit_count, cost_per_unit, licensing_fee, entity_id, staff_id, notes)
        # db.session.add(new_prod)
        
        # try:
        #     db.session.commit()
        #     print('added!')
        #     flash(f'Intake has been added!','success')
        #     return redirect(url_for('show_intake'))
        # except sq.IntegrityError:
        #     db.session.rollback()
        #     print('failed!')
        #     flash(f'This product already exists.', 'danger')
        #     return redirect('/intake')
        
    return render_template("intake.html", details=i_details, form=i_form)

@app.route("/staff/", methods = ['GET', 'POST'])
def show_staff():
    """list staff/add staff."""
    form = AddStaff()
    
    form 
    
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