import io
import os

from flask import Flask, request, json, send_file

from database.tb_builder import TableBuilder

app = Flask(__name__)

table_builder = TableBuilder(
    host=os.environ.get('DB_URI'),
    port=os.environ.get('DB_PORT'),
    user=os.environ.get('DB_ACCOUNT'),
    password=os.environ.get('DB_PASSWORD')
)


@app.route('/')
def hello_world():
    return json.jsonify({
        "Get article meta": "GET /posts/meta/one?id=:post_id",
        "Get multiple articles meta": "GET /posts/meta/all?query_num=:query_num&offset_num=:offset_num",
        "Get article content": "GET /posts/content?id=:post_id",
    })


@app.route('/posts/meta/one', methods=['GET'])
def get_post_meta():
    if 'id' not in request.args:
        return 'WARNING: INVALID SYNTAX (NO ARGUMENT ID)', 404
    post_id = request.args.get('id')
    result = table_builder.article.select_meta(post_id)
    return json.jsonify(result)


@app.route('/posts/meta/all', methods=['GET'])
def get_all_posts_meta():
    output = list()
    query_num = int(request.args.get('query_num', 0))
    offset_num = int(request.args.get('offset_num', 0))
    if query_num == 0:
        result = table_builder.article.select_all_meta()
    else:
        result = table_builder.article.select_multi_meta(query_num, offset_num)
    output.extend(result)
    return json.jsonify(output)


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
        attachment_filename='%s.txt' % post_id
    )


if __name__ == '__main__':
    app.run()
