import asyncio
import logging
import time
from datetime import datetime, timedelta
from itertools import islice

import betterlogging as bl

from models import TickersDAO, StatisticsDAO
from ticker_data import TickerData, TickerParser

ticker_data = TickerParser()

logger = logging.getLogger(__name__)
log_level = logging.INFO
bl.basic_colorized_config(level=log_level)


def paginator(data_list: list) -> tuple:
    it = iter(data_list)
    chunks = list(iter(lambda: tuple(islice(it, 400)), ()))
    return chunks


async def five_creates(chunk: list):
    for _ in range(5):
        try:
            await TickersDAO.create_many(data=list(chunk))
            return
        except Exception as ex:
            logger.exception(ex)



async def main():
    tickers = await TickersDAO.get_many()
    tickers = [i["f10960"] for i in tickers]
    tickers_total = []
    for ticker in tickers:
        data: TickerData = await ticker_data.get_data(ticker=ticker)
        if data:
            create_dtime = datetime.utcnow() + timedelta(hours=3)
            ticker_dict = dict(f11210=create_dtime,
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
            tickers_total.append(ticker_dict)

            logger.info(f"{ticker} PARSED")
        else:
            logger.info(f"{ticker} is None")
    chunks = paginator(data_list=tickers_total)
    for chunk in chunks:
        await five_creates(chunk=chunk)
        await asyncio.sleep(3)


if __name__ == "__main__":
    while True:
        if (datetime.utcnow() + timedelta(hours=3)).time().strftime("%H:%M:%S") == "23:30:00":
            logger.info("Script Started")
            try:
                asyncio.run(main())
            except Exception as ex:
                logger.error(ex)
            finally:
                time.sleep(3)
                logger.info("Script stopped")
