from flaskinventory.crud import calculate_quantity_instock
from flask import render_template, url_for, redirect, flash, request, jsonify
# additem, addsale, recordsample,
from flaskinventory.forms import AddStaff, addpayment, AddEntity, addproduct, addintake, LoginForm, RegisterForm, additem, addsample, addsampleitem, addsale
from flaskinventory.model import db, Payment, User, Staff, Entity, Product, Intake, Sale, Item, Sample, SampleItem
from flask_bootstrap import Bootstrap
from flaskinventory.app import app
from flask_bootstrap import Bootstrap
from flask_wtf import form
import time
import datetime
import flaskinventory.crud as crud
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
                return redirect(url_for('go_home'))

        return '<h1> Username or Password is incorrect. <h1>'
    return render_template("login.html", form=form)


@app.route("/")
def go_home():
    """dummy development page"""
    
    latest_sales = Sale.query.order_by(Sale.id.desc()).limit(5)
    latest_intakes = Intake.query.order_by(Intake.date.desc()).limit(5)
    broker_info = crud.outstanding_broker_fees()
    
    return render_template("home.html", latest_sales=latest_sales, latest_intakes=latest_intakes, broker_info=broker_info)


@app.route("/admin_new_user", methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        # return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'
        new_user = User(username=form.username.data,
                        email=form.email.data, 
                        password=form.password.data)
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
            return redirect(url_for('show_intake'))
        except sq.IntegrityError:
            db.session.rollback()
            flash(f'This product already exists.', 'danger')
            return redirect('/intake')
    
    details = Intake.query.all()
    exists = bool(Intake.query.all())
    
    form = addintake()

    form.product_id.choices = [(product.id, product.product_name)
                                 for product in Product.query.all()]
    form.supplier.choices = [(entity.id, entity.contact_name)
                               for entity in Entity.query.all()]

    if exists == False and request.method == 'GET':
        flash(f'Add intake to view', 'info')

    if form.validate_on_submit():

        # return '<h1>' + form.product_id.data + form.sku.data + ' ' + form.init_unitcount.data + ' ' +  form.supplier.data + ' ' +  '</h1>'

        new_intake = Intake(date=form.date.data,
                            product_id=form.product_id.data,
                            sku=form.sku.data,
                            type_key=form.type_key.data,
                            notes=form.notes.data,
                            initial_unit_count=form.init_unitcount.data,
                            cost_per_unit=form.cost_perunit.data,
                            licensing_fee=form.licensingfee.data,
                            broker_fee=form.broker_fee.data,
                            entity_id=form.supplier.data,)

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
    return render_template("intake.html", details=details, form=form, p_details=p_details, p_form=p_form)


@app.route("/inventory/", methods=['GET'])
def show_inventory():
    """list staff/add staff."""
    
    all_products = Product.query.order_by(Product.product_name).all()
    
    product_dict = {}
    
    for product in all_products:
        
        product_dict[product] = {"variants":{},
                                         "intake_count": crud.prod_get_intake_quantity(product.id),
                                         "sale_count": crud.prod_get_sale_quantity(product.id),
                                         "sample_count": crud.prod_get_sample_quantity(product.id)
                                         }

        variant_dict = product_dict[product]["variants"]
        
        for variant in product.intake_variants:
            variant_dict[variant] = {"original_count": crud.sku_get_intake_quantity(variant.id),
                              "sale_count": crud.sku_get_sale_quantity(variant.id),
                              "sample_count": crud.sku_get_sample_quantity(variant.id),
                              "current_count": calculate_quantity_instock(variant.id)
                              }
    
    return render_template("inventory.html", product_dict=product_dict)


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


@app.route("/customer/", methods=['GET', 'POST'])
def show_customers():
    """list staff/add staff."""
    form = AddEntity()
    details = Entity.query.filter(Entity.entity_role == "customer").all()
    exists = bool(Entity.query.all())

    if exists == False and request.method == 'GET':
        flash(f'Add an entity to view', 'info')

    if form.validate_on_submit():


        new_entity = Entity(contact_name=form.contact_name.data,
                            entity_role=form.entity_role.data,
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
            return redirect(url_for('show_customers'))
        except sq.IntegrityError:
            db.session.rollback()
            flash(f'This staff member already exists.', 'danger')
            return redirect('/entity')
    print (form.errors)
    return render_template("customer.html", details=details, form=form)

@app.route("/customer/<entity_id>", methods=['GET'])
def show_customer_record(entity_id):
    """list staff/add staff."""
    
    customer = Entity.query.filter(Entity.id == entity_id).first()
    
    payments = Payment.query.order_by(Payment.entity == customer).all()
    
    sample_dict = customer.get_samples_out()
    
    return render_template("customer_record.html", payments=payments, customer=customer, sample_dict=sample_dict)

@app.route("/vendor/", methods=['GET', 'POST'])
def show_vendors():
    """list staff/add staff."""
    form = AddEntity()
    details = Entity.query.filter(Entity.entity_role == "vendor").all()
    exists = bool(Entity.query.all())

    if exists == False and request.method == 'GET':
        flash(f'Add an entity to view', 'info')

    if form.validate_on_submit():


        new_entity = Entity(contact_name=form.contact_name.data,
                            entity_role=form.entity_role.data,
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
            return redirect(url_for('show_vendors'))
        except sq.IntegrityError:
            db.session.rollback()
            flash(f'This staff member already exists.', 'danger')
            return redirect('/show_vendors')
    print (form.errors)
    return render_template("vendor.html", details=details, form=form)

@app.route("/vendor/<entity_id>", methods=['GET'])
def show_vendor_record(entity_id):
    """list staff/add staff."""
    
    vendor = Entity.query.filter(Entity.id == entity_id).first()
    
    intakes = Intake.query.order_by(Intake.entity == vendor).all()
    
    
    return render_template("vendor_record.html", intakes=intakes, vendor=vendor)


@app.route("/payment/", methods=['GET', 'POST'])
def show_payment():
    """list sales."""
    
    details = Payment.query.order_by(Payment.date).all()
    exists = bool(Payment.query.all())
    
    form = addpayment()

    form.entity.choices = [(entity.id, entity.contact_name)
                               for entity in Entity.query.all()]
    form.staff_id.choices = [(staff.id, staff.staff_name)
                               for staff in Staff.query.all()]

    if exists == False and request.method == 'GET':
        flash(f'Add sale to view', 'info')

    if form.validate_on_submit():

        # return '<h1>' + form.product_id.data + form.sku.data + ' ' + form.init_unitcount.data + ' ' +  form.supplier.data + ' ' +  '</h1>'
        
        new_payment = Payment(date=form.date.data,
                          entity_id=form.entity.data,
                          staff_id=form.staff_id.data,
                          amount_received=form.amount_received.data,
                          notes=form.notes.data
                          )
                          
        print(new_payment)
        db.session.add(new_payment)
        db.session.commit()
        
        print('added!')
        flash(f'Payment has been recorded!', 'success')
        
        return redirect(url_for('show_payment'))

    return render_template("payment.html", details=details, form=form)


@app.route("/sale/", methods=['GET', 'POST'])
def show_sales():
    """list sales."""
    
    details = Sale.query.order_by(Sale.date).all()
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
                          broker_fee=form.broker_fee.data,
                          broker_fee_paid=form.broker_fee_paid.data,
                          notes=form.notes.data
                          )
                          
        print(new_sale)
        db.session.add(new_sale)
        db.session.commit()
        
        print('added!')
        flash(f'Sale has been recorded!', 'success')
        
        return redirect(url_for('show_sale_record',sale_id=new_sale.id))

    print (form.errors)
    return render_template("sale.html", details=details, form=form)


@app.route("/sale/<sale_id>", methods=['GET', 'POST'])
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
    
    form.sku.choices = [(intake.id, intake.sku)
                                 for intake in Intake.query.all()]
    
    if exists == False and request.method == 'GET':
        flash(f'Add sale items to view', 'info')

    if form.validate_on_submit():

        # return '<h1>' + form.product_id.data + form.sku.data + ' ' + form.init_unitcount.data + ' ' +  form.supplier.data + ' ' +  '</h1>'
        
        new_item = Item(product_id=form.product_id.data,
                        intake_id=form.sku.data,
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


@app.route("/sale_all/", methods=['GET'])
def show_sale_all():
    """list staff/add staff."""
    
    latest_sales = Sale.query.order_by(Sale.id.desc()).limit(5)
    
    all_customers = Entity.query.filter(Entity.entity_role == "customer").order_by(Entity.contact_name).all()
    
    return render_template("sale_all.html", latest_sales=latest_sales, all_customers=all_customers)


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


