from psycopg2 import pool, extensions
import os
import logging
from functools import cache

from utils.logger import create_logger
from utils.config import Config


logger = create_logger("database/connection")

# TODO - determine if we actually want this; we're potentially losing precision
#   by converting decimals to floats from the database. However, numpy can't
#   handle decimals for things like np.log so for now, using floats
decimal_to_float = extensions.new_type(
    extensions.DECIMAL.values,
    "decimal_to_float",
    lambda value, _cursor: float(value) if value is not None else None,
)
extensions.register_type(decimal_to_float)


class LoggingCursor(extensions.cursor):
    def execute(self, sql, args=None):
        logger.debug(
            "Traced query", extra={"query": self.mogrify(sql, args).decode("utf-8")}
        )
        extensions.cursor.execute(self, sql, args)


connection_pool = None


def get_connection_pool():
    if connection_pool:
        return connection_pool

    host = Config.db_host()
    port = Config.db_port()
    db_name = Config.db_name()
    user = Config.db_user()
    password = Config.db_password()
    ssl_mode = Config.db_ssl_mode()
    logger.debug(
        "Creating connection pool",
        extra={
            "host": host,
            "port": port,
            "db_name": db_name,
            "user": user,
            "ssl_mode": ssl_mode,
        },
    )
    return pool.ThreadedConnectionPool(
        1,
        10,
        host=host,
        port=port,
        dbname=db_name,
        user=user,
        password=password,
        sslmode=ssl_mode,
        cursor_factory=LoggingCursor,
    )
