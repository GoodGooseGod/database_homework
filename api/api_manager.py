from fastapi import FastAPI

from database.database_manager import DatabaseManager

api = FastAPI()
db_manager = DatabaseManager()


@api.get('/')
async def index():
    return 'Test'