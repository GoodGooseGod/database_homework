from tkinter import *

from config import DBPATH
from sqlalchemy.ext.asyncio import create_async_engine
from database.database_manager import DatabaseManager


class App:
    def __init__(self):
        self.engine = create_async_engine(DBPATH)
        self.db = DatabaseManager(self.engine)

    async def run(self) -> None:
        pass