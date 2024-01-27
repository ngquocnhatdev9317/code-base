import argparse
import asyncio

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy_utils import create_database, database_exists, drop_database

from database.base_model import BaseModel
from utilities.configs import URL
from utilities.logger import logger_info


async def init(dbname: str = "dummy", force=False):
    url = f"postgresql+asyncpg://{URL.replace('host.docker.internal', 'localhost')}/{dbname}"
    url_psycopg = url.replace("asyncpg", "psycopg2")
    engine = create_async_engine(
        url,
        execution_options={"isolation_level": "AUTOCOMMIT"},
    )
    is_exists = database_exists(url_psycopg)
    if is_exists and not force:
        logger_info(f'database "{dbname}" already exists')

    elif is_exists:
        drop_database(url_psycopg)
        create_database(url_psycopg)
        logger_info(f'create force to exists database "{dbname}"')

    else:
        create_database(url_psycopg)

    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
        await conn.run_sync(BaseModel.metadata.create_all)

        logger_info(f'init database "{dbname}" DONE')

    await engine.dispose()


def remove(dbname):
    url = f"postgresql+asyncpg://{URL.replace('host.docker.internal', 'localhost')}/{dbname}"
    url_psycopg = url.replace("asyncpg", "psycopg2")
    is_exists = database_exists(url_psycopg)
    if is_exists:
        drop_database(url_psycopg)
        logger_info(f'dropped the exists database "{dbname}"')
    else:
        logger_info(f'"{dbname}" is unexist')


if __name__ == "__main__":
    parser = argparse.ArgumentParser("manage_aiohttp")
    parser.add_argument("action", help="Action", type=str, choices=["init", "remove"])
    parser.add_argument("dbname", help="The init database name", type=str)
    parser.add_argument(
        "-f", "--force", help="Init database with force mode", action="store_true"
    )
    args = parser.parse_args()

    loop = asyncio.get_event_loop()

    if args.action == "init":
        loop.run_until_complete(init(args.dbname, args.force))
    if args.action == "remove":
        remove(args.dbname)

    loop.stop()
