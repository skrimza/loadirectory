from flask import request, Blueprint, render_template
from utils import Cars, Problems, Profile

base_bp = Blueprint('catalog', __name__)

@base_bp.route('/get_updated_cars', methods=['GET'])
def get_updated_cars():
    request_data = request.form.to_dict()
    print(request_data.get('register'))
    if request_data.get('register'):
        context_all = {'all_users': Profile.get_all_users(), 
                   'all_cars': Cars.get_all_cars(),
                   'all_problems': Problems.get_all_problems()}
    else:
        Cars.update_active_car()
        context_all = {'all_users': Profile.get_all_users(), 
                   'all_cars': Cars.get_all_cars(),
                   'all_problems': Problems.get_all_problems()}
    return render_template('chunk/cars-block.html', context=context_all)

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