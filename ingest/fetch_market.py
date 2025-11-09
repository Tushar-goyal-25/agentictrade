import yfinance as yf 
import asyncpg
from datetime import datetime

async def insert_bar(pool, symbol, ts, open_price, high_price, low_price, close_price, volume):
    async with pool.acquire() as connection:
        await connection.execute('''
            INSERT INTO market_bars_raw(symbol, ts, interval, open, high, low, close, volume)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
        ''', symbol, ts, '1h', open_price, high_price, low_price, close_price, volume)

async def main():
    pool = await asyncpg.create_pool("postgresql://postgres:postgres@localhost:5432/postgres")
    data = yf.download(tickers="AAPL", period="5d", interval="1h")
    for ts, row in data.iterrows():
        await insert_bar(
            pool,
            "AAPL",
            ts.to_pydatetime(),
            row['Open'],
            row['High'],
            row['Low'],
            row['Close'],
            row['Volume']
        )

import asyncio; asyncio.run(main())
