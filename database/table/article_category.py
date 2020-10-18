from pymysql import Connection

from database.table.abs_table import AbsTableHandler, AbsSqlStmtHolder


class ArticleCategoryStmts(AbsSqlStmtHolder):

    @property
    def create_db(self) -> str: return """
        CREATE TABLE IF NOT EXISTS Relation_ArticleCategory (
            id          int auto_increment primary key,
            post_id     int not null comment '文章外键, 设置链接删除, 当主表Row删除时此表对应Rows将被删除',
            category_id int not null comment '分类外键, 设置链接删除, 当主表Row删除时此表对应Rows将被删除',
            constraint Classification_Article_id_fk
                foreign key (post_id) references Article (id)
                    on update cascade on delete cascade,
            constraint Classification_Category_id_fk
                foreign key (category_id) references Category (id)
                    on update cascade on delete cascade
        ) comment '文章和类别之间存在的分类关系';
    """

    @property
    def insert(self) -> str: return """
        INSERT INTO post.Relation_ArticleCategory(post_id, category_id)
        VALUES (:post_id, :category_id)
    """

    @property
    def delete_by_pk(self) -> str: return """
        DELETE FROM post.Relation_ArticleCategory
        WHERE id=:id
    """

    @property
    def update_by_pk(self) -> str: return """
        UPDATE post.Relation_ArticleCategory
        SET name=:name
        WHERE id=:id
    """

    @property
    def select_by_pk(self) -> str: return """
        SELECT * FROM post.Relation_ArticleCategory
        WHERE id=:id
    """


class ArticleCategoryTable(AbsTableHandler):

    def __init__(self, connection: Connection):
        super().__init__(connection, ArticleCategoryStmts())

