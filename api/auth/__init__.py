from flask import Blueprint

router = Blueprint('auth', __name__)

from .views import *