from http import HTTPMethod
from flask import request

from main import app
from utils.cars import Cars
from utils.problems import Problems

@app.route(rule='/register_car', methods=[HTTPMethod.POST])
def register_car():
    request_data = request.form.to_dict()
    new_car = Cars(car_name=request_data['car_name'],
                   car_number=request_data['car_number'],
                   load_capacity=request_data['load_capacity'],
                   date_publish=request_data['date_publish'],
                   user_id=request_data['user_id']).add_new_car()
    return new_car

@app.route('/delete_car', methods=[HTTPMethod.POST])
def delete_car():
    request_data = request.form.to_dict()
    delete = Cars.delete_car(
        car_id=request_data['id']
    )
    return delete

@app.route('/update_car_information', methods=[HTTPMethod.POST])
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