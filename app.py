from tkinter import *

import uvicorn

from config import DBPATH
from sqlalchemy.ext.asyncio import create_async_engine
from database.database_manager import DatabaseManager
from api.api_manager import api


class App:
    def __init__(self):
        # self.engine = create_async_engine(DBPATH)
        # self.db = DatabaseManager(self.engine)
        self.api = api

    def run(self) -> None:
        uvicorn.run(self.api)
