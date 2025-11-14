import asyncio
from ingest.fetch_market import fetchhistoricaldata

async def main():
    symbols = ['NVDA', 'TSLA', 'AAPL', 'MSFT', 'AMD', 'COIN', 'SPY', 'QQQ']
    await fetchhistoricaldata(symbols)

if __name__ == "__main__":
    asyncio.run(main())