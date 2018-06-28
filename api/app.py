from api import app, dbase
from flask import request, jsonify
from models import *
from datetime import datetime


@app.route('/', methods=['GET'])
def index():
    return 'this is index to test'


@app.route('/newEmployee', methods=['POST'])
def addemployee():
    data = request.get_json()
    new_employee = Employee(fname=data['fname'], mname=data['mname'], lname=data['lname'], position=data['position'],
                            code=data['code'], contact=data['contact'], email=data['email'],
                            birth_date=data['birth_date'],  gender=data['gender'], employeestatus=1)

    employee = Employee.query.filter_by(code=data['code']).first()
    if employee is None:
        dbase.session.add(new_employee)
        dbase.session.commit()
        return jsonify({'message': 'New employee created!'})
    else:
        return jsonify({'message': 'employee already created'})

@app.route('/deactivate', methods=['GET', 'POST'])
def delEmployee():
    
	data = request.get_json()

	employee = Employee.query.filter_by(code=data['code']).first()
	if employee:
		employee.employeestatus = 0
		dbase.session.add(employee)
		dbase.session.commit()

		return jsonify({'message': 'Employee deactivated'})
	else:
		return jsonify({'message': 'Employee is not found'})
