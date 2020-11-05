from typing import Dict, Optional, Any

import pymysql
from database.table.article import ArticleTable
from database.table.author import AuthorTable


class TableBuilder(object):

    def __init__(self, host: str, port: str, user: str, password: str):
        self.__connection = pymysql.connect(
            host=host, port=int(port), user=user, password=password,
            cursorclass=pymysql.cursors.DictCursor
        )
        self.__article_tb: Optional[ArticleTable] = None
        self.__author_tb: Optional[AuthorTable] = None

    @property
    def article(self) -> ArticleTable:
        if self.__article_tb is None:
            self.__article_tb = ArticleTable(self.__connection)
        return self.__article_tb

    @property
    def author(self) -> AuthorTable:
        if self.__author_tb is None:
            self.__author_tb = AuthorTable(self.__connection)
        return self.__author_tb
