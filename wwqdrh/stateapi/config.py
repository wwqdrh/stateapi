import pathlib
import os

import pydantic
from pykit.configer import NewSetting

BaseSetting = NewSetting(
    pathlib.Path(__file__).parents[1], "config", os.environ.get("MODE", "")
)


class IServer(pydantic.BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class IApp(BaseSetting):  # type: ignore
    server: IServer = IServer()


AppConfig = IApp()
