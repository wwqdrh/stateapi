from pathlib import Path

import pytest

from stateapi.sdk import build, insert, delete
from stateapi.pkg.orm import source, base

testdata = Path(__file__).parents[0] / "testdata"


@pytest.mark.asyncio
async def test_table_delete():
    source.DefaultManager.register(
        "test_table_delete", source.ISqlite(db=str(testdata / "test_table_delete.db"))
    )
    await build.TableBuild(
        db="test_table_delete",
        app="testapp",
        table="test_table_delete",
        fields=[
            build.TableField(name="id", mode="idx"),
            build.TableField(name="name", mode="char"),
            build.TableField(name="create_time", mode="date"),
            build.TableField(name="complete_time", mode="date", null=True),
        ],
    ).handle()

    res = await insert.TableSpecInsert(
        db="test_table_delete",
        app="testapp",
        table="test_table_insert",
        returns="*",
        fields=[
            insert.TableInsertField(
                name="name",
                value="zhangsan",
                mode="char",
            ),
            insert.TableInsertField(
                name="create_time",
                value="2022-11-21",
                mode="date",
            ),
        ],
    ).handle()
    print(res)
    res = await delete.TableSpecDelete(
        db="test_table_delete",
        app="testapp",
        table="test_table_insert",
        returns="*",
        expr=[
            delete.TableQueryExpr(
                op="eq",
                value=base.FieldValue(name="name", mode="char", value="zhangsan"),
            )
        ],
    ).handle()
    print(res)
