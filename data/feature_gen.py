import asyncpg
from datetime import datetime
import pandas as pd


async def fetch_from_bars(pool,n=100):
    async with pool.acquire() as connection:
        rows = await connection.fetch('''SELECT * FROM market_bars_raw WHERE symbol = 'AAPL' AND interval = '1h' ORDER BY ts ASC LIMIT $1''', n)

    return rows



async def main():


    pool = await asyncpg.create_pool("postgresql://postgres:postgres@localhost:5432/postgres")
    rows = await fetch_from_bars(pool, 10)
    rows = pd.DataFrame(rows, columns=[' symbol', ' ts', ' interval', ' open', ' high', ' low', ' close', ' volume'])
    # rows = rows.set_index(' ts')

    print(rows)
    # print(rows[' close'].last('3H'))

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())