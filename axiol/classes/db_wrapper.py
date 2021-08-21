from __future__ import annotations

import os
from abc import ABC
from typing import Optional, Tuple, TYPE_CHECKING

import dotenv

from axiol import DOTENV_PATH
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import InvalidURI
from classes.logger import log

if TYPE_CHECKING:
    from motor.motor_asyncio import (
        AsyncIOMotorCollection,
        AsyncIOMotorDatabase
    )

DB_PATH: Optional[str] = (
    os.environ.get('MONGO_URL')
    or dotenv.dotenv_values(DOTENV_PATH).get('MONGO_URL')
)

if DB_PATH is None:
    log.error(
        'No mongo db path has been provided.'
        ' Make sure to create an `.env` file'
        ' or add in environ key'
    )

MONGO_CLIENT = None

try:
    MONGO_CLIENT = AsyncIOMotorClient(DB_PATH)

except InvalidURI:
    log.error(
        'Cant connect to the mongo db database, '
        'make sure that the `.env` or os.ENVIRON'
        ' as been set properly.'
    )

else:
    log.success('Connected to the mongo db database.')


class StaticClassList(ABC):
    __instances = set()

    def __init__(self, base) -> None:
        cls_name: str = self.__class__.__name__

        if cls_name in self.__instances:
            log.warn(
                'Classes from db wrapper should not be instantiated.'
                f' Consider using {self.__class__.__name__.lower()}.'
            )
            return

        self.__instances.add(cls_name)

        for attr_name in self.__slots__:
            setattr(
                self, attr_name,
                base['_'.join(map(str.capitalize, attr_name.split()))]
            )

    def __repr__(self) -> str:
        return (
            f'<{self.__class__.__name__}(StaticClassList)'
            f'[{", ".join(self.__slots__)}]>'
        )


class Database(StaticClassList):
    """A class to group all mongo databases."""
    __slots__: Tuple[str, ...] = (
        "axiol", "leveling", "karma", "custom", "warnings"
    )

    axiol: AsyncIOMotorDatabase
    leveling: AsyncIOMotorDatabase
    karma: AsyncIOMotorDatabase
    custom: AsyncIOMotorDatabase
    warnings: AsyncIOMotorDatabase


database: Database = Database(MONGO_CLIENT)


class Collections(StaticClassList):
    """A class to group all mongo collections from main database."""
    __slots__: Tuple[str, ...] = (
        "plugins", "prefixes", "reaction_roles", "welcome", "verify",
        "chatbot", "chatbot", "permissions"
    )

    plugins: AsyncIOMotorCollection
    prefixes: AsyncIOMotorCollection
    reaction_roles: AsyncIOMotorCollection
    welcome: AsyncIOMotorCollection
    verify: AsyncIOMotorCollection
    chatbot: AsyncIOMotorCollection
    permissions: AsyncIOMotorCollection


collections: Collections = Collections(database.axiol)

__all__ = (collections, database)
