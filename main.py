import asyncio
import logging
from datetime import datetime, timedelta

import betterlogging as bl

from models import TickersDAO, StatisticsDAO
from ticker_data import TickerData, TickerParser

ticker_data = TickerParser()

logger = logging.getLogger(__name__)
log_level = logging.INFO
bl.basic_colorized_config(level=log_level)


async def main():
    tickers = await TickersDAO.get_many()
    tickers = [i["f10960"] for i in tickers]
    # tickers = ["LKOH", "SBER"]
    for ticker in tickers:
        data: TickerData = await ticker_data.get_data(ticker=ticker)
        if data:
            create_dtime = datetime.utcnow() + timedelta(hours=3)
            await StatisticsDAO.create(f11210=create_dtime,
                                       f11030=ticker,
                                       f11040=data.year_data.high,
                                       f11050=data.quarter_data.high,
                                       f11060=data.month_data.high,
                                       f11100=data.day_data.high,
                                       f11070=data.year_data.low,
                                       f11080=data.quarter_data.low,
                                       f11090=data.month_data.low,
                                       f11110=data.day_data.low,
                                       f11120=data.year_bb.bull,
                                       f11130=data.quarter_bb.bull,
                                       f11140=data.month_bb.bull,
                                       f11150=data.year_bb.bear,
                                       f11170=data.quarter_bb.bear,
                                       f11160=data.month_bb.bear,
                                       f11180=data.year_bb.neutral,
                                       f11190=data.quarter_bb.neutral,
                                       f11200=data.month_bb.neutral)
            print(f"{ticker} PARSED")
        else:
            print(f"{ticker} is None")


if __name__ == "__main__":
    try:
        asyncio.run(main())
        logger.info("Script Started")
    except Exception as ex:
        logger.error(ex)
