import peewee
from playhouse.shortcuts import model_to_dict

from stateapi.pkg.orm import spec
from stateapi.logger import Logger


def insert_one(
    db: peewee.Database, tablename: str, returns: str = "*", **values
) -> dict:
    model = spec.get_model(db, tablename)

    try:
        record = model()
        for key, value in values.items():
            setattr(record, key, value)
        record.save()
    except Exception as e:
        Logger().error(e)
        return dict()

    res = model_to_dict(record)
    if returns == "*":
        return res

    r = dict()
    for item in returns.split(","):
        r[item] = res.get(item, "")
    return r
