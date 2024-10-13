from flask import url_for, Blueprint
from flask import request, session, render_template, redirect
from utils import DataBaseRegister, Profile, Cars, Problems

bp = Blueprint('router', __name__)

@bp.route('/', methods=['GET'])
def homepage():
    DataBaseRegister.create_tables()
    return render_template("index.html")


@bp.route('/catalog', methods=['GET'])
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

@bp.route('/get_updated_cars', methods=['GET'])
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


