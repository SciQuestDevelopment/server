import re
from datetime import datetime
from typing import Any, Optional


class Post(object):

    def __init__(self, handler_factory):
        self.__table_handler = handler_factory
