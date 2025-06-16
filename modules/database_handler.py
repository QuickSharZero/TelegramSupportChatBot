from logging import Logger

import asyncpg
from asyncpg import Connection
from typing import Optional
import asyncio

from modules.config_handler import ConfigManager


class DatabaseHandler:

    def __init__(self, logger: Logger, config: ConfigManager):
        self.config = config
        self.logger = logger

        self.host = asyncio.run(self.config.get("postgres", "host"))
        self.port = asyncio.run(self.config.get("postgres", "port"))
        self.database = asyncio.run(self.config.get("postgres", "database"))
        self.username = asyncio.run(self.config.get("postgres", "username"))
        self.password = asyncio.run(self.config.get("postgres", "password"))

        self._connection: Optional[Connection] = None

    async def _connect(self) -> Connection:
        if not self._connection or self._connection.is_closed():
            self._connection = await asyncpg.connect(
                user=self.username,
                password=self.password,
                database=self.database,
                host=self.host,
                port=self.port
            )
        return self._connection

    async def _close(self):
        if self._connection and not self._connection.is_closed():
            await self._connection.close()
            self._connection = None

    async def check_connection(self) -> bool:
        try:
            conn = await self._connect()
            await conn.execute("SELECT 1")
            return True
        except Exception as e:
            print(f"Ошибка подключения к БД:\n{e}")
            return False
        finally:
            await self._close()

    async def create_tables(self):
        try:
            conn = await self._connect()
        except Exception as e:
            self.logger.error("Не удалось создать таблицы", exc_info=True)
        finally:
            await self._close()
