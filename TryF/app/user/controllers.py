from flask import *
from sqlalchemy.exc import IntegrityError
from app import *
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash


mod_user = Blueprint('user', __name__)

@mod_user.route('/', methods=['GET'])
def home_page():
    if 'user_id' in session:
        return redirect("/dashboard",code=302)
    return render_template('home.html')

@mod_user.route('/login', methods=['GET'])
def login_page():
    if 'user_id' in session:
        return redirect("/dashboard",code=302)
    return render_template('/login.html')

@mod_user.route('/signup', methods=['GET'])
def signup_page():
    if 'user_id' in session:
        return redirect("/dashboard",code=302)
    return render_template('/signup.html')

@mod_user.route('/dashboard', methods=['GET'])
def dashboard_page():
    return render_template('dashboard.html')

@mod_user.route('/playlists', methods=['GET'])
def playlists_page():
    return render_template('playlist.html')

@mod_user.route('/plsredirecttodash', methods=['POST'])
def red_dashboard_page():
    try:
        session['DoReload']=1;
        return jsonify(success=True),200
    except:
        return jsonify(success=False),400

@mod_user.route('/reloadDone', methods=['POST'])
def rel_dashboard_page():
    if(session['DoReload']!=1):
        return jsonify(success=True),200
    try:
        session['DoReload']=0;
        return jsonify(success=True),200
    except:
        return jsonify(success=False),400


@mod_user.route('/viewlogin', methods=['GET'])
def check_login():
    if 'user_id' in session:
        user = User.query.filter(User.id == session['user_id']).first()
        return jsonify(success=True, user=user.to_dict())

    return jsonify(success=False), 401


@mod_user.route('/login', methods=['POST'])
def login():
    try:
        username = request.form['username']
        password = request.form['password']
    except KeyError as e:
        return jsonify(success=False, message="%s not sent in the request" % e.args), 400

    user = User.query.filter(User.username == username).first()
    if user is None or not user.check_password(password):
        return jsonify(success=False, message="Invalid Credentials"), 400

    session['user_id'] = user.id

    return jsonify(success=True, user=user.to_dict())

@mod_user.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id')
    return jsonify(success=True)

@mod_user.route('/register', methods=['POST'])
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

@mod_user.route('/edit/name',methods=['GET'])
@requires_auth
def updatename():
    return render_template('edit.html')

@mod_user.route('/edit/name',methods=['POST'])
@requires_auth
def update_name():
    try:
        nm=request.form['name']
        usrname=request.form['username']
        uid=request.form['uid']
    except KeyError as e:
        return jsonify(success=False, message="%s not sent in the request" % e.args), 400
    if uid!=str(session['user_id']):
        return jsonify(success=False, loggedin=uid,message="Don not mess with others' accounts",user=session['user_id']), 200 
    u=User.query.filter(User.id==uid).first()
    if u is None:
        return jsonify(success=False, message="No such user"), 400
    u.name = nm
    u.username = usrname
    try:
        db.session.commit()
    except IntegrityError as e:
        return jsonify(success=False, message="This username already exists!,Try Different Name"), 400
    return jsonify(success=True,message="Updated Successfuly")

@mod_user.route('/edit/password',methods=['POST'])
@requires_auth
def update_pwd():
    try:
        old_pwd=request.form['old']
        new_pwd=request.form['new']
        cnew_pwd=request.form['cnew']
        uid=request.form['uid']
    except KeyError as e:
        return jsonify(success=False, message="%s not sent in the request" % e.args), 400
    if uid!=str(session['user_id']):
        return jsonify(success=False, message="Do not mess with other people's accounts"), 400 
    u=User.query.filter(User.id==uid).first()
    #print(u)
    if u is None:
        return jsonify(success=False, message="No such user"), 400
    if not u.check_password(old_pwd):
        return jsonify(success=False,message="Old Password Is Wrong"),400
    u.password=generate_password_hash(new_pwd)
    try:
        db.session.commit()
    except IntegrityError as e:
        return jsonify(success=False, message="Somethong went wrong..please try again"), 400
    return jsonify(success=True,message="Updated Successfuly")

@mod_user.route('/edit/password',methods=['GET'])
@requires_auth
def updatepwd():
    return render_template('edit.html')

@mod_user.route('/edit',methods=['GET'])
@requires_auth
def updateboth():
    return render_template('edit.html')
