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
    def insert(self) -> str: return """
        INSERT INTO post.Author(name) 
        VALUES (:name)
    """

    @property
    def delete_by_pk(self) -> str: return """
        DELETE FROM post.Author 
        WHERE id=:id
    """

    @property
    def update_by_pk(self) -> str: return """
        UPDATE post.Author 
        SET name=:name
        WHERE id=:id
    """

    @property
    def select_by_pk(self) -> str: return """
        SELECT * FROM post.Author
        WHERE id=:id
    """


class AuthorTable(AbsTableHandler):

    def __init__(self, connection: Connection):
        super().__init__(connection, AuthorStmts())

