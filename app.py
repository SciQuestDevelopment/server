import io
import os
import logging

from flask import Flask, request, json, send_file

from database.tb_builder import TableBuilder

app = Flask(__name__)

try:
    table_builder = TableBuilder(
        host=os.environ.get('DB_URI'),
        port=os.environ.get('DB_PORT'),
        user=os.environ.get('DB_ACCOUNT'),
        password=os.environ.get('DB_PASSWORD')
    )
except TypeError as error:
    logging.exception('CANNOT INITIALISE SERVER, PLEASE CHECK THE CORRECTION OF THE ".env" FILE.')
    exit()


@app.route('/')
def get_all_apis():
    return json.jsonify({
        "Get meta data of a single article ": "GET /posts/meta/one?id=:post_id",
        "Get meta data of all articles": "GET /posts/meta/all",
        "Get meta data of multiple articles": "GET /posts/meta/range?query_num=:query_num&offset_num=:offset_num",
        "Get article content": "GET /posts/content?id=:post_id",
    })


@app.route('/posts/meta/one', methods=['GET'])
def get_post_meta():
    if 'id' not in request.args:
        rlt_msg = {'TYPE': 'SYNTAX', 'MSG': 'NO QUERY_NUM'}
        rlt_code = 404
    else:
        post_id = request.args.get('id')
        rlt_msg = table_builder.article.select_meta(post_id)
        rlt_msg['authors_list'] = table_builder.author.select_ids_of_article(post_id)
        rlt_code = 200
    return json.jsonify(rlt_msg), rlt_code


@app.route('/posts/meta/range', methods=['GET'])
def get_multi_posts_meta():
    try:
        if 'query_num' not in request.args:
            rlt_msg = {'TYPE': 'SYNTAX', 'MSG': 'NO QUERY_NUM'}
            rlt_code = 404
        else:
            query_num = int(request.args.get('query_num'))
            offset_num = int(request.args.get('offset_num', 0))
            main_metas = table_builder.article.select_multi_meta(query_num, offset_num)
            rlt_msg = list()
            for each_article in main_metas:
                each_article['authors_list'] = table_builder.author.select_ids_from_author(each_article['id'])
                rlt_msg.append(each_article)
            rlt_code = 200
    except TypeError as e:
        rlt_msg = {'TYPE': 'SYNTAX', 'MSG': 'INVALID QUERY_NUM'}
        rlt_code = 404
    return json.jsonify(rlt_msg), rlt_code


@app.route('/posts/meta/all', methods=['GET'])
def get_all_posts_meta():
    main_metas = table_builder.article.select_all_meta()
    rlt_msg = list()
    for each_article in main_metas:
        each_article['authors_list'] = table_builder.author.select_ids_from_author(each_article['id'])
        rlt_msg.append(each_article)
    return json.jsonify(rlt_msg), 200


@app.route('/posts/content', methods=['GET'])
def get_post_content():
    if 'id' not in request.args:
        return 'WARNING: INVALID SYNTAX (NO ARGUMENT ID)', 404
    post_id = request.args.get('id')
    binary_content = table_builder.article.select_content(post_id)
    return send_file(
        io.BytesIO(binary_content),
        mimetype='text/plain',
        as_attachment=True,
        attachment_filename=f'{post_id}.txt'
    )


@app.route('/authors/meta', methods=['GET'])
def get_author_meta():
    if 'id' not in request.args:
        rlt_msg = {'TYPE': 'SYNTAX', 'MSG': 'NO AUTHOR_ID'}
        rlt_code = 404
    else:
        author_id = request.args.get('id')
        rlt_msg = table_builder.author.select_author_meta(author_id)
        rlt_code = 200
    return json.jsonify(rlt_msg), rlt_code


@app.route('/authors/all_publishes', methods=['GET'])
def get_author_all_publishes():
    if 'id' not in request.args:
        rlt_msg = {'TYPE': 'SYNTAX', 'MSG': 'NO AUTHOR_ID'}
        rlt_code = 404
    else:
        author_id = request.args.get('id')
        rlt_msg = table_builder.article.select_ids_belong_author(author_id)
        rlt_code = 200
    return json.jsonify(rlt_msg), rlt_code


if __name__ == '__main__':
    app.run()
