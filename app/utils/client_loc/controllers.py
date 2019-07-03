from flask import *
from sqlalchemy.exc import IntegrityError
from app import *
from .models import ClientLocation

mod_clientlocation = Blueprint('clientlocation', __name__)

@mod_clientlocation.route('/addAddress', methods=['GET'])
def add_addr():
    return render_template('add_addr.html')

@mod_clientlocation.route('/clientlocation', methods=['POST'])
def create_clientlocation():
    try:
        client_id = request.form['client_id']
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        location = request.form['location']
    except KeyError as e:
        return jsonify(success=False, message="%s not sent in the request" % e.args), 400

    cl = ClientLocation(client_id, latitude, longitude, location)
    db.session.add(cl)
    try:
        db.session.commit()
    except IntegrityError as e:
        return jsonify(success=False, message="This address already exists"), 400

    return jsonify(success=True)

@mod_clientlocation.route('/getAddr', methods=['POST'])
def getAddr():
    client_id = request.form['client_id']
    u=ClientLocation.query.filter(ClientLocation.client_id==client_id).all()
    import json
    ans=[]
    for i in u:
        ans.append([i.latitude,i.longitude,i.location])
    print(ans)
    return jsonify(ans)