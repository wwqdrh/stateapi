from pathlib import Path
from datetime import date

from peewee import SqliteDatabase

from stateapi.pkg.orm import builder, query, spec, base, delete, insert

testdata = Path(__file__).parents[0] / "testdata"

db = SqliteDatabase(str(testdata / "people.db"))


def test_delete_record():
    table_name = "test_delete_record"
    model, exist = builder.build_model(
        db,
        table_name,
        [
            builder.Field("name", base.FieldType.char),
            builder.Field("tag", base.FieldType.char),
        ],
        create=True,
        clean=True,
    )
    assert exist is True
    model.create(name="Grandma", tag="test")
    model.create(name="Grandma1", tag="test")
    res = query.query_one(
        db,
        table_name,
        [base.Query(name="name", op=base.QueryType.eq, mode="char", value="Grandma")],
        [],
        "*",
    )
    print(res)
    delete.delete_record(
        db, table_name, [base.Query(name="name", op=base.QueryType.eq, mode="char", value="Grandma")]
    )
    res = query.query_one(
        db,
        table_name,
        [base.Query(name="name", op=base.QueryType.eq, mode="char", value="Grandma")],
        [],
        "*",
    )
    print(res)
