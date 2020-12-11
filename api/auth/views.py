from typing import Tuple, Optional, Dict

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


def __get_data_from_both_json_and_form() -> Optional[Dict]:
    request_form = request.form.to_dict()
    if request_form is not None and len(request_form) != 0: return request_form
    request_json = request.json
    return request_json


@router.route('/register', methods=['POST'])
def register():
    data = __get_data_from_both_json_and_form()
    if data is None or len(data) == 0: return __error_response(f'ARGS: EMPTY FORM IN REQUEST {request}')
    expect_par_names = {'account', 'password', 'first_name', 'second_name', 'phone_num', 'email_address'}
    actual_par_names = set(data.keys())
    needed_par_names = expect_par_names - actual_par_names
    if len(needed_par_names) != 0: return __error_response(f'ARGS: NEEDED {needed_par_names}. ACTUAL {data}')
    account = str(data.get('account'))
    password = str(data.get('password'))
    first_name = str(data.get('first_name'))
    second_name = str(data.get('second_name'))
    phone_num = str(data.get('phone_num'))
    email_address = str(data.get('email_address'))
    is_success = tables.user.register(first_name, second_name, account, password, phone_num, email_address)
    rlt_msg = {'is_success': f'{is_success}'}
    rlt_code = 200
    return json.jsonify(rlt_msg), rlt_code


@router.route('/login', methods=['POST'])
def login():
    data = __get_data_from_both_json_and_form()
    if data is None or len(data) == 0: return __error_response(f'ARGS: EMPTY FORM IN REQUEST {request}')
    expect_par_names = {'account', 'password'}
    actual_par_names = set(data.keys())
    needed_par_names = expect_par_names - actual_par_names
    if len(needed_par_names) != 0: return __error_response(f'ARGS: NEEDED {needed_par_names} ACTUAL {data}')
    account = str(data.get('account'))
    password = str(data.get('password'))
    user_id = tables.user.login_and_get_id(account, password)
    is_success = user_id is not None
    if is_success:
        session['user_id'] = user_id
        session.permanent = True
    rlt_msg = {'is_success': f'{is_success}'}
    rlt_code = 200
    return json.jsonify(rlt_msg), rlt_code


@router.route('/meta', methods=['GET'])
def meta():
    user_id = session.get('user_id')
    if user_id is None: return __error_response('STATUS: EXPECT LOGIN STATE')
    meta_data = tables.user.get_meta(user_id)
    if meta_data is None: return __error_response('VALUE: USER_ID IS INCORRECT')
    rlt_msg = {'is_success': True, 'meta_data': meta_data}
    rlt_code = 200
    return json.jsonify(rlt_msg), rlt_code

