from pymysql import Connection

from database.table.abs_table import AbsTableHandler, AbsSqlStmtHolder


class ArticleInstitutionStmts(AbsSqlStmtHolder):

    @property
    def create_db(self) -> str: return """
        CREATE TABLE IF NOT EXISTS Relation_ArticleInstitution(
            id            int auto_increment
                primary key,
            ArticleID     int not null,
            InstitutionID int not null,
            constraint Institution_Article_id_fk
                foreign key (ArticleID) references Article (id)
                    on delete cascade,
            constraint Institution_Institution_id_fk
                foreign key (InstitutionID) references Institution (id)
                    on delete cascade
        );
    """

    @property
    def insert(self) -> str: return """
        INSERT INTO post.Relation_ArticleInstitution(ArticleID, InstitutionID)
        VALUES (:ArticleID, :InstitutionID)
    """

    @property
    def delete_by_pk(self) -> str: return """
        DELETE FROM post.Relation_ArticleInstitution
        WHERE id=:id
    """

    @property
    def update_by_pk(self) -> str: return """
        UPDATE post.Relation_ArticleInstitution
        SET name=:name
        WHERE id=:id
    """

    @property
    def select_by_pk(self) -> str: return """
        SELECT * FROM post.Relation_ArticleInstitution
        WHERE id=:id
    """


class ArticleCategoryTable(AbsTableHandler):

    def __init__(self, connection: Connection):
        super().__init__(connection, ArticleCategoryStmts())

