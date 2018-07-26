from api import dbase, generate_password_hash
from flask_login import UserMixin

class Admin(UserMixin, dbase.Model):
    __tablename__ = 'admin'
    id = dbase.Column(dbase.Integer, primary_key=True)
    username = dbase.Column(dbase.String(50), nullable=False)
    password = dbase.Column(dbase.String(256), nullable=False)
    morning_time_in_start = dbase.Column(dbase.Time)
    morning_time_out_start = dbase.Column(dbase.Time)
    morning_time_out_end = dbase.Column(dbase.Time)
    afternoon_time_in_start = dbase.Column(dbase.Time)
    afternoon_time_out_start = dbase.Column(dbase.Time)
    afternoon_time_out_end = dbase.Column(dbase.Time)

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password, method='sha256')


class Employee(dbase.Model):
    __tablename__ = 'employee'
    employeeid = dbase.Column(dbase.Integer, primary_key=True, autoincrement= True)
    employeestatus = dbase.Column(dbase.Integer, default=0)
    fname = dbase.Column(dbase.String(50))
    mname = dbase.Column(dbase.String(50))
    lname = dbase.Column(dbase.String(50))
    position = dbase.Column(dbase.String(30))
    code = dbase.Column(dbase.String(100), unique = True)
    contact = dbase.Column(dbase.String(15))
    email = dbase.Column(dbase.String(30))
    birth_date = dbase.Column(dbase.DATE, nullable=False)
    gender = dbase.Column(dbase.String(6), nullable=False)
    address = dbase.Column(dbase.String(50))
    late = dbase.Column(dbase.Integer, default=0)
    absent = dbase.Column(dbase.Integer, default=0)
    overtimes = dbase.Column(dbase.Integer, default=0)
    attendance1 = dbase.relationship('Attendance', backref='employee', lazy=True)
    overtime = dbase.relationship('Overtime', backref='employee', lazy=True)

    def __init__(self, fname, mname, lname, position, code, contact, email, birth_date, gender, employeestatus, address):
        self.employeestatus = employeestatus
        self.fname = fname
        self.mname = mname
        self.lname = lname
        self.position = position
        self.code = code
        self.contact = contact
        self.email = email
        self.birth_date = str(birth_date)
        self.gender = gender
        self.address = address

class Attendance(dbase.Model):
    __tablename__ = 'attendance'
    AttendanceId = dbase.Column(dbase.Integer, primary_key=True)
    employeeid = dbase.Column(dbase.Integer, dbase.ForeignKey('employee.employeeid'))
    lateTotal = dbase.Column(dbase.Integer, default=0)
    absentTotal = dbase.Column(dbase.Integer, default=0)
    morningTimeIn = dbase.Column(dbase.DateTime)
    morningTimeOut = dbase.Column(dbase.DateTime)
    morningStatus = dbase.Column(dbase.Integer, default=0, nullable =False)
    morningDailyStatus = dbase.Column(dbase.String(8))
    morningRemark = dbase.Column(dbase.String(50))
    afterTimeIn = dbase.Column(dbase.DateTime)
    afterTimeOut = dbase.Column(dbase.DateTime)
    afterStatus = dbase.Column(dbase.Integer, default=0, nullable = False)
    afterDailyStatus = dbase.Column(dbase.String(8)) 
    afterRemark = dbase.Column(dbase.String(50))
    date = dbase.Column(dbase.DATE)
    week_number = dbase.Column(dbase.Integer)

    def __init__(self, employeeid):
        self.employeeid = employeeid

class Overtime(dbase.Model):
    __tablename__ = 'overtime'
    overtimeid = dbase.Column(dbase.Integer, primary_key=True)
    employeeid = dbase.Column(dbase.Integer, dbase.ForeignKey('employee.employeeid'))
    overtimeDate = dbase.Column(dbase.DATE)
    overtimeIn = dbase.Column(dbase.DateTime)
    overtimeOut = dbase.Column(dbase.DateTime)
    overtimeInStatus = dbase.Column(dbase.Integer, default=0)
    overtimeStatus = dbase.Column(dbase.Integer, default=0)
    overtimeTotal = dbase.Column(dbase.Integer, default=0)

    def __init__(self, employeeid, overtimeDate):
        self.employeeid = employeeid
        self.overtimeDate = overtimeDate

class Logs(dbase.Model):
    __tablename__ = "logs"
    logID = dbase.Column(dbase.Integer, primary_key=True, autoincrement=True)
    details = dbase.Column(dbase.String(60))
    log_date = dbase.Column(dbase.DateTime)
    logStatus = dbase.Column(dbase.Integer, default=0)
    counter = dbase.Column(dbase.Integer, default=0)

    def __init__(self, details, log_date):
        self.details = details
        self.log_date = log_date
