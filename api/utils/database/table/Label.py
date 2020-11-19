from pymysql import Connection

from .abs_table import AbsTableHandler, AbsSqlStmtHolder


class CategoryStmts(AbsSqlStmtHolder):

    @property
    def create_db(self) -> str: return """
        CREATE TABLE IF NOT EXISTS post.Category (
            id   INTEGER auto_increment PRIMARY KEY,
            name VARCHAR (64) NOT NULL,
            CONSTRAINT Category_name_uindex UNIQUE (name)
        )
    """

    @property
    def insert(self) -> str: return """
        INSERT INTO post.Category(name)
        VALUES (:name)
    """

    @property
    def delete_by_pk(self) -> str: return """
        DELETE FROM post.Category
        WHERE id=:id
    """

    @property
    def update_by_pk(self) -> str: return """
        UPDATE post.Category
        SET name=:name
        WHERE id=:id
    """

    @property
    def select_by_pk(self) -> str: return """
        SELECT * FROM post.Category
        WHERE id=:id
    """


class CategoryTable(AbsTableHandler):

    def __init__(self, connection: Connection):
        super().__init__(connection, CategoryStmts())

