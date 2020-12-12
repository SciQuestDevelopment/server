import abc
from typing import Any

from pymysql import Connection


class AbsSqlStmtHolder(object):
    __metaclass__ = abc.ABCMeta

    @property
    @abc.abstractmethod
    def create_db(self) -> str: pass


class AbsTableHandler(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, connection: Connection, stmts: AbsSqlStmtHolder):
        with connection.cursor() as cursor:
            cursor.execute(stmts.create_db)
            connection.commit()
        self.__db_stmts = stmts
        self.__db_connection = connection

    @property
    def _stmts_holder(self) -> AbsSqlStmtHolder:
        return self.__db_stmts

    @property
    def _db_connection(self) -> Connection:
        self.__db_connection.ping(reconnect=True)
        return self.__db_connection

    def flash(self) -> Any:
        return self.__db_connection.commit()
