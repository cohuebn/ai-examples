from os import getenv

from database.postgres_connection_settings import PostgresConnectionSettings


def get_required(name: str) -> str:
    if env_value := getenv(name):
        return env_value
    raise Exception(f"The {name} environment variable must be provided")


class Config:
    @staticmethod
    def metrics_db() -> PostgresConnectionSettings:
        return PostgresConnectionSettings(
            get_required("METRICS_DB_HOST"),
            get_required("METRICS_DB_PORT"),
            getenv("METRICS_DB_NAME", "tsdb"),
            get_required("METRICS_DB_USER"),
            get_required("METRICS_DB_PASSWORD"),
            getenv("METRICS_DB_SSL_MODE", "allow"),
        )

    @staticmethod
    def features_db() -> PostgresConnectionSettings:
        return PostgresConnectionSettings(
            get_required("FEATURES_DB_HOST"),
            get_required("FEATURES_DB_PORT"),
            getenv("FEATURES_DB_NAME", "tsdb"),
            get_required("FEATURES_DB_USER"),
            get_required("FEATURES_DB_PASSWORD"),
            getenv("FEATURES_DB_SSL_MODE", "allow"),
        )

    @staticmethod
    def log_level() -> str:
        return getenv("LOG_LEVEL", "info")
