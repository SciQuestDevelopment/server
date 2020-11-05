from pymysql import Connection

from database.table.abs_table import AbsTableHandler, AbsSqlStmtHolder


class AuthorStmts(AbsSqlStmtHolder):

    @property
    def create_db(self) -> str: return """
        CREATE TABLE Author (
            id   INTEGER auto_increment PRIMARY KEY,
            name VARCHAR (64) NOT NULL 
        );
    """

    @property
    def select_by_pk(self) -> str: return """
        SELECT * FROM post.Author
        WHERE id=:id
    """


class AuthorTable(AbsTableHandler):

    def __init__(self, connection: Connection):
        super().__init__(connection, AuthorStmts())

    @property
    def _stmts_holder(self) -> AuthorStmts:
        holder = super(AuthorTable, self)._stmts_holder
        if not isinstance(holder, AuthorStmts): raise TypeError("IMPOSSIBLE")
        return holder


