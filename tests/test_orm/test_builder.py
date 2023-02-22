from pathlib import Path
from datetime import date

from peewee import SqliteDatabase

from stateapi.pkg.orm import builder, query, spec, base

testdata = Path(__file__).parents[0] / "testdata"

db = SqliteDatabase(str(testdata / "people.db"))


def test_filedtype_default():
    assert base.FieldType.idx.get_default() is None
    assert base.FieldType.char.get_default() == ""

def test_build_model():
    table_name = "test_build_model"
    model, exist = builder.build_model(
        db,
        table_name,
        [
            builder.Field("name", base.FieldType.char),
            builder.Field("birthday", base.FieldType.date),
        ],
        create=False,
        clean=True,
    )
    assert exist is False
    db.create_tables([model])

    uncle_bob = model(name="Bob", birthday=date(1960, 1, 15))
    uncle_bob.save()
    grandma = model.create(name="Grandma", birthday=date(1935, 3, 1))
    gran = model.select().where(model.name == "Grandma").get()

    for person in model.select():
        print(person.name)


def test_get_model():
    table_name = "test_get_model"
    model, _ = builder.get_model(
        db,
        table_name,
        lambda db, tablename: [
            builder.Field("name", base.FieldType.char),
            builder.Field("birthday", base.FieldType.date),
        ],
    )
    db.create_tables([model])

    uncle_bob = model(name="Bob", birthday=date(1960, 1, 15))
    uncle_bob.save()
    grandma = model.create(name="Grandma", birthday=date(1935, 3, 1))
    gran = model.select().where(model.name == "Grandma").get()

    for person in model.select():
        print(person.name)
