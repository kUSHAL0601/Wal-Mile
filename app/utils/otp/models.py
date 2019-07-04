from flask_sqlalchemy import SQLAlchemy
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class Otp(db.Model):
    __tablename__ = 'otp'
    client_id = db.Column(db.Integer(), primary_key=True)
    otp = db.Column(db.String(255))

    def __init__(self, client_id, otp):
        self.client_id = client_id
        self.otp = otp
