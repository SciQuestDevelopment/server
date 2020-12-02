from typing import Tuple

from flask import json, request, session

from . import router

from ..utils.database.tb_builder import tables


@router.route('/', methods=['GET'])
def get_all_apis():
    return json.jsonify({
        "Register": {
            "Method": "GET",
            "Subpath": "/register"
        },
        "Login": {
            "Method": "GET",
            "Subpath": "/login"
        }
    })


def __boolean_error_response_body() -> Tuple:
    rlt_msg = {'is_success': False}
    rlt_code = 400
    return json.jsonify(rlt_msg), rlt_code


@router.route('/register', methods=['POST'])
def register():
    data = request.form.to_dict()
    if data is None: data = request.json
    if data is None: return __boolean_error_response_body()
    account = data.get('account')
    password = data.get('password')
    first_name = data.get('first_name')
    second_name = data.get('second_name')
    phone_num = data.get('phone_num')
    email_address = data.get('email_address')
    is_success = tables.user.register(first_name, second_name, account, password, phone_num, email_address)
    rlt_msg = {'is_success': f'{is_success}'}
    rlt_code = 200
    return json.jsonify(rlt_msg), rlt_code


@router.route('/login', methods=['POST'])
def login():
    data = request.form.to_dict()
    if data is None: data = request.json
    if data is None: return __boolean_error_response_body()
    account = data.get('account')
    password = data.get('password')
    user_id = tables.user.login_and_get_id(account, password)
    is_success = user_id is not None
    if is_success:
        session['username'] = account
        # activate session usage
        session.permanent = True
    rlt_msg = {'is_success': f'{is_success}'}
    rlt_code = 200
    return json.jsonify(rlt_msg), rlt_code

