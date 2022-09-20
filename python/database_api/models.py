from python.database_api import db, ma


class Event(db.Model):
    id = db.Column('id', db.String(40), primary_key=True)
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


class RequestForSupport(db.Model):
    id = db.Column('id', db.String(40), primary_key=True)
    remote_addr = db.Column(db.String(70), nullable=False)
    description_of_the_problem = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(40), nullable=False)
    last_name = db.Column(db.String(40), nullable=False)
    urgent = db.Column(db.String(3), nullable=False)

    def __init__(self, submission_id, remote_addr, description_of_the_problem, first_name, last_name, urgent):
        self.id = submission_id
        self.remote_addr = remote_addr
        self.description_of_the_problem = description_of_the_problem
        self.first_name = first_name
        self.last_name = last_name
        self.urgent = urgent
