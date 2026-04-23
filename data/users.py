import datetime
# модуль datetime необходим для работы с датами и временем
import sqlalchemy
# доступ к базовым типам данных для создания БД
from sqlalchemy import orm
# для связи между таблицами
from .db_session import SqlAlchemyBase
# импортирует класс для всех моделей БД
from werkzeug.security import generate_password_hash, check_password_hash
# werkzeug.security - одуль безопасности
# generate_password_hash(password) - создает хеш пароля (для безопасного хранения)
# check_password_hash(hashed_password, password) - проверяет, совпадает ли введенный пароль с хешем
from flask_login import UserMixin
# мискин добавляет к классу User стандартные методы и атрибуты для работы с аутентификацией
# is_authenticated - авторизован ли пользователь

class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'
    # имя таблицы

    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True
    )
    # primary_key - первичный ключ таблицы (уникальный идентификатор)
    # autoincrement - генерируется автоматически при добавлении новой записи

    surname = sqlalchemy.Column(
        sqlalchemy.String
    )

    name = sqlalchemy.Column(
        sqlalchemy.String,
    )

    age = sqlalchemy.Column(
        sqlalchemy.Integer
    )

    position = sqlalchemy.Column(
        sqlalchemy.String
    )

    speciality = sqlalchemy.Column(
        sqlalchemy.String
    )

    address = sqlalchemy.Column(
        sqlalchemy.String
    )

    email = sqlalchemy.Column(
        sqlalchemy.String,
        unique=True,
    )

    hashed_password = sqlalchemy.Column(
        sqlalchemy.String,
    )

    modified_date = sqlalchemy.Column(
        sqlalchemy.DateTime,
        default=datetime.datetime.now
    )

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)
        # создает безопасный хеш

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    # Обратная связь с таблицей Jobs
    jobs = orm.relationship('Jobs', back_populates='user', lazy='dynamic')
    # 'Jobs' - имя связанной таблицы
    # back_populates='user' - в модели Jobs должно быть поле user, ссылающееся на User
    # lazy='dynamic' - при обращении к user.jobs не загружаются все записи сразу
