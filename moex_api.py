import asyncio

import requests

import apimoex


async def get_ticker_data(ticker: str, start_date: str):
    with requests.Session() as session:
        result = apimoex.get_market_candles(session=session, security=ticker, start=start_date, interval=24)
        return result


if __name__ == "__main__":
    asyncio.run(get_ticker_data(ticker="VTBR", start_date="2023-01-10"))
