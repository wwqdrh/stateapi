from pydantic import BaseModel

from stateapi.api import orm

TableQueryJoin = orm.TableQueryJoin
TableQueryExpr = orm.TableQueryExpr


class TableQuery(BaseModel):
    """
    if select all, you can set page and page_size to control how many data query
    """

    app: str
    table: str
    all: bool = False
    selects: str = "*"
    page: int = 1
    page_size: int = 50
    expr: list[TableQueryExpr] = []
    joins: list[TableQueryJoin] = []
    db: str = "default"


    def handle(self):
        return orm.table_query(
            self.db,
            self.app,
            self.table,
            orm.TableQuery(
                expr=self.expr,
                joins=self.joins,
                selects=self.selects,
            ),
            self.all,
            page=self.page,
            page_size=self.page_size,
        )


class TableQueryGroup(BaseModel):
    app: str
    table: str
    group: str = ""
    selects: str = "*"
    expr: list[TableQueryExpr] = []
    joins: list[TableQueryJoin] = []
    db: str = "default"

    def handle(self):
        return orm.table_query_group(
            self.db,
            self.app,
            self.table,
            orm.TableQuery(
                expr=self.expr,
                joins=self.joins,
                selects=self.selects,
                group=self.group,
            ),
        )
