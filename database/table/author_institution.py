from pymysql import Connection

from database.table.abs_table import AbsTableHandler, AbsSqlStmtHolder


class AuthorInstitutionStmts(AbsSqlStmtHolder):

    @property
    def create_db(self) -> str: return """
        CREATE TABLE IF NOT EXISTS Relation_AuthorInstitution (
            id             int auto_increment primary key,
            author_id      int not null,
            institution_id int not null,
            constraint Relation_AuthorInstitution_Author_id_fk
                foreign key (author_id) references Author (id)
                    on delete cascade,
            constraint Relation_AuthorInstitution_Institution_id_fk
                foreign key (institution_id) references Institution (id)
                    on delete cascade
        );
    """

    @property
    def insert(self) -> str: return """
        INSERT INTO post.Relation_AuthorInstitution(ArticleID, InstitutionID)
        VALUES (:author_id, :institution_id)
    """

    @property
    def delete_by_pk(self) -> str: return """
        DELETE FROM post.Relation_AuthorInstitution
        WHERE id=:id
    """

    @property
    def update_by_pk(self) -> str: return """
        UPDATE post.Relation_AuthorInstitution
        SET name=:name
        WHERE id=:id
    """

    @property
    def select_by_pk(self) -> str: return """
        SELECT * FROM post.Relation_ArticleInstitution
        WHERE id=:id
    """


class AuthorInstitutionTable(AbsTableHandler):

    def __init__(self, connection: Connection):
        super().__init__(connection, AuthorInstitutionStmts())

