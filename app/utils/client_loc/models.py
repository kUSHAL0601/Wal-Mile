from flask_sqlalchemy import SQLAlchemy
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class ClientLocation(db.Model):
    __tablename__ = 'clientlocation'
    addr_id=db.Column(db.Integer,primary_key=True)
    client_id = db.Column(db.String)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    location = db.Column(db.String(255))
    


    def __init__(self, client_id, latitude, longitude, location):
        self.client_id = client_id
        self.latitude = latitude
        self.longitude = longitude
        self.location = location
    