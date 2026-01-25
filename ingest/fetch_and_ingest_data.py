import asyncio
from fetch_market import fetchhistoricaldata

async def main():
    # Add any stocks that are missing from your database
    missing_stocks = ['PLTR', 'COIN', 'SHOP', 'SQ', 'RIOT', 'AMD', 'META', 'NFLX', 'CRWD']

    print(f"Fetching data for {len(missing_stocks)} missing stocks...")
    print(f"Symbols: {', '.join(missing_stocks)}")

    await fetchhistoricaldata(missing_stocks)

    print("\n✅ All missing stocks fetched successfully!")

if __name__ == "__main__":
    asyncio.run(main())
