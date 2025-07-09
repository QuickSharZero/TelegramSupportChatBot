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
            self.logger.error(f"Ошибка подключения к БД: %s", str(e), exc_info=True)
            return False
        finally:
            await self._close()

    async def create_tables(self):
        try:
            conn = await self._connect()
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS users(
                    tgID BIGINT PRIMARY KEY,
                    username VARCHAR(255),
                    threadID BIGINT,
                    isBlocked BOOLEAN DEFAULT False
                )
            """)
        except Exception as e:
            self.logger.error("Не удалось создать таблицы", exc_info=True)
        finally:
            await self._close()

    async def addUser(self, tgID: int, username: str, threadID: int):
        try:
            conn = await self._connect()
            await conn.execute("""
                INSERT INTO users(tgID, username, threadID)
                VALUES ($1, $2, $3)
            """, tgID, username, threadID)
            self.logger.debug(f"В БД добавлен новый пользователь: {tgID}|{username}")
        except Exception as e:
            self.logger.error(f"Ошибка при добавлении пользователя: {e}", exc_info=True)
        finally:
            await self._close()

    async def checkUserExists(self, tgID: int):
        try:
            conn = await self._connect()
            exists = await conn.fetchval("SELECT EXISTS(SELECT 1 FROM users WHERE tgID = $1)",
                                         tgID)
            return exists
        except Exception as e:
            self.logger.error(f"Не удалось проверить существования пользователя: {e}", exc_info=True)
        finally:
            await self._close()

    async def getThreadID(self, tgID: int):
        try:
            conn = await self._connect()
            record = await conn.fetchrow("SELECT threadID FROM users WHERE tgID = $1",
                                         tgID)
            return record['threadid'] if record else None
        except Exception:
            self.logger.error("Ошибка при получении threadID", exc_info=True)
        finally:
            await self._close()

    async def getUserID(self, threadID: int):
        try:
            conn = await self._connect()
            record = await conn.fetchrow("SELECT tgID FROM users WHERE threadID = $1",
                                         threadID)
            return record['tgid'] if record else None
        except Exception:
            self.logger.error("Ошибка при получении tgID", exc_info=True)
        finally:
            await self._close()

    async def isUserBlocked(self, tgID: int) -> bool:
        try:
            conn = await self._connect()
            is_blocked = await conn.fetchval("SELECT isBlocked FROM users WHERE tgID = $1",
                                       tgID)
            return bool(is_blocked)
        except Exception:
            self.logger.error("Ошибка при получении isBlocked", exc_info=True)
        finally:
            await self._close()
