from flask import jsonify, make_response

def create_success_response(message, code):
    response = make_response(jsonify({'status': 'success', 'message': message}), code)
    print(response.get_json())
    return response

def create_error_response(message, code):
    response = make_response(jsonify({'status': 'error', 'message': message}), code)
    print(response.get_json())
    return response