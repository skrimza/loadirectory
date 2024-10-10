from http import HTTPMethod
from json import dumps
from datetime import timedelta
from flask import (Flask, 
                   render_template,
                   jsonify, 
                   request, 
                   url_for, 
                   session,
                   redirect)
from data import DataBaseRegister
from validation import pyform
from data import Profile, Cars, Problems
from sessions.session import generic_session_key


app = Flask(__name__)

app.secret_key = generic_session_key()
app.permanent_session_lifetime = timedelta(days=1)

@app.route('/')
def homepage():
    DataBaseRegister.create_tables()
    return render_template("index.html")


@app.route(rule='/register', methods=[HTTPMethod.POST])
def register_user():
    register_form = pyform(register=request.form.to_dict())
    print(jsonify({'text': register_form}))
    return jsonify(dumps({'Content-Type': 'application/json', 'response': register_form}))


@app.route(rule='/login', methods=[HTTPMethod.POST])
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


@app.route('/catalog')
def catalog():
    Cars.update_active_car()
    context_all = {'all_users': Profile.get_all_users(), 
                   'all_cars': Cars.get_all_cars(),
                   'all_problems': Problems.get_all_problems()}
    if not session.get('visits'):
        return redirect(url_for('homepage'))
    session.permanent = True
    if 'visits' in session:
        session['visits'] = session.get('visits') + 1
    else:
        session['visits'] = 1
    return render_template("main.html", visits=session['visits'], context=context_all)
        

@app.route(rule='/register_car', methods=[HTTPMethod.POST])
def register_car():
    request_data = request.form.to_dict()
    new_car = Cars(car_name=request_data['car_name'],
                   car_number=request_data['car_number'],
                   load_capacity=request_data['load_capacity'],
                   date_publish=request_data['date_publish'],
                   user_id=request_data['user_id']).add_new_car()
    return new_car


@app.route(rule='/register_problem', methods=[HTTPMethod.POST])
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

    
@app.route('/get_updated_cars', methods=[HTTPMethod.GET])
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


@app.route('/delete_car', methods=[HTTPMethod.POST])
def delete_car():
    request_data = request.form.to_dict()
    delete = Cars.delete_car(
        car_id=request_data['id']
    )
    return delete


@app.route('/delete_problem', methods=[HTTPMethod.POST])
def delete_problem():
    request_data = request.form.to_dict()
    delete_problem_car = Problems.delete_problem(
        problem_id=request_data['id']
    )
    return delete_problem_car

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
    return 'update_info_car'

if __name__ == "__main__":
    app.run(debug=True)
    