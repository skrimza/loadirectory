from json import dumps
from flask import request, Blueprint, jsonify, session, url_for
from utils import Cars, Problems, Profile
from validators import pyform

base_bp = Blueprint('catalog', __name__)

@base_bp.route(rule='/register', methods=['POST'])
def register_user():
    register_form = pyform(register=request.form.to_dict())
    print(jsonify({'text': register_form}))
    return jsonify(dumps({'Content-Type': 'application/json', 'response': register_form}))


@base_bp.route(rule='/login', methods=['POST'])
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

@base_bp.route(rule='/register_car', methods=['POST'])
def register_car():
    request_data = request.form.to_dict()
    new_car = Cars(car_name=request_data['car_name'],
                   car_number=request_data['car_number'],
                   load_capacity=request_data['load_capacity'],
                   date_publish=request_data['date_publish'],
                   user_id=request_data['user_id']).add_new_car()
    return new_car

@base_bp.route('/delete_car', methods=['POST'])
def delete_car():
    request_data = request.form.to_dict()
    delete = Cars.delete_car(
        car_id=request_data['id']
    )
    return delete

@base_bp.route('/update_car_information', methods=['POST'])
def update_car_information():
    request_data = request.form.to_dict()
    print(request_data)
    update_info_car = Problems.update_info_car(
        car_id = request_data['car_id'],
        description = request_data['description'],
        date_start = request_data['date_start'],
        date_finish = request_data['date_finish']
    )
    return update_info_car


@base_bp.route(rule='/register_problem', methods=['POST'])
def register_problem():
    request_data = request.form.to_dict()
    new_problem = Problems(title=request_data['title'], 
                           description=request_data['description'], 
                           car_id=request_data['car_id'], 
                           date_start=request_data['date_start'], 
                           date_finish=request_data['date_finish']).add_new_problem()
    if new_problem.startswith('Недостаточно'):
        return 'False'
    else:
        return 'True'
    
    
@base_bp.route('/delete_problem', methods=['POST'])
def delete_problem():
    request_data = request.form.to_dict()
    delete_problem_car = Problems.delete_problem(
        problem_id=request_data['id']
    )
    return delete_problem_car

@base_bp.route('/update_problem_information', methods=['POST'])
def update_problem_information():
    request_data = request.form.to_dict()
    print(request_data)
    update_info_problem = Problems.update_problem_information(
        problem_id = request_data['problem_id'],
        title = request_data['title'],
        car_id = request_data['car_id'],
        description = request_data['description'],
        date_start = request_data['date_start'],
        date_finish = request_data['date_finish']
    )
    return update_info_problem