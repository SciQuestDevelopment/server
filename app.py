import datetime
import os

from flask import Flask, make_response
from flask_cors import CORS

from api import auth, post

app = Flask(__name__)
# 24bits random secret key
app.config['SECRET_KEY'] = f'{os.urandom(24)}'
app.permanent_session_lifetime = datetime.timedelta(minutes=30)

# Blueprint to the apis for authentication
app.register_blueprint(auth.router, url_prefix='/auth')
# Blueprint to the apis for CRUD post related data
app.register_blueprint(post.router, url_prefix='/post')

# CORS to allow the cross-domain issues
CORS(app, supports_credentials=True)


@app.after_request
def after(resp):
    resp = make_response(resp)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST'
    resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return resp


if __name__ == '__main__':
    app.run()
