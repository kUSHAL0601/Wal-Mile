from flask import *
from sqlalchemy.exc import IntegrityError
from app import *
from .models import Vehicle
from werkzeug.security import generate_password_hash, check_password_hash

mod_vehicle = Blueprint('vehicle', __name__)

@mod_vehicle.route('/register', methods=['POST'])
def create_user():
    try:
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
    except KeyError as e:
        return jsonify(success=False, message="%s not sent in the request" % e.args), 400

    u = User(name, username, password)
    db.session.add(u)
    try:
        db.session.commit()
    except IntegrityError as e:
        return jsonify(success=False, message="This username already exists"), 400

    return jsonify(success=True)
