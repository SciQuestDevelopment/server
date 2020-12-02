import io
import os

from . import router
from flask import request, json, send_file
from ..utils.database.tb_builder import tables



@router.route('/', methods=['GET'])
def get_all_apis():
    return json.jsonify({
        'Meta of an article': 'GET /meta/one?id=:post_id',
        'Meta of all articles': 'GET /meta/all',
        'Meta of specific articles': 'GET /meta/range?query_num=:query_num&offset_num=:offset_num',
        'Content of an article': 'GET /content?id=:post_id',
        'Meta of an author': 'GET /author/meta?id=:author_id',
        'Meta of all articles from an author': 'GET /author/all_publishes?id=:author_id',
    })


@router.route('/meta/one', methods=['GET'])
def get_post_meta():
    if 'id' not in request.args:
        rlt_msg = {'TYPE': 'SYNTAX', 'MSG': 'NO QUERY_NUM'}
        rlt_code = 404
    else:
        post_id = request.args.get('id')
        rlt_msg = tables.article.select_meta(post_id)
        rlt_msg['authors_list'] = tables.author.select_ids_of_article(post_id)
        rlt_code = 200
    return json.jsonify(rlt_msg), rlt_code


@router.route('/meta/range', methods=['GET'])
def get_multi_articles_meta():
    try:
        if 'query_num' not in request.args:
            rlt_msg = {'TYPE': 'SYNTAX', 'MSG': 'NO QUERY_NUM'}
            rlt_code = 404
        else:
            query_num = int(request.args.get('query_num'))
            offset_num = int(request.args.get('offset_num', 0))
            main_metas = tables.article.select_multi_meta(query_num, offset_num)
            rlt_msg = list()
            for each_article in main_metas:
                each_article['authors_list'] = tables.author.select_ids_from_author(each_article['id'])
                rlt_msg.append(each_article)
            rlt_code = 200
    except TypeError as e:
        rlt_msg = {'TYPE': 'SYNTAX', 'MSG': 'INVALID QUERY_NUM'}
        rlt_code = 404
    return json.jsonify(rlt_msg), rlt_code


@router.route('/meta/all', methods=['GET'])
def get_all_articles_meta():
    main_metas = tables.article.select_all_meta()
    rlt_msg = list()
    for each_article in main_metas:
        each_article['authors_list'] = tables.author.select_ids_from_author(each_article['id'])
        rlt_msg.append(each_article)
    return json.jsonify(rlt_msg), 200


@router.route('/content', methods=['GET'])
def get_post_content():
    if 'id' not in request.args:
        return 'WARNING: INVALID SYNTAX (NO ARGUMENT ID)', 404
    post_id = request.args.get('id')
    binary_content = tables.article.select_content(post_id)
    return send_file(
        io.BytesIO(binary_content),
        mimetype='text/plain',
        as_attachment=True,
        attachment_filename=f'{post_id}.txt'
    )


@router.route('/authors/meta', methods=['GET'])
def get_author_meta():
    if 'id' not in request.args:
        rlt_msg = {'TYPE': 'SYNTAX', 'MSG': 'NO AUTHOR_ID'}
        rlt_code = 404
    else:
        author_id = request.args.get('id')
        rlt_msg = tables.author.select_author_meta(author_id)
        rlt_code = 200
    return json.jsonify(rlt_msg), rlt_code


@router.route('/authors/all_publishes', methods=['GET'])
def get_author_all_publishes():
    if 'id' not in request.args:
        rlt_msg = {'TYPE': 'SYNTAX', 'MSG': 'NO AUTHOR_ID'}
        rlt_code = 404
    else:
        author_id = request.args.get('id')
        rlt_msg = tables.article.select_ids_belong_author(author_id)
        rlt_code = 200
    return json.jsonify(rlt_msg), rlt_code


@router.route('/test', methods=['GET'])
def test_path():
    return os.path.abspath(os.path.dirname(__file__))

