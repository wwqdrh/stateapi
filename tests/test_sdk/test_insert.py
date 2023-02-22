from pathlib import Path

import pytest

from stateapi.sdk import build, insert
from stateapi.pkg.orm import source, base

testdata = Path(__file__).parents[0] / "testdata"


@pytest.mark.asyncio
async def test_table_insert():
    source.DefaultManager.register(
        "test_table_insert", source.ISqlite(db=str(testdata / "test_table_insert.db"))
    )
    await build.TableBuild(
        db="test_table_insert",
        app="testapp",
        table="test_table_insert",
        fields=[
            build.TableField(name="id", mode="idx"),
            build.TableField(name="name", mode="char"),
            build.TableField(name="create_time", mode="date"),
            build.TableField(name="complete_time", mode="date", null=True),
        ],
    ).handle()

    res = await insert.TableSpecInsert(
        db="test_table_insert",
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
            )
        ],
    ).handle()
    print(res)
