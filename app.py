from flask import Flask, request, json
from flask_mysqldb import MySQL
import yaml
app = Flask(__name__)

db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_PORT'] = db['mysql_port']
app.config['MYSQL_USER '] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

@app.route('/')
def hello_world():
    return json.jsonify({
        "Get article details": "GET /post/:post_id",
        "Get all article details": "GET /post",
        "Get all article details of a user": "GET /posts/author/:userID",
        "Creat a article": "PUT /post",
        "Delete a article": "DELETE /posts/:postID",
        "Modify details of a article": "POST /posts/:postID"
    })


@app.route('/post/<post_id>', methods=['GET'])
def get_post(post_id: str):
    return f'Get article details of {post_id}'


@app.route('/post', methods=['GET'])
def get_all_post():
    return 'Get all article details of a user'


@app.route('/posts/author/<user_id>', methods=['GET'])
def get_all_post_of_author(user_id: str):
    return f'Get all article details of a user {user_id}'


@app.route('/post', methods=['PUT'])
def create_post():
    json_body = request.get_json()
    return json_body if json_body is not None else {}


@app.route('/post/<post_id>', methods=['DELETE'])
def delete_post(post_id: str):
    return f'Delete a article {post_id}'


@app.route('/post/<post_id>', methods=['POST'])
def update_post(post_id: str):
    return f'Modify details of a article {post_id}'


if __name__ == '__main__':
    app.run()
