from flask import *
from sqlalchemy.exc import IntegrityError
from app import *
from .models import Vehicle

mod_vehicle = Blueprint('vehicle', __name__)

@mod_vehicle.route('/vehicle', methods=['GET'])
def render_item_page():
    return render_template('vehicle.html')


@mod_vehicle.route('/vehicle/add', methods=['POST'])
def create_vehicle():
    try:
        vehicle_no = request.form['vehicle_no']
        # present_location = request.form['present_location']
        driver_name= request.form['driver_name']
        capacity = request.form['capacity']
        base_cost = request.form['base_cost']
        cost_per_km = request.form['cost_per_km']
    except KeyError as e:
        return jsonify(success=False, message="%s not sent in the request" % e.args), 400

    v = Vehicle(vehicle_no, 'NA', driver_name, capacity, base_cost, cost_per_km)
    db.session.add(v)
    try:
        db.session.commit()
    except IntegrityError as e:
        return jsonify(success=False, message="This vehicle already exists"), 400

    return jsonify(success=True)

@mod_vehicle.route('/vehicle/get', methods=['GET'])
def get_vehicle():
    all_items= Vehicle.query.filter("NA"=="NA").all()
    ans=[]
    for i in all_items:
        ans.append([i.vehicle_no,i.driver_name,i.capacity,i.base_cost,i.cost_per_km])
    return jsonify(ans)

@mod_vehicle.route('/vehicle/getAll', methods=['GET'])
def get_vehicle_all():
    all_items= Vehicle.query.filter("NA"=="NA").all()
    ans=[]
    for i in all_items:
        ans.append([i.vehicle_no,i.capacity])
    return jsonify(ans)


@mod_vehicle.route('/vehicle/remove', methods=['POST'])
def remove_item():
    try:
        item_id = request.form['vid']
        print(item_id)
    except KeyError as e:
        return jsonify(success=False, message="%s not sent in the request" % e.args), 400
    u=Vehicle.query.filter(Vehicle.vehicle_no==item_id).first()
    db.session.delete(u)
    try:
        db.session.commit()
    except IntegrityError as e:
        return jsonify(success=False, message="This item already exists"), 400

    return jsonify(success=True)
