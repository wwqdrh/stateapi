import typing

import peewee
from playhouse.shortcuts import model_to_dict

from stateapi.pkg.orm import spec, base
from stateapi.logger import Logger


def query_one(
    db: peewee.Database,
    tablename: str,
    querys: list[base.Query],
    joins: typing.Sequence[base.Join] = (),
    selects: str = "*",
) -> dict:
    model = spec.get_model(db, tablename)
    selectsfield = base.get_selects(db, tablename, selects)
    expressions = base.get_expressions(db, model, querys)
    try:
        if len(joins) > 0:
            res = (
                base.get_joins(db, model, list(joins), selectsfield)
                .where(*expressions)
                .get()
            )
        else:
            res = model.select(*selectsfield).where(*expressions).get()
        return model_to_dict(res)
    except Exception as e:
        Logger().error(e)
        return dict()


def query_all(
    db: peewee.Database,
    tablename: str,
    querys: list[base.Query],
    joins: typing.Sequence[base.Join] = (),
    selects: str = "*",
    page: int = 1,
    page_size: int = 50,
) -> list[dict]:
    model = spec.get_model(db, tablename)
    selectsfield = base.get_selects(db, tablename, selects)
    try:
        if len(querys) > 0:
            expressions = base.get_expressions(db, model, querys)
            if len(joins) > 0:
                res = base.get_joins(db, model, list(joins), selectsfield).where(
                    *expressions
                )
            else:
                res = (
                    model.select(*selectsfield)
                    .where(*expressions)
                    .paginate(page, page_size)
                )
        else:
            res = model.select(*selectsfield).paginate(page, page_size)

        return base.get_result_all(res.objects(), selects)
    except Exception as e:
        Logger().error(e)
        return []


def query_group(
    db: peewee.Database,
    tablename: str,
    group: str,
    querys: list[base.Query],
    joins: typing.Sequence[base.Join] = (),
    selects: str = "*",
):
    """
    group: "name.tag"
    根据group的值，例如user.tag，即先获取所有的tag，然后将每个tag作为一个where条件加入查询，组合到最终结果里面
    """
    group_tablename, group_column = group.split(".")
    groupsrecord = query_all(
        db, group_tablename, [], [], "distinct@{} {}".format(group, group_column)
    )

    res = []
    for record in groupsrecord:
        curquery = querys[:] + [
            base.Query(
                name=group,
                op=base.QueryType.eq,
                mode="char",
                value=record.get(group_column, ""),
            )
        ]
        res.append(
            {
                group_column: record.get(group_column, ""),
                "data": query_all(db, tablename, curquery, joins, selects),
            }
        )
    return res
