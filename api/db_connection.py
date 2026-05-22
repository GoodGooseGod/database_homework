from sqlalchemy.ext.asyncio import create_async_engine

from config import DBPATH
from database.database_manager import DatabaseManager


engine = create_async_engine(DBPATH)
db_manager = DatabaseManager(engine)
