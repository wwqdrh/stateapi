from enum import Enum
import typing
import dataclasses
import datetime

import peewee
from playhouse.shortcuts import model_to_dict
import pydantic

from stateapi.pkg.orm import spec


# class FieldValueType(Enum):
#     idx = 1
#     int = 2
#     char = 3


class QueryType(Enum):
    eq = 0
    ne = 1
    lt = 2
    gt = 3
    in_ = 4
    is_ = 5
    like = 6
    ilike = 7


class FieldType(Enum):
    idx = peewee.AutoField
    char = peewee.CharField
    date = peewee.DateField
    datetime = peewee.DateTimeField
    number = peewee.IntegerField
    bigInteger = peewee.BigIntegerField
    float = peewee.FloatField
    double = peewee.DoubleField
    decimal = peewee.DecimalField
    text = peewee.TextField
    blob = peewee.BlobField

    def get_default(self) -> typing.Any:
        match self:
            case FieldType.idx:
                return None
            case FieldType.char:
                return ""
            case FieldType.text:
                return ""
            case FieldType.blob:
                return ""
            case FieldType.number:
                return 0
            case FieldType.bigInteger:
                return 0
            case FieldType.float:
                return 0
            case FieldType.double:
                return 0
            case FieldType.decimal:
                return 0
            case FieldType.date:
                return datetime.datetime.now()
            case FieldType.datetime:
                return datetime.datetime.now()
            case _:
                return None

    def trans_value(self, val: typing.Any) -> typing.Any:
        match self:
            case FieldType.idx:
                return int(val)
            case FieldType.char | FieldType.text | FieldType.blob:
                return str(val)
            case FieldType.number | FieldType.bigInteger | FieldType.float | FieldType.double | FieldType.decimal:
                return int(val)
            case FieldType.date | FieldType.datetime:
                return datetime.datetime(2000, 1, 1)
            case _:
                return None


@dataclasses.dataclass
class Query:
    name: str
    op: QueryType
    mode: str
    value: str


class FieldValue(pydantic.BaseModel):
    name: str
    mode: str
    value: str


class JoinType(Enum):
    inner = peewee.JOIN.INNER
    lout = peewee.JOIN.LEFT_OUTER
    rout = peewee.JOIN.RIGHT_OUTER
    full = peewee.JOIN.FULL
    fout = peewee.JOIN.FULL_OUTER
    cross = peewee.JOIN.CROSS
    natural = peewee.JOIN.NATURAL
    lateral = peewee.JOIN.LATERAL
    llateral = peewee.JOIN.LEFT_LATERAL


@dataclasses.dataclass
class Join:
    this: str  # table.columnname
    other: str  # table.columnname
    mode: JoinType


def get_expressions(
    db: peewee.Database, model: peewee.Model, querys: list[Query]
) -> list[peewee.Expression]:
    expressions: list[peewee.Expression] = []
    for item in querys:
        if "." not in item.name:
            cur = getattr(model, item.name)
        else:
            cur = spec.get_column_bystr(db, item.name)

        value = FieldType[item.mode].trans_value(item.value)

        match item.op:
            case QueryType.eq:
                expressions.append(cur == value)
            case QueryType.ne:
                expressions.append(cur != value)
            case QueryType.lt:
                expressions.append(cur < value)
            case QueryType.gt:
                expressions.append(cur > value)
            case QueryType.in_:
                expressions.append(cur << value)
            case QueryType.is_:
                expressions.append(cur >> value)
            case QueryType.like:
                expressions.append(cur % value)
            case QueryType.ilike:
                expressions.append(cur**value)
    return expressions


def get_selects(
    db: peewee.Database, tablename: str, selects: str
) -> list[peewee.Field]:
    """
    1、*
    2、User.id uid, Shop.name shopname
    3、id uid, name name
    """
    if selects == "*":
        return []

    res: list[peewee.Field] = []
    for item in selects.split(","):
        item = item.strip()
        if item.startswith("@"):
            # 整个table
            res.append(spec.get_model(db, item[1:]))
            continue

        parts = item.split(" ")

        if len(parts) == 2:
            # table.field or field
            field = spec.get_column_bystr(db, parts[0], tablename)
            res.append(field.alias(parts[1]))
        else:
            res.append(spec.get_column_bystr(db, parts[0], tablename))
    return res


def get_joins(
    db: peewee.Database,
    model: peewee.Model,
    joins: list[Join],
    selects: typing.Sequence[peewee.Field] = (),
):
    """
    joins: [(Tag.id == TagUser.tagid), (User.id == TagUser.userid)]
    select t1.* from table1 as t1 inner join table2 t2 on table1.id = t2.t1id inner join table3
    """
    model = model.select(*selects)

    for item in joins:
        thistable, thiscolumn = item.this.split(".")
        othertable, othercolumn = item.other.split(".")
        thismodel = spec.get_model(db, thistable)
        othermodel = spec.get_model(db, othertable)

        model = model.join(
            othermodel,
            item.mode.value,
            on=(getattr(thismodel, thiscolumn) == getattr(othermodel, othercolumn)),
        )
    return model


def get_result(record: object, selects: str) -> dict[str, typing.Any]:
    if selects == "*":
        return model_to_dict(record)

    cur: dict[str, typing.Any] = dict()
    for item in selects.split(","):
        parts = item.strip().split(" ")
        if len(parts) == 2:
            if hasattr(record, parts[1]):
                cur[parts[1]] = getattr(record, parts[1])
            else:
                relatable = parts[0].split(".")[0].strip()
                cur[parts[1]] = getattr(getattr(record, relatable), parts[1])
        else:
            cur[parts[0]] = getattr(record, parts[0])
    return cur


def get_result_all(res: typing.Iterable[typing.Any], selects: str) -> list[dict]:
    """
    1、*
    2、User.id uid, Shop.name shopname
    """
    if selects == "*":
        return [model_to_dict(item) for item in res]

    result: list[dict] = []
    for record in res:
        result.append(get_result(record, selects))
    return result


def field_value_trans(
    fields: list[FieldValue], db: peewee.Database = None, tablename: str = ""
) -> typing.Dict[str, typing.Any]:
    """将字符串转成对应的数据类型"""
    values: dict[str, typing.Any] = dict()
    for field in fields:
        if field.mode == "int" or field.mode == "number":
            values[field.name] = int(field.value)
        elif field.mode == "date" or field.mode == "datetime":
            values[field.name] = datetime.datetime.fromisoformat(field.value)
        elif field.mode == "expression":
            # +1, -1之类
            if db is None:
                continue
            f = spec.get_column_bystr(db, field.name, tablename)
            if field.value[0] == "+":
                values[field.name] = f + int(field.value[1:])
            elif field.value[0] == "-":
                values[field.name] = f - int(field.value[1:])
        else:
            values[field.name] = field.value
    return values


@dataclasses.dataclass
class IUpdateField:
    field: peewee.Field
    value: typing.Any


def field_value_update_trans(
    fields: list[FieldValue],
    db: peewee.Database,
    tablename: str = "",
    skip: typing.Sequence[str] = tuple(),
):
    """
    将其变为字段和字，而不是名字和值

    skip用于跳过部分字段，例如expression类型的，用于upesert的时候，生成默认值
    """
    skip_fields = set(skip)
    values: dict[str, IUpdateField] = dict()
    for field in fields:
        f = spec.get_column_bystr(db, field.name, tablename)
        if field.mode in skip_fields:
            continue

        if field.mode == "int" or field.mode == "number":
            values[field.name] = IUpdateField(field=f, value=int(field.value))
        elif field.mode == "date" or field.mode == "datetime":
            values[field.name] = IUpdateField(
                field=f,
                value=datetime.datetime.fromisoformat(field.value),
            )
        elif field.mode == "expression":
            # +1, -1之类
            if field.value[0] == "+":
                values[field.name] = IUpdateField(
                    field=f, value=f + int(field.value[1:])
                )
            elif field.value[0] == "-":
                values[field.name] = IUpdateField(
                    field=f, value=f - int(field.value[1:])
                )
        else:
            values[field.name] = IUpdateField(field=f, value=field.value)
    return values
