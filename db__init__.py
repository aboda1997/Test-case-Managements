from models import ExecutionResult, TestCase, User
from  database import db
from app import app
with app.app_context():  # Add this line to establish the application context

    User1 = User(username='admin', password='admin' , role = "admin")
    User2 = User(username='Abdelrahman', password='Abdelrahman' , role = "user")
    User3 = User(username='Mohammed', password='Mohammed' , role = "user")

    TestCase1 = TestCase(name='get all test case', description="return all test cases from database using postman")
    TestCase2 = TestCase(name='return specific test case ', description="return individual test case from database")
    TestCase3 = TestCase(name='get all the execution test cases', description="test the retutn of all execution test cases")


    db.session.add_all([User1, User2, User3])
    db.session.add_all([TestCase1, TestCase2, TestCase3])

    db.session.commit()