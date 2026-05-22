from tkinter import *

import uvicorn

from api.api_manager import api
from requests import request


class App:
    def __init__(self):
        # self.engine = create_async_engine(DBPATH)
        # self.db = DatabaseManager(self.engine)
        self.api = api

    def run(self) -> None:
        uvicorn.run(self.api)