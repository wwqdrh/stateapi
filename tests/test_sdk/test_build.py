from pathlib import Path

import pytest

from stateapi.sdk import build
from stateapi.pkg.orm import source, query, base

testdata = Path(__file__).parents[0] / "testdata"


@pytest.mark.asyncio
async def test_table_build():
    source.DefaultManager.register(
        "test_table_build", source.ISqlite(db=str(testdata / "test_table_build.db"))
    )
    res = await build.TableBuild(
        db="test_table_build",
        app="testapp",
        table="testtable",
        fields=[
            build.TableField(name="id", mode="idx"),
            build.TableField(name="name", mode="char"),
        ],
    ).handle()
    print(res)


@pytest.mark.asyncio
async def test_table_build_default():
    source.DefaultManager.register(
        "test_table_build_default",
        source.ISqlite(db=str(testdata / "test_table_build_default.db")),
    )
    res = await build.TableBuild(
        db="test_table_build_default",
        app="testapp",
        table="test_table_build_default",
        fields=[
            build.TableField(name="id", mode="idx"),
            build.TableField(name="name", mode="char"),
        ],
        default=[[build.ValueField(name="name", value="zhangsan", mode="char")]],
    ).handle()
    print(res)
    res = query.query_one(
        source.DefaultManager.db("test_table_build_default"),
        "test_table_build_default",
        [base.Query("name", base.QueryType.eq, "char", "zhangsan")],
        [],
        "id,name",
    )
    assert res['id'] == 1
