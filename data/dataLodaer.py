import asyncpg
import pandas as pd
import datetime
import os


async def getMarketData(symbols,lookback_days):
    db_url = os.environ.get('DATABASE_URL', "postgresql://postgres:postgres@localhost:5432/postgres")
    pool = await asyncpg.create_pool(db_url)
    async with pool.acquire() as connection:
        rows = await connection.fetch("SELECT ts,open,high,low,close,volume FROM market_bars_raw WHERE symbol = $1 AND interval = '1d' ORDER BY ts DESC LIMIT $2", symbols, lookback_days)
        df = pd.DataFrame(rows, columns=['ts', 'open', 'high', 'low', 'close', 'volume'])
    await pool.close()

    df = df.sort_values('ts')
    if df.empty:
        print("Error: Dataset empty")
        return df
    
    return df
    


# if __name__ == "__main__":
#     import asyncio
    
#     async def test():
#         df = await getMarketData('AAPL', 250)
#         print(f"Loaded {len(df)} rows")
#         print(f"Columns: {df.columns.tolist()}")
#         print(f"Date range: {df['ts'].min()} to {df['ts'].max()}")
#         print(f"\nFirst 5 rows:")
#         print(df.head())
#         print(f"\nLast 5 rows:")
#         print(df.tail())
    
#     asyncio.run(test())