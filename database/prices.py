from datetime import datetime, time, timezone

from data_types.prices import DailyTokenPrice
from database.connection import get_connection_pool
from utils.logger import create_logger


logger = create_logger("database/prices")


def _run_daily_price_query(
    cursor,
    token: str,
    start_date: datetime,
    end_date: datetime,
    rolling_window: str,
):
    """Get a query that'll return daily price data including volatility information"""

    start_time = datetime.combine(start_date, time.min, tzinfo=timezone.utc)
    end_time = datetime.combine(end_date, time.max, tzinfo=timezone.utc)
    logger.debug(
        "Fetching daily price data",
        extra={"token": token, "start_time": start_time, "end_time": end_time},
    )
    cursor.execute(
        """
      with daily_prices as (
        select
          token, quote_day,
          first(first_price, quote_day) as first_price,
          last(last_price, quote_day) as last_price,
          max(maximum_price) as daily_maximum_price,
          min(minimum_price) as daily_minimum_price,
          (last(last_price, quote_day) - first(first_price, quote_day)) / first(first_price, quote_day) as daily_return
        from daily_token_prices p
        where token = %(token)s
        -- Additional buffer on start time to ensure requested start-time can still calculate volatility based on previous days
        and quote_day between %(start_time)s - %(rolling_window)s::interval and %(end_time)s
        group by token, quote_day
      ),
      volatility as (
        select
          d.token, d.quote_day,
          -- Volatility using annualized standard deviation
          stddev_samp(r.daily_return) * (|/ (extract(epoch from interval '1 year') / extract(epoch from %(rolling_window)s::interval))) as rolling_volatility,
          min(r.daily_minimum_price) rolling_minimum_price,
          max(r.daily_maximum_price) rolling_maximum_price
        from daily_prices d
        join daily_prices r
          on d.token = r.token
          and r.quote_day between d.quote_day - %(rolling_window)s::interval and d.quote_day
        group by d.token, d.quote_day
      )
      select
        d.token, d.quote_day, d.first_price, d.last_price,
        d.daily_minimum_price, d.daily_maximum_price,
        v.rolling_minimum_price, v.rolling_maximum_price,
        v.rolling_volatility
      from daily_prices d
      join volatility v
        on d.token = v.token
        and d.quote_day = v.quote_day
      where d.quote_day between %(start_time)s and %(end_time)s
      order by token, quote_day;""",
        {
            "token": token,
            "start_time": start_time,
            "end_time": end_time,
            "rolling_window": rolling_window,
        },
    )
    return cursor.fetchall()


def get_daily_prices(
    token: str, start_date: datetime, end_date: datetime, high_low_window: str
) -> list[DailyTokenPrice]:
    """Get all prices within the given date range for the requested token
    Parameters:
      token: str
        The symbol of the token to get prices for
      start_date: datetime
        The earliest date to find prices for
      end_date: datetime
        The latest date to find prices for
      high_low_window: str
        An interval representing the window to find high/lows for (e.g. '14 days')

    Returns:
      results (list[DailyTokenPrice]): All matching price information
    """
    connection_pool = get_connection_pool()
    with connection_pool.getconn() as connection:
        with connection.cursor() as cursor:
            query_results = _run_daily_price_query(
                cursor, token, start_date, end_date, high_low_window
            )
            return list(
                map(lambda query_result: DailyTokenPrice(*query_result), query_results)
            )
