from api import app, dbase, generate_password_hash, check_password_hash
from flask import request, jsonify
from models import *
# add to req.txt
from flask_login import login_user, login_required, LoginManager, logout_user
from datetime import datetime
# add to req.txt
import pyqrcode
# add to req.txt
import png


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    data = request.get_json()
    user = Admin.query.filter_by(username=data['username']).first()
    if user is None:
        return jsonify({'message': 'Invalid username or password'})
    else:
        if check_password_hash(user.password, data['password']):
            login_user(user)
            return jsonify({'message': 'Login Successful!'})


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out'})


@app.route('/newEmployee', methods=['POST'])
@login_required
def addemployee():
    data = request.get_json()
    # birth_date = Strip the time!!!!!!!!
    new_employee = Employee(fname=data['fname'], mname=data['mname'], lname=data['lname'], position=data['position'],
                            code=data['code'], contact=data['contact'], email=data['email'],
                            birth_date=data['birth_date'],  gender=data['gender'], employeestatus=1)

    employee = Employee.query.filter_by(code=generate_password_hash(data['code'], method='sha256')).first()
    if employee is None:
        dbase.session.add(new_employee)
        dbase.session.commit()
        return jsonify({'message': 'New employee created!'})
    else:
        return jsonify({'message': 'Employee already created'})


@app.route('/generate/qrcode', methods=['POST'])
@login_required
def genereate_code():
    data = request.get_json()
    qr = pyqrcode.create(data['code'])
    qr.png('code.png', scale=6)
    return jsonify({'message': 'QR Code Generated!'})


@app.route('/edit/<string:user_id>', methods=['POST'])
@login_required
def edit(user_id):
    data = request.get_json()
    employee = Employee.query.filter_by(code=user_id).first()
    if employee is None:
        return jsonify({'message': 'user not found'})
    else:
        try:
            # Check if the jsondata is empty, can be done here or front end.
            if data['fname'] == '' or data['fname'] is None:
                employee.fname = employee.fname
            else:
                employee.fname = data['fname']
            if data['mname'] == '':
                employee.mname = employee.mname
            else:
                employee.mname = data['mname']
            if data['lname'] == '':
                employee.lname = employee.lname
            else:
                employee.lname = data['lname']
            if data['position'] == '':
                employee.position = employee.position
            else:
                employee.position = data['position']
            if data['code'] == '':
                employee.code = employee.code
            else:
                employee.code = generate_password_hash(data['code'], method='sha256')
            if data['contact'] == '':
                employee.contact = employee.contact
            else:
                employee.contact = data['contact']
            if data['email'] == '':
                employee.email = employee.email
            else:
                employee.email = data['email']
            if data['birth_date'] == '':
                employee.birth_date = employee.birth_date
            else:
                employee.birth_date = data['birth_date']
            if data['gender'] == '':
                employee.gender = employee.gender
            else:
                employee.gender = data['gender']
            dbase.session.commit()
            return jsonify({'message': 'Success!'})
        except:
            return jsonify({'message': 'edit failed'})


@app.route('/time-in-pin/', methods=['GET'])
def time_in_pin():
    data = request.get_json()
    pin = generate_password_hash(data['pin'], method='sha256')
    employee = Employee.query.filter_by(code=pin).first()
    if employee:
        # add log in function here!
        return jsonify({'message': 'Time-in Successful!'})
    else:
        return jsonify({'message': 'Time-'})
