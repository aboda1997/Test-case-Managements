from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity,verify_jwt_in_request , get_jwt
from models import db, User , TestCase , ExecutionResult
from functools import wraps
from validations import TestCaseValidation , TestCaseExecution

def role_required(role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            user_role = claims.get('role')
            user_id = claims.get('user')
            request.user_id = user_id 
            if user_role != role:
                return jsonify({'message': 'Unauthorized access'}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator

testcases_bp = Blueprint('testcases', __name__, url_prefix='/testcases')



@testcases_bp.route('', methods=['GET'])
@jwt_required()
def get_testcases():
    print(request.user_id)
    testcases = TestCase.query.all()
    result = [{'id': tc.id, 'name': tc.name, 'description': tc.description} for tc in testcases]
    return jsonify(result)

@testcases_bp.route('/<int:testcase_id>', methods=['GET'])
@jwt_required()
def get_test_case_by_id(testcase_id):
    testcase = TestCase.query.get(testcase_id)
    if not testcase:
        return jsonify({'error': 'Test case not found'}), 404

    response = {
        'id': testcase.id,
        'name': testcase.name,
        'description': testcase.description
    }
    return jsonify(response), 200

@testcases_bp.route('/testasset/<int:asset_id>', methods=['POST'])
@jwt_required()
@role_required('admin')
def create_testcase(asset_id):
    data = request.get_json()
    validData = TestCaseValidation(data)
    if validData.get("valid"):
        name = data.get("name")  
        description = data.get("description")  
        testcase = TestCase(name=name, description=description, asset_id = asset_id)
        db.session.add(testcase)
        db.session.commit()
        return jsonify({'message': 'Test case created successfully.'}),200
    else:
        errors = validData.get("error")
        return jsonify({'errors': errors}), 400
    

@testcases_bp.route('/testasset/<int:asset_id>', methods=['GET'])
@jwt_required()
def Get_all_testcases_for_specific_asset_id(asset_id):
    executions = ExecutionResult.query.join(TestCase).filter(TestCase.asset_id == asset_id).all()
    result = [{'id': tc.id, 'status': tc.status} for tc in executions]
    return jsonify(result)


@testcases_bp.route('/<int:testcase_id>', methods=['PUT'])
@jwt_required()
@role_required('admin')
def update_testcase(testcase_id):
    testcase = TestCase.query.get(testcase_id)
    if not testcase:
        return jsonify({'error': 'Test case not found'}), 404

    data = request.get_json()
    validData = TestCaseValidation(data)
    if validData.get("valid"):
        testcase.name = data.get('name', testcase.name)
        testcase.description = data.get('description', testcase.description)
        db.session.commit()

        response = {
            'id': testcase.id,
            'name': testcase.name,
            'description': testcase.description
        }
        return jsonify(response), 200

    else:
        errors = validData.get("error")
        return jsonify({'errors': errors}), 400

@testcases_bp.route('/<int:testcase_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_testcase(testcase_id):
    testcase = TestCase.query.get(testcase_id)
    if not testcase:
        return jsonify({'error': 'Test case not found'}), 404

    db.session.delete(testcase)
    db.session.commit()

    return jsonify({'message': 'Test case deleted successfully'}), 200


@testcases_bp.route('/<int:testcase_id>/execution', methods=['POST'])
@jwt_required()
@role_required('admin')
def execute_testcase(testcase_id):
    testcase = TestCase.query.get(testcase_id)
    if not testcase:
        return jsonify({'error': 'Test case not found'}), 404

    data = request.get_json()
    validData = TestCaseExecution(data)
    if validData.get("valid"):
        execution_result = ExecutionResult(testcase_id=testcase_id, status=data['status'])
        db.session.add(execution_result)
        db.session.commit()
        return jsonify({'message': 'Execution result saved successfully.'})
    else:
        errors = validData.get("error")
        return jsonify({'errors': errors}), 400    