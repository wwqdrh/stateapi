"""
获取数据库实例
"""
import typing

import pydantic
import peewee


class DatabaseBuilder(typing.Protocol):
    def build(self) -> peewee.Database:
        pass


class ISqlite(pydantic.BaseModel):
    db: str

    def build(self) -> peewee.Database:
        return peewee.SqliteDatabase(self.db)


class IMysql(pydantic.BaseModel):
    username: str
    password: str
    db: str
    host: str = "localhost"
    port: int = 3306

    def build(self) -> peewee.Database:
        return peewee.MySQLDatabase(
            self.db,
            user=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
        )


class IPostgres(pydantic.BaseModel):
    username: str
    password: str
    db: str
    host: str = "localhost"
    port: int = 5432

    def build(self) -> peewee.Database:
        return peewee.MySQLDatabase(
            self.db,
            user=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
        )


class DatasourceManager:
    def __init__(self) -> None:
        self.__dbs: dict[str, peewee.Database] = dict()

    def register(self, name: str, builder: DatabaseBuilder):
        self.__dbs[name] = builder.build()

    def db(self, name: str):
        if (db := self.__dbs.get(name, None)) is None:
            raise Exception(f"{name}不是已经注册过的数据库")
        return db


DefaultManager = DatasourceManager()
