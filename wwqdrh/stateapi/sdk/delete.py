from pydantic import BaseModel

from stateapi.pkg.orm import base
from stateapi.api import orm


TableQueryExpr = orm.TableQueryExpr


class TableSpecDelete(BaseModel):
    app: str
    table: str
    returns: str = "*"
    expr: list[TableQueryExpr] = []
    db: str = "default"

    def handle(self):
        return orm.table_delete(
            self.db,
            self.app,
            self.table,
            orm.TableDelete(returns=self.returns, expr=self.expr),
        )
