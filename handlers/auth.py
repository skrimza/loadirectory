from json import dumps
from flask import url_for, jsonify
from flask import request, session, render_template, redirect
from utils import DataBaseRegister, Profile, Cars, Problems
from validators import pyform
from flask import Blueprint

bp = Blueprint('router', __name__)

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
    try:
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
                                'redirect': url_for('router.catalog')
                                }))
    except Exception:
        return jsonify(dumps({'Content-Type': 'application/json', 'response': 'Что-то пошло не так'}))
    else:
        return jsonify(dumps({'Content-Type': 'application/json', 'response': login_form}))  

@bp.route('/catalog', methods=['GET'])
def catalog():
    Cars.update_active_car()
    context_all = {'all_users': Profile.get_all_users(), 
                   'all_cars': Cars.get_all_cars(),
                   'all_problems': Problems.get_all_problems()}
    if not session.get('visits'):
        return redirect(url_for('router.homepage'))
    session.permanent = True
    if 'visits' in session:
        session['visits'] = session.get('visits') + 1
    else:
        session['visits'] = 1
    return render_template("main.html", visits=session['visits'], context=context_all)


@bp.route('/quit', methods=['POST'])
def quit_app():
    session.clear()
    return redirect(url_for('router.homepage'))