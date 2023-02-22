from pydantic import BaseModel

from stateapi.api import orm
from stateapi.pkg.orm import base


TableField = orm.TableSpecField
ValueField = base.FieldValue


class TableBuild(BaseModel):
    app: str
    table: str
    fields: list[TableField]
    default: list[list[ValueField]] = []
    create: bool = True
    clean: bool = False
    db: str = "default"

    def handle(self):
        return orm.table_create(
            self.db,
            self.app,
            orm.TableSpec(
                table_name=self.table,
                default=self.default,
                fields=self.fields,
                create=self.create,
                clean=self.clean,
            ),
        )
