from flask import Blueprint

router = Blueprint('post', __name__)

from .views import *
