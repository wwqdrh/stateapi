import fastapi

from stateapi.api import orm


def register(app: fastapi.FastAPI):
    app.post("/orm/{db}/{app}/create")(orm.table_create)
    app.post("/orm/{db}/{app}/{table}/insert")(orm.table_insert)
    app.post("/orm/{db}/{app}/{table}/query")(orm.table_query)
    app.post("/orm/{db}/{app}/{table}/query/group")(orm.table_query_group)
    app.post("/orm/{db}/{app}/{table}/update")(orm.table_update)
    app.post("/orm/{db}/{app}/{table}/delete")(orm.table_delete)
