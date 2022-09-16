from python.database_api import db, ma


class Event(db.Model):
    id = db.Column('id', db.String(20), primary_key=True)
    type = db.Column(db.String(20), nullable=False)
    version = db.Column(db.String(20), nullable=False)
    received = db.Column(db.DateTime, nullable=False)
    department = db.Column(db.String(20), nullable=False)
    form_id = db.Column(db.String(20), nullable=False)

    def __init__(self, submission_id, form_type, version, received, department, form_id):
        self.id = submission_id
        self.type = form_type
        self.version = version
        self.received = received
        self.department = department
        self.form_id = form_id


class ReportPothole(db.Model):
    id = db.Column('id', db.String(20), primary_key=True)
    location = db.Column(db.String(70), nullable=False)
    affects = db.Column(db.String(60), nullable=False)
    first_name = db.Column(db.String(40), nullable=False)
    last_name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(40), nullable=False)

    def __init__(self, submission_id, location, affects, first_name, last_name, email):
        self.id = submission_id
        self.location = location
        self.affects = affects
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
