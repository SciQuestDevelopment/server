from typing import Tuple, Optional

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


def __error_response(details: Optional[str]) -> Tuple:
    rlt_msg = {'is_success': False, 'details': details}
    rlt_code = 400
    return json.jsonify(rlt_msg), rlt_code


@router.route('/register', methods=['POST'])
def register():
    data = request.form.to_dict()
    if data is None: data = request.json
    if data is None: return __error_response('ERROR: BOTH FORM AND RAW BODY IS EMPTY.')
    expect_par_names = {'account', 'password', 'first_name', 'second_name', 'phone_num', 'email_address'}
    actual_par_names = set(data.keys())
    needed_par_names = expect_par_names - actual_par_names
    if len(needed_par_names) != 0: return __error_response(f'ERROR: \n\tNEEDED: {needed_par_names}\n\tACTUAL: {data}')
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
    if data is None: return __error_response('ERROR: BOTH FORM AND RAW BODY IS EMPTY.')
    expect_par_names = {'account', 'password'}
    actual_par_names = set(data.keys())
    needed_par_names = expect_par_names - actual_par_names
    if len(needed_par_names) != 0: return __error_response(f'ERROR: \n\tNEEDED: {needed_par_names}\n\tACTUAL: {data}')
    account = data.get('account')
    password = data.get('password')
    user_id = tables.user.login_and_get_id(account, password)
    is_success = user_id is not None
    if is_success:
        session['user_id'] = user_id
        session.permanent = True
    rlt_msg = {'is_success': f'{is_success}'}
    rlt_code = 200
    return json.jsonify(rlt_msg), rlt_code

