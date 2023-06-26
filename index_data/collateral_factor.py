from datetime import datetime, timedelta
from pandas import DataFrame


from static_data.collateral_factors import collateral_factors
from utils.datetimes import start_of_day, end_of_day
from utils.logger import create_logger
from database.prices import get_daily_prices

logger = create_logger("model_loaders/collateral_factor")


def load_collateral_factor_data(
    token: str, target_time: datetime, high_low_window: str
):
    logger.info("Loaded collateral factors into model", extra={"token": token})
    data_start_time = start_of_day(target_time - timedelta(days=60))
    data_end_time = end_of_day(target_time)
    pricing_data = get_daily_prices(
        token, data_start_time, data_end_time, high_low_window
    )
    logger.info(
        "Loaded pricing data into model",
        extra={
            "token": token,
            "start_time": data_start_time,
            "end_time": data_end_time,
        },
    )
    return {
        "collateral_factors": DataFrame(collateral_factors),
        "prices": DataFrame(pricing_data),
    }
