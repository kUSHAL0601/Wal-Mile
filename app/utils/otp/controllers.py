from flask import *
from sqlalchemy.exc import IntegrityError
from app import *
from .models import Otp

mod_otp = Blueprint('otp', __name__)

@mod_vehicle.route('/otp/add', methods=['POST'])
def add_otp():
    v = Otp(42, "999999")
    db.session.add(v)
    try:
        db.session.commit()
    except IntegrityError as e:
        return jsonify(success=True)
    return jsonify(success=True)


@mod_vehicle.route('/otp/update', methods=['POST'])
def update_otp():
    try:
        cid = int(request.form['cid'])
        # present_location = request.form['present_location']
        otp= request.form['otp']
    except KeyError as e:
        return jsonify(success=False, message="%s not sent in the request" % e.args), 400

    v = Otp.query.filter(Otp.client_id==cid).first()
    v.otp=otp
    db.session.add(v)
    try:
        db.session.commit()
    except IntegrityError as e:
        return jsonify(success=False, message="This vehicle already exists"), 400

    return jsonify(success=True)

@mod_vehicle.route('/otp/verify', methods=['POST'])
def verify_otp():
    try:
        cid = int(request.form['cid'])
        # present_location = request.form['present_location']
        otp= request.form['otp']
    except KeyError as e:
        return jsonify(success=False, message="%s not sent in the request" % e.args), 400
    all_items= Otp.query.filter(Otp.client_id==cid).first()
    print(otp,cid,all_items.otp)
    if all_items.otp==otp:
        return jsonify(success=True)
    else:
        return jsonify(success=False),400
