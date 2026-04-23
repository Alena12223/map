import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Jobs(SqlAlchemyBase):
    __tablename__ = 'jobs'

    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True
    )

    team_leader = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("users.id")
        # внешний ключ с таблицей users
    )

    job = sqlalchemy.Column(
        sqlalchemy.String
    )

    work_size = sqlalchemy.Column(
        sqlalchemy.Integer
    )

    collaborators = sqlalchemy.Column(
        sqlalchemy.String
    )

    start_date = sqlalchemy.Column(
        sqlalchemy.DateTime,
        default=datetime.datetime.now
    )

    end_date = sqlalchemy.Column(
        sqlalchemy.DateTime
    )

    is_finished = sqlalchemy.Column(
        sqlalchemy.Boolean
    )

    is_private = sqlalchemy.Column(sqlalchemy.Boolean, default=True)

    user = orm.relationship('User', foreign_keys=[team_leader], back_populates='jobs')
