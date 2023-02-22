from pydantic import BaseModel

from stateapi.api import orm
from stateapi.pkg.orm import base

TableQueryExpr = orm.TableQueryExpr
TableSpecUpdateItem = base.FieldValue


class TableUpdate(BaseModel):
    app: str
    table: str
    returns: str = ""
    insert: bool = False  # 如果没有这条记录，是否尝试插入
    expr: list[TableQueryExpr] = []
    fields: list[TableSpecUpdateItem] = []
    db: str = "default"

    def handle(self):
        return orm.table_update(
            self.db,
            self.app,
            self.table,
            orm.TableUpdate(
                insert=self.insert,
                returns=self.returns,
                expr=self.expr,
                fields=self.fields,
            ),
        )
