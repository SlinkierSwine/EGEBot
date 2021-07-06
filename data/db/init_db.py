import config
from data.db.database import DataBase
import asyncio


if __name__ == '__main__':
    db = DataBase(config.DATABASE_PATH)
    asyncio.run(db.create_tables())
