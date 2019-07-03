from flask import *
from sqlalchemy.exc import IntegrityError
from app import *
from .models import Item

mod_item = Blueprint('item', __name__)

@mod_item.route('/item', methods=['GET'])
def render_item_page():
	print("Here")
	return render_template('item.html')

@mod_item.route('/item/add', methods=['POST'])
def create_item():
    try:
        # item_id = request.form['item_id']
        height = request.form['height']
        width = request.form['width']
        fragile = request.form['fragile']
        status = request.form['status']
        client_id = request.form['client_id']
        vehicle_no = request.form['vehicle_no']
        weight = request.form['weight']
    except KeyError as e:
        return jsonify(success=False, message="%s not sent in the request" % e.args), 400

    i = Item(height, weight, fragile, status, client_id, vehicle_no, weight)
    db.session.add(i)
    try:
        db.session.commit()
    except IntegrityError as e:
        return jsonify(success=False, message="This item already exists"), 400

    return jsonify(success=True)

@mod_item.route('/item/get', methods=['GET'])
def get_item():
	all_items= Item.query.filter(Item.client_id=="NA").all()
	ans=[]
	for i in all_items:
		ans.append([i.item_id,i.height,i.width,i.weight,i.fragile])
	return jsonify(ans)

@mod_item.route('/item/remove', methods=['POST'])
def remove_item():
    try:
        item_id = int(request.form['itd'])
        print(item_id)
    except KeyError as e:
        return jsonify(success=False, message="%s not sent in the request" % e.args), 400
    u=Item.query.filter(Item.item_id==item_id).first()
    db.session.delete(u)
    try:
        db.session.commit()
    except IntegrityError as e:
        return jsonify(success=False, message="This item already exists"), 400

    return jsonify(success=True)
