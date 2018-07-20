from api import app, dbase, generate_password_hash, cross_origin, CORS, check_password_hash
from flask import request, jsonify
from models import *
# newly added
from flask_login import login_user, login_required, LoginManager, logout_user
import datetime as dt
import time
#pip install timedate, time
from sqlalchemy import and_, desc, extract
import png
import pyqrcode
from datetime import date, datetime, time
import os, string

lgdate = datetime.now()
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
  return Admin.query.get(int(user_id))

@app.route('/', methods=['GET'])
def admin_create():
  admin_password = 'admin'
  admin = Admin(username='admin', password=admin_password)
  dbase.session.add(admin)
  dbase.session.commit()
 
@app.route('/login', methods=['GET', 'POST'])
@cross_origin(allow_headers=['Content-Type'])
def login():
  data = request.get_json()
  code = str(data['password'])
  user = Admin.query.filter_by(username=data['username']).first()
  if user is None:
    return jsonify({'message': 'Invalid username or password'})
  else:
    if check_password_hash(user.password, code):
      login_user(user, remember=True)
      print(login_user(user, remember=True))
      msg = "Logged in"
      logmessage = Logs(details = msg,log_date = lgdate)
      dbase.session.add(logmessage)
      dbase.session.commit()
      return jsonify({'message': 'Login Successful!'})
  return jsonify({'message': 'invalid password'})


@app.route('/logout', methods=['GET'])
@cross_origin(allow_headers=['Content-Type'])
# @login_required
def logout():
  
  msg = "Logged out"
  logmessage = Logs(details = msg,log_date = lgdate)
  dbase.session.add(logmessage)
  dbase.session.commit()
  logout_user()
  return jsonify({'message': 'Logged out'})


@app.route('/newAdmin', methods=['POST'])
@cross_origin(allow_headers=['Content-Type'])
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
        msg = "username or password updated"
        logmessage = Logs(details = msg,log_date = lgdate)
        dbase.session.add(logmessage)
        dbase.session.commit()
        return jsonify({'message': 'successfull!'})
    except:
        return jsonify({'message': 'edit failed'})


@app.route('/newEmployee', methods=['POST'])
# @login_required
@cross_origin(allow_headers=['Content-Type'])
def addemployee():
    data = request.get_json()
    now = datetime.now().strftime("%m%d%Y%H%M")
    # birth_date = Strip the time!!!!!!!!
    # birthdate = datetime.datetime.strptime(data['birth_date'], '%Y-%M-%d')
    new_employee = Employee(fname=data['fname'], mname=data['mname'], lname=data['lname'], position=data['position'],
                            code=data['code'], contact=data['contact'], email=data['email'],
                            birth_date=data['birth_date'],  gender=data['gender'], address=data['address'], employeestatus=1)
    
    #search for employee using QRCODE
    employee = Employee.query.filter_by(code=data['code']).first()
    if employee is None:
        print now
        dbase.session.add(new_employee)
        dbase.session.commit()
        msg = data['code'] + " employee added"
        logmessage = Logs(details = msg,log_date = lgdate)
        dbase.session.add(logmessage)
        dbase.session.commit()
        return jsonify({'message': 'New employee created!'})

    else:
        return jsonify({'message': 'Employee already created'})

@app.route('/view/', methods=['GET'])
# @login_required
@cross_origin('*')
def viewEmployee():
    employess = Employee.query.filter_by(employeestatus=1).all()

    data = []
    if employess:
        for i in employess:
          data1 = {}
          data1['fname'] = i.fname
          data1['mname'] = i.mname
          data1['lname'] = i.lname
          data1['position'] = i.position
          data1['code'] = i.code
          data1['employeeid'] = i.employeeid
          data1['contact'] = i.contact
          data1['email'] = i.email
          data1['birth_date'] = str(i.birth_date)
          data1['gender'] = i.gender
          data1['address'] = i.address
          data.append(data1)
        return jsonify({'users':data})
    else:
        return jsonify({'message': 'no employee found'})

@app.route('/viewDeactivated/', methods=['GET', 'POST'])
# @login_required
@cross_origin('*')
def viewEmployeeDeactivated():
    employess = Employee.query.filter_by(employeestatus=0).all()

    data = []
    if employess:
        for i in employess:
            data1 = {}
            data1['fname'] = i.fname
            data1['mname'] = i.mname
            data1['lname'] = i.lname
            data1['position'] = i.position
            data1['code'] = i.code
            data1['employeeid'] = i.employeeid
            data1['contact'] = i.contact
            data1['email'] = i.email
            data1['birth_date'] = str(i.birth_date)
            data1['gender'] = i.gender
            data1['address'] = i.address
            data.append(data1)
        return jsonify({'users':data})
    else:
        return jsonify({'message': 'no employee found'})


@app.route('/search/', methods =['GET', 'POST'])
# @login_required
@cross_origin('*')
def searchEmployee():
    data = request.get_json()
    employee1 = data['lname']
    notactive = []
    activate =  Employee.query.filter(and_(Employee.lname == employee1 , Employee.employeestatus == 0)).all()

    if activate is None:
        return jsonify({'message':'not found'})
    else:    
        
        for i in activate:
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
            notactive.append(data)
        return jsonify({'message': notactive})        


@app.route('/generate/qrcode', methods=['POST'])
@cross_origin('*')
# @login_required
def genereate_code():
    data = request.get_json()
    qr = pyqrcode.create(data['code'])
    qr.png('code.png', scale=6)
    msg = "generate new code: " + data['code']
    logmessage = Logs(details = msg,log_date = lgdate)
    dbase.session.add(logmessage)
    dbase.session.commit()
    return jsonify({'message': 'QR Code Generated!'})


@app.route('/deactivate', methods=['GET', 'POST'])
@cross_origin('*')
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
      msg = data['code'] + " deactivated"
      logmessage = Logs(details = msg,log_date = lgdate)
      dbase.session.add(logmessage)
      dbase.session.commit()
      return jsonify({'message': 'Employee deactivated'})
    else:
    	return jsonify({'message': 'Employee is not found'})

@app.route('/activate', methods=['GET', 'POST'])
@cross_origin('*')
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
        msg = data['code'] + " activated"
        logmessage = Logs(details = msg,log_date = lgdate)
        dbase.session.add(logmessage)
        dbase.session.commit()
        return jsonify({'message': 'Employee Activated'})
    else:
        return jsonify({'message': 'Employee is not found'})


@app.route('/edit/<string:user_id>', methods=['POST'])
@cross_origin(allow_headers=['Content-Type'])
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
            msg = user_id + " updated"
            logmessage = Logs(details = msg,log_date = lgdate)
            dbase.session.add(logmessage)
            dbase.session.commit()
            return jsonify({'message': 'Success!'})
        except:
            return jsonify({'message': 'edit failed'})


@app.route('/company_summary/monthly/<string:dates>', methods=['GET'])
@cross_origin("*")
# @login_required
def company_month(dates):
   dates = datetime.strptime(dates, "%Y-%m-%d")
   summary = Attendance.query.filter(extract('year', Attendance.date) == (dates.strftime("%Y")))\
       .filter(extract('month', Attendance.date) == (dates.strftime("%m"))).all()
   employees = []
   for employee in summary:
       employee_data = {}
       name = Employee.query.filter_by(employeeid=employee.employeeid).first()
       overtimee = Overtime.query.filter_by(employeeid=employee.employeeid).order_by(Overtime.overtimeDate.desc()).first()
       employee_data['name'] = name.fname + " " + name.mname + " " + name.lname
       if overtimee is None:
            employee_data['overtimeTotal'] = 0
       else:
            employee_data['overtimeTotal'] = overtimee.overTimeTotal
       employee_data['employeeid'] = employee.employeeid
       employee_data['lateTotal'] = employee.lateTotal
       employee_data['absentTotal'] = employee.absentTotal
       employee_data['morningTimeIn'] = str(employee.morningTimeIn)
       employee_data['morningTimeOut'] = str(employee.morningTimeOut)
       employee_data['afterTimeIn'] = str(employee.afterTimeIn)
       employee_data['afterTimeOut'] = str(employee.afterTimeOut)
       employee_data['morningStatus'] = employee.morningStatus
       employee_data['afterStatus'] = employee.afterStatus
       employee_data['morningDailyStatus'] = employee.morningDailyStatus
       employee_data['afterDailyStatus'] = employee.afterDailyStatus
       employee_data['morningRemark'] = employee.morningRemark
       employee_data['afterRemark'] = employee.afterRemark
       employees.append(employee_data)
   return jsonify({'Employee': employees})


@app.route('/company_summary/weekly/<string:sort_date>', methods=['GET'])
@cross_origin("*")
# @login_required
def company_week(sort_date):
   dates = string.replace(sort_date,"W","")
   print dates
   year, week_number = dates.split("-")
   print year
   print week_number
   summary = Attendance.query.filter(Attendance.week_number == week_number).filter(extract('year', Attendance.date) == year).order_by(Attendance.week_number.desc()).all()
   employees = []
   if summary is None:
       return jsonify({"message": "No data to show"})
   for employee in summary:
       employee_data = {}
       name = Employee.query.filter_by(employeeid=employee.employeeid).first()
       overtimee = Overtime.query.filter_by(employeeid=employee.employeeid).order_by(Overtime.overtimeDate.desc()).first()
       employee_data['name'] = name.fname + " " + name.mname + " " + name.lname
       if overtimee is None:
            employee_data['overtimeTotal'] = 0
       else:
            employee_data['overtimeTotal'] = overtimee.overTimeTotal
       employee_data['employeeid'] = employee.employeeid
       employee_data['lateTotal'] = employee.lateTotal
       employee_data['absentTotal'] = employee.absentTotal
       employee_data['morningTimeIn'] = str(employee.morningTimeIn)
       employee_data['morningTimeOut'] = str(employee.morningTimeOut)
       employee_data['afterTimeIn'] = str(employee.afterTimeIn)
       employee_data['afterTimeOut'] = str(employee.afterTimeOut)
       employee_data['morningStatus'] = employee.morningStatus
       employee_data['afterStatus'] = employee.afterStatus
       employee_data['morningDailyStatus'] = employee.morningDailyStatus
       employee_data['afterDailyStatus'] = employee.afterDailyStatus
       employee_data['morningRemark'] = employee.morningRemark
       employee_data['afterRemark'] = employee.afterRemark
       employees.append(employee_data)
   return jsonify({'Employee': employees})

@app.route('/employee_summary/monthly/<int:emp_id>', methods=['GET'])
@cross_origin("*")
# @login_required
def employee_monthly(emp_id):
   summary = Attendance.query.filter(Attendance.employeeid == emp_id).order_by(Attendance.date.desc()).all()
   employees = []
   for employee in summary:
       employee_data = {}
       name = Employee.query.filter_by(employeeid=employee.employeeid).first()
       overtimee = Overtime.query.filter_by(employeeid=employee.employeeid).order_by(Overtime.overtimeDate.desc()).first()
       employee_data['name'] = name.fname + " " + name.mname + " " + name.lname
       if overtimee is None:
            employee_data['overtimeTotal'] = 0
       else:
            employee_data['overtimeTotal'] = overtimee.overTimeTotal
       employee_data['employeeid'] = employee.employeeid
       employee_data['lateTotal'] = employee.lateTotal
       employee_data['absentTotal'] = employee.absentTotal
       employee_data['morningTimeIn'] = str(employee.morningTimeIn)
       employee_data['morningTimeOut'] = str(employee.morningTimeOut)
       employee_data['afterTimeIn'] = str(employee.afterTimeIn)
       employee_data['afterTimeOut'] = str(employee.afterTimeOut)
       employee_data['morningStatus'] = employee.morningStatus
       employee_data['afterStatus'] = employee.afterStatus
       employee_data['morningDailyStatus'] = employee.morningDailyStatus
       employee_data['afterDailyStatus'] = employee.afterDailyStatus
       employee_data['morningRemark'] = employee.morningRemark
       employee_data['afterRemark'] = employee.afterRemark
       employees.append(employee_data)
   return jsonify({'employee': employees})


@app.route('/employee_summary/weekly/<string:dates>/<int:emp_id>', methods=['GET'])
@cross_origin("*")
# @login_required
def employee_week(dates, emp_id):
   dates = string.replace(dates,"W","")
   print dates
   year, week_number = dates.split("-")
   print year
   print week_number
   summary = Attendance.query.filter(Attendance.employeeid == emp_id).filter(Attendance.week_number == week_number).filter(extract('year', Attendance.date) == year).order_by(Attendance.week_number.desc()).all()
   employees = []
   if summary is None:
       return jsonify({"message": "No data to show"})
   for employee in summary:
       employee_data = {}
       name = Employee.query.filter_by(employeeid=employee.employeeid).first()
       overtimee = Overtime.query.filter_by(employeeid=employee.employeeid).order_by(Overtime.overtimeDate.desc()).first()
       employee_data['name'] = name.fname + " " + name.mname + " " + name.lname
       if overtimee is None:
            employee_data['overtimeTotal'] = 0
       else:
            employee_data['overtimeTotal'] = overtimee.overTimeTotal
       employee_data['employeeid'] = employee.employeeid
       employee_data['lateTotal'] = employee.lateTotal
       employee_data['absentTotal'] = employee.absentTotal
       employee_data['morningTimeIn'] = str(employee.morningTimeIn)
       employee_data['morningTimeOut'] = str(employee.morningTimeOut)
       employee_data['afterTimeIn'] = str(employee.afterTimeIn)
       employee_data['afterTimeOut'] = str(employee.afterTimeOut)
       employee_data['morningStatus'] = employee.morningStatus
       employee_data['afterStatus'] = employee.afterStatus
       employee_data['morningDailyStatus'] = employee.morningDailyStatus
       employee_data['afterDailyStatus'] = employee.afterDailyStatus
       employee_data['morningRemark'] = employee.morningRemark
       employee_data['afterRemark'] = employee.afterRemark
       employees.append(employee_data)
   return jsonify({'employee': employees})


@app.route('/edit/login-time', methods=['POST'])
@cross_origin(allow_headers=['Content-Type'])
# @login_required
def edit_time():
   data = request.get_json()
   
   morning1 = dt.datetime.strptime(data['morning_time_in_start'], "%H:%M")
   morning2 = dt.datetime.strptime(data['morning_time_out_start'], "%H:%M")
   morning3 = dt.datetime.strptime(data['morning_time_out_end'], "%H:%M")
   after1 = dt.datetime.strptime(data['afternoon_time_in_start'], "%H:%M")
   after2 = dt.datetime.strptime(data['afternoon_time_out_start'], "%H:%M")
   after3 = dt.datetime.strptime(data['afternoon_time_out_end'], "%H:%M")
   new_time = Admin.query.filter_by(id=1).first()
   if new_time is None:
       return jsonify({'Message': 'Edit failed'})
   else:
       try:
           # new morning log time
           # morning time in start
           if morning1 == '':
               new_time.morning_time_in_start = new_time.morning_time_in_start
           else:
               new_time.morning_time_in_start = morning1
           # morning time out start
           if morning2 == '':
               new_time.morning_time_out_start = new_time.morning_time_out_start
           else:
               new_time.morning_time_out_start = morning2
           # morning time out end
           if morning3 == '':
               new_time.morning_time_out_end = new_time.morning_time_out_end
           else:
               new_time.morning_time_out_end = morning3
           # new afternoon log time
           # afternoon time in start
           if after1 == '':
               new_time.afternoon_time_in_start = new_time.afternoon_time_in_start
           else:
               new_time.afternoon_time_in_start = after1
           # afternoon time out start
           if after2 == '':
               new_time.afternoon_time_out_start = new_time.afternoon_time_out_start
           else:
               new_time.afternoon_time_out_start = after2
           # afternoon time out end
           if after3 == '':
               new_time.afternoon_time_out_end = new_time.afternoon_time_out_end
           else:
               new_time.afternoon_time_out_end = after3
           dbase.session.commit()
           msg = "timein or timeout edited"
           logmessage = Logs(details = msg,log_date = lgdate)
           dbase.session.add(logmessage)
           dbase.session.commit()
           return jsonify({'message': 'Success!'})
       except:
           return jsonify({'message': 'failed'})
 

@app.route('/TimeIn/', methods=['POST'])
def timein():
    now = datetime.now().strftime("%m%d%Y%H%M")
    datenow1 = datetime.now().strftime("%m%d%Y")
    datenow = datetime.strptime(str(datenow1), "%m%d%Y")
    week_no = datetime.strptime(str(datenow1), "%m%d%Y").isocalendar()[1]
    timeAdmin = Admin.query.get(1)

    morning7 = timeAdmin.morning_time_in_start.strftime("%H%M")
    morning9 = timeAdmin.morning_time_out_start.strftime("%H%M")
    morning12 = timeAdmin.morning_time_out_end.strftime("%H%M")

    afte1 = timeAdmin.afternoon_time_in_start.strftime("%H%M")
    afte6 = timeAdmin.afternoon_time_out_start.strftime("%H%M")
    afte7 = timeAdmin.afternoon_time_out_end.strftime("%H%M")

    m7 = ''.join([datenow1, morning7])
    m9 = ''.join([datenow1, morning9])
    m12 = ''.join([datenow1, morning12])

    a1 = ''.join([datenow1, afte1])
    a6 = ''.join([datenow1, afte6])
    a7 = ''.join([datenow1, afte7])

    # 1 for active and 0 for inactive
    data = request.get_json()
    employee = Employee.query.filter_by(code=data['code']).first()
    empID = employee.employeeid
    attendancenNew = Attendance(employeeid=empID)

    if employee is None:
        return jsonify({'message': 'user not found'})
    else:

        atts = Attendance.query.filter(and_(Attendance.employeeid == empID, Attendance.date ==str(datenow))).order_by(Attendance.date.desc()).first()
        
        # ////////////////////////////IF ID IS NOT LISTED IN THE ATTENDACE CRETAE NEW///////////////////////////////#
        if atts is None:

            dbase.session.add(attendancenNew)
            dbase.session.commit()

            atts = Attendance.query.filter_by(employeeid=empID).order_by(Attendance.date.desc()).first()
            print atts
            print '1st'
            atts.date = datenow
            atts.week_number = week_no
            dbase.session.commit()
            dates = Attendance.query.filter_by(date=datenow).first()
            if dates:
                print '444546456646546465465465464654654654654'

            else:
                dbase.session.add(attendancenNew)
                dbase.session.commit()
                print '0987654321=-098765'

            # nowdate = atts.date
            if (now >= m7) and (now <= m9):
                if atts.morningStatus == 0 and atts.afterStatus == 0:
                    if atts.morningTimeOut is None:
                        atts.morningStatus = 1
                        atts.morningTimeIn = datetime.now()
                        atts.morningDailyStatus = 'not late'
                        print "aaaaaaa"
                        dbase.session.commit()
                        return jsonify({'message': 'not late'})
                    else:
                        print 'bbbbbbbbbbbbbbbbbbbbbbb'
                        return jsonify({'message': 'you cannot time in twice'})
                elif atts.morningStatus == 1 and atts.afterStatus == 0:
                    print 'ccccccccc'
                    return jsonify({'message': 'no time out at this time'})
                elif atts.morningStatus == 0 and atts.afterStatus == 1:
                    if atts.morningTimeOut is None:
                        atts.afterStatus = 0
                        atts.morningStatus = 1
                        atts.afterTimeOut = datetime.now()
                        atts.morningTimeIn = datetime.now()
                        atts.morningDailyStatus = 'not late'
                        dbase.session.commit()
                        print'ddddddddddddd'
                        return jsonify({'message': 'not late, kindly dont forget to timeout in morning'})
                    else:
                        print'eeeeeeeeeeeeeee'
                        return jsonify({'message': 'you cannot time in twice'})
                elif atts.morningStatus == 1 and atts.afterStatus == 1:
                    atts.afterStatus = 0
                    atts.afterTimeOut = datetime.now()
                    dbase.session.commit()
                    print'fffffffffffff'
                    return jsonify({'message': 'no time out at this time'})

            elif (now > m9) and (now <= m12):
                if atts.morningStatus == 0 and atts.afterStatus == 0:
                    if atts.morningTimeOut is None:
                        atts.morningStatus = 1
                        atts.lateTotal = atts.lateTotal + 1
                        atts.morningDailyStatus = 'late'
                        atts.morningTimeIn = datetime.now()
                        # atts.morningRemark = wala pa nabutang
                        print 'ggggggggggg'
                        dbase.session.commit()
                        return jsonify({'message': 'late'})
                    else:
                        print'hhhhhhhhhhhhhhhhhh'
                        return jsonify({'message': 'you cannot time in twice'})
                elif atts.morningStatus == 1 and atts.afterStatus == 0:
                    if atts.morningTimeOut is None:
                        atts.morningStatus = 0
                        atts.morningTimeOut = datetime.now()
                        # atts.morningRemark = wala pa nabutang
                        print 'iiiiiiiiiiii'
                        dbase.session.commit()
                        return jsonify({'message': 'time out'})
                    else:
                        print'jjjjjjjjjjjjjj'
                        return jsonify({'message': 'you cannot time in twice'})
                elif atts.morningStatus == 0 and atts.afterStatus == 1:
                    if atts.morningTimeOut is None:
                        atts.afterStatus = 0
                        atts.morningStatus = 1
                        atts.afterTimeOut = datetime.now()
                        atts.morningTimeIn = datetime.now()
                        atts.morningDailyStatus = 'late'
                        # atts.morningRemark = wala pa nabutang
                        print 'kkkkkkkkkkkkk'
                        dbase.session.commit()
                        return jsonify({'message': 'late, kindly dont forget to timeout in morning'})
                    else:
                        print'lllllllllllllllll'
                        return jsonify({'message': 'you cannot time in twice'})
                elif atts.morningStatus == 1 and atts.afterStatus == 1:
                    if atts.morningTimeOut is None:
                        atts.afterStatus = 0
                        atts.morningStatus = 0
                        atts.afterTimeOut = datetime.now()
                        atts.morningTimeOut = datetime.now()
                        print 'mmmmmmmmmmmmmmm'
                        dbase.session.commit()
                        return jsonify({'message': 'time out'})
                    else:
                        print'nnnnnnnnnnnnnn'
                        return jsonify({'message': 'you cannot time in twice'})
            elif (now > m12) and (now <= a1):  # 12 -7pm
                if atts.morningStatus == 0 and atts.afterStatus == 0:
                    if atts.afterTimeOut is None:
                        atts.afterStatus = 1
                        atts.afterDailyStatus = 'not late'
                        atts.afterTimeIn = datetime.now()
                        # atts.morningRemark = wala pa nabutang
                        print 'ooooooooooo'
                        dbase.session.commit()
                        print'ppppppppppppppp'
                        return jsonify({'message': 'time in for afternoon'})
                    else:
                        print'qqqqqqqqqqqqqq'
                        return jsonify({'message': 'you cannot time in twice'})
                elif atts.morningStatus == 1 and atts.afterStatus == 0:
                    if atts.afterTimeOut is None:
                        atts.morningStatus = 0
                        atts.morningTimeOut = datetime.now()
                        # atts.morningRemark = wala pa nabutang
                        print 'rrrrrrrrrrrrrrrr'
                        dbase.session.commit()
                        return jsonify({'message': 'time out for morning'})
                    else:
                        print'ssssssssssssssss'
                        return jsonify({'message': 'you cannot time in twice'})
                elif atts.morningStatus == 0 and atts.afterStatus == 1:
                    print'tttttttttttttttttt'
                    return jsonify({'message': 'no time out for afternoon at this time'})
                elif atts.morningStatus == 1 and atts.afterStatus == 1:
                    atts.morningStatus = 0
                    atts.morningTimeOut = datetime.now()
                    dbase.session.commit()
                    print'uuuuuuuuuuuuuuuuuuuu'
                    return jsonify({'message': 'no time out for afternoon at this time'})
            elif (now > a1) and (now <= a6):
                if atts.morningStatus == 0 and atts.afterStatus == 0:
                    if atts.afterTimeOut is None:
                        atts.afterStatus = 1
                        atts.lateTotal = atts.lateTotal + 1
                        atts.afterDailyStatus = 'late'
                        atts.afterTimeIn = datetime.now()
                        # atts.morningRemark = wala pa nabutang
                        dbase.session.commit()
                        print'vvvvvvvvvvvvvvvvvv'
                        return jsonify({'message': 'late'})
                    else:
                        print'wwwwwwwwwwwwwwwwww'
                        return jsonify({'message': 'you cannot time in twice'})
                elif atts.morningStatus == 1 and atts.afterStatus == 0:
                    if atts.afterTimeOut is None:
                        atts.morningStatus = 0
                        atts.afterStatus = 1
                        atts.morningTimeOut = datetime.now()
                        atts.lateTotal = atts.lateTotal + 1
                        atts.afterDailyStatus = 'late'
                        atts.afterTimeIn = datetime.now()
                        # atts.morningRemark = wala pa nabutang
                        print'xxxxxxxxxxxxxxxxxxxxxx'
                        return jsonify({'message': 'time out'})
                    else:
                        print'yyyyyyyyyyyyyyyyy'
                        return jsonify({'message': 'you cannot time in twice'})
                elif atts.morningStatus == 0 and atts.afterStatus == 1:
                    atts.afterStatus = 0
                    atts.afterTimeOut = datetime.now()
                    dbase.session.commit()
                    print'zzzzzzzzzzzzzzzzzzzzzz'
                    return jsonify({'message': 'time out'})
                elif atts.morningStatus == 1 and atts.afterStatus == 1:
                    atts.afterStatus = 0
                    atts.morningStatus = 0
                    atts.afterTimeOut = datetime.now()
                    atts.morningTimeOut = datetime.now()
                    dbase.session.commit()
                    print'1111111111111'
                    return jsonify({'message': 'time out'})
            elif (now > a6) and (now <= a7):
                if atts.morningStatus == 0 and atts.afterStatus == 0:
                    print'2222222222222222222'
                    absents()
                    dbase.session.commit()
                    return jsonify({'message': 'no time in for this time'})

                elif atts.morningStatus == 1 and atts.afterStatus == 0:
                    atts.morningStatus = 0
                    atts.morningTimeOut = datetime.now()
                    absents()
                    dbase.session.commit()
                    print'3333333333333333333'
                    return jsonify({'message': 'not time in for afternoon'})

                elif atts.morningStatus == 0 and atts.afterStatus == 1:
                    atts.afterStatus = 0
                    atts.afterTimeOut = datetime.now()
                    absents()
                    dbase.session.commit()
                    print'4444444444444444'
                    return jsonify({'message': 'time out for afternoon'})
                elif atts.morningStatus == 1 and atts.afterStatus == 1:
                    atts.morningStatus = 0
                    atts.afterStatus = 0
                    atts.morningTimeOut = datetime.now()
                    atts.afterTimeOut = datetime.now()
                    absents()
                    dbase.session.commit()
                    print'555555555555555555555'
                    return jsonify({'message': 'time out for afternoon and morning'})
            else:
                pass
# ////////// ///////////////////////////////IF ID IS EXISTING/////////////////////////////////////////////////////////
        elif atts:
            dates = Attendance.query.filter_by(date=datenow).order_by(Attendance.date.desc()).first()
            print dates
            atts = Attendance.query.filter(and_(Attendance.employeeid == empID, Attendance.date == datenow)).order_by(
                Attendance.date.desc()).first()
            # dbase.session.commit()
            # date1 = atts.date
            print "second"
            dates = Attendance.query.filter_by(date=datenow).first()
            if dates:
                pass
            else:
                dbase.session.add(attendancenNew)
                dbase.session.commit()
                atts.date = datenow
                print atts.date + 'jfjfjfjfjfjfjfhfnr nvjfnfnhmfn'
                dbase.session.commit()

                print '1234567890-'
                print datenow + "mkmkmkkmkkkmkmkmkkkmkmkmk"
                atts = Attendance.query.filter(
                    and_(Attendance.employeeid == empID, Attendance.date == datenow)).order_by(
                    Attendance.date.desc()).first()
        # ///////////////////////////////////////////CHECK IF THE DATE IS SAME//////////////////////////////////////
            if atts.date == datenow:

                # ////////////////////////IF DATE IS SAME////////////////////////////#
                print atts.date + 'nabuang siya'
                if now >= m7 and now <= m9:
                    if atts.morningStatus == 0 and atts.afterStatus == 0:
                        if atts.morningTimeOut is None:
                            atts.morningStatus = 1
                            atts.morningTimeIn = datetime.now()
                            atts.morningDailyStatus = 'not late'
                            print "AAAAAAAAAAAAAAAA"
                            dbase.session.commit()
                            return jsonify({'message': 'not late'})
                        else:
                            print'BBBBBBBBBBBBBBBBBBBBB'
                            return jsonify({'message': 'you cannot time in twice'})
                    elif atts.morningStatus == 1 and atts.afterStatus == 0:
                        print 'CCCCCCCCCCCCCCCC'
                        return jsonify({'message': 'no time out at this time'})
                    elif atts.morningStatus == 0 and atts.afterStatus == 1:
                        if atts.morningTimeOut is None:
                            atts.afterStatus = 0
                            atts.morningStatus = 1
                            atts.afterTimeOut = datetime.now()
                            atts.morningTimeIn = datetime.now()
                            atts.morningDailyStatus = 'not late'
                            dbase.session.commit()
                            print'DDDDDDDDDDDDDDDDDD'
                            return jsonify({'message': 'not late, kindly dont forget to timeout in morning'})
                        else:
                            print'EEEEEEEEEEEEEEEEEE'
                            return jsonify({'message': 'you cannot time in twice'})
                    elif atts.morningStatus == 1 and atts.afterStatus == 1:
                        atts.afterStatus = 0
                        atts.afterTimeOut = datetime.now()
                        dbase.session.commit()
                        print'FFFFFFFFFFFFFFFF'
                        return jsonify({'message': 'no time out at this time'})

                elif now > m9 and now <= m12:
                    if atts.morningStatus == 0 and atts.afterStatus == 0:
                        if atts.morningTimeOut is None:
                            atts.morningStatus = 1
                            atts.lateTotal = atts.lateTotal + 1
                            atts.morningDailyStatus = 'late'
                            atts.morningTimeIn = datetime.now()
                            # atts.morningRemark = wala pa nabutang
                            print 'GGGGGGGGGGGGGGGGGGGGGGGGG'
                            dbase.session.commit()
                            return jsonify({'message': 'late'})
                        else:
                            print'HHHHHHHHHHHHHHHHHHHHHHHHHHH'
                            return jsonify({'message': 'you cannot time in twice'})
                    elif atts.morningStatus == 1 and atts.afterStatus == 0:
                        if atts.morningTimeOut is None:
                            atts.morningStatus = 0
                            atts.morningTimeOut = datetime.now()
                            # atts.morningRemark = wala pa nabutang
                            print 'IIIIIIIIIIIIIIIIII'
                            dbase.session.commit()
                            return jsonify({'message': 'time out'})
                        else:
                            print'JJJJJJJJJJJJJJJ'
                            return jsonify({'message': 'you cannot time in twice'})
                    elif atts.morningStatus == 0 and atts.afterStatus == 1:
                        if atts.morningTimeOut is None:
                            atts.afterStatus = 0
                            atts.morningStatus = 1
                            atts.afterTimeOut = datetime.now()
                            atts.morningTimeIn = datetime.now()
                            atts.morningDailyStatus = 'late'
                            # atts.morningRemark = wala pa nabutang
                            print'KKKKKKKKKKKK'
                            dbase.session.commit()
                            return jsonify({'message': 'late, kindly dont forget to timeout in morning'})
                        else:
                            print'LLLLLLLLLLLLLLLLLL'
                            return jsonify({'message': 'you cannot time in twice'})
                    elif atts.morningStatus == 1 and atts.afterStatus == 1:
                        if atts.morningTimeOut is None:
                            atts.afterStatus = 0
                            atts.morningStatus = 0
                            atts.afterTimeOut = datetime.now()
                            atts.morningTimeOut = datetime.now()
                            dbase.session.commit()
                            print'MMMMMMMMMMMMMMMMMM'
                            return jsonify({'message': 'time out'})
                        else:
                            print'NNNNNNNNNNNNNN'
                            return jsonify({'message': 'you cannot time in twice'})
                elif now > m12 and now <= a1:  # 12 -7pm
                    if atts.morningStatus == 0 and atts.afterStatus == 0:
                        if atts.afterTimeOut is None:
                            atts.afterStatus = 1
                            atts.afterDailyStatus = 'not late'
                            atts.afterTimeIn = datetime.now()
                            # atts.morningRemark = wala pa nabutang
                            print 'OOOOOOOOOOOOOOOOOO'
                            dbase.session.commit()
                            return jsonify({'message': 'time in for afternoon'})
                        else:
                            print'PPPPPPPPPPPPPPPPPPPPPPP'
                            return jsonify({'message': 'you cannot time in twice'})
                    elif atts.morningStatus == 1 and atts.afterStatus == 0:
                        if atts.afterTimeOut is None:
                            atts.morningStatus = 0
                            atts.morningTimeOut = datetime.now()
                            # atts.morningRemark = wala pa nabutang
                            print 'QQQQQQQQQQQQQQQQQQQ'
                            dbase.session.commit()
                            return jsonify({'message': 'time out for morning'})
                        else:
                            print'RRRRRRRRRRRRRRR'
                            return jsonify({'message': 'you cannot time in twice'})
                    elif atts.morningStatus == 0 and atts.afterStatus == 1:
                        print'SSSSSSSSSSSSSSSSSSSSS'
                        return jsonify({'message': 'no time out for afternoon at this time'})
                    elif atts.morningStatus == 1 and atts.afterStatus == 1:
                        atts.morningStatus = 0
                        atts.morningTimeOut = datetime.now()
                        dbase.session.commit()
                        print'TTTTTTTTTTTTTTT'
                        return jsonify({'message': 'no time out for afternoon at this time'})
                elif now > a1 and now <= a6:
                    if atts.morningStatus == 0 and atts.afterStatus == 0:
                        if atts.afterTimeOut is None:
                            atts.afterStatus = 1
                            atts.lateTotal = atts.lateTotal + 1
                            atts.afterDailyStatus = 'late'
                            atts.afterTimeIn = datetime.now()
                            # atts.morningRemark = wala pa nabutang
                            print 'UUUUUUUUUUUUUUUUU'
                            dbase.session.commit()
                            return jsonify({'message': 'late'})
                        else:
                            print'VVVVVVVVVVVV'
                            return jsonify({'message': 'you cannot time in twice'})
                    elif atts.morningStatus == 1 and atts.afterStatus == 0:
                        if atts.afterTimeOut is None:
                            atts.morningStatus = 0
                            atts.afterStatus = 1
                            atts.morningTimeOut = datetime.now()
                            atts.lateTotal = atts.lateTotal + 1
                            atts.afterDailyStatus = 'late'
                            atts.afterTimeIn = datetime.now()
                            # atts.morningRemark = wala pa nabutang
                            print 'WWWWWWWWWWWWWWWWWWWW'
                            dbase.session.commit()
                            return jsonify({'message': '"time in for afternoon." (time out for morning next time,) '})
                        else:
                            print'XXXXXXXXXXXXXXX'
                            return jsonify({'message': 'you cannot time in twice'})
                    elif atts.morningStatus == 0 and atts.afterStatus == 1:
                        atts.afterStatus = 0
                        atts.afterTimeOut = datetime.now()
                        dbase.session.commit()
                        print'YYYYYYYYYYYYYYYY'
                        return jsonify({'message': 'time out'})
                    elif atts.morningStatus == 1 and atts.afterStatus == 1:
                        atts.afterStatus = 0
                        atts.morningStatus = 0
                        atts.afterTimeOut = datetime.now()
                        atts.morningTimeOut = datetime.now()
                        dbase.session.commit()
                        print'ZZZZZZZZZZZZZZZZZZZZ'
                        return jsonify({'message': 'time out'})
                elif now > a6 and now <= a7:
                    if atts.morningStatus == 0 and atts.afterStatus == 0:
                        print'!!!!!!!!!!!!!!!!!'
                        absents()
                        return jsonify({'message': 'no time in for this time'})

                    elif atts.morningStatus == 1 and atts.afterStatus == 0:
                        atts.morningStatus = 0
                        atts.morningTimeOut = datetime.now()
                        dbase.session.commit()
                        absents()
                        print'@@@@@@@@@@@@@@@'
                        return jsonify({'message': 'not time in for afternoon'})

                    elif atts.morningStatus == 0 and atts.afterStatus == 1:
                        atts.afterStatus = 0
                        atts.afterTimeOut = datetime.now()
                        dbase.session.commit()
                        absents()
                        print'#################'
                        return jsonify({'message': 'time out for afternoon'})
                    elif atts.morningStatus == 1 and atts.afterStatus == 1:
                        atts.morningStatus = 0
                        atts.afterStatus = 0
                        atts.morningTimeOut = datetime.now()
                        atts.afterTimeOut = datetime.now()
                        dbase.session.commit()
                        print'$$$$$$$$$$$$$$$$$$$$$'
                        absents()
                        return jsonify({'message': 'time out for afternoon and morning'})
                else:
                    pass

# ///////////////////////////////////////IF DATE IS NOT THE SAME CREATE NEW ATTENDANCE////////////////////////
            else:
                # dbase.session.add(attendancenNew)
                # dbase.session.commit()
                atts = Attendance.query.filter(
                    and_(Attendance.employeeid == empID, Attendance.date == datenow)).order_by(
                    Attendance.date.desc()).first()
                # atts.date = datenow
                print "last"
                # dates = Attendance.query.filter_by(date = datenow).first()
                # print "1st"
                # print dates.date
                # if dates.date == datenow:
                #     print '444546456646546465465465464654654654654'

                # elif dates.date != datenow:
                #     atts.morningStatus = 0
                #     atts.afterStatus = 0
                #     dbase.session.add(attendancenNew)
                #     dbase.session.commit()
                #     print '0987654321=-098765'

                # dbase.session.commit()
                if (now >= m7) and (now <= m9):
                    if atts.morningStatus == 0 and atts.afterStatus == 0:
                        if atts.morningTimeOut is None:
                            atts.morningStatus = 1
                            atts.morningTimeIn = datetime.now()
                            atts.morningDailyStatus = 'not late'
                            print "9999999999999999999999"
                            dbase.session.commit()
                            return jsonify({'message': 'not late'})
                        else:
                            print'8888888888888888888888'
                            return jsonify({'message': 'you cannot time in twice'})
                    elif atts.morningStatus == 1 and atts.afterStatus == 0:
                        print '777777777777777777777777'
                        return jsonify({'message': 'no time out at this time'})
                    elif atts.morningStatus == 0 and atts.afterStatus == 1:
                        if atts.morningTimeOut is None:
                            atts.afterStatus = 0
                            atts.morningStatus = 1
                            atts.afterTimeOut = datetime.now()
                            atts.morningTimeIn = datetime.now()
                            atts.morningDailyStatus = 'not late'
                            dbase.session.commit()
                            print'66666666666666666666665454565'
                            return jsonify({'message': 'not late, kindly dont forget to timeout in morning'})
                        else:
                            print'555555555555555555555555555'
                            return jsonify({'message': 'you cannot time in twice'})
                    elif atts.morningStatus == 1 and atts.afterStatus == 1:
                        atts.afterStatus = 0
                        atts.afterTimeOut = datetime.now()
                        dbase.session.commit()
                        print'444441254'
                        return jsonify({'message': 'no time out at this time'})

                elif now > m9 and now <= m12:
                    if atts.morningStatus == 0 and atts.afterStatus == 0:
                        if atts.morningTimeOut is None:
                            atts.morningStatus = 1
                            atts.lateTotal = atts.lateTotal + 1
                            atts.morningDailyStatus = 'late'
                            atts.morningTimeIn = datetime.now()
                            # atts.morningRemark = wala pa nabutang
                            print '3'
                            dbase.session.commit()
                            return jsonify({'message': 'late'})
                        else:
                            print'2'
                            return jsonify({'message': 'you cannot time in twice'})
                    elif atts.morningStatus == 1 and atts.afterStatus == 0:
                        if atts.morningTimeOut is None:
                            atts.morningStatus = 0
                            atts.morningTimeOut = datetime.now()
                            # atts.morningRemark = wala pa nabutang
                            print '1'
                            dbase.session.commit()
                            return jsonify({'message': 'time out'})
                        else:
                            print'A`'
                            return jsonify({'message': 'you cannot time in twice'})
                    elif atts.morningStatus == 0 and atts.afterStatus == 1:
                        if atts.morningTimeOut is None:
                            atts.afterStatus = 0
                            atts.morningStatus = 1
                            atts.afterTimeOut = datetime.now()
                            atts.morningTimeIn = datetime.now()
                            atts.morningDailyStatus = 'late'
                            # atts.morningRemark = wala pa nabutang
                            dbase.session.commit()
                            print'B`'
                            return jsonify({'message': 'late, kindly dont forget to timeout in morning'})
                        else:
                            print'C`'
                            return jsonify({'message': 'you cannot time in twice'})
                    elif atts.morningStatus == 1 and atts.afterStatus == 1:
                        if atts.morningTimeOut is None:
                            atts.afterStatus = 0
                            atts.morningStatus = 0
                            atts.afterTimeOut = datetime.now()
                            atts.morningTimeOut = datetime.now()
                            dbase.session.commit()
                            print'D`'
                            return jsonify({'message': 'time out'})
                        else:
                            print'E`'
                            return jsonify({'message': 'you cannot time in twice'})
                elif (now > m12) and (now <= a1):  # 12 -7pm
                    if atts.morningStatus == 0 and atts.afterStatus == 0:
                        if atts.afterTimeOut is None:
                            atts.afterStatus = 1
                            atts.afterDailyStatus = 'not late'
                            atts.afterTimeIn = datetime.now()
                            # atts.morningRemark = wala pa nabutang
                            print 'F`'
                            dbase.session.commit()
                            return jsonify({'message': 'time in for afternoon'})
                        else:
                            print'G`'
                            return jsonify({'message': 'you cannot time in twice'})
                    elif atts.morningStatus == 1 and atts.afterStatus == 0:
                        if atts.afterTimeOut is None:
                            atts.morningStatus = 0
                            atts.morningTimeOut = datetime.now()
                            # atts.morningRemark = wala pa nabutang
                            print 'H`'
                            dbase.session.commit()
                            return jsonify({'message': 'time out for morning'})
                        else:
                            print'I`'
                            return jsonify({'message': 'you cannot time in twice'})
                    elif atts.morningStatus == 0 and atts.afterStatus == 1:
                        print'J`'
                        return jsonify({'message': 'no time out for afternoon at this time'})
                    elif atts.morningStatus == 1 and atts.afterStatus == 1:
                        atts.morningStatus = 0
                        atts.morningTimeOut = datetime.now()
                        dbase.session.commit()
                        print'K`'
                        return jsonify({'message': 'no time out for afternoon at this time'})
                elif now > a1 and now <= a6:
                    if atts.morningStatus == 0 and atts.afterStatus == 0:
                        if atts.afterTimeOut is None:
                            atts.afterStatus = 1
                            atts.lateTotal = atts.lateTotal + 1
                            atts.afterDailyStatus = 'late'
                            atts.afterTimeIn = datetime.now()
                            # atts.morningRemark = wala pa nabutang
                            print 'L`'
                            dbase.session.commit()
                            return jsonify({'message': 'late'})
                        else:
                            print'M`'
                            return jsonify({'message': 'you cannot time in twice'})
                    elif atts.morningStatus == 1 and atts.afterStatus == 0:
                        if atts.afterTimeOut is None:
                            atts.morningStatus = 0
                            atts.afterStatus = 1
                            atts.morningTimeOut = datetime.now()
                            atts.lateTotal = atts.lateTotal + 1
                            atts.afterDailyStatus = 'late'
                            atts.afterTimeIn = datetime.now()
                            # atts.morningRemark = wala pa nabutang
                            print 'N`'
                            dbase.session.commit()
                            return jsonify({'message': 'time out'})
                        else:
                            print'O`'
                            return jsonify({'message': 'you cannot time in twice'})
                    elif atts.morningStatus == 0 and atts.afterStatus == 1:
                        atts.afterStatus = 0
                        atts.afterTimeOut = datetime.now()
                        dbase.session.commit()
                        print'P`'
                        return jsonify({'message': 'time out'})
                    elif atts.morningStatus == 1 and atts.afterStatus == 1:
                        atts.afterStatus = 0
                        atts.morningStatus = 0
                        atts.afterTimeOut = datetime.now()
                        atts.morningTimeOut = datetime.now()
                        dbase.session.commit()
                        print'Q`'
                        return jsonify({'message': 'time out'})
                elif now > a6 and now <= a7:
                    if atts.morningStatus == 0 and atts.afterStatus == 0:
                        print'R`'
                        absents()
                        return jsonify({'message': 'no time in for this time'})

                    elif atts.morningStatus == 1 and atts.afterStatus == 0:
                        atts.morningStatus = 0
                        atts.morningTimeOut = datetime.now()
                        dbase.session.commit()
                        print'S`'
                        absents()
                        return jsonify({'message': 'not time in for afternoon'})

                    elif atts.morningStatus == 0 and atts.afterStatus == 1:
                        atts.afterStatus = 0
                        atts.afterTimeOut = datetime.now()
                        dbase.session.commit()
                        print'T`'
                        absents()
                        return jsonify({'message': 'time out for afternoon'})
                    elif atts.morningStatus == 1 and atts.afterStatus == 1:
                        atts.morningStatus = 0
                        atts.afterStatus = 0
                        atts.morningTimeOut = datetime.now()
                        atts.afterTimeOut = datetime.now()
                        dbase.session.commit()
                        print'U`'
                        absents()
                        return jsonify({'message': 'time out for afternoon and morning'})
                else:
                    pass

def absents():
    datenow1 = datetime.now().strftime("%m%d%Y")
    employs = Employee.query.filter_by(employeestatus = 1).all()
    employees = []
    for i in employs:
        employees.append(i.employeeid)

    present = Attendance.query.filter(and_(Attendance.date == datenow1, Attendance.absentTotal == 0)).all()
    presents = []
    
    if present:
        for e in present:
            presents.append(e.employeeid)
        
        absent = []
        for i in employees:
            # print "this" + str(i)
            for j in presents:
                if i == j:
                    pass
                else:
                    absent.append(i)

        for i in absent:
            v = Attendance.query.filter(and_(Attendance.employeeid == i, Attendance.absentTotal == None)).first()
            if v:    
                absent =  Attendance(employeeid = i)
                dbase.session.add(absent)
                dbase.session.commit()
                absent.absentTotal = absent.absentTotal + 1
                absent.date = datenow1
                dbase.session.commit()
            else:
                pass
        else:
            pass  

@app.route('/remark/<string:codes>', methods=['GET', 'POST'])
def add_remarks(codes):
  data = request.get_json()
  ids = Employee.query.filter_by(code=codes).first()
  remarks = Attendance.query.filter_by(employeeid=ids.employeeid).order_by(Attendance.date.desc()).first()
  if remarks.morningDailyStatus == "late":
    if remarks.morningRemark is None:
      remarks.morningRemark = data['reason']
      dbase.session.commit()
      return jsonify({'message':'Remark added'})
    else:
      pass
  elif remarks.afterDailyStatus == "late":
    if remarks.afterRemark is None:
      remarks.afterRemark = data['reason']
      dbase.session.commit()
      return jsonify({'message':'Remark added'})
    else:
      pass

@app.route('/autoTimeOut/', methods=['GET', 'POST'])
def auto_TimeOut():
  timeout = Overtime.query.filter(and_(Overtime.overtimeid == 1, Overtime.overtimeDate == lgdate).order_by(Overtime.overtimeDate.desc())).all()
  if timeout is None:
    pass
  else:
    for i in timeout:
      i.overtimeInStatus = 0
      dbase.session.commit()

@app.route('/overtime/request', methods=['POST'])
def request_overtime():
   data = request.get_json()
   employee = Employee.query.filter_by(code=data['code']).first()
   if employee is None:
        return jsonify({'message': 'Employee not found'})
   overtime = Overtime.query.filter(Overtime.employeeid == employee.employeeid).filter(Overtime.overtimeStatus == 0).order_by(Overtime.overtimeDate.desc()).first()
   if overtime is None:
       new_overtime = Overtime(employeeid=employee.employeeid)
       dbase.session.add(new_overtime)
       dbase.session.commit()
       overtime_date = Overtime.query.filter_by(employeeid = employee.employeeid)
       overtime_date.overtimeDate = datetime.strptime(str(data['date']), "%m-%d-%Y")
       dbase.session.commit()
       return jsonify({'message': 'Request Created'})
   else:
       return jsonify({'message': 'Request already sent, Please wait for the admin to approve'})


@app.route('/view/overtime/requests', methods=['GET'])
def view_requests():
   overtime = Overtime.query.filter_by(overtimeStatus=0).all()
   if overtime is None:
       return jsonify({'message': 'No request found'})
   else:
       overtimers = []
       for overtimee in overtime:
           employee = Employee.query.filter_by(employeeid=overtimee.employeeid).first()
           employee_data = {}
           employee_data['name'] = employee.fname + " " + employee.mname + " " + employee.lname
           employee_data['id'] = employee.employeeid
           employee_data['date'] = overtimee.overtimeDate
           overtimers.append(employee_data)
           return jsonify({'employee': overtimers})


@app.route('/approve/request', methods=['POST'])
def approve():
   data = request.get_json()
   overtime = Overtime.query.filter(Overtime.overtimeStatus == 0).filter(Overtime.employeeid == data['id']).first()
   if overtime is None:
       return jsonify({'message': 'Error'})
   else:
       overtime.overtimeStatus = 1
       overtime.overtimeTotal = overtime.overtimeTotal + 1
       dbase.session.commit()
       return jsonify({'message': 'Overtime approved successfuly!'})
