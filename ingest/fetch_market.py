import yfinance as yf 
import asyncpg
from datetime import datetime

async def insert_bar(pool, symbol, ts, open_price, high_price, low_price, close_price, volume):
    async with pool.acquire() as connection:
        await connection.execute('''
            INSERT INTO market_bars_raw(symbol, ts, interval, open, high, low, close, volume)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8) ON CONFLICT (symbol, ts, interval) DO NOTHING
        ''', symbol, ts, '1d', open_price, high_price, low_price, close_price, volume)

async def fetchhistoricaldata(universe):
    pool = await asyncpg.create_pool("postgresql://postgres:postgres@localhost:5432/postgres")
    for i in universe:
        try:
            print(f"Fetching data for {i}")
            data = yf.download(tickers=i, period="6mo", interval="1d")
            for ts, row in data.iterrows():
                await insert_bar(
                    pool,
                    i,
                ts.to_pydatetime(),
                row['Open'],
                row['High'],
                row['Low'],
                row['Close'],
                row['Volume']
            )
        except Exception as e:
            print(f"Error fetching data for {i}: {e}")

    await pool.close()
        

