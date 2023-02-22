import json
import typing

from pydantic import BaseModel

from stateapi.pkg.orm import base
from stateapi.api import orm


TableInsertField = base.FieldValue


class TableSpecInsert(BaseModel):
    app: str
    table: str
    returns: str = "*"
    fields: list[TableInsertField] = []
    db: str = "default"

    def handle(self):
        return orm.table_insert(
            self.db,
            self.app,
            self.table,
            orm.TableSpecInsert(returns=self.returns, fields=self.fields),
        )
