from api import app, dbase, generate_password_hash, cross_origin, CORS, check_password_hash
from flask import request, jsonify
from models import *
# newly added
from flask_login import login_user, login_required, LoginManager, logout_user
import datetime as dt
import time
#pip install timedate, time
from sqlalchemy import and_, desc
import png
import pyqrcode
import  easy_date
from datetime import timedelta, date, datetime, time
import os

# TIME AND DATE FORMAT
# 

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
    new = Admin(username = data['username'], password = data['password'])
    try:
        if data['username'] == '' or data['username'] is None:
            new.fname = new.fname
        else:
            new.fname = data['username']
        if data['code'] == '':
            new.code = new.code
        else:
            new.code = generate_password_hash(data['code'], method='sha256')
        dbase.session.commit()
        return jsonify({'message': 'successfull!'})
    except:
         return jsonify({'message': 'edit failed'})


@app.route('/newEmployee', methods=['POST'])
# @login_required
@cross_origin(allow_headers=['Content-Type'])
def addemployee():
    data = request.get_json()
    
    # birth_date = Strip the time!!!!!!!!
    # birthdate = dt.datetime.date()
    b = str(data['birth_date'])
    print b
    new_employee = Employee(fname=data['fname'], mname=data['mname'], lname=data['lname'], position=data['position'],
                            code=data['code'], contact=data['contact'], email=data['email'],
                            birth_date=b,  gender=data['gender'], address=data['address'], employeestatus=1)
    
    #search for employee using QRCODE
    employee = Employee.query.filter_by(code=data['code']).first()
    if employee:
        return jsonify({'message': 'Employee already created'})
    else:
        dbase.session.add(new_employee)
        dbase.session.commit()
        return jsonify({'message': 'New employee created!'})


@app.route('/view/', methods=['GET', 'POST'])
def viewEmployee():
    employess = Employee.query.filter_by(employeestatus=1).all()

    all = []
    for i in employess:
        data = {}
        data['fname'] = i.fname
        data['mname'] = i.mname
        data['lname'] = i.lname
        data['position'] = i.position
        data['code'] = i.code
        data['contact'] = i.contact
        data['email'] = i.email
        data['birth_date'] = str(i.birth_date)
        data['gender'] = i.gender
        data['address'] = i.address
        all.append(data)
    return jsonify({'message': all})
# @app.route('/search/', mothods =['GET', 'POST'])
# def searchEmployee():
#     data = request.get_json()
#     employee1 = '%' + data['lname'] + '%'

#     activate =  Employee.query.filter(and_(Employee.lname == employee1 , Employee.employeestatus == 0)).all()
    

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
                employee.code = data['code']
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


@app.route('/TimeIn/', methods=['POST'])
def timein():
    now = datetime.now().strftime("%m%d%Y%H%M")
    datenow = datetime.now().strftime("%m%d%Y")
    datenow1 = datetime.now().strftime("%m%d%Y")
    now1 = datetime.now().strftime("%m%d%Y")
    print now

    morning7 = "0700"
    morning9 = "0900"
    morning12 = "1200"

    afte1 = "1300"
    afte6 = "1800"
    afte7= "1900"
        

    m7 = ''.join([now1, morning7])
    m9 = ''.join([now1, morning9])
    m12 = ''.join([now1, morning12])
    
    a1 = ''.join([now1, afte1])
    a6 = ''.join([now1, afte6])
    a7 = ''.join([now1, afte7]) 

    # 1 for active and 0 for inactive
    data = request.get_json()
    employee = Employee.query.filter_by(code=data['code']).first()

    if employee is None:
        return jsonify({'message': 'user not found'})
    else:    
        empID = employee.employeeid
        attendancenNew = Attendance(employeeid = empID)
        atts = Attendance.query.filter_by(employeeid=empID).first()
        print empID
        print atts  
#////////////////////////////IF ID IS NOT LISTED IN THE ATTENDACE CRETAE NEW///////////////////////////////#
        if atts is None:
            dbase.session.add(attendancenNew)
            dbase.session.commit()
            atts = Attendance.query.filter_by(employeeid=empID).first()
            atts.date = datenow
            dbase.session.commit()

            nowdate = atts.date
            
            if now >= m7 and now <= m9:
                if atts.morningStatus == 0 and atts.afterStatus == 0:
                    if atts.morningTimeOut is None:
                        atts.morningStatus = 1
                        atts.morningTimeIn = datetime.now()
                        atts.morningDailyStatus = 'not late'
                        print "dsjahsfdfkjdslafsjjkj"
                        dbase.session.commit()
                        return jsonify({'message': 'not late'})
                    else:
                        return jsonify({'message':'you cannot time in twice'})           
                elif atts.morningStatus == 1 and atts.afterStatus == 0:
                    print 'aaaaaaaaa'
                    return jsonify({'message':'no time out at this time'})
                elif atts.morningStatus == 0 and atts.afterStatus == 1:
                    if atts.morningTimeOut is None:
                        atts.afterStatus = 0
                        atts.morningStatus = 1
                        atts.afterTimeOut = datetime.now()
                        atts.morningTimeIn = datetime.now()
                        atts.morningDailyStatus = 'not late'
                        dbase.session.commit()
                        return jsonify({'message':'not late, kindly dont forget to timeout in morning'})
                    else:
                        return jsonify({'message':'you cannot time in twice'})
                elif atts.morningStatus == 1 and atts.afterStatus == 1:
                    atts.afterStatus = 0
                    atts.afterTimeOut = datetime.now()
                    dbase.session.commit()
                    return jsonify({'message':'no time out at this time'})

            elif now > m9 and now <= m12:
                if atts.morningStatus == 0 and atts.afterStatus == 0:
                    if atts.morningTimeOut is None:
                        atts.morningStatus = 1
                        atts.lateTotal = atts.lateTotal + 1
                        atts.morningDailyStatus = 'late'
                        atts.morningTimeIn = datetime.now()
                        # atts.morningRemark = wala pa nabutang
                        print 'bbbbbbbbbbbb' 
                        dbase.session.commit()
                        absents()
                        return jsonify({'message': 'late'})
                    else:
                        absents()
                        return jsonify({'message':'you cannot time in twice'})
                elif atts.morningStatus == 1 and atts.afterStatus == 0:
                    if atts.morningTimeOut is None:
                        atts.morningStatus = 0
                        atts.morningTimeOut = datetime.now()
                        # atts.morningRemark = wala pa nabutang
                        print 'cccccccccccc'
                        dbase.session.commit()
                        absents()
                        return jsonify({'message': 'time out'})
                    else: 
                        absents()
                        return jsonify({'message':'you cannot time in twice'})
                elif atts.morningStatus == 0 and atts.afterStatus == 1:
                    if atts.morningTimeOut is None:
                        atts.afterStatus = 0
                        atts.morningStatus = 1
                        atts.afterTimeOut = datetime.now()
                        atts.morningTimeIn = datetime.now()
                        atts.morningDailyStatus = 'late'
                        # atts.morningRemark = wala pa nabutang
                        print 'dddddddddddddd'
                        dbase.session.commit()
                        absents()
                        return jsonify({'message':'late, kindly dont forget to timeout in morning'})
                    else:
                        absents()
                        return jsonify({'message':'you cannot time in twice'})
                elif atts.morningStatus == 1 and atts.afterStatus == 1:
                    if atts.morningTimeOut is None:  
                        atts.afterStatus = 0
                        atts.morningStatus = 0
                        atts.afterTimeOut = datetime.now()
                        atts.morningTimeOut = datetime.now()
                        print 'eeeeeeeeeeeeeee'
                        dbase.session.commit()
                        absents()
                        return jsonify({'message':'time out'})
                    else:
                        absents()
                        return jsonify({'message':'you cannot time in twice'})
            elif now > m12 and now <= a1: # 12 -7pm
                if atts.morningStatus == 0 and atts.afterStatus == 0:
                    if atts.afterTimeOut is None:
                        atts.afterStatus = 1
                        atts.afterDailyStatus = 'not late'
                        atts.afterTimeIn = datetime.now()
                        # atts.morningRemark = wala pa nabutang
                        print 'fffffffffffffff'
                        employs = Employee.query.filter_by(employeestatus = 1).all()
                        ids = []
                        for i in employs:
                            ids.append(employs.code)
                        print ids
                        # present = Attendance.query.filter(Attendance.employeeid == )
                        dbase.session.commit()
                        return jsonify({'message': 'time in for afternoon'})
                    else:
                        return jsonify({'message':'you cannot time in twice'})
                elif atts.morningStatus == 1 and atts.afterStatus == 0:
                    if atts.afterTimeOut is None:
                        atts.morningStatus = 0
                        atts.morningTimeOut = datetime.now()
                        # atts.morningRemark = wala pa nabutang
                        print 'ggggggggggg'
                        dbase.session.commit()
                        return jsonify({'message': 'time out for morning'})
                    else:
                        return jsonify({'message':'you cannot time in twice'})
                elif atts.morningStatus == 0 and atts.afterStatus == 1:
                    return jsonify({'message':'no time out for afternoon at this time'})
                elif atts.morningStatus == 1 and atts.afterStatus == 1:
                    atts.morningStatus = 0
                    atts.morningTimeOut = datetime.now()
                    dbase.session.commit()
                    return jsonify({'message':'no time out for afternoon at this time'})
            elif now > a1 and now <= a6:
                if atts.morningStatus == 0 and atts.afterStatus == 0:
                    if atts.afterTimeOut is None:
                        atts.afterStatus = 1
                        atts.lateTotal = atts.lateTotal + 1
                        atts.afterDailyStatus = 'late'
                        atts.afterTimeIn = datetime.now()
                        # atts.morningRemark = wala pa nabutang
                        dbase.session.commit()
                        return jsonify({'message': 'late'})
                    else:
                        return jsonify({'message':'you cannot time in twice'})
                elif atts.morningStatus == 1 and atts.afterStatus == 0:
                    if atts.afterTimeOut is None:
                        atts.morningStatus = 0
                        atts.afterStatus = 1
                        atts.morningTimeOut = datetime.now()
                        atts.lateTotal = atts.lateTotal + 1
                        atts.afterDailyStatus = 'late'
                        atts.afterTimeIn = datetime.now()
                        # atts.morningRemark = wala pa nabutang
                        return jsonify({'message': 'time out'})
                    else:
                        return jsonify({'message':'you cannot time in twice'})
                elif atts.morningStatus == 0 and atts.afterStatus == 1:
                    atts.afterStatus = 0
                    atts.afterTimeOut = datetime.now()
                    dbase.session.commit()
                    return jsonify({'message':'time out'})
                elif atts.morningStatus == 1 and atts.afterStatus == 1:
                    atts.afterStatus = 0
                    atts.morningStatus = 0
                    atts.afterTimeOut = datetime.now()
                    atts.morningTimeOut = datetime.now()
                    dbase.session.commit()
                    return jsonify({'message':'time out'})
            elif now > a6 and now <= a7:
                if atts.morningStatus == 0 and atts.afterStatus == 0:
                    return jsonify({'message':'no time in for this time'})

                elif atts.morningStatus == 1 and atts.afterStatus == 0:
                    atts.morningStatus = 0
                    atts.morningTimeOut = datetime.now()
                    dbase.session.commit()
                    return jsonify({'message':'not time in for afternoon'})

                elif atts.morningStatus == 0 and atts.afterStatus == 1:
                    atts.afterStatus = 0
                    atts.afterTimeOut = datetime.now()
                    dbase.session.commit()
                    return jsonify({'message':'time out for afternoon'})
                elif atts.morningStatus == 1 and atts.afterStatus == 1:
                    atts.morningStatus = 0
                    atts.afterStatus = 0
                    atts.morningTimeOut = datetime.now()
                    atts.afterTimeOut = datetime.now()
                    dbase.session.commit()
                    return jsonify({'message':'time out for afternoon and morning'})
            else:
                print datenow
                return jsonify({'message':'OT napud siya'})
#////////// ///////////////////////////////IF ID IS EXISTING///////////////////////////////////////////////////////////////#
        elif atts:

            atts = Attendance.query.filter_by(employeeid=empID).first()
            date1 = atts.date
            #///////////////////////////////////////////CHECK IF THE DATE IS SAME//////////////////////////////////////#
            if date1 == datenow1:
                #////////////////////////IF DATE IS SAME////////////////////////////#
                if now >= m7 and now <= m9:
                    if atts.morningStatus == 0 and atts.afterStatus == 0:
                        if atts.morningTimeOut is None:
                            atts.morningStatus = 1
                            atts.morningTimeIn = datetime.now()
                            atts.morningDailyStatus = 'not late'
                            # print "dsjahsfdfkjdslafsjjkj"
                            dbase.session.commit()
                            return jsonify({'message': 'not late'})
                        else:
                            return jsonify({'message':'you cannot time in twice'})           
                    elif atts.morningStatus == 1 and atts.afterStatus == 0:
                        # print 'aaaaaaaaa'
                        return jsonify({'message':'no time out at this time'})
                    elif atts.morningStatus == 0 and atts.afterStatus == 1:
                        if atts.morningTimeOut is None:
                            atts.afterStatus = 0
                            atts.morningStatus = 1
                            atts.afterTimeOut = datetime.now()
                            atts.morningTimeIn = datetime.now()
                            atts.morningDailyStatus = 'not late'
                            dbase.session.commit()
                            return jsonify({'message':'not late, kindly dont forget to timeout in morning'})
                        else:
                            return jsonify({'message':'you cannot time in twice'})
                    elif atts.morningStatus == 1 and atts.afterStatus == 1:
                        atts.afterStatus = 0
                        atts.afterTimeOut = datetime.now()
                        dbase.session.commit()
                        return jsonify({'message':'no time out at this time'})

                elif now > m9 and now <= m12:
                    if atts.morningStatus == 0 and atts.afterStatus == 0:
                        if atts.morningTimeOut is None:
                            atts.morningStatus = 1
                            atts.lateTotal = atts.lateTotal + 1
                            atts.morningDailyStatus = 'late'
                            atts.morningTimeIn = datetime.now()
                            # atts.morningRemark = wala pa nabutang
                            # print 'bbbbbbbbbbbb' 
                            dbase.session.commit()
                            absents()
                            return jsonify({'message': 'late'})
                        else:
                            absents()
                            return jsonify({'message':'you cannot time in twice'})
                    elif atts.morningStatus == 1 and atts.afterStatus == 0:
                        if atts.morningTimeOut is None:
                            atts.morningStatus = 0
                            atts.morningTimeOut = datetime.now()
                            # atts.morningRemark = wala pa nabutang
                            # print 'cccccccccccc'
                            dbase.session.commit()
                            absents()
                            return jsonify({'message': 'time out'})
                        else:
                            absents()
                            return jsonify({'message':'you cannot time in twice'})
                    elif atts.morningStatus == 0 and atts.afterStatus == 1:
                        if atts.morningTimeOut is None:
                            atts.afterStatus = 0
                            atts.morningStatus = 1
                            atts.afterTimeOut = datetime.now()
                            atts.morningTimeIn = datetime.now()
                            atts.morningDailyStatus = 'late'
                            # atts.morningRemark = wala pa nabutang
                            dbase.session.commit()
                            absents()
                            return jsonify({'message':'late, kindly dont forget to timeout in morning'})
                        else:
                            absents()
                            return jsonify({'message':'you cannot time in twice'})
                    elif atts.morningStatus == 1 and atts.afterStatus == 1:
                        if atts.morningTimeOut is None:  
                            atts.afterStatus = 0
                            atts.morningStatus = 0
                            atts.afterTimeOut = datetime.now()
                            atts.morningTimeOut = datetime.now()
                            dbase.session.commit()
                            absents()
                            return jsonify({'message':'time out'})
                        else:
                            absents()
                            return jsonify({'message':'you cannot time in twice'})
                elif now > m12 and now <= a1: # 12 -7pm
                    if atts.morningStatus == 0 and atts.afterStatus == 0:
                        if atts.afterTimeOut is None:
                            atts.afterStatus = 1
                            atts.afterDailyStatus = 'not late'
                            atts.afterTimeIn = datetime.now()
                            # atts.morningRemark = wala pa nabutang
                            # print 'ddddddddddddd' 
                            dbase.session.commit()
                            return jsonify({'message': 'time in for afternoon'})
                        else:
                            return jsonify({'message':'you cannot time in twice'})
                    elif atts.morningStatus == 1 and atts.afterStatus == 0:
                        if atts.afterTimeOut is None:
                            atts.morningStatus = 0
                            atts.morningTimeOut = datetime.now()
                            # atts.morningRemark = wala pa nabutang
                            # print 'eeeeeeeeeeeeeeee'
                            dbase.session.commit()
                            return jsonify({'message': 'time out for morning'})
                        else:
                            return jsonify({'message':'you cannot time in twice'})
                    elif atts.morningStatus == 0 and atts.afterStatus == 1:
                        return jsonify({'message':'no time out for afternoon at this time'})
                    elif atts.morningStatus == 1 and atts.afterStatus == 1:
                        atts.morningStatus = 0
                        atts.morningTimeOut = datetime.now()
                        dbase.session.commit()
                        return jsonify({'message':'no time out for afternoon at this time'})
                elif now > a1 and now <= a6:
                    if atts.morningStatus == 0 and atts.afterStatus == 0:
                        if atts.afterTimeOut is None:
                            atts.afterStatus = 1
                            atts.lateTotal = atts.lateTotal + 1
                            atts.afterDailyStatus = 'late'
                            atts.afterTimeIn = datetime.now()
                            # atts.morningRemark = wala pa nabutang
                            # print 'fffffffffffff' 
                            dbase.session.commit()
                            return jsonify({'message': 'late'})
                        else:
                            return jsonify({'message':'you cannot time in twice'})
                    elif atts.morningStatus == 1 and atts.afterStatus == 0:
                        if atts.afterTimeOut is None:
                            atts.morningStatus = 0
                            atts.afterStatus = 1
                            atts.morningTimeOut = datetime.now()
                            atts.lateTotal = atts.lateTotal + 1
                            atts.afterDailyStatus = 'late'
                            atts.afterTimeIn = datetime.now()
                            # atts.morningRemark = wala pa nabutang
                            # print 'ggggggggggggg'
                            dbase.session.commit()
                            return jsonify({'message': 'time out'})
                        else:
                            return jsonify({'message':'you cannot time in twice'})
                    elif atts.morningStatus == 0 and atts.afterStatus == 1:
                        atts.afterStatus = 0
                        atts.afterTimeOut = datetime.now()
                        dbase.session.commit()
                        return jsonify({'message':'time out'})
                    elif atts.morningStatus == 1 and atts.afterStatus == 1:
                        atts.afterStatus = 0
                        atts.morningStatus = 0
                        atts.afterTimeOut = datetime.now()
                        atts.morningTimeOut = datetime.now()
                        dbase.session.commit()
                        return jsonify({'message':'time out'})
                elif now > a6 and now <= a7:
                    if atts.morningStatus == 0 and atts.afterStatus == 0:
                        return jsonify({'message':'no time in for this time'})

                    elif atts.morningStatus == 1 and atts.afterStatus == 0:
                        atts.morningStatus = 0
                        atts.morningTimeOut = datetime.now()
                        dbase.session.commit()
                        return jsonify({'message':'not time in for afternoon'})

                    elif atts.morningStatus == 0 and atts.afterStatus == 1:
                        atts.afterStatus = 0
                        atts.afterTimeOut = datetime.now()
                        dbase.session.commit()
                        return jsonify({'message':'time out for afternoon'})
                    elif atts.morningStatus == 1 and atts.afterStatus == 1:
                        atts.morningStatus = 0
                        atts.afterStatus = 0
                        atts.morningTimeOut = datetime.now()
                        atts.afterTimeOut = datetime.now()
                        dbase.session.commit()
                        return jsonify({'message':'time out for afternoon and morning'})
                else:
                    print datenow
                    return jsonify({'message':'OT napud siya'})
       



#///////////////////////////////////////IF DATE IS NOT THE SAME CREATE NEW ATTENDANCE//////////////////////////////////////////# 
            else:
                dbase.session.add(attendancenNew)
                dbase.session.commit()
                atts = Attendance.query.filter_by(employeeid=empID).first()
                atts.date = datenow
                dbase.session.commit()
                if now >= m7 and now <= m9:
                    if atts.morningStatus == 0 and atts.afterStatus == 0:
                        if atts.morningTimeOut is None:
                            atts.morningStatus = 1
                            atts.morningTimeIn = datetime.now()
                            atts.morningDailyStatus = 'not late'
                            print "dsjahsfdfkjdslafsjjkj"
                            dbase.session.commit()
                            return jsonify({'message': 'not late'})
                        else:
                            return jsonify({'message':'you cannot time in twice'})           
                    elif atts.morningStatus == 1 and atts.afterStatus == 0:
                        print 'aaaaaaaaa'
                        return jsonify({'message':'no time out at this time'})
                    elif atts.morningStatus == 0 and atts.afterStatus == 1:
                        if atts.morningTimeOut is None:
                            atts.afterStatus = 0
                            atts.morningStatus = 1
                            atts.afterTimeOut = datetime.now()
                            atts.morningTimeIn = datetime.now()
                            atts.morningDailyStatus = 'not late'
                            dbase.session.commit()
                            return jsonify({'message':'not late, kindly dont forget to timeout in morning'})
                        else:
                            return jsonify({'message':'you cannot time in twice'})
                    elif atts.morningStatus == 1 and atts.afterStatus == 1:
                        atts.afterStatus = 0
                        atts.afterTimeOut = datetime.now()
                        dbase.session.commit()
                        return jsonify({'message':'no time out at this time'})

                elif now > m9 and now <= m12:
                    if atts.morningStatus == 0 and atts.afterStatus == 0:
                        if atts.morningTimeOut is None:
                            atts.morningStatus = 1
                            atts.lateTotal = atts.lateTotal + 1
                            atts.morningDailyStatus = 'late'
                            atts.morningTimeIn = datetime.now()
                            # atts.morningRemark = wala pa nabutang
                            print 'bbbbbbbbbbbb' 
                            dbase.session.commit()
                            return jsonify({'message': 'late'})
                        else:
                            return jsonify({'message':'you cannot time in twice'})
                    elif atts.morningStatus == 1 and atts.afterStatus == 0:
                        if atts.morningTimeOut is None:
                            atts.morningStatus = 0
                            atts.morningTimeOut = datetime.now()
                            # atts.morningRemark = wala pa nabutang
                            print 'cccccccccccc'
                            dbase.session.commit()
                            return jsonify({'message': 'time out'})
                        else:
                            return jsonify({'message':'you cannot time in twice'})
                    elif atts.morningStatus == 0 and atts.afterStatus == 1:
                        if atts.morningTimeOut is None:
                            atts.afterStatus = 0
                            atts.morningStatus = 1
                            atts.afterTimeOut = datetime.now()
                            atts.morningTimeIn = datetime.now()
                            atts.morningDailyStatus = 'late'
                            # atts.morningRemark = wala pa nabutang
                            dbase.session.commit()
                            return jsonify({'message':'late, kindly dont forget to timeout in morning'})
                        else:
                            return jsonify({'message':'you cannot time in twice'})
                    elif atts.morningStatus == 1 and atts.afterStatus == 1:
                        if atts.morningTimeOut is None:  
                            atts.afterStatus = 0
                            atts.morningStatus = 0
                            atts.afterTimeOut = datetime.now()
                            atts.morningTimeOut = datetime.now()
                            dbase.session.commit()
                            return jsonify({'message':'time out'})
                        else:
                            return jsonify({'message':'you cannot time in twice'})
                elif now > m12 and now <= a1: # 12 -7pm
                    if atts.morningStatus == 0 and atts.afterStatus == 0:
                        if atts.afterTimeOut is None:
                            atts.afterStatus = 1
                            atts.afterDailyStatus = 'not late'
                            atts.afterTimeIn = datetime.now()
                            # atts.morningRemark = wala pa nabutang
                            print 'ddddddddddddd' 
                            dbase.session.commit()
                            return jsonify({'message': 'time in for afternoon'})
                        else:
                            return jsonify({'message':'you cannot time in twice'})
                    elif atts.morningStatus == 1 and atts.afterStatus == 0:
                        if atts.afterTimeOut is None:
                            atts.morningStatus = 0
                            atts.morningTimeOut = datetime.now()
                            # atts.morningRemark = wala pa nabutang
                            print 'eeeeeeeeeeeeeeee'
                            dbase.session.commit()
                            return jsonify({'message': 'time out for morning'})
                        else:
                            return jsonify({'message':'you cannot time in twice'})
                    elif atts.morningStatus == 0 and atts.afterStatus == 1:
                        return jsonify({'message':'no time out for afternoon at this time'})
                    elif atts.morningStatus == 1 and atts.afterStatus == 1:
                        atts.morningStatus = 0
                        atts.morningTimeOut = datetime.now()
                        dbase.session.commit()
                        return jsonify({'message':'no time out for afternoon at this time'})
                elif now > a1 and now <= a6:
                    if atts.morningStatus == 0 and atts.afterStatus == 0:
                        if atts.afterTimeOut is None:
                            atts.afterStatus = 1
                            atts.lateTotal = atts.lateTotal + 1
                            atts.afterDailyStatus = 'late'
                            atts.afterTimeIn = datetime.now()
                            # atts.morningRemark = wala pa nabutang
                            print 'fffffffffffff' 
                            dbase.session.commit()
                            return jsonify({'message': 'late'})
                        else:
                            return jsonify({'message':'you cannot time in twice'})
                    elif atts.morningStatus == 1 and atts.afterStatus == 0:
                        if atts.afterTimeOut is None:
                            atts.morningStatus = 0
                            atts.afterStatus = 1
                            atts.morningTimeOut = datetime.now()
                            atts.lateTotal = atts.lateTotal + 1
                            atts.afterDailyStatus = 'late'
                            atts.afterTimeIn = datetime.now()
                            # atts.morningRemark = wala pa nabutang
                            print 'ggggggggggggg'
                            dbase.session.commit()
                            return jsonify({'message': 'time out'})
                        else:
                            return jsonify({'message':'you cannot time in twice'})
                    elif atts.morningStatus == 0 and atts.afterStatus == 1:
                        atts.afterStatus = 0
                        atts.afterTimeOut = datetime.now()
                        dbase.session.commit()
                        return jsonify({'message':'time out'})
                    elif atts.morningStatus == 1 and atts.afterStatus == 1:
                        atts.afterStatus = 0
                        atts.morningStatus = 0
                        atts.afterTimeOut = datetime.now()
                        atts.morningTimeOut = datetime.now()
                        dbase.session.commit()
                        return jsonify({'message':'time out'})
                elif now > a6 and now <= a7:
                    if atts.morningStatus == 0 and atts.afterStatus == 0:
                        return jsonify({'message':'no time in for this time'})

                    elif atts.morningStatus == 1 and atts.afterStatus == 0:
                        atts.morningStatus = 0
                        atts.morningTimeOut = datetime.now()
                        dbase.session.commit()
                        return jsonify({'message':'not time in for afternoon'})

                    elif atts.morningStatus == 0 and atts.afterStatus == 1:
                        atts.afterStatus = 0
                        atts.afterTimeOut = datetime.now()
                        dbase.session.commit()
                        return jsonify({'message':'time out for afternoon'})
                    elif atts.morningStatus == 1 and atts.afterStatus == 1:
                        atts.morningStatus = 0
                        atts.afterStatus = 0
                        atts.morningTimeOut = datetime.now()
                        atts.afterTimeOut = datetime.now()
                        dbase.session.commit()
                        return jsonify({'message':'time out for afternoon and morning'})
                else:
                    print datenow
                    return jsonify({'message':'OT napud siya'})
def absents():
    datenow1 = datetime.now().strftime("%m%d%Y")
    employs = Employee.query.filter_by(employeestatus = 1).all()
    employees = []
    for i in employs:
        employees.append(i.employeeid)
    # print employees[0]
    # print employees
    present = Attendance.query.filter(and_(Attendance.date == datenow1, Attendance.absentTotal == 0)).all()
    presents = []
    if present:
        for e in present:
            presents.append(e.employeeid)
        # print 'hjkbnmbnmhj'
        # print presents[0]
        # print 'hhhhhhhhhhhhhhhhhh'
        absent = []

        for i in employees:
            # print "this" + str(i)
            for j in presents:
                if i == j:
                    pass
                else:
                    absent.append(i)

        for i in absent:

            absent =  Attendance(employeeid = i)
            # absentstat = Attendance.query.filter(and_(absent.employeeid == None ,  )
            dbase.session.add(absent)
            dbase.session.commit()
            absent.absentTotal = absent.absentTotal + 1
            absent.date = datenow1
            dbase.session.commit()
        else:
            pass  

