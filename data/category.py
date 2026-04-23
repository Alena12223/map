import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase

# Промежуточная таблица для связи многие-ко-многим
association_table = sqlalchemy.Table(
    'association',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('news_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('jobs.id')),
    sqlalchemy.Column('category_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('category.id'))
)


class Category(SqlAlchemyBase):
    __tablename__ = 'category'

    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True
    )

    name = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=True
    )
