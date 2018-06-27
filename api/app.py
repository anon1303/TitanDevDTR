import models
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, LoginManager, current_user
from models import *


@app.route('/newEmployee', methods=['POST'])
def addemployee()
	
	data = request.get_json()
	birthdate = datetime.datetime.strptime(data['birth_date'], '%Y-%M-%d')

	new_Employee = employee(fname=data['fname'], mname=data['mname'], lname=data['lname'], position=data['position'], code=data['code'],
							 contact=data['contact'], email=data['email'], birth_date=data['birth_date'],  gender=['gender'])

	employee = Employee.query.filter_by(code=data['code']).first()

	if employee is None:
		db.session.add(new_Employee)
        db.session.commit()

        return jsonify({'message': 'New employee created!'})
    else:
        return jsonify({'message': 'employee already created'})


