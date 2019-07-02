from flask import *
from sqlalchemy.exc import IntegrityError
from app import *
from .models import Item

mod_item = Blueprint('item', __name__)

@mod_item.route('/itemAdd', methods=['POST'])
def create_item():
    try:
        item_id = request.form['item_id']
        height = request.form['height']
        width = request.form['width']
        fragile = request.form['fragile']
        status = request.form['status']
        vehicle_no = request.form['vehicle_no']
    except KeyError as e:
        return jsonify(success=False, message="%s not sent in the request" % e.args), 400

    i = Item(item_id, vehicle_no)
    db.session.add(i)
    try:
        db.session.commit()
    except IntegrityError as e:
        return jsonify(success=False, message="This item already exists"), 400

    return jsonify(success=True)
