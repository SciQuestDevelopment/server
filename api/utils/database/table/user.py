import hashlib
import logging
from typing import Optional, Tuple

from pymysql import Connection, IntegrityError
from .abs_table import AbsTableHandler, AbsSqlStmtHolder


class UserStmts(AbsSqlStmtHolder):

    @property
    def create_db(self) -> str: return """
        create table IF NOT EXISTS main.User (
            id              int auto_increment
                primary key,
            first_name      varchar(64)                         not null,
            second_name     varchar(64)                         not null,
            account_name    varchar(128)                        not null,
            password_hash   varchar(128)                        not null,
            phone_num       varchar(11)                         null,
            email_address   varchar(128)                        null,
            created_time    timestamp default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP,
            last_login_time timestamp default CURRENT_TIMESTAMP not null,
            profile         blob                                null,
            constraint User_account_name_uindex
                unique (account_name),
            constraint User_email_address_uindex
                unique (email_address),
            constraint User_phone_num_uindex
                unique (phone_num)
        );
    """

    @property
    def insert_new_user(self) -> str: return """
        INSERT INTO main.User(
            first_name, second_name, 
            account_name, password_hash, 
            phone_num, email_address
        )
        VALUE (
            %(first_name)s, %(second_name)s, 
            %(account_name)s, %(password_hash)s, 
            %(phone_num)s, %(email_address)s
        )
    """

    @property
    def select_id(self) -> str: return """
        SELECT id FROM main.User
        WHERE account_name = %(account_name)s
            AND password_hash = %(password_hash)s
    """

    @property
    def select_user_info_by_id(self) -> str: return """
        SELECT * FROM main.User
        WHERE id = %(user_id)s
    """

    @property
    def update_login_time(self) -> str: return """
        UPDATE main.User SET last_login_time = CURRENT_TIMESTAMP
        WHERE id = %(user_id)s
    """


class UserTable(AbsTableHandler):

    def __init__(self, connection: Connection):
        super().__init__(connection, UserStmts())

    @property
    def _stmts_holder(self) -> UserStmts:
        holder = super(UserTable, self)._stmts_holder
        if not isinstance(holder, UserStmts): raise TypeError("IMPOSSIBLE")
        return holder

    def register(
            self, first_name: str, second_name: str,
            account_name: str, password: str,
            phone_num: str, email_address: str
    ) -> bool:
        password_hash = hashlib.sha224(str.encode(password)).hexdigest()
        insrt_stmt = self._stmts_holder.insert_new_user
        insrt_pars = {
            'first_name': first_name, 'second_name': second_name,
            'account_name': account_name, 'password_hash': password_hash,
            'phone_num': phone_num, 'email_address': email_address
        }
        try:
            cursor = self._db_connection.cursor()
            cursor.execute(insrt_stmt, insrt_pars)
            cursor.close()
            self._db_connection.commit()
            return True
        except IntegrityError as exc:
            logging.debug(exc)
            return False

    def login_and_get_id(self, account_name: str, password: str) -> Optional[int]:
        try:
            cursor = self._db_connection.cursor()
            slct_stmt = self._stmts_holder.select_id
            password_hash = hashlib.sha224(str.encode(password)).hexdigest()
            slct_pars = {'account_name': account_name, 'password_hash': password_hash}
            cursor.execute(slct_stmt, slct_pars)
            query_result = cursor.fetchone()
            if query_result is None or 'id' not in query_result: return None
            user_id = query_result.get('id')
            updt_stmt = self._stmts_holder.update_login_time
            cursor.execute(updt_stmt, {'user_id': user_id})
            cursor.close()
            return user_id
        except IntegrityError as exc:
            logging.debug(exc)
            return None

    def get_meta(self, user_id) -> Optional[Tuple[str, str]]:
        with self._db_connection.cursor() as cursor:
            slct_stmt = self._stmts_holder.select_user_info_by_id
            cursor.execute(slct_stmt, {'user_id': user_id})
            query_result = cursor.fetchone()
            if query_result is None: return None
        return query_result
