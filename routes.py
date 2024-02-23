from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity,verify_jwt_in_request , get_jwt
from models import db, User , TestCase , ExecutionResult
from functools import wraps

def role_required(role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            user_role = claims.get('role')
            if user_role != role:
                return jsonify({'message': 'Unauthorized access'}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator

testcases_bp = Blueprint('testcases', __name__, url_prefix='/testcases')

@testcases_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Check if the username and password are valid
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id , additional_claims={'role': user.role} )
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401


@testcases_bp.route('', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_testcases(f=7):
    testcases = TestCase.query.all()
    result = [{'id': tc.id, 'name': tc.name, 'description': tc.description} for tc in testcases]
    return jsonify(result)

@testcases_bp.route('', methods=['POST'])
@jwt_required()
def create_testcase():
    data = request.get_json()
    testcase = TestCase(name=data['name'], description=data['description'])
    db.session.add(testcase)
    db.session.commit()
    return jsonify({'message': 'Test case created successfully.'})

@testcases_bp.route('/<int:testcase_id>/execution', methods=['POST'])
@jwt_required()
def execute_testcase(testcase_id):
    data = request.get_json()
    execution_result = ExecutionResult(testcase_id=testcase_id, status=data['status'])
    db.session.add(execution_result)
    db.session.commit()
    return jsonify({'message': 'Execution result saved successfully.'})