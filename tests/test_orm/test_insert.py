import pathlib
from datetime import date

from peewee import SqliteDatabase

from stateapi.pkg.orm import insert, builder, base

testdata = pathlib.Path(__file__).parents[0] / "testdata"

db = SqliteDatabase(str(testdata / "people.db"))


def test_insert_one():
    table_name = "test_insert_one"
    model = builder.build_model(
        db,
        table_name,
        [
            builder.Field("id", base.FieldType.idx),
            builder.Field("name", base.FieldType.char),
            builder.Field("birthday", base.FieldType.date),
        ],
        create=True,
        clean=True,
    )

    res = insert.insert_one(
        db, table_name, returns="id", name="zhangsan", birthday=date(1935, 3, 1)
    )
    res2 = insert.insert_one(
        db, table_name, name="zhangsan1", birthday=date(1935, 3, 1)
    )
    print(res, res2)
