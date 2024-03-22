import asyncio

from sqlalchemy import MetaData, DateTime, Column, Integer, String, select, insert
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, as_declarative

from config import load_config

config = load_config(".env")

DATABASE_URL = f'mysql+aiomysql://{config.db.user}:{config.db.password}@{config.db.host}:{config.db.port}/{config.db.database}'

engine = create_async_engine(DATABASE_URL)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@as_declarative()
class Base:
    metadata = MetaData()


class TickersDB(Base):
    __tablename__ = "cb_data570"

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    f10960 = Column(String)  # тикеры


class StatisticsDB(Base):
    __tablename__ = "cb_data580"

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    f11210 = Column(DateTime)  # Дата запроса
    f11030 = Column(String)  # тикер
    f11040 = Column(Integer)  # high за год
    f11050 = Column(Integer)  # high за квартал
    f11060 = Column(Integer)  # high за месяц
    f11100 = Column(Integer)  # high за день
    f11070 = Column(Integer)  # low за год
    f11080 = Column(Integer)  # low за квартал
    f11090 = Column(Integer)  # low за месяц
    f11110 = Column(Integer)  # low за день
    f11120 = Column(Integer)  # бык годовой
    f11130 = Column(Integer)  # бык квартальный
    f11140 = Column(Integer)  # бык месячный
    f11150 = Column(Integer)  # медведь годовой
    f11170 = Column(Integer)  # медведь квартальный
    f11160 = Column(Integer)  # медведь месячный
    f11180 = Column(Integer)  # нейтральный год
    f11190 = Column(Integer)  # нейтральный квартал
    f11200 = Column(Integer)  # нейтральный месяц


class BaseDAO:
    """Класс взаимодействия с БД"""
    model = None

    @classmethod
    async def get_many(cls, **filter_by) -> list:
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by).order_by(cls.model.id.asc())
            result = await session.execute(query)
            await engine.dispose()
            return result.mappings().all()

    @classmethod
    async def create(cls, **data):
        async with async_session_maker() as session:
            stmt = insert(cls.model).values(**data)
            await session.execute(stmt)
            await engine.dispose()
            await session.commit()

    @classmethod
    async def create_many(cls, data: List[dict]):
        async with async_session_maker() as session:
            stmt = insert(cls.model).values(data)
            await session.execute(stmt)
            await session.commit()


class TickersDAO(BaseDAO):
    model = TickersDB


class StatisticsDAO(BaseDAO):
    model = StatisticsDB


async def test():
    # users = await TickersDB.get_many()
    # print(users)
    # await engine.dispose()
    print(1.005**2000)


if __name__ == "__main__":
    asyncio.run(test())
