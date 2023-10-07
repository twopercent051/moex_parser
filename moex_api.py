import asyncio

import requests

import apimoex

proxy = {"https": "http://yhv02e:SP9zBP@46.161.47.116:9358"}


async def get_ticker_data(ticker: str, start_date: str):
    with requests.Session() as session:
        session.proxies.update(proxy)
        result = apimoex.get_market_candles(session=session, security=ticker, start=start_date, interval=24)
        return result




if __name__ == "__main__":
    asyncio.run(get_ticker_data(ticker="VTBR", start_date="2023-01-10"))
