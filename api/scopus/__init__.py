from flask import Blueprint

router = Blueprint('scopus', __name__)

from .views import *
