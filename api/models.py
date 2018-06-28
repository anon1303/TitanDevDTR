from api import dbase, generate_password_hash


class Admin(dbase.Model):
    __tablename__ = 'admin'
    username = dbase.Column(dbase.String(50), nullable=False, primary_key=True)
    password = dbase.Column(dbase.String(100), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password, method='sha256')


class Employee(dbase.Model):
    __tablename__ = 'employee'
    employeeid = dbase.Column(dbase.Integer, primary_key=True)
    employeestatus = dbase.Column(dbase.Integer, default=0)
    fname = dbase.Column(dbase.String(50))
    mname = dbase.Column(dbase.String(50))
    lname = dbase.Column(dbase.String(50))
    position = dbase.Column(dbase.String(30))
    code = dbase.Column(dbase.String(15))
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
        self.code = code
        self.contact = contact
        self.email = email
        self.birth_date = birth_date
        self.gender = gender
        self.address = address


class Attendance(dbase.Model):
    __tablename__ = 'attendance'
    id = dbase.Column(dbase.Integer, primary_key=True)
    employeeid = dbase.Column(dbase.Integer, dbase.ForeignKey('employee.employeeid'))
    lateTotal = dbase.Column(dbase.Integer, default=0)
    absentTotal = dbase.Column(dbase.Integer, default=0)
    timeIn = dbase.Column(dbase.DateTime)
    timeOut = dbase.Column(dbase.DateTime)
    status = dbase.Column(dbase.Integer, default=0)
    dailyStatus = dbase.Column(dbase.String(6))

    def __init__(self, lateTotal, absentTotal, timeIn, timeOut, status, dailyStatus, employeeid):
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
    log_date = dbase.Column(dbase.DateTime)

    def __init__(self, details, log_date):
        self.details = details
        self.log_date = log_date

