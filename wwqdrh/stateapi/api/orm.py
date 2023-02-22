import typing

from pydantic import BaseModel


from stateapi.pkg.orm import builder, query, source, spec, insert, update, base, delete
from stateapi.logger import Logger

FieldValue = base.FieldValue

class TableSpecField(BaseModel):
    """
    字段的类型
    """

    name: str
    mode: str  # FieldType[mode]
    default: str = ""
    unique: bool = False
    index: bool = False
    null: bool = False


class TableSpec(BaseModel):
    """
    创建表时声明的类型
    """

    table_name: str
    fields: list[TableSpecField]
    default: list[list[FieldValue]] = []
    create: bool = True
    clean: bool = False


async def table_create(db: str, app: str, tablespec: TableSpec):
    try:
        # spec.save_spec(db, "{}_{}".format(app, tablespec.table_name), tablespec.dict())
        spec.save_spec(
            source.DefaultManager.db(db), tablespec.table_name, tablespec.dict()
        )
    except Exception as e:
        Logger().error(e)
        return str(e)

    fields: list[builder.Field] = []
    for item in tablespec.fields:
        if item.default != "":
            fields.append(
                builder.Field(
                    item.name,
                    base.FieldType[item.mode],
                    base.FieldType[item.mode].trans_value(item.default),
                    item.unique,
                    item.index,
                    item.null,
                )
            )
        else:
            fields.append(
                builder.Field(
                    item.name,
                    base.FieldType[item.mode],
                    base.FieldType[item.mode].get_default(),
                    item.unique,
                    item.index,
                    item.null,
                )
            )
    try:
        model, isnew = builder.build_model(
            # db, "{}_{}".format(app, tablespec.table_name), fields, create=True
            source.DefaultManager.db(db),
            tablespec.table_name,
            fields,
            create=tablespec.create,
            clean=tablespec.clean,
        )
        if isnew and len(tablespec.default) > 0:
            for record in tablespec.default:
                await table_insert(
                    db,
                    app,
                    tablespec.table_name,
                    TableSpecInsert(returns="id", fields=record),
                )

        return "ok"
    except Exception as e:
        Logger().error(e)
        return str(e)


class TableSpecInsert(BaseModel):
    """
    插入数据时的类型，这里只能表示一行数据
    """

    returns: str = "*"
    fields: list[FieldValue] = []


async def table_insert(db: str, app: str, table: str, data: TableSpecInsert):
    values = base.field_value_trans(data.fields, source.DefaultManager.db(db), table)

    try:
        return insert.insert_one(
            # db, "{}_{}".format(app, table), returns=data.returns, **values
            source.DefaultManager.db(db),
            table,
            returns=data.returns,
            **values
        )
    except Exception as e:
        Logger().error(e)
        return str(e)


class TableQueryJoin(BaseModel):
    this: str  # columnname
    other: str  # columnname
    mode: str


class TableQueryExpr(BaseModel):
    op: str
    value: base.FieldValue


class TableQuery(BaseModel):
    expr: list[TableQueryExpr]
    joins: list[TableQueryJoin]
    selects: str = ""
    group: str = ""


async def table_query(
    db: str,
    app: str,
    table: str,
    querys: TableQuery,
    all: bool = False,
    page: int = 1,
    page_size: int = 50,
):
    exp: list[base.Query] = []
    for item in querys.expr:
        exp.append(
            base.Query(
                item.value.name,
                base.QueryType[item.op],
                item.value.mode,
                item.value.value,
            )
        )

    joins: list[base.Join] = []
    for jitem in querys.joins:
        joins.append(base.Join(jitem.this, jitem.other, base.JoinType[jitem.mode]))

    try:
        if all:
            return query.query_all(
                source.DefaultManager.db(db),
                table,
                exp,
                joins,
                selects=querys.selects,
                page=page,
                page_size=page_size,
            )
        else:
            return query.query_one(
                source.DefaultManager.db(db), table, exp, joins, selects=querys.selects
            )
    except Exception as e:
        Logger().error(e)
        return str(e)


async def table_query_group(db: str, app: str, table: str, data: TableQuery):
    exp: list[base.Query] = []
    for item in data.expr:
        exp.append(
            base.Query(
                item.value.name,
                base.QueryType[item.op],
                item.value.mode,
                item.value.value,
            )
        )

    joins: list[base.Join] = []
    for jitem in data.joins:
        joins.append(base.Join(jitem.this, jitem.other, base.JoinType[jitem.mode]))

    try:
        return query.query_group(
            source.DefaultManager.db(db),
            table,
            data.group,
            exp,
            joins,
            selects=data.selects,
        )
    except Exception as e:
        Logger().error(e)
        return str(e)


class TableUpdate(BaseModel):
    returns: str = "*"
    insert: bool = False
    expr: list[TableQueryExpr]
    fields: list[FieldValue]


async def table_update(db: str, app: str, table: str, data: TableUpdate):
    if len(data.fields) == 0:
        return "ok"

    exp: list[base.Query] = []
    for item in data.expr:
        exp.append(
            base.Query(
                item.value.name,
                base.QueryType[item.op],
                item.value.mode,
                item.value.value,
            )
        )

    values = base.field_value_update_trans(
        data.fields, source.DefaultManager.db(db), table
    )
    default = base.field_value_update_trans(
        data.fields, source.DefaultManager.db(db), table, skip=["expression"]
    )

    try:
        return update.update_one(
            source.DefaultManager.db(db), table, exp, values, default, data.returns
        )
    except Exception as e:
        Logger().error(e)
        return str(e)


class TableDelete(BaseModel):
    expr: list[TableQueryExpr]
    returns: str = "*"


async def table_delete(db: str, app: str, table: str, data: TableDelete):
    if len(data.expr) == 0:
        return 0

    exp: list[base.Query] = []
    for item in data.expr:
        exp.append(
            base.Query(
                item.value.name,
                base.QueryType[item.op],
                item.value.mode,
                item.value.value,
            )
        )

    try:
        return delete.delete_record(source.DefaultManager.db(db), table, exp)
    except Exception as e:
        Logger().error(e)
        return 0
