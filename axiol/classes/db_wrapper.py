import os
from typing import Optional

import dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import InvalidURI

from classes.logger import log

DB_PATH: Optional[str] = (
    os.environ.get('MONGO_DB_URL')
    or dotenv.dotenv_values('.env').get('MONGO_DB_URL')
)

if DB_PATH is None:
    log.error(
        'No mongo db path has been provided.'
        ' Make sure to create an `.env` file'
        ' or add in environ key'
    )


try:
    MONGO_CLIENT = AsyncIOMotorClient(DB_PATH)

except InvalidURI:
    log.error(
        'Cant connect to the mongo db database, '
        'make sure that the `.env` or os.ENVIRON'
        ' as been set properly.'
    )


class StaticClassList:

    def __init__(self):
        log.warn(
            'Classes from db wrapper should not be instantiated.'
            f' Consider using `{self.__class__.__name__}`.'
        )


class Database(StaticClassList):
    MAIN = MONGO_CLIENT["Axiol"]
    LEVEL = MONGO_CLIENT["Leveling"]
    KARMA = MONGO_CLIENT["Karma"]
    CUSTOM = MONGO_CLIENT["Custom"]
    WARNINGS = MONGO_CLIENT["Warnings"]


class Collections(StaticClassList):
    PLUGINS = Database.MAIN["Plugins"]
    PREFIXES = Database.MAIN["Prefixes"]
    REACTION_ROLES = Database.MAIN["Reaction Roles"]
    WELCOME = Database.MAIN["Welcome"]
    VERIFY = Database.MAIN["Verify"]
    CHATBOT = Database.MAIN["Chatbot"]
    PERMISSIONS = Database.MAIN["Permissions"]
    AUTO_MOD = Database.MAIN["AutoMod"]
    GIVEAWAY = Database.MAIN["Giveaway"]
