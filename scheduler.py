from apscheduler.schedulers.asyncio import AsyncIOScheduler

from models import TickersDAO


class Worker:

    def __init__(self):
        self.scheduler = AsyncIOScheduler(timezone="Europe/Moscow")


    # @staticmethod
    # async def


    async def __dispatcher(self):
        # tickers = await TickersDAO.get_many()
        # tickers = [i["f10960"] for i in tickers]

        print(123)



    async def create_task(self):
        self.scheduler.add_job(func=self.__dispatcher, trigger="cron", hour=23, minute=30)
        # self.scheduler.add_job(func=self.__dispatcher, trigger="interval", seconds=2)
