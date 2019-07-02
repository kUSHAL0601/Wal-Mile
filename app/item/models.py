from flask_sqlalchemy import SQLAlchemy
from app import db

class Item(db.Model):
    __tablename__ = 'items'
    item_id = db.Column(db.Integer, primary_key=True)
    vehicle_no = db.Column(db.String(255))

    def __init__(self, item_id, vehicle_no):
        self.item_id = item_id
        self.vehicle_no = vehicle_no
