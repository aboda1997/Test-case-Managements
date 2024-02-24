from flask import Flask , jsonify , request
from models import User
from routes import testcases_bp 
import os 
from database import db
from flask_jwt_extended import JWTManager , create_access_token

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    # Check if the username and password are valid
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id , additional_claims={'role': user.role , 'user' : user.id} )
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

app.register_blueprint(testcases_bp)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] =\
           'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_secret_key'


@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

db.init_app(app)
jwt = JWTManager(app)

if __name__ == '__main__':
    with app.app_context():  # Add this line to establish the application context
        db.create_all()
    app.run(debug=True)