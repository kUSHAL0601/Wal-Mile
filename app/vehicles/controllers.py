from flask import *
from sqlalchemy.exc import IntegrityError
from app import *
from .models import Vehicle

mod_vehicle = Blueprint('vehicle', __name__)

@mod_vehicle.route('/register', methods=['POST'])
def create_vehicle():
    try:
        vehicle_no = request.form['vehicle_no']
        present_location = request.form['present_location']
        driver_name= request.form['driver_name']
        capacity = request.form['capacity']
        base_cost = request.form['base_cost']
        cost_per_km = request.form['cost_per_km']
    except KeyError as e:
        return jsonify(success=False, message="%s not sent in the request" % e.args), 400

    v = Vehicle(vehicle_no, present_location, driver_name, capacity, base_cost, cost_per_km)
    db.session.add(v)
    try:
        db.session.commit()
    except IntegrityError as e:
        return jsonify(success=False, message="This vehicle already exists"), 400

    return jsonify(success=True)
