from api import app, dbase, generate_password_hash, cross_origin
from flask import request, jsonify
from models import *
from datetime import datetime, date
# newly added
from sqlalchemy import and_ 
import png
import pyqrcode
# 

@app.route('/login', methods=['GET', 'POST'])
@cross_origin('*')
def login():
    pass


@app.route('/newEmployee', methods=['POST'])
@cross_origin('*')
def addemployee():
    data = request.get_json()
    
    # birth_date = Strip the time!!!!!!!!
    # birthdate = datetime.strptime(data['birth_date'], '%Y-%M-%d')
    new_employee = Employee(fname=data['fname'], mname=data['mname'], lname=data['lname'], position=data['position'],
                            code=data['code'], contact=data['contact'], email=data['email'],
                            birth_date=data['birth_date'],  gender=data['gender'],address=data['address'], employeestatus=1)
    
    #search for employee using QRCODE
    employee = Employee.query.filter_by(code=generate_password_hash(data['code'], method='sha256')).first()
    if employee is None:
        dbase.session.add(new_employee)
        dbase.session.commit()
        return jsonify({'message': 'New employee created!'})
    else:
        return jsonify({'message': 'Employee already created'})

@app.route('/generate/qrcode', methods=['POST'])
@cross_origin('*')
def genereate_code():
    data = request.get_json()
    qr = pyqrcode.create(data['code'])
    qr.png('code.png', scale=6)
    return jsonify({'message': 'QR Code Generated!'})


@app.route('/deactivate', methods=['GET', 'POST'])
@cross_origin('*')
def delEmployee():
    
    data = request.get_json()
    #search for employee using QRCODE and if the employee is active
    employee = Employee.query.filter(and_(Employee.code==data['code'], Employee.employeestatus == 1)).first()
    # employee = Employee.query.filter_by(code=data['code']).first()
    if employee:
        # 1 for active
        # 0 for inactive
        #change the status to 0
    	employee.employeestatus = 0
    	dbase.session.add(employee)
    	dbase.session.commit()

    	return jsonify({'message': 'Employee deactivated'})
    else:
    	return jsonify({'message': 'Employee is not found'})

@app.route('/activate', methods=['GET', 'POST'])
@cross_origin('*')
def ReActEmployee():
    
    data = request.get_json()
    #search for employee using QRCODE and if the employee is active
    employee = Employee.query.filter(and_(Employee.code==data['code'], Employee.employeestatus == 0)).first()
    # employee = Employee.query.filter_by(code=data['code']).first()
    if employee:
        # 1 for active
        # 0 for inactive
        #change the status to 0
        employee.employeestatus = 1
        dbase.session.add(employee)
        dbase.session.commit()

        return jsonify({'message': 'Employee Activated'})
    else:
        return jsonify({'message': 'Employee is not found'})


@app.route('/edit/<string:user_id>', methods=['POST'])
@cross_origin('*')
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
            if data['address'] == '':
                employee.address = employee.address
            else:
                employee.address = data['address']
            dbase.session.commit()
            return jsonify({'message': 'Success!'})
        except:
            return jsonify({'message': 'edit failed'})
