import typing

import peewee
from playhouse.shortcuts import model_to_dict

from stateapi.pkg.orm import spec, base
from stateapi.logger import Logger


def update_one(
    db: peewee.Database,
    tablename: str,
    querys: list[base.Query],
    values: dict[str, base.IUpdateField],
    default: dict[str, base.IUpdateField],
    returns: str = "",
) -> dict:
    model = spec.get_model(db, tablename)
    expressions = base.get_expressions(db, model, querys)

    record = model.update(**{item: val.value for item, val in values.items()}).where(
        *expressions
    )
    cnt = record.execute()
    if cnt == 0:
        # 不存在这个数据，尝试使用default进行插入
        if len(default) == 0:
            Logger().error("不存在这个数据")
            raise Exception("不存在这个数据")

        try:
            record = model.create(**{item: val.value for item, val in default.items()})
            return update_one(db, tablename, querys, values, default, returns)
        except Exception as e:
            Logger().error("使用默认值新增数据失败: " + str(e))
            raise Exception("使用默认值新增数据失败: " + str(e))
    else:
        if returns == "":
            return dict()
        selectsfield = base.get_selects(db, tablename, "*")
        record = model.select(*selectsfield).where(*expressions).get()

    res = model_to_dict(record)
    if returns == "*":
        return res

    r = dict()
    for item in returns.split(","):
        r[item] = res.get(item, "")
    return r
