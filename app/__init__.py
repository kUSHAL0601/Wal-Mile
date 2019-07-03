# Import flask and template operators
from flask import *

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from functools import wraps

# Define the WSGI application object
app = Flask(__name__)
CORS(app)
# Configurations
app.config.from_object('config')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
   return render_template('404.html')

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify(message="Unauthorized", success=False), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/', methods=['GET'])
def home_page():
    # if 'user_id' in session:
    #     return redirect("/dashboard",code=302)
    return render_template('input.html')

# Import a module / component using its blueprint handler variable (mod_auth)
from app.utils.vehicles.controllers import mod_vehicle
from app.utils.item.controllers import mod_item
from app.utils.user.controllers import mod_user
from app.utils.client_loc.controllers import mod_clientlocation


# Register blueprint(s)
app.register_blueprint(mod_vehicle)
app.register_blueprint(mod_item)
app.register_blueprint(mod_clientlocation)
#app.register_blueprint(mod_todo)

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()
