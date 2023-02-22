import uvicorn
from fastapi import FastAPI

from stateapi import api, config

app = FastAPI()


@app.post("/")
async def root():
    return {"message": "Hello World!"}


def main():
    api.register(app)

    uvicorn.run(
        "stateapi.app:app",
        host=config.AppConfig.server.host,
        port=config.AppConfig.server.port,
    )
