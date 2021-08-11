from flask import Flask
from flask import render_template
from flaskinventory.ext import db


def create_app(config_file='config.py'):
    
    app = Flask(__name__.split('.')[0])
    app.config.from_pyfile(config_file)
    
    connect_to_db(app)
    
    return app

def connect_to_db(flask_app):  
    
    db.app = flask_app
    db.init_app(flask_app)
    
    print('Connected to the db!')
    
    return None

if __name__ == '__main__':
    
    app = create_app()
    
    db.create_all()
    db.session.commit()

    


