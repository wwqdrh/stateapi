"""
Field Type	Sqlite	Postgresql	MySQL
====
AutoField	integer	serial	integer
BigAutoField	integer	bigserial	bigint
IntegerField	integer	integer	integer
BigIntegerField	integer	bigint	bigint
SmallIntegerField	integer	smallint	smallint
IdentityField	not supported	int identity	not supported
FloatField	real	real	real
DoubleField	real	double precision	double precision
DecimalField	decimal	numeric	numeric
CharField	varchar	varchar	varchar
FixedCharField	char	char	char
TextField	text	text	text
BlobField	blob	bytea	blob
BitField	integer	bigint	bigint
BigBitField	blob	bytea	blob
UUIDField	text	uuid	varchar(40)
BinaryUUIDField	blob	bytea	varbinary(16)
DateTimeField	datetime	timestamp	datetime
DateField	date	date	date
TimeField	time	time	time
TimestampField	integer	integer	integer
IPField	integer	bigint	bigint
BooleanField	integer	boolean	bool
BareField	untyped	not supported	not supported
ForeignKeyField	integer	integer	integer
"""
import dataclasses
from enum import Enum
import typing
import datetime

import peewee

from stateapi.pkg.orm import base, insert

model_pool: dict[str, peewee.Model] = dict()  # 用于缓存tablename与model


@dataclasses.dataclass
class Field:
    name: str
    typ: base.FieldType
    default: typing.Any = None
    unique: bool = False
    index: bool = False
    null: bool = False


def build_model(
    db: peewee.Database,
    tablename: str,
    fields: list[Field],
    create: bool = False,
    clean: bool = False,
) -> tuple[peewee.Model, bool]:
    class Meta:
        database = db
        table_name = tablename

    if clean:
        old: peewee.Model = type("old", (peewee.Model,), dict(Meta=Meta))
        old.drop_table()

    class Basic:
        def __init_subclass__(cls) -> None:
            for field in fields:
                if field.null:
                    setattr(
                        cls,
                        field.name,
                        field.typ.value(
                            unique=field.unique,
                            index=field.index,
                            null=field.null,
                        ),
                    )
                else:
                    setattr(
                        cls,
                        field.name,
                        field.typ.value(
                            unique=field.unique,
                            index=field.index,
                            default=field.typ.get_default(),
                        ),
                    )

    model = type(tablename, (Basic, peewee.Model), dict(Meta=Meta))
    # class Meta(Basic, peewee.Model):

    model_pool[tablename] = model

    if not db.table_exists(tablename):
        if create:
            db.create_tables([model])
            return model, True

    return model, False


def get_model(
    db: peewee.Database,
    tablename: str,
    get_data: typing.Callable[[peewee.Database, str], list[Field]],
) -> peewee.Model:
    """
    根据tablename获取对应的model
    在构造的时候将字段缓存到数据库
    使用的时候根据tablename查询出来然后进行构造
    """
    if tablename in model_pool:
        return model_pool[tablename]

    fields = get_data(db, tablename)
    model = build_model(db, tablename, fields)
    model_pool[tablename] = model
    return model
