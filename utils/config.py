from os import getenv


def get_required(name: str) -> str:
    if env_value := getenv(name):
        return env_value
    raise Exception(f"The {name} environment variable must be provided")


class Config:
    @staticmethod
    def db_host() -> str:
        return get_required("METRICS_DB_HOST")

    @staticmethod
    def db_port() -> str:
        return get_required("METRICS_DB_PORT")

    @staticmethod
    def db_name() -> str:
        return getenv("METRICS_DB_NAME", "tsdb")

    @staticmethod
    def db_user() -> str:
        return get_required("METRICS_DB_USER")

    @staticmethod
    def db_password() -> str:
        return get_required("METRICS_DB_PASSWORD")

    @staticmethod
    def db_ssl_mode() -> str:
        return getenv("METRICS_DB_SSL_MODE", "allow")

    @staticmethod
    def log_level() -> str:
        return getenv("LOG_LEVEL", "info")
