from pathlib import Path
from datetime import date

from peewee import SqliteDatabase

from stateapi.pkg.orm import builder, query, spec, base

testdata = Path(__file__).parents[0] / "testdata"

db = SqliteDatabase(str(testdata / "people.db"))


def test_query_one():
    table_name = "test_query_one"
    model, exist = builder.build_model(
        db,
        table_name,
        [
            builder.Field("name", base.FieldType.char),
            builder.Field("birthday", base.FieldType.date),
        ],
        create=True,
        clean=True,
    )
    assert exist is True
    model.create(name="Grandma", birthday=date(1935, 3, 1))

    res = query.query_one(
        db,
        table_name,
        [base.Query("name", base.QueryType.eq, "char", "Grandma")],
        [],
        "name,birthday",
    )
    print(res)


def test_query_all():
    table_name = "test_query_all"
    model, _ = builder.build_model(
        db,
        table_name,
        [
            builder.Field("name", base.FieldType.char),
            builder.Field("birthday", base.FieldType.date),
        ],
        create=True,
        clean=True,
    )
    model.create(name="Grandma", birthday=date(1935, 3, 1))
    model.create(name="Grandma", birthday=date(1935, 3, 2))

    res = query.query_all(
        db, table_name, [base.Query("name", base.QueryType.eq, "char", "Grandma")], []
    )
    print(res)


def test_query_join():
    table_name1 = "test_query_join_1"
    model1, _ = builder.build_model(
        db,
        table_name1,
        [
            builder.Field("id", base.FieldType.idx),
            builder.Field("name", base.FieldType.char),
            builder.Field("birthday", base.FieldType.date),
        ],
        create=True,
        clean=True,
    )
    model1.create(name="Grandma", birthday=date(1935, 3, 1))

    table_name2 = "test_query_join_2"
    model2, _ = builder.build_model(
        db,
        table_name2,
        [
            builder.Field("id", base.FieldType.idx),
            builder.Field("userid", base.FieldType.number),
            builder.Field("tag", base.FieldType.char),
        ],
        create=True,
        clean=True,
    )
    model2.create(userid="1", tag="1")
    model2.create(userid="1", tag="2")
    model2.create(userid="1", tag="3")

    res = query.query_all(
        db,
        table_name1,
        [base.Query("name", base.QueryType.eq, "char", "Grandma")],
        [
            base.Join(
                "{}.id".format(table_name1),
                "{}.userid".format(table_name2),
                base.JoinType.inner,
            )
        ],
        selects="test_query_join_1.id tid, test_query_join_1.name tname, test_query_join_2.tag ttag",
    )
    print(res)


def test_query_group():
    table_name = "test_query_group"
    model, _ = builder.build_model(
        db,
        table_name,
        [
            builder.Field("name", base.FieldType.char),
            builder.Field("tag", base.FieldType.char),
            builder.Field("birthday", base.FieldType.date),
        ],
        create=True,
        clean=True,
    )
    model.create(name="Grandma", tag="1", birthday=date(1935, 3, 1))
    model.create(name="Grandma2", tag="2", birthday=date(1935, 3, 2))
    model.create(name="Grandma3", tag="2", birthday=date(1935, 3, 2))

    res = query.query_group(
        db,
        table_name,
        "{}.tag".format(table_name),
        [],
        [],
    )
    print(res)


def test_query_join_group():
    table_name = "test_query_group_user"
    model, _ = builder.build_model(
        db,
        table_name,
        [
            builder.Field("id", base.FieldType.idx),
            builder.Field("name", base.FieldType.char),
        ],
        create=True,
        clean=True,
    )
    model.create(name="Grandma")
    model.create(name="Grandma2")
    model.create(name="Grandma3")

    table_name2 = "test_query_group_user_tag"
    model2, _ = builder.build_model(
        db,
        table_name2,
        [
            builder.Field("id", base.FieldType.idx),
            builder.Field("userid", base.FieldType.number),
            builder.Field("tagid", base.FieldType.number),
        ],
        create=True,
        clean=True,
    )
    model2.create(userid=1, tagid=1)
    model2.create(userid=2, tagid=2)
    model2.create(userid=3, tagid=2)

    res = query.query_group(
        db,
        table_name,
        "{}.tagid".format(table_name2),
        [],
        [
            base.Join(
                this=table_name + ".id",
                other=table_name2 + ".userid",
                mode=base.JoinType.inner,
            )
        ],
    )
    print(res)


def test_query_join2_group():
    """
    连三张表
    """
    table_name = "test_query_group_user"
    model, _ = builder.build_model(
        db,
        table_name,
        [
            builder.Field("id", base.FieldType.idx),
            builder.Field("name", base.FieldType.char),
        ],
        create=True,
        clean=True,
    )
    model.create(name="Grandma")
    model.create(name="Grandma2")
    model.create(name="Grandma3")

    table_name1 = "test_query_group_tag"
    model1, _ = builder.build_model(
        db,
        table_name1,
        [
            builder.Field("id", base.FieldType.idx),
            builder.Field("name", base.FieldType.char),
        ],
        create=True,
        clean=True,
    )
    model1.create(name="tag1")
    model1.create(name="tag2")

    table_name2 = "test_query_group_user_tag"
    model2, _ = builder.build_model(
        db,
        table_name2,
        [
            builder.Field("id", base.FieldType.idx),
            builder.Field("userid", base.FieldType.number),
            builder.Field("tagid", base.FieldType.number),
        ],
        create=True,
        clean=True,
    )
    model2.create(userid=1, tagid=1)
    model2.create(userid=2, tagid=2)
    model2.create(userid=3, tagid=2)

    res = query.query_group(
        db,
        table_name2,
        "{}.id".format(table_name1),
        [],
        [
            base.Join(
                this=table_name2 + ".userid",
                other=table_name + ".id",
                mode=base.JoinType.inner,
            ),
            base.Join(
                this=table_name2 + ".tagid",
                other=table_name1 + ".id",
                mode=base.JoinType.inner,
            ),
        ],
        selects="{}.id userid, {}.name tagname".format(table_name, table_name1),
    )
    print(res)


def test_query_withpage():
    table_name = "test_query_withpage"
    model, _ = builder.build_model(
        db,
        table_name,
        [
            builder.Field("name", base.FieldType.char),
            builder.Field("tag", base.FieldType.char),
        ],
        create=True,
        clean=True,
    )
    model.create(name="Grandma", tag="test")
    model.create(name="Grandma1", tag="test")
    model.create(name="Grandma2", tag="test")
    model.create(name="Grandma3", tag="test")
    model.create(name="Grandma4", tag="test")
    model.create(name="Grandma5", tag="test")
    model.create(name="Grandma6", tag="test")

    res = query.query_all(
        db,
        table_name,
        [base.Query(op=base.QueryType.eq, name="tag", mode="char", value="test")],
        [],
        "id,name",
        page=1,
        page_size=3,
    )
    print(res)
    res = query.query_all(
        db,
        table_name,
        [base.Query(op=base.QueryType.eq, name="tag", mode="char", value="test")],
        [],
        "id,name",
        page=3,
        page_size=3,
    )
    print(res)
