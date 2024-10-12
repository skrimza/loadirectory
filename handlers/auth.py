from http import HTTPMethod
from json import dumps
from flask import (jsonify,
                   request,
                   session,
                   url_for)
from validators.validation import pyform
from utils.user import Profile
from routes import all_bp


@all_bp.route(rule='/register', methods=[HTTPMethod.POST])
def register_user():
    register_form = pyform(register=request.form.to_dict())
    print(jsonify({'text': register_form}))
    return jsonify(dumps({'Content-Type': 'application/json', 'response': register_form}))


@all_bp.route(rule='/login', methods=[HTTPMethod.POST])
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