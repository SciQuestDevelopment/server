from pymysql import Connection

from database.table.abs_table import AbsTableHandler, AbsSqlStmtHolder


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
    def insert(self) -> str: return """
        INSERT INTO post.Article(doi, url, title, venue, summary, content, publish_date) 
        VALUES (:doi, :url, :title, :venue, :summary, :content, :publish_date)
    """

    @property
    def delete_by_pk(self) -> str: return """
        DELETE FROM post.Article 
        WHERE id=:id
    """

    @property
    def update_by_pk(self) -> str: return """
        UPDATE 
            post.Article 
        SET    
            doi=:doi, 
            url=:url, 
            title=:title, 
            venue=:venue, 
            summary=:summary, 
            content=:content, 
            publish_date=:publish_date 
        WHERE 
            id=:id
    """

    @property
    def select_by_pk(self) -> str: return """
        SELECT * FROM post.Article
        WHERE id=:id
    """


class ArticleTable(AbsTableHandler):

    def __init__(self, connection: Connection):
        super().__init__(connection, ArticleStmts())

