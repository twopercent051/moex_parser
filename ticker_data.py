import asyncio
from datetime import datetime, timedelta
from typing import List

from pydantic import BaseModel

from moex_api import get_ticker_data


class PeriodicData(BaseModel):
    high: int | float
    low: int | float


class BullAndBearData(BaseModel):
    bull: int
    bear: int
    neutral: int


class TickerData(BaseModel):
    year_data: PeriodicData
    quarter_data: PeriodicData
    month_data: PeriodicData
    day_data: PeriodicData
    year_bb: BullAndBearData
    quarter_bb: BullAndBearData
    month_bb: BullAndBearData


class TickerParser:

    def __init__(self):
        pass

    @staticmethod
    def __date_str_to_datetime(date: str) -> datetime:
        return datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

    @staticmethod
    def __get_high_and_low(ticker_list: List[dict]) -> PeriodicData:
        highs = [i["high"] for i in ticker_list]
        lows = [i["low"] for i in ticker_list]
        return PeriodicData(high=max(highs), low=min(lows))

    def __get_periodic_days(self, ticker_list: List[dict], days: int) -> List[dict]:
        result = []
        for item in ticker_list:
            if self.__date_str_to_datetime(item["begin"]) > (datetime.today() - timedelta(days=days)):
                result.append(item)
        return result

    @staticmethod
    def __get_bear_and_bull(periodic_data: PeriodicData, day_data: PeriodicData) -> BullAndBearData:
        # todo Поменять тут быков и медведей местами
        bull = 1 if day_data.low < periodic_data.low else 0
        bear = 1 if day_data.high > periodic_data.high else 0
        neutral = 1 if (bull + bear == 0) else 0
        return BullAndBearData(bull=bull, bear=bear, neutral=neutral)

    async def get_data(self, ticker: str) -> TickerData:
        start_date = (datetime.today() - timedelta(days=365)).strftime("%Y-%m-%d")
        ticker_list = await get_ticker_data(ticker=ticker, start_date=start_date)
        if len(ticker_list) == 0:
            return
        last_date = self.__date_str_to_datetime(ticker_list[-1]["begin"])
        if last_date.date() != datetime.today().date():
            return
        quarter_list = self.__get_periodic_days(ticker_list=ticker_list[:-1], days=90)
        month_list = self.__get_periodic_days(ticker_list=ticker_list[:-1], days=30)
        year_data = self.__get_high_and_low(ticker_list=ticker_list[:-1])
        quarter_data = self.__get_high_and_low(ticker_list=quarter_list)
        month_data = self.__get_high_and_low(ticker_list=month_list)
        day_data = self.__get_high_and_low(ticker_list=[ticker_list[-1]])
        year_bb = self.__get_bear_and_bull(periodic_data=year_data, day_data=day_data)
        quarter_bb = self.__get_bear_and_bull(periodic_data=quarter_data, day_data=day_data)
        month_bb = self.__get_bear_and_bull(periodic_data=month_data, day_data=day_data)
        return TickerData(year_data=year_data,
                          quarter_data=quarter_data,
                          month_data=month_data,
                          day_data=day_data,
                          year_bb=year_bb,
                          quarter_bb=quarter_bb,
                          month_bb=month_bb)


async def main():
    tickers = TickerParser()
    a = await tickers.get_data("LKOH")
    print(a)


if __name__ == "__main__":
    asyncio.run(main())
