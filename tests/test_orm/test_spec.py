from pathlib import Path
from datetime import date

from peewee import SqliteDatabase

from stateapi.pkg.orm import builder, query, spec

testdata = Path(__file__).parents[0] / "testdata"

db = SqliteDatabase(str(testdata / "people.db"))

def test_spec_save_get():
    specdict = {"table_name": "testtable", "fields": [{"name": "name", "mode": "char"}]}

    spec.save_spec(
        db,
        "test_spec_save_get",
        specdict,
    )

    newspec = spec.get_spec(
        db,
        "test_spec_save_get",
    )

    assert specdict == newspec, "spec失败"
