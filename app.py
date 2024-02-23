from flask import Flask
from routes import testcases_bp 
import os 
from database import db
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.register_blueprint(testcases_bp)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] =\
           'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_secret_key' 


@app.route('/', methods=['GET'])
def get_testcases():
    return "Welcome to Home Page!"

db.init_app(app)
jwt = JWTManager(app)

if __name__ == '__main__':
    with app.app_context():  # Add this line to establish the application context
        db.create_all()
    app.run(debug=True)