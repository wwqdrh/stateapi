from pathlib import Path
from datetime import date
import os

from peewee import SqliteDatabase

from stateapi.pkg.orm import builder, source, base

testdata = Path(__file__).parents[0] / "testdata"


def test_database_register():
    source.DefaultManager.register(
        "db1", source.ISqlite(db=str(testdata / "test_database_register.db1.db"))
    )
    source.DefaultManager.register(
        "db2", source.ISqlite(db=str(testdata / "test_database_register.db2.db"))
    )
    builder.build_model(
        source.DefaultManager.db("db1"),
        "testtable",
        [
            builder.Field("name", base.FieldType.char),
            builder.Field("birthday", base.FieldType.date),
        ],
        create=False,
        clean=True,
    )
    assert os.path.exists(testdata / "test_database_register.db1.db") == True
    assert os.path.exists(testdata / "test_database_register.db2.db") == False

    os.remove(testdata / "test_database_register.db1.db")
