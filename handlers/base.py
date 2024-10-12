from http import HTTPMethod
from flask import (render_template,
                   request,
                   url_for,
                   redirect,
                   session)
from utils.database import DataBaseRegister
from utils.cars import Cars
from utils.user import Profile
from utils.problems import Problems
from routes import all_bp
from main import app

@all_bp.route('/')
def homepage():
    database=DataBaseRegister(conn=connect(app.config['DATABASE_URL']))
    database.create_tables()
    return render_template("index.html")

@all_bp.route('/catalog')
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
        
    
@all_bp.route('/get_updated_cars', methods=[HTTPMethod.GET])
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