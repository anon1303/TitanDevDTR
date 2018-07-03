from api import dbase, generate_password_hash
from flask_login import UserMixin

class Admin(UserMixin, dbase.Model):
    __tablename__ = 'admin'
    adminId = dbase.Column(dbase.Integer, primary_key=True)
    username = dbase.Column(dbase.String(50), nullable=False)
    password = dbase.Column(dbase.String(100), nullable=False)

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
    code = dbase.Column(dbase.String(100))
    contact = dbase.Column(dbase.String(15))
    email = dbase.Column(dbase.String(30))
    birth_date = dbase.Column(dbase.DATE, nullable=False)
    gender = dbase.Column(dbase.String(6), nullable=False)
    address = dbase.Column(dbase.String(50))
    attendance1 = dbase.relationship('Attendance', backref='employee', lazy=True)

    def __init__(self, fname, mname, lname, position, code, contact, email, birth_date, gender, employeestatus, address):
        self.employeestatus = employeestatus
        self.fname = fname
        self.mname = mname
        self.lname = lname
        self.position = position
        self.code = generate_password_hash(code, method='sha256')
        self.contact = contact
        self.email = email
        self.birth_date = birth_date
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
    afterTimeIn = dbase.Column(dbase.DateTime)
    afterTimeOut = dbase.Column(dbase.DateTime)
    morningStatus = dbase.Column(dbase.Integer, default=0)
    afterStatus = dbase.Column(dbase.Integer, default=0)
    morningDailyStatus = dbase.Column(dbase.String(8))
    afterDailyStatus = dbase.Column(dbase.String(8)) 
    morningRemark = dbase.Column(dbase.String(50))
    afterRemamrk = dbase.Column(dbase.String(50))

    def __init__(self, lateTotal, absentTotal, employeeid, morningRemark, afterRemamrk, morningTimeIn, morningTimeOut,
                    afterTimeIn, afterTimeOut, morningStatus, afterStatus, morningDailyStatus, afterDailyStatus):
        self.lateTotal = lateTotal
        self.absentTotal = absentTotal
        self.employeeid = employeeid
        self.morningRemark = morningRemark
        self.afterRemamrk = afterRemamrk
        self.morningTimeIn = morningTimeIn
        self.morningTimeOut = morningTimeOut
        self.afterTimeIn = afterTimeIn
        self.afterTimeOut = afterTimeOut
        self.morningStatus = morningStatus
        self.afterStatus = afterStatus
        self.morningDailyStatus = morningDailyStatus
        self.afterDailyStatus = afterDailyStatus


class Logs(dbase.Model):
    __tablename__ = "logs"
    logID = dbase.Column(dbase.Integer, primary_key=True, autoincrement=True)
    details = dbase.Column(dbase.String(60))
    log_date = dbase.Column(dbase.DateTime)

    def __init__(self, details, log_date):
        self.details = details
        self.log_date = log_date
