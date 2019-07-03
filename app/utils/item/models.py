from flask_sqlalchemy import SQLAlchemy
from app import db

class Item(db.Model):
    __tablename__ = 'items'
    item_id = db.Column(db.Integer, primary_key=True)
    height = db.Column(db.String(255))
    width = db.Column(db.String(255))
    fragile = db.Column(db.String(255))
    status = db.Column(db.String(255))
    client_id = db.Column(db.Integer)
    vehicle_no = db.Column(db.String(255))
    weight = db.Column(db.String(255))


    def __init__(self, height, width, fragile, status,client_id, vehicle_no, weight):
        self.height = height
        self.width = width
        self.fragile = fragile
        self.status = status
        self.vehicle_no = vehicle_no
        self.client_id = client_id
        self.weight = weight
