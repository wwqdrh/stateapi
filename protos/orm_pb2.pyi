from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
Eq: QueryOpType
Int: FieldValueType
Primary: FieldValueType
String: FieldValueType

class DeleteRequest(_message.Message):
    __slots__ = ["expr", "returns"]
    EXPR_FIELD_NUMBER: _ClassVar[int]
    RETURNS_FIELD_NUMBER: _ClassVar[int]
    expr: _containers.RepeatedCompositeFieldContainer[QueryExpr]
    returns: str
    def __init__(self, expr: _Optional[_Iterable[_Union[QueryExpr, _Mapping]]] = ..., returns: _Optional[str] = ...) -> None: ...

class DeleteResponse(_message.Message):
    __slots__ = ["code"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    code: int
    def __init__(self, code: _Optional[int] = ...) -> None: ...

class FieldSpec(_message.Message):
    __slots__ = ["default", "index", "mode", "name", "null", "unique"]
    DEFAULT_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    NULL_FIELD_NUMBER: _ClassVar[int]
    UNIQUE_FIELD_NUMBER: _ClassVar[int]
    default: str
    index: bool
    mode: str
    name: str
    null: bool
    unique: bool
    def __init__(self, name: _Optional[str] = ..., mode: _Optional[str] = ..., default: _Optional[str] = ..., unique: bool = ..., index: bool = ..., null: bool = ...) -> None: ...

class FieldValue(_message.Message):
    __slots__ = ["mode", "name", "value"]
    MODE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    mode: FieldValueType
    name: str
    value: str
    def __init__(self, name: _Optional[str] = ..., mode: _Optional[_Union[FieldValueType, str]] = ..., value: _Optional[str] = ...) -> None: ...

class QueryExpr(_message.Message):
    __slots__ = ["left", "mode", "op", "right"]
    LEFT_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    OP_FIELD_NUMBER: _ClassVar[int]
    RIGHT_FIELD_NUMBER: _ClassVar[int]
    left: str
    mode: FieldValueType
    op: QueryOpType
    right: str
    def __init__(self, left: _Optional[str] = ..., op: _Optional[_Union[QueryOpType, str]] = ..., mode: _Optional[_Union[FieldValueType, str]] = ..., right: _Optional[str] = ...) -> None: ...

class QueryJoin(_message.Message):
    __slots__ = ["mode", "other", "this"]
    MODE_FIELD_NUMBER: _ClassVar[int]
    OTHER_FIELD_NUMBER: _ClassVar[int]
    THIS_FIELD_NUMBER: _ClassVar[int]
    mode: str
    other: str
    this: str
    def __init__(self, this: _Optional[str] = ..., other: _Optional[str] = ..., mode: _Optional[str] = ...) -> None: ...

class QueryRequest(_message.Message):
    __slots__ = ["expr", "group", "joins", "selects"]
    EXPR_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    JOINS_FIELD_NUMBER: _ClassVar[int]
    SELECTS_FIELD_NUMBER: _ClassVar[int]
    expr: _containers.RepeatedCompositeFieldContainer[QueryExpr]
    group: str
    joins: _containers.RepeatedCompositeFieldContainer[QueryJoin]
    selects: str
    def __init__(self, expr: _Optional[_Iterable[_Union[QueryExpr, _Mapping]]] = ..., joins: _Optional[_Iterable[_Union[QueryJoin, _Mapping]]] = ..., selects: _Optional[str] = ..., group: _Optional[str] = ...) -> None: ...

class QueryResponse(_message.Message):
    __slots__ = ["code"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    code: int
    def __init__(self, code: _Optional[int] = ...) -> None: ...

class RecordValue(_message.Message):
    __slots__ = ["data"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedCompositeFieldContainer[FieldValue]
    def __init__(self, data: _Optional[_Iterable[_Union[FieldValue, _Mapping]]] = ...) -> None: ...

class TableBuildRequest(_message.Message):
    __slots__ = ["clean", "create", "default", "fields", "name"]
    CLEAN_FIELD_NUMBER: _ClassVar[int]
    CREATE_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_FIELD_NUMBER: _ClassVar[int]
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    clean: bool
    create: bool
    default: _containers.RepeatedCompositeFieldContainer[RecordValue]
    fields: _containers.RepeatedCompositeFieldContainer[FieldSpec]
    name: str
    def __init__(self, name: _Optional[str] = ..., fields: _Optional[_Iterable[_Union[FieldSpec, _Mapping]]] = ..., default: _Optional[_Iterable[_Union[RecordValue, _Mapping]]] = ..., create: bool = ..., clean: bool = ...) -> None: ...

class TableBuildResponse(_message.Message):
    __slots__ = ["code"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    code: int
    def __init__(self, code: _Optional[int] = ...) -> None: ...

class TableInsertRequest(_message.Message):
    __slots__ = ["fields", "returns"]
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    RETURNS_FIELD_NUMBER: _ClassVar[int]
    fields: RecordValue
    returns: str
    def __init__(self, returns: _Optional[str] = ..., fields: _Optional[_Union[RecordValue, _Mapping]] = ...) -> None: ...

class TableInsertResponse(_message.Message):
    __slots__ = ["code"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    code: int
    def __init__(self, code: _Optional[int] = ...) -> None: ...

class UpdateRequest(_message.Message):
    __slots__ = ["expr", "fields", "insert", "returns"]
    EXPR_FIELD_NUMBER: _ClassVar[int]
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    INSERT_FIELD_NUMBER: _ClassVar[int]
    RETURNS_FIELD_NUMBER: _ClassVar[int]
    expr: _containers.RepeatedCompositeFieldContainer[QueryExpr]
    fields: RecordValue
    insert: bool
    returns: str
    def __init__(self, returns: _Optional[str] = ..., insert: bool = ..., expr: _Optional[_Iterable[_Union[QueryExpr, _Mapping]]] = ..., fields: _Optional[_Union[RecordValue, _Mapping]] = ...) -> None: ...

class UpdateResponse(_message.Message):
    __slots__ = ["code"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    code: int
    def __init__(self, code: _Optional[int] = ...) -> None: ...

class FieldValueType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class QueryOpType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
