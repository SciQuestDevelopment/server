from . import router
from flask import request, json
from ..utils.datasource.springer_nature import springer
from ..utils.datasource.elsevier import elsevier
from ..utils.datasource.nature import nature


@router.route('/', methods=['GET'])
def get_all_apis():
    return json.jsonify({
        'springer': 'GET /springer?{param..}',
        'springer_params info': 'https://dev.springernature.com/adding-constraints',
        'elsevier': 'GET /elsevier?{param..}',
        'elsevier_params info': 'https://dev.elsevier.com/sc_search_tips.html',
        'nature': 'GET /nature?keyword=:keyword'
    })


@router.route('/springer', methods=['GET'])
def query_springer():
    rlt_msg = request.args
    api = springer('metadata')
    result = api.query(dict(rlt_msg))
    return json.jsonify(result), 200


@router.route('/elsevier', methods=['GET'])
def query_elsevier():
    rlt_msg = request.args
    api = elsevier('scopus')
    result = api.query(dict(rlt_msg))
    return json.jsonify(result), 200

@router.route('/nature', methods=['GET'])
def query_nature():
    rlt_msg = request.args
    api = nature()
    if 'keyword' not in rlt_msg:
        return 'ERROR: INVALID SYNTAX (NO KEYWORD)', 404
    keyword = request.args.get('keyword')
    result = api.query(keyword)
    return json.jsonify(result), 200