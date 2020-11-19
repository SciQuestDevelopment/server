from typing import Dict, Any, List, Optional

from pymysql import Connection
from .abs_table import AbsTableHandler, AbsSqlStmtHolder


class ArticleStmts(AbsSqlStmtHolder):

    @property
    def create_db(self) -> str: return """
        CREATE TABLE IF NOT EXISTS post.Article (
            id           INTEGER auto_increment primary key,
            doi          VARCHAR(128) NULL,
            url          VARCHAR(128) NULL,
            title        TINYTEXT     NOT NULL,
            venue        VARCHAR(256) NULL,
            summary      MEDIUMTEXT   NULL,
            content      MEDIUMBLOB   NULL,
            publish_date DATE         NULL,

            CONSTRAINT Article_doi_uindex UNIQUE (doi),
            CONSTRAINT Article_url_uindex UNIQUE (url)
        )
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
    def select_meta_by_pk(self) -> str: return """
        SELECT id, doi, url, title, venue, summary, publish_date
        FROM post.Article
        WHERE id=%(post_id)s 
    """

    @property
    def select_content_by_pk(self) -> str: return """
        SELECT content
        FROM post.Article
        WHERE id=%(post_id)s
    """

    @property
    def select_meta_n_rows_with_offset(self) -> str: return """
        SELECT id, doi, url, title, venue, summary, publish_date
        FROM post.Article
        ORDER BY id
        LIMIT %(offset_num)s, %(query_num)s
    """

    @property
    def select_all_meta(self) -> str: return """
        SELECT id, doi, url, title, venue, summary, publish_date
        FROM post.Article
    """

    @property
    def select_all_ids_by_author_id(self) -> str: return """
        SELECT * FROM post.Relation_Article_Author
        WHERE author_id=%(author_id)s
    """


class ArticleTable(AbsTableHandler):

    def __init__(self, connection: Connection):
        super().__init__(connection, ArticleStmts())

    @property
    def _stmts_holder(self) -> ArticleStmts:
        holder = super(ArticleTable, self)._stmts_holder
        if not isinstance(holder, ArticleStmts): raise TypeError("IMPOSSIBLE")
        return holder

    def __select_by_id(self, slc_stmts: str, post_id: int) -> Dict[str, Any]:
        output = dict()
        with self._db_connection.cursor() as cursor:
            cursor.execute(slc_stmts, {'post_id': post_id})
            result = cursor.fetchone()
            output.update(result)
        return output

    def select_meta(self, post_id: int) -> Dict[str, Any]:
        select_meta_sql = self._stmts_holder.select_meta_by_pk
        return self.__select_by_id(select_meta_sql, post_id)

    def select_content(self, post_id: int) -> Any:
        select_meta_sql = self._stmts_holder.select_content_by_pk
        return self.__select_by_id(select_meta_sql, post_id).get('content', None)

    def __select_multi_row(self, slc_stmts: str, pars: Optional[Dict] = None) -> List[Dict[str, Any]]:
        output = list()
        with self._db_connection.cursor() as cursor:
            cursor.execute(slc_stmts, pars)
            result = cursor.fetchall()
            output.extend(result)
        return output

    def select_multi_meta(self, query_num: int, offset_num: int = 0) -> List[Dict[str, Any]]:
        sql_stmts = self._stmts_holder.select_meta_n_rows_with_offset
        sql_pars = {'query_num': query_num, 'offset_num': offset_num}
        return self.__select_multi_row(sql_stmts, sql_pars)

    # The method should not be used in the real project.
    # Use the `select_multi_meta` to replace when needed.
    def select_all_meta(self) -> List[Dict[str, Any]]:
        sql_stmts = self._stmts_holder.select_all_meta
        return self.__select_multi_row(sql_stmts)

    def select_ids_belong_author(self, author_id: int) -> List[int]:
        output = list()
        with self._db_connection.cursor() as cursor:
            cursor.execute(self._stmts_holder.select_all_ids_by_author_id, {'author_id': author_id})
            for row in cursor.fetchall(): output.append(row['article_id'])
        return output
