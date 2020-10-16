import abc
from pymysql import Connection
from typing import Any


class AbsSqlStmtHolder(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def create_db_stmt(self) -> str: pass

    @abc.abstractmethod
    def insert_row_stmt(self) -> str: pass

    @abc.abstractmethod
    def select_primary_key_stmt(self) -> str: pass

    @abc.abstractmethod
    def remove_primary_key_stmt(self) -> str: pass


class AbsTableHandler(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, connection: Connection, stmts: AbsSqlStmtHolder):
        connection.execute(stmts.create_db_stmt()).close()
        connection.commit()
        self.__db_stmts = stmts
        self.__db_connection = connection

    def _get_stmts_holder(self) -> AbsSqlStmtHolder:
        return self.__db_stmts

    def _get_db_connection(self) -> Connection:
        return self.__db_connection

    def _select_primary_key(self, **unique_keys) -> Any:
        select_sql = self.__db_stmts.select_primary_key_stmt()
        exe_cursor = self.__db_connection.execute(select_sql, unique_keys)
        primary_key_holder = exe_cursor.fetchone()
        result = primary_key_holder[0] if primary_key_holder is not None else None
        exe_cursor.close()
        return result

    def _insert_new_row(self, **parameters) -> Any:
        insert_sql = self.__db_stmts.insert_row_stmt()
        exe_cursor = self.__db_connection.execute(insert_sql, parameters)
        result = exe_cursor.lastrowid
        exe_cursor.close()
        return result

    def flash(self) -> Any:
        return self.__db_connection.commit()
