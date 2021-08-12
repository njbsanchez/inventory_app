from flask import render_template,url_for,redirect,flash,request,jsonify
from flaskinventory.forms import addstaff, addentity, addproduct, addintake, additem, addsale, recordsample
from flaskinventory.model import db, Staff, Entity, Product, Intake, Sale, Item, get_all_staff
from flaskinventory.app import app
import time, datetime
import sqlalchemy.exc as sq

@app.route("/")
def coming_soon():
    """dummy development page"""
    return render_template("coming_soon.html")

@app.route("/intake", methods = ['GET', 'POST'])
def show_staff():
    """list staff/add staff."""
    form = addstaff()
    details = get_all_staff()
    exists = bool(get_all_staff())
    # exists = bool(Staff.query.all())
    if exists == False and request.method == 'GET':
        flash(f'Add staff to view', 'info')
        
    if form.validate_on_submit():
        staff_name = form.staff_name.data
        role = form.role.data
        email = form.email.data
        phone = form.phone.data
        notes = form.notes.data
    
        new_staff = Staff(staff_name, role, email, phone, notes)
        db.session.add(new_staff)
        
        try:
            db.session.commit()
            print('added!')
            flash(f'{form.staff_name} has been added!','success')
            return redirect(url_for('staff'))
        except sq.IntegrityError:
            db.session.rollback()
            flash(f'This staff member already exists.', 'danger')
            return redirect('/staff')
        
    return render_template("staff.html", details=details, form=form)

@app.route("/staff", methods = ['GET', 'POST'])
def show_staff():
    """list staff/add staff."""
    form = addstaff()
    details = get_all_staff()
    exists = bool(get_all_staff())
    # exists = bool(Staff.query.all())
    if exists == False and request.method == 'GET':
        flash(f'Add staff to view', 'info')
        
    if form.validate_on_submit():
        staff_name = form.staff_name.data
        role = form.role.data
        email = form.email.data
        phone = form.phone.data
        notes = form.notes.data
    
        new_staff = Staff(staff_name, role, email, phone, notes)
        db.session.add(new_staff)
        
        try:
            db.session.commit()
            print('added!')
            flash(f'{form.staff_name} has been added!','success')
            return redirect(url_for('staff'))
        except sq.IntegrityError:
            db.session.rollback()
            flash(f'This staff member already exists.', 'danger')
            return redirect('/staff')
        
    return render_template("staff.html", details=details, form=form)
