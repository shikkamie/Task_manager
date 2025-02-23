import asyncio
from datetime import datetime

import aiohttp
from bs4 import BeautifulSoup
from sqlalchemy import Column, Integer, String, select, DateTime, ForeignKey
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

import logging


# Подключение к базе данных
DATABASE_URL = 'postgresql+asyncpg://postgres:db132123@localhost:5432/ldb'
engine = create_async_engine(DATABASE_URL, echo=True)


SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


Base = declarative_base()

# Определение таблиц
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    username = Column(String, unique=True)
    request_count = Column(Integer, default=0)

    parser_result = relationship('ParserResult', back_populates='user')

class ParserResult(Base):
    __tablename__ = 'parser_result'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    link = Column(String)
    datetime = Column(DateTime)
    request_number = Column(Integer)

    user = relationship('User', back_populates='parser_result')

BASE_URL = 'https://habr.com'
SEARCH_URL = BASE_URL + '/ru/articles/page{}/'

async def create_tables():
    """Создание таблиц в базе данных"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def fetch_page(url):
    """Функция для загрузки HTML-страницы"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.text()
    except Exception as e:
        print(f'Ошибка при получении страницы {url}: {e}')
        return None

async def save_to_db(data):
    """Сохранение результата в базу данных"""
    session = SessionLocal()
    try:
        title, link, posting_data, request_number = data

        result = await session.execute(select(User).filter_by(username='test_1'))
        user = result.scalars().first()

        parser_result = ParserResult(
            title=title,
            link=link,
            datetime=posting_data,
            request_number=request_number,
            user_id=user.id
        )
        session.add(parser_result)
        await session.commit()
    finally:
        await session.close()

async def parse_page(html):
    """Парсинг HTML-страницы"""
    if not html:
        print("Ошибка загрузки страницы, пропускаем...")
        return

    session = SessionLocal()
    try:
        result = await session.execute(select(User).filter_by(username='test_1'))
        user = result.scalars().first()



        request_number = user.request_count

        soup = BeautifulSoup(html, 'html.parser')
        articles = soup.find_all('article', {'class': 'tm-articles-list__item'})

        for article in articles:
            title_tag = article.find('h2', {'class': 'tm-title tm-title_h2'})
            link_tag = article.find('a')
            time_tag = article.find('time')

            if title_tag and link_tag and time_tag:
                title = title_tag.text.strip()
                link = link_tag.get('href')
                posting_data = datetime.fromisoformat(time_tag.get('datetime').replace("Z", "+00:00")).replace(tzinfo=None)
                await save_to_db((title, link, posting_data, request_number))
            else:
                print('Не нашли заголовок')

        await session.commit()
    finally:
        await session.close()

async def main():
    """Главная функция парсера"""
    await create_tables()

    session = SessionLocal()
    try:
        result = await session.execute(select(User).filter_by(username='test_1'))
        user = result.scalars().first()
        if not user:
            user = User(username='test_1')
            session.add(user)
            await session.commit()

        for i in range(1, 10):
            url = SEARCH_URL.format(i)
            html = await fetch_page(url)
            await parse_page(html)
            print(f'Спарсили страницу {i}')

        user.request_count += 1
        await session.commit()

        print('Парсинг завершен')
    finally:
        await session.close()

if __name__ == '__main__':
    asyncio.run(main())