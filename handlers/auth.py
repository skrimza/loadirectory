from json import dumps
from flask import url_for, Blueprint, jsonify
from flask import request, session, render_template
from utils import DataBaseRegister, Profile
from validators import pyform

bp = Blueprint('route', __name__)

@bp.route('/', methods=['GET'])
def homepage():
    DataBaseRegister.create_tables()
    return render_template("index.html")

@bp.route(rule='/register', methods=['POST'])
def register_user():
    register_form = pyform(register=request.form.to_dict())
    print(jsonify({'text': register_form}))
    return jsonify(dumps({'Content-Type': 'application/json', 'response': register_form}))


@bp.route(rule='/login', methods=['POST'])
def login_user():
    request_data = request.form.to_dict()
    print(request_data)
    login_form = Profile(name=None, 
                         lastname=None, 
                         email=request_data['email'], 
                         password=request_data['password']).login_user()
    if 'message' in login_form.keys():
        session['visits'] = 1
        session['name'] = login_form['name']
        return jsonify(dumps({'Content-Type': 'application/json', 
                              'response': login_form, 
                              'redirect': url_for('catalog')
                              }))
    else:
        return jsonify(dumps({'Content-Type': 'application/json', 'response': login_form}))
