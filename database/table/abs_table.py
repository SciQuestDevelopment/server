import abc
from pymysql import Connection
from typing import Any, Dict


class AbsSqlStmtHolder(object):
    __metaclass__ = abc.ABCMeta

    @property
    @abc.abstractmethod
    def create_db(self) -> str: pass

    @property
    @abc.abstractmethod
    def insert(self) -> str: pass

    @property
    @abc.abstractmethod
    def delete_by_pk(self) -> str: pass

    @property
    @abc.abstractmethod
    def update_by_pk(self) -> str: pass

    @property
    @abc.abstractmethod
    def select_by_pk(self) -> str: pass


class AbsTableHandler(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, connection: Connection, stmts: AbsSqlStmtHolder):
        connection.execute(stmts.create_db).close()
        connection.commit()
        self.__db_stmts = stmts
        self.__db_connection = connection

    @property
    def _stmts_holder(self) -> AbsSqlStmtHolder:
        return self.__db_stmts

    @property
    def _db_connection(self) -> Connection:
        return self.__db_connection

    def _insert(self, parameters: Dict[str, Any]) -> Any:
        insert_sql = self.__db_stmts.insert
        exe_cursor = self.__db_connection.execute(insert_sql, parameters)
        result = exe_cursor.lastrowid
        exe_cursor.close()
        return result

    def _delete(self, unique_keys: Dict[str, Any]) -> Any:
        remove_sql = self.__db_stmts.delete_by_pk
        exe_cursor = self.__db_connection.execute(remove_sql, unique_keys)
        result = exe_cursor.lastrowid
        exe_cursor.close()
        return result

    def _update(self, unique_keys: Dict[str, Any], new_data: Dict[str, Any]) -> Any:
        update_sql = self.__db_stmts.insert
        parameters = unique_keys.update(new_data)
        exe_cursor = self.__db_connection.execute(update_sql, parameters)
        result = exe_cursor.lastrowid
        exe_cursor.close()
        return result

    def _select(self, unique_keys: Dict[str,Any]) -> Any:
        select_sql = self.__db_stmts.select_by_pk
        exe_cursor = self.__db_connection.execute(select_sql, unique_keys)
        primary_key_holder = exe_cursor.fetchone()
        result = primary_key_holder[0] if primary_key_holder is not None else None
        exe_cursor.close()
        return result

    def flash(self) -> Any:
        return self.__db_connection.commit()

