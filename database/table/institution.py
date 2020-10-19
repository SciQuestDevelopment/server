from pymysql import Connection

from database.table.abs_table import AbsTableHandler, AbsSqlStmtHolder


class InstitutionStmts(AbsSqlStmtHolder):

    @property
    def create_db(self) -> str: return """
        CREATE TABLE IF NOT EXISTS post.Institution (
            id   INTEGER auto_increment PRIMARY KEY,
            name VARCHAR (64) NOT NULL,
        )
    """

    @property
    def insert(self) -> str: return """
        INSERT INTO post.Institution (name) 
        VALUES (:name)
    """

    @property
    def delete_by_pk(self) -> str: return """
        DELETE FROM post.Institution 
        WHERE id=:id
    """

    @property
    def update_by_pk(self) -> str: return """
        UPDATE post.Institution 
        SET name=:name
        WHERE id=:id
    """

    @property
    def select_by_pk(self) -> str: return """
        SELECT * FROM post.Institution 
        WHERE id=:id
    """


class InstitutionTable(AbsTableHandler):

    def __init__(self, connection: Connection):
        super().__init__(connection, ArticleStmts())

