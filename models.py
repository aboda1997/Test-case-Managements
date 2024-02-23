from  database import db 
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), nullable=False)


    def __init__(self, username, password ,role):
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.role = role 

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
class TestCase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)

class ExecutionResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    testcase_id = db.Column(db.Integer, db.ForeignKey('test_case.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False)