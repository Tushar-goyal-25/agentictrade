import asyncio
from data.dataLodaer import getMarketData
from data.strategies import (
    MomentumStrategy,
    MeanReversionStrategy, 
    BreakoutStrategy,
    MovingAverageCrossoverStrategy
)

def printSignal(signal, strategy):
    print("here is the signal generated")
    print(f"Symbol: {signal.symbol}")
    print(f"Strategy name: {strategy}")
    print(f"Action: {signal.action}")
    print(f"confidence:{signal.confidence}")
    print(f"Reason:{signal.reason}")
    print(f"Position size:{signal.suggested_position_size}")
    print(f"StopLoss:{signal.stop_loss}")
    print(f"Take Profit:{signal.take_profit}")


async def test_momentum():
    symbols = ['NVDA','TSLA','AAPL']
    momentumstrategy = MomentumStrategy()
    for i in symbols:
        data = await getMarketData(i, 250)
        signal = momentumstrategy.generate_signals(i, data )
        printSignal(signal,"Momentum")
async def test_meanreversionstrategy():
    symbols = ['AAPL','MSFT']
    momentumstrategy = MeanReversionStrategy()
    for i in symbols:
        data = await getMarketData(i, 250)
        signal = momentumstrategy.generate_signals(i, data )
        printSignal(signal,"Momentum")
async def test_breakoutstrategy():
    symbols = ['COIN','AMD']
    momentumstrategy = BreakoutStrategy()
    for i in symbols:
        data = await getMarketData(i, 250)
        signal = momentumstrategy.generate_signals(i, data )
        printSignal(signal,"Momentum")
async def test_movingaveragecrossover():
    symbols = ['SPY','QQQ']
    momentumstrategy = MovingAverageCrossoverStrategy()
    for i in symbols:
        data = await getMarketData(i, 250)
        signal = momentumstrategy.generate_signals(i, data )
        printSignal(signal,"Momentum")

async def main():
    print("=" * 60)
    print("TESTING TRADING STRATEGIES")
    print("=" * 60)
    
    await test_momentum()
    await test_meanreversionstrategy()
    await test_breakoutstrategy()
    await test_movingaveragecrossover()
    print("\n" + "=" * 60)
    print("TESTING COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
