from pathlib import Path

import pytest

from stateapi.sdk import build, insert, update
from stateapi.pkg.orm import source, base

testdata = Path(__file__).parents[0] / "testdata"


@pytest.mark.asyncio
async def test_table_update():
    source.DefaultManager.register(
        "test_table_update", source.ISqlite(db=str(testdata / "test_table_update.db"))
    )
    await build.TableBuild(
        db="test_table_update",
        app="testapp",
        table="testtable",
        fields=[
            build.TableField(name="id", mode="idx"),
            build.TableField(name="name", mode="char"),
        ],
    ).handle()

    res = await insert.TableSpecInsert(
        db="test_table_update",
        app="testapp",
        table="testtable",
        returns="id,name",
        fields=[
            insert.TableInsertField(
                name="name",
                value="zhangsan",
                mode="char",
            )
        ],
    ).handle()
    print(res)
    res = await update.TableUpdate(
        db="test_table_update",
        app="testapp",
        table="testtable",
        returns="id,name",
        expr=[
            update.TableQueryExpr(
                op="eq", value=base.FieldValue(name="id", mode="idx", value="1")
            )
        ],
        fields=[
            update.TableSpecUpdateItem(
                name="name",
                value="zhangsannew",
                mode="char",
            )
        ],
    ).handle()
    assert res["name"] == "zhangsannew", "update fail"


@pytest.mark.asyncio
async def test_table_update_with_expression():
    source.DefaultManager.register(
        "test_table_update_with_expression",
        source.ISqlite(db=str(testdata / "test_table_update_with_expression.db")),
    )
    await build.TableBuild(
        db="test_table_update_with_expression",
        app="testapp",
        table="test_table_update_with_expression",
        fields=[
            build.TableField(name="id", mode="idx"),
            build.TableField(name="name", mode="char"),
            build.TableField(name="count", mode="number"),
        ],
        clean=True,
    ).handle()

    res = await insert.TableSpecInsert(
        db="test_table_update_with_expression",
        app="testapp",
        table="test_table_update_with_expression",
        returns="id,name,count",
        fields=[
            insert.TableInsertField(
                name="name",
                value="zhangsan",
                mode="char",
            ),
            insert.TableInsertField(
                name="count",
                value="1",
                mode="number",
            ),
        ],
    ).handle()
    print(res["count"])
    res = await update.TableUpdate(
        db="test_table_update_with_expression",
        app="testapp",
        table="test_table_update_with_expression",
        returns="id,name,count",
        expr=[
            update.TableQueryExpr(
                op="eq", value=base.FieldValue(name="id", mode="idx", value="1")
            )
        ],
        fields=[
            update.TableSpecUpdateItem(
                name="count",
                value="+1",
                mode="expression",
            )
        ],
    ).handle()
    assert res["count"] == 2


@pytest.mark.asyncio
async def test_table_update_with_expression_default():
    source.DefaultManager.register(
        "test_table_update_with_expression_default",
        source.ISqlite(
            db=str(testdata / "test_table_update_with_expression_default.db")
        ),
    )
    table = "test_table_update_with_expression_default"
    await build.TableBuild(
        db="test_table_update_with_expression_default",
        app="testapp",
        table=table,
        fields=[
            build.TableField(name="id", mode="idx"),
            build.TableField(name="name", mode="char"),
            build.TableField(name="count", mode="number"),
        ],
        clean=True,
    ).handle()
    res = await update.TableUpdate(
        db="test_table_update_with_expression_default",
        app="testapp",
        table=table,
        returns="id,name,count",
        expr=[
            update.TableQueryExpr(
                op="eq", value=base.FieldValue(name="id", mode="idx", value="1")
            )
        ],
        fields=[
            update.TableSpecUpdateItem(
                name="count",
                value="+1",
                mode="expression",
            ),
            update.TableSpecUpdateItem(
                name="name",
                value="zhangsan",
                mode="char",
            ),
        ],
        insert=True,
    ).handle()
    assert res["count"] == 1
    res = await update.TableUpdate(
        db="test_table_update_with_expression_default",
        app="testapp",
        table=table,
        returns="id,name,count",
        expr=[update.TableQueryExpr(op="eq", value=base.FieldValue(name="id", mode="idx", value="1"))],
        fields=[
            update.TableSpecUpdateItem(
                name="count",
                value="+1",
                mode="expression",
            ),
            update.TableSpecUpdateItem(
                name="name",
                value="zhangsan",
                mode="char",
            ),
        ],
        insert=True,
    ).handle()
    assert res["count"] == 2
