from api import app, dbase, generate_password_hash, check_password_hash
from flask import request, jsonify
from models import *
# newly added
from flask_login import login_user, login_required, LoginManager, logout_user
import datetime
#pip install timedate, time
from sqlalchemy import and_ 
import png
import pyqrcode
from datetime import timedelta, date, datetime, time


login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(user_id)

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

@app.route('/newAdmin', methods=['POST'])
# @login_required
def newAdmin():
    data = request.get_json()
    # new = Admin(username = data['username'], password = data['password'])
    try:
        if data['username'] == '' or data['username'] is None:
            admin.fname = admin.fname
        else:
            admin.fname = data['username']
        if data['code'] == '':
            admin.code = admin.code
        else:
            admin.code = generate_password_hash(data['code'], method='sha256')
        dbase.session.commit()
        return jsonify({'message': 'successfull!'})
    except:
         return jsonify({'message': 'edit failed'})


@app.route('/newEmployee', methods=['POST'])
# @login_required
def addemployee():
    data = request.get_json()
    
    # birth_date = Strip the time!!!!!!!!
    birthdate = datetime.strptime(data['birth_date'], '%Y-%M-%d')
    new_employee = Employee(fname=data['fname'], mname=data['mname'], lname=data['lname'], position=data['position'],
                            code=data['code'], contact=data['contact'], email=data['email'],
                            birth_date=data['birth_date'],  gender=data['gender'],address=data['address'], employeestatus=1)
    
    #search for employee using QRCODE
    employee = Employee.query.filter_by(code=generate_password_hash(data['code'], method='sha256')).first()
    print generate_password_hash(data['code'], method='sha256')
    if employee is None:
        dbase.session.add(new_employee)
        dbase.session.commit()
        return jsonify({'message': 'New employee created!'})

    else:
        return jsonify({'message': 'Employee already created'})


@app.route('/generate/qrcode', methods=['POST'])
# @login_required
def genereate_code():
    data = request.get_json()
    qr = pyqrcode.create(data['code'])
    qr.png('code.png', scale=6)
    return jsonify({'message': 'QR Code Generated!'})


@app.route('/deactivate', methods=['GET', 'POST'])
# @login_required
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
# @login_required
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
# @login_required
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


@app.route('/TimeIn/<string:user_id>', methods=['POST'])
def timein(user_id):

    employee = Employee.query.filter_by(code=user_id).first()
    print employee
    empID = employee.employeeid
    atts = Attendance.query.filter_by(employeeid =  empID).first()
    attsID = atts.status
    print atts
    print attsID
    if employee is None:
        return jsonify({'message': 'user not found'})
    else: 
        now = datetime.now().strftime("%m%d%Y%H%M")
        # print str(now)
        now1 = datetime.now().strftime("%m%d%Y")
        # # print str(now1)
        morninglate = "0900"
        aftelate = "1305"
        morningIN1 = "0700"
        morningIN2 = "1159"
        morningOUT1 = "0901"
        morningOUT2 = "1259"
        afteIN1 = "1201"
        afteIN2 = "1759"
        afteOUT1 = "1301"
        afteOUT2 = "1900"        
        # MORNING
        #     Timein  -   7:00AM to 11:59AM
        #     Timeout -   9:01AM to 12:59PM


        # AFTERNOON
        #     Timein  -   12:01PM to 5:59PM
        #     Timeout -   1:01PM to 7:00PM

        # OVERTIME
        #     Timein  -   6:01 to 9:59PM
        #     Timeout -   7:01 to 10:00PM (AUTOMATIC OUT by 10:00PM)

        morningTimeIn1 = ''.join([now1, morningIN1])
        morningTimeIn2 = ''.join([now1, morningIN2])
        morningTimeOut1 = ''.join([now1, morningOUT1])
        morningTimeOut2 = ''.join([now1, morningOUT2])
        afteIn1 = ''.join([now1, afteIN1])
        afteIn2 = ''.join([now1, afteIN2])
        afteOut1 = ''.join([now1, afteOUT1])
        afteOut2 = ''.join([now1, afteOUT2])
        lateafte = ''.join([now1, aftelate])
        latemorning = ''.join([now1, morninglate]) 
        times = datetime.time(datetime.now())
        # timeins1 = "9:00:00"
        # print time
        # print times 
        # print late
        status1 = ""
        if now < morningTimeIn1 and now > morningTimeIn2:
            # 1 for timein and 
            # 0 for timeout
            if now < latemorning:
                if attsID == 0:
                    status = 1
                    status1 = "not late"
                else:
                    status = 0
                    status1 = "timeOut"
                return jsonify({'message': status1})
            else:
                
                if attsID == 0:
                    status = 1
                    status1 = "late"
                else:
                    status = 0
                    status1 = "timeOut"
                return jsonify({'message': status1})
        elif now > morningTimeOut1 and now < morningTimeOut2   :
            if now < latemorning:
                if attsID == 0:
                    status = 1
                    status1 = "not late"
                else:
                    status = 0
                    status1 = "timeOut"
                return jsonify({'message': status1})
            else:
                
                if attsID == 0:
                    status = 1
                    status1 = "late"
                else:
                    status = 0
                    status1 = "timeOut"
                return jsonify({'message': status1})
        elif now > afteIn1 and now < afteIn2  :
            if now < lateafte:
                if attsID == 0:
                    status = 1
                    status1 = "not late"
                else:
                    status = 0
                    status1 = "timeOut"
                return jsonify({'message': status1})
            else:
                
                if attsID == 0:
                    status = 1
                    status1 = "late"
                else:
                    status = 0
                    status1 = "timeOut"
                return jsonify({'message': status1})
        elif now > afteOu1 and now < afteOut2  :
            if now < lateafte:
                if attsID == 0:
                    status = 1
                    status1 = "not late"
                else:
                    status = 0
                    status1 = "timeOut"
                return jsonify({'message': status1})
            else:
                
                if attsID == 0:
                    status = 1
                    status1 = "late"
                else:
                    status = 0
                    status1 = "timeOut"
                return jsonify({'message': status1})
            print "dasdasd"
            print status1
        # EmployeeTimeIn = Attendance(lateTotal, absentTotal, timeIn=now, timeOut, status, dailyStatus, employeeid)
        # dbase.session.add(EmployeeTimeIn)
        # dbase.session.commit()