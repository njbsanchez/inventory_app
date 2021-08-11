from flask import render_template,url_for,redirect,flash,request,jsonify
from flaskinventory.forms import addentity, addproduct, addintake, additem, addsale, recordsample
from flaskinventory.model import Staff, Entity, Product, Intake, Sale, Item
import time, datetime
# from sqlalchemy.exc import IntegrityError

@app.route("/")
def coming_soon():
    """dummy development page"""
    return render_template("pages/coming_soon.html")

@app.route("/addproduct", methods = ['POST'])
def add_product():
    """add product."""
    form = addproduct()
