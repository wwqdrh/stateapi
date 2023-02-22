import peewee
from playhouse.shortcuts import model_to_dict

from stateapi.pkg.orm import spec, base
from stateapi.logger import Logger


def delete_record(
    db: peewee.Database,
    tablename: str,
    querys: list[base.Query],
) -> int:
    model = spec.get_model(db, tablename)
    expressions = base.get_expressions(db, model, querys)

    try:
        res = model.get(*expressions)
        return res.delete_instance()
    except Exception as e:
        Logger().error(e)
        return 0
