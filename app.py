import os
import datetime
from flask import Flask
from flask_cors import CORS

from dotenv import load_dotenv
# Set environment variables for APIs
dotenv_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '.env')
if os.path.exists(dotenv_path): load_dotenv(dotenv_path, override=True)

from api import auth, post, scopus
app = Flask(__name__)
# 24bits random secret key
app.config['SECRET_KEY'] = f'{os.urandom(24)}'
app.permanent_session_lifetime = datetime.timedelta(minutes=30)
# CORS to allow the cross-domain issues
CORS(app, supports_credentials=True)

# Blueprint to the apis for authentication
app.register_blueprint(auth.router, url_prefix='/auth')
# Blueprint to the apis for CRUD post related data
app.register_blueprint(post.router, url_prefix='/post')
# Blueprint to the apis for scopus searching
app.register_blueprint(scopus.router, url_prefix='/scopus')

if __name__ == '__main__':
    app.run()
