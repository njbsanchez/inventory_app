
from flaskinventory.model import db, connect_to_db
from flaskinventory.app import app
import flaskinventory.routes

if __name__ == '__main__':
    
    connect_to_db(app)
    db.create_all()
    app.run()
        