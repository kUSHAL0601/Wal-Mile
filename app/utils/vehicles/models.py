from flask_sqlalchemy import SQLAlchemy
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    vehicle_no = db.Column(db.String(255), primary_key=True)
    present_location = db.Column(db.String(255))
    driver_name= db.Column(db.String(255))
    capacity = db.Column(db.Integer)
    base_cost = db.Column(db.String(255))
    cost_per_km = db.Column(db.String(255))


    def __init__(self, vehicle_no, present_location, driver_name, capacity, base_cost, cost_per_km):
        self.vehicle_no = vehicle_no
        self.present_location = present_location
        self.driver_name = driver_name
        self.capacity = capacity
        self.base_cost = base_cost
        self.cost_per_km = cost_per_km
