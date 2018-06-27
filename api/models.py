from api import *
from itsdangerous import JSONWebSignatureSerializer as Serialize
from flask_login import AnonymousUserMixin
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, ForeignKey, String, Column
from datetime import datetime

class Admin(dbase.Model):
	__tablename__ = 'admin'
	username = dbase.Column(dbase.String(50), primary_key=True, nullable=False)
	password = dbase.Column(dbase.String(100), nullable=False)

	def __init__(self, username, password):
		self.username = username
		self.password = generate_password_hash(password, method='sha256')

class Employee(dbase.Model):
	__tablename__ = 'employee'
	employeeid = dbase.Column(dbase.Integer, primary_key = True , autoincrement = True )
	employeestatus = dbase.Column(dbase.Integer) 
	fname = dbase.Column(dbase.String(50))
	mname = dbase.Column(dbase.String(50))
	lname = dbase.Column(dbase.String(50))
	position = dbase.Column(dbase.String(30))
	code = dbase.Column(dbase.String(15))
	contact = dbase.Column(dbase.String(15))
	email = dbase.Column(dbase.String(30))
	birth_date = db.Column(db.DATE, nullable=False)
	gender = db.Column(db.String(6), nullable=False)

	def __init__(self,fname, mname, lname, position, code, contact, email, birth_date, gender, employeestatus ):
		self.employeestatus = 0
		self.fname = fname
		self.mname = mname
		self.lname = lname
		self.position = position
		self.code = code
		self.contact = contact
		self.email = email
		self.birth_date = birth_date
        self.gender = gender

class Attendance(dbase.Model):
	__tablename__ = 'attendance'

	employeeid = dbase.Column(dbase.Integer, dbase.ForeignKey("employee.employeeid"),primary_key = True, nullable=False)
	lateTotal = dbase.Column(dbase.Integer)
	absentTotal = dbase.Column(dbase.Integer)
	timeIn = dbase.Column(dbase.DateTime)
	timeOut = dbase.Column(dbase.DateTime)
	status = dbase.Column(dbase.Integer)
	dailyStatus = dbase.Column(dbase.String(6))

	def __init__(self,lateTotal, absentTotal, timeIn, timeOut, status, dailyStatus, employeeid):
		self.lateTotal = lateTotal
		self.absentTotal = absentTotal
		self.timeIn = timeIn
		self.timeOut = timeOut
		self.status = 0
		self.dailyStatus = dailyStatus 
		self.employeeid = employeeid


class Logs(dbase.Model):
    __tablename__ = "logs"
    logID = dbase.Column(dbase.Integer, primary_key=True, autoincrement=True)
    details = dbase.Column(dbase.String(60))
    log_date =dbase.Column(dbase.DateTime)

    def __init__(self, details, log_date):
        self.details = details
        self.log_date = log_date






