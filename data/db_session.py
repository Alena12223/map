import sqlalchemy as sa
# импорт библиотеки sqlalchemy (sa) - 'моста' между кодом на Python и SQL-базами данных
import sqlalchemy.orm as orm
# orm - интерфейс библиотеки sqlalchemy, позволяющий описывать таблицы БД через классы Python

from sqlalchemy.orm import Session
# Session - объект для взаимодействия с БД

SqlAlchemyBase = orm.declarative_base()
# Создает базовый класс для всех моделей БД с помощью функции declarative_base

__factory = None
# __ - переменная не экспортируется при импорте
# __factory будет хранить фабрику сессий

def global_init(db_file):
    # подключение к конкретной базе данных
    global __factory
    # указывает на то, что внтри функции будет изменяться глобальная переменная __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    #?check_same_thread = False — параметр для SQLite: разрешает использовать соединение из разных потоков
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)
    # создание движка для взаимодействия с БД
    # echo=False - если True, все запросы будут выводиться

    __factory = orm.sessionmaker(bind=engine)
    # создание фабрики сессий __factory с помощью sessionmaker()
    # bind=engine привязывает фабрику к созданному движку
    # фабрика будет создавать сессии, подключенные к этой БД

    SqlAlchemyBase.metadata.create_all(engine)
    # metadata - метаданные всех моделей
    # metadata.create_all(engine) - выполнение SQL-команд CREATE TABLE для несуществующих таблиц


def create_session() -> Session:
    global __factory
    # использование глобальной переменной __factory
    return __factory()
    # вызывает фабрику, которая создает и возвращает новый объект Session
