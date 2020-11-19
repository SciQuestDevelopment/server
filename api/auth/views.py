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


@router.route('/register', methods=['POST'])
def register():
    account = request.json.get('account')
    password = request.json.get('password')
    first_name = request.json.get('first_name')
    second_name = request.json.get('second_name')
    phone_num = request.json.get('phone_num')
    email_address = request.json.get('email_address')
    is_success = tables.user.register(first_name, second_name, account, password, phone_num, email_address)
    rlt_msg = {'is_success': f'{is_success}'}
    rlt_code = 200
    return json.jsonify(rlt_msg), rlt_code


@router.route('/login', methods=['POST'])
def login():
    account = request.json.get('account')
    password = request.json.get('password')
    is_success = tables.user.login(account, password)
    if is_success: session['username'] = account
    # activate session usage
    session.permanent = True
    rlt_msg = {'is_success': f'{is_success}'}
    rlt_code = 200
    return json.jsonify(rlt_msg), rlt_code
