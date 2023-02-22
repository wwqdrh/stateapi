import json

import peewee

from stateapi.pkg.orm import builder


def get_model(db: peewee.Database, tablename: str) -> peewee.Model:
    def getfields(db: peewee.Database, tablename: str) -> list[builder.Field]:
        specdict = get_spec(db, tablename)
        fields: list[builder.Field] = []
        for item in specdict["fields"]:
            fields.append(builder.Field(item["name"], builder.FieldType[item["mode"]]))
        return fields

    model = builder.get_model(db, tablename, getfields)
    return model


def get_column(db: peewee.Database, tablename: str, colname: str) -> peewee.Field:
    model = get_model(db, tablename)
    return getattr(model, colname)


def get_column_bystr(
    db: peewee.Database, name: str, tablename: str = ""
) -> peewee.Field:
    """
    User.id
    distinct@User.id
    distinct@id
    id
    """
    distinct: bool = False
    if name.startswith("distinct@"):
        name = name.replace("distinct@", "")
        distinct = True

    if "." in name:
        tablename, name = name.strip().split(".")

    if distinct:
        return peewee.fn.Distinct(get_column(db, tablename, name))
    else:
        return get_column(db, tablename, name)


def save_spec(db: peewee.Database, table_name: str, spec: dict):
    class Spec(peewee.Model):
        tablename = peewee.CharField()
        specstr = peewee.CharField()

        class Meta:
            database = db
            table_name = "spec"

    db.create_tables([Spec])
    record = Spec(tablename=table_name, specstr=json.dumps(spec))
    record.save()


def get_spec(db: peewee.Database, table_name: str) -> dict:
    class Spec(peewee.Model):
        tablename = peewee.CharField()
        specstr = peewee.CharField()

        class Meta:
            database = db
            table_name = "spec"

    db.create_tables([Spec])
    record = Spec.select(Spec.specstr).where(Spec.tablename == table_name).get()
    return json.loads(record.specstr)
