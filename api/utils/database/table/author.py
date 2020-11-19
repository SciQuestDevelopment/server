from typing import Dict, Any, List

from pymysql import Connection

from .abs_table import AbsTableHandler, AbsSqlStmtHolder


class AuthorStmts(AbsSqlStmtHolder):

    @property
    def create_db(self) -> str: return """
        CREATE TABLE IF NOT EXISTS post.Author (
            id   INTEGER auto_increment PRIMARY KEY,
            name VARCHAR (64) NOT NULL 
        );
    """

    @property
    def create_db_for_relation(self) -> str: return """
        CREATE TABLE IF NOT EXISTS post.Relation_Article_Author (
            id INTEGER auto_increment PRIMARY KEY,
            article_id INTEGER NOT NULL,
            author_id  INTEGER NOT NULL,
            CONSTRAINT Author_id_fk
                FOREIGN KEY (author_id) REFERENCES Author (id)
                    ON DELETE CASCADE,
            CONSTRAINT Article_id_fk
                FOREIGN KEY (article_id) REFERENCES Article (id)
                    ON DELETE CASCADE
        );
    """

    @property
    def select_by_pk(self) -> str: return """
        SELECT * FROM post.Author
        WHERE id=%(author_id)s
    """

    @property
    def select_ids_by_article_id(self) -> str: return """
        SELECT author_id FROM post.Relation_Article_Author
        WHERE article_id=%(article_id)s
    """


class AuthorTable(AbsTableHandler):

    def __init__(self, connection: Connection):
        super().__init__(connection, AuthorStmts())

    @property
    def _stmts_holder(self) -> AuthorStmts:
        holder = super(AuthorTable, self)._stmts_holder
        if not isinstance(holder, AuthorStmts): raise TypeError("IMPOSSIBLE")
        return holder

    def select_author_meta(self, author_id)-> Dict[str, Any]:
        output = dict()
        with self._db_connection.cursor() as cursor:
            cursor.execute(self._stmts_holder.select_by_pk, {'author_id': author_id})
            result = cursor.fetchone()
            output.update(result)
        return output

    def select_ids_of_article(self, article_id: int) -> List[int]:
        output = list()
        with self._db_connection.cursor() as cursor:
            cursor.execute(self._stmts_holder.select_ids_by_article_id, {'article_id': article_id})
            for row in cursor.fetchall(): output.append(row['author_id'])
        return output

