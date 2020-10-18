from pymysql import Connection

from database.table.abs_table import AbsTableHandler, AbsSqlStmtHolder


class ArticleAuthorStmts(AbsSqlStmtHolder):

    @property
    def create_db(self) -> str: return """
        CREATE TABLE IF NOT EXISTS post.Relation_ArticleAuthor (
            id        INTEGER auto_increment primary key,
            articleID INTEGER NOT NULL,
            authorID  INTEGER NOT NULL,
            CONSTRAINT Author_Article_id_fk
                FOREIGN KEY(articleID) REFERENCES Article (id) ON DELETE CASCADE,
            CONSTRAINT Author_Author_id_fk
                FOREIGN KEY(authorID) REFERENCES Author (id) ON DELETE CASCADE
        );
    """

    @property
    def insert(self) -> str: return """
        INSERT INTO post.Relation_ArticleAuthor(articleID, authorID)
        VALUES (:articleID, :authorID)
    """

    @property
    def delete_by_pk(self) -> str: return """
        DELETE FROM post.Relation_ArticleAuthor
        WHERE id=:id
    """

    @property
    def update_by_pk(self) -> str: return """
        UPDATE post.Relation_ArticleAuthor
        SET name=:name
        WHERE id=:id
    """

    @property
    def select_by_pk(self) -> str: return """
        SELECT * FROM post.Relation_ArticleAuthor
        WHERE id=:id
    """


class ArticleAuthorTable(AbsTableHandler):

    def __init__(self, connection: Connection):
        super().__init__(connection, ArticleAuthorStmts())

