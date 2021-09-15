from flask import render_template, url_for, redirect, flash, request, jsonify
# additem, addsale, recordsample,
from flaskinventory.forms import AddStaff, AddEntity, addproduct, addintake, LoginForm, RegisterForm, additem, addsample, addsampleitem, addsale
from flaskinventory.model import db, User, Staff, Entity, Product, Intake, Sale, Item, Sample, SampleItem
from flask_bootstrap import Bootstrap
from flaskinventory.app import app
from flask_bootstrap import Bootstrap
from flask_wtf import form
import time
import datetime
import sqlalchemy.exc as sq

bootstrap = Bootstrap(app)


@app.route("/login", methods=['GET', 'POST'])
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


@app.route("/admin_new_user", methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'
        new_user = User(username=form.username.data,
                        email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()

        return '<h1> New user has been created!</h1>'

    return render_template("signup.html", form=form)


@app.route("/")
def coming_soon():
    """dummy development page"""
    return render_template("coming_soon.html")


@app.route("/product", methods=['GET', 'POST'])
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
            flash(f'{p_form.prodname} has been added!', 'success')
            return redirect(url_for('show_product'))
        except sq.IntegrityError:
            db.session.rollback()
            flash(f'This product already exists.', 'danger')
            return redirect('/product')

    return render_template("product.html", details=p_details, form=p_form)


@app.route("/intake/", methods=['GET', 'POST'])
def show_intake():
    """list staff/add staff."""
    
    details = Intake.query.all()
    exists = bool(Intake.query.all())
    
    form = addintake()

    form.product_id.choices = [(product.id, product.product_name)
                                 for product in Product.query.all()]
    form.supplier.choices = [(entity.id, entity.contact_name)
                               for entity in Entity.query.all()]
    form.staff_id.choices = [(staff.id, staff.staff_name)
                               for staff in Staff.query.all()]

    if exists == False and request.method == 'GET':
        flash(f'Add intake to view', 'info')

    if form.validate_on_submit():

        # return '<h1>' + form.product_id.data + form.sku.data + ' ' + form.init_unitcount.data + ' ' +  form.supplier.data + ' ' +  '</h1>'

        new_intake = Intake(date=form.date.data,
                            product_id=form.product_id.data,
                            sku=form.sku.data,
                            selling_price=form.selling_price.data,
                            notes=form.notes.data,
                            initial_unit_count=form.init_unitcount.data,
                            cost_per_unit=form.cost_perunit.data,
                            licensing_fee=form.licensingfee.data,
                            entity_id=form.supplier.data,
                            staff_id=form.staff_id.data)

        print(new_intake)
        db.session.add(new_intake)

        try:
            db.session.commit()
            print('added!')
            flash(f'Intake has been added!', 'success')
            return redirect(url_for('show_intake'))
        except sq.IntegrityError:
            db.session.rollback()
            print('failed!')
            flash(f'This product already exists.', 'danger')
            return redirect('/intake')

    print (form.errors)
    return render_template("intake.html", details=details, form=form)


@app.route("/staff/", methods=['GET', 'POST'])
def show_staff():
    """list staff/add staff."""
    form = AddStaff()

    details = Staff.query.all()
    exists = bool(Staff.query.all())

    if exists == False and request.method == 'GET':
        flash(f'Add staff to view', 'info')

    if form.validate_on_submit():

        # return '<h1>' + form.staff_name.data + ' ' + form.role.data + ' ' + form.email.data + ' ' + form.notes.data + '</h1>'

        new_staff = Staff(staff_name=form.staff_name.data,
                          role=form.role.data,
                          email=form.email.data,
                          phone=form.phone.data,
                          notes=form.notes.data)

        print(new_staff)
        db.session.add(new_staff)

        try:
            db.session.commit()
            print('added!')
            flash(f'Staff has been added!', 'success')
            return redirect(url_for('show_staff'))
        except sq.IntegrityError:
            db.session.rollback()
            flash(f'This staff member already exists.', 'danger')
            return redirect('/staff')

    return render_template("staff.html", details=details, form=form)


@app.route("/entity/", methods=['GET', 'POST'])
def show_entity():
    """list staff/add staff."""
    form = AddEntity()
    details = Entity.query.all()
    exists = bool(Entity.query.all())

    if exists == False and request.method == 'GET':
        flash(f'Add an entity to view', 'info')

    if form.validate_on_submit():

        new_entity = Entity(contact_name=form.contact_name.data,
                            company_name=form.company_name.data,
                            entity_type=form.entity_type.data,
                            email=form.email.data,
                            phone=form.phone.data,
                            notes=form.notes.data)

        print(new_entity)
        db.session.add(new_entity)

        try:
            db.session.commit()
            print('added!')
            flash(f'Entity has been added!', 'success')
            return redirect(url_for('show_entity'))
        except sq.IntegrityError:
            db.session.rollback()
            flash(f'This staff member already exists.', 'danger')
            return redirect('/entity')

    return render_template("entity.html", details=details, form=form)


@app.route("/sale/", methods=['GET', 'POST'])
def show_sales():
    """list sales."""
    
    details = Sale.query.all()
    exists = bool(Sale.query.all())
    
    form = addsale()

    form.entity.choices = [(entity.id, entity.contact_name)
                               for entity in Entity.query.all()]
    form.staff_id.choices = [(staff.id, staff.staff_name)
                               for staff in Staff.query.all()]

    if exists == False and request.method == 'GET':
        flash(f'Add sale to view', 'info')

    if form.validate_on_submit():

        # return '<h1>' + form.product_id.data + form.sku.data + ' ' + form.init_unitcount.data + ' ' +  form.supplier.data + ' ' +  '</h1>'
        
        new_sale = Sale(  invoice_no=form.invoice_no.data,
                          date=form.date.data,
                          prem_disc_percentage=form.prem_disc.data,
                          wiring_fee=form.wiring_fee.data,
                          entity_id=form.entity.data,
                          staff_id=form.staff_id.data,
                          broker_fee=form.broker_fee.data
                          )
                          
        print(new_sale)
        db.session.add(new_sale)
        db.session.commit()
        
        print('added!')
        flash(f'Sale has been recorded!', 'success')
        
        return redirect(url_for('show_sale_record',sale_id=new_sale.id))

    print (form.errors)
    return render_template("sale.html", details=details, form=form)


@app.route("/sale_record/<sale_id>", methods=['GET', 'POST'])
def show_sale_record(sale_id):
    """list sales."""
    
    sale_instance = Sale.query.filter(Sale.id == sale_id).first()
    
    entity_info = Entity.query.filter(Entity.id==sale_instance.entity_id).first()
    staff_info = Staff.query.filter(Staff.id==sale_instance.staff_id).first()
    
    details = Item.query.filter(Item.sale_id == sale_id).all()
    exists = bool(details)
    
    form = additem()

    form.product_id.choices = [(product.id, product.product_name)
                                 for product in Product.query.all()]
    
    form.sku.choices = [(intake.sku)
                                 for intake in Intake.query.all()]
    
    if exists == False and request.method == 'GET':
        flash(f'Add sale items to view', 'info')

    if form.validate_on_submit():

        # return '<h1>' + form.product_id.data + form.sku.data + ' ' + form.init_unitcount.data + ' ' +  form.supplier.data + ' ' +  '</h1>'
        
        new_item = Item(product_id=form.product_id.data,
                        sku=form.sku.data,
                        quantity=form.quantity.data,
                        sale_id=sale_id
                        )
                          
        print(new_item)
        db.session.add(new_item)
        db.session.commit()
        
        print('added!')
        flash(f'Item has been added!', 'success')
        
        
        return redirect(url_for('show_sale_record',sale_id=sale_id))

    print (form.errors)
    return render_template("sale_record.html",details=details, staff_info=staff_info, entity_info=entity_info, sale_instance=sale_instance, form=form, sale_id=sale_id)


@app.route("/sample/", methods=['GET', 'POST'])
def show_samples():
    """list samples."""
    
    details = Sample.query.all()
    exists = bool(Sample.query.all())
    
    form = addsample()

    form.entity.choices = [(entity.id, entity.contact_name)
                               for entity in Entity.query.all()]
    form.staff_id.choices = [(staff.id, staff.staff_name)
                               for staff in Staff.query.all()]

    if exists == False and request.method == 'GET':
        flash(f'Add sample to view', 'info')

    if form.validate_on_submit():

        # return '<h1>' + form.product_id.data + form.sku.data + ' ' + form.init_unitcount.data + ' ' +  form.supplier.data + ' ' +  '</h1>'
        
        new_sample_record = Sample(  record_no=form.record_no.data,
                          date=form.date.data,
                          entity_id=form.entity.data,
                          staff_id=form.staff_id.data,
                          movement=form.movement.data,
                          notes=form.notes.data
                          )
                          
        print(new_sample_record)
        db.session.add(new_sample_record)
        db.session.commit()
        
        print('added!')
        flash(f'Sample has been recorded!', 'success')
        
        return redirect(url_for('show_sample_record',sample_record_id=new_sample_record.id))

    print (form.errors)
    return render_template("sample.html", details=details, form=form)


@app.route("/sample_record/<sample_record_id>", methods=['GET', 'POST'])
def show_sample_record(sample_record_id):
    """list samples."""
    
    sample_instance = Sample.query.filter(Sample.id == sample_record_id).first()
    
    entity_info = Entity.query.filter(Entity.id==sample_instance.entity_id).first()
    
    details = SampleItem.query.filter(SampleItem.sample_record_id == sample_record_id).all()
    exists = bool(details)
    
    form = addsampleitem()

    form.product_id.choices = [(product.id, product.product_name)
                                 for product in Product.query.all()]
    
    form.sku.choices = [(intake.sku)
                                 for intake in Intake.query.all()]
    
    if exists == False and request.method == 'GET':
        flash(f'Add sample items to view', 'info')

    if form.validate_on_submit():

        # return '<h1>' + form.product_id.data + form.sku.data + ' ' + form.init_unitcount.data + ' ' +  form.supplier.data + ' ' +  '</h1>'
        
        new_sample_item = SampleItem(product_id=form.product_id.data,
                        sku=form.sku.data,
                        quantity=form.quantity.data,
                        sample_record_id=sample_record_id,
                        notes=form.notes.data
                        )
                          
        print(new_sample_item)
        db.session.add(new_sample_item)
        db.session.commit()
        
        print('added!')
        flash(f'Item has been added!', 'success')
        
        return redirect(url_for('show_sample_record',sample_record_id=sample_record_id))

    print (form.errors)
    return render_template("sample_record.html", entity_info=entity_info, sample_instance=sample_instance, details=details, form=form, sample_reocrd_id=sample_record_id)


