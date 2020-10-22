from typing import Dict, Optional, Any

import pymysql
from database.table.article import ArticleTable


class TableBuilder(object):

    def __init__(self, host: str, port: str, user: str, password: str):
        self.__connection = pymysql.connect(
            host=host, port=int(port), user=user, password=password,
            cursorclass=pymysql.cursors.DictCursor
        )
        self.__article_tb: Optional[ArticleTable] = None

    @property
    def article(self) -> ArticleTable:
        if self.__article_tb is None:
            self.__article_tb = ArticleTable(self.__connection)
        return self.__article_tb
