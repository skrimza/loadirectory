from http import HTTPMethod
from flask import request
from utils.problems import Problems
from routes import all_bp


@all_bp.route(rule='/register_problem', methods=[HTTPMethod.POST])
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
    
    
@all_bp.route('/delete_problem', methods=[HTTPMethod.POST])
def delete_problem():
    request_data = request.form.to_dict()
    delete_problem_car = Problems.delete_problem(
        problem_id=request_data['id']
    )
    return delete_problem_car

@all_bp.route('/update_problem_information', methods=[HTTPMethod.POST])
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