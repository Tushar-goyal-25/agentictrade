from abc import abstractmethod, ABC
from data.signals import Signals

class Strategies(ABC):
    def __init__(self, name):
        self.name = name
        self.requiredbars = 0

    @abstractmethod
    def generate_signals(self, symbol, data):
        pass

    def validatedata(self, data):
        if len(data) < self.requiredbars:
             return False
        return True

class MomentumStrategy(Strategies):
        def __init__(self, lookback_period=14, threshold=0.05):
            super().__init__("Momentum Strategy")
            self.lookback_period = lookback_period #n days
            self.threshold = threshold
            self.requiredbars = lookback_period

        def generate_signals(self, symbol, data):
            currentPrice = data['close'].iloc[-1]
            oldPrice = data['close'].iloc[-self.lookback_period]
            momentum = (currentPrice - oldPrice) / oldPrice
            momentumPercent = momentum * 100

            if momentumPercent > self.threshold*100:
                signal = Signals()
                signal.symbol = symbol
                signal.action = "BUY"
                signal.confidence = min(abs(momentum) / (self.threshold*2), 1.0)
                signal.reason = f"Momentum of {momentumPercent:.2f}% exceeds threshold of {self.threshold*100}%"
                signal.suggested_position_size = signal.confidence * 0.2  # Example position sizing
                signal.stop_loss = data['close'].iloc[-1] * (1 - self.threshold)  # 2% stop loss
                signal.take_profit = data['close'].iloc[-1] * (1 + self.threshold)  # 5% take profit
                return signal
            elif momentumPercent < -self.threshold*100:
                signal = Signals()
                signal.symbol = symbol
                signal.action = "SELL"
                signal.confidence = min(abs(momentum) / (self.threshold*2), 1.0)
                signal.reason = f"Momentum of {momentumPercent:.2f}% below negative threshold of {-self.threshold*100}%"
                signal.suggested_position_size = signal.confidence * 0.2  # Example position sizing
                signal.stop_loss = data['close'].iloc[-1] * (1 + self.threshold)  # 2% stop loss
                signal.take_profit = data['close'].iloc[-1] * (1 - self.threshold)  # 5% take profit
                return signal
            else:
                signal = Signals()
                signal.symbol = symbol
                signal.action = "HOLD"
                signal.confidence = 1.0
                signal.reason = f"Momentum of {momentumPercent:.2f}% within threshold of ±{self.threshold*100}%"
                return signal

class MeanReversionStrategy(Strategies):
        def __init__(self, lookback_period=20, entry_zscore=2.0, exit_zscore=0.5):
            super().__init__("Mean Reversion Strategy")
            self.lookback_period = lookback_period
            self.entry_zscore = entry_zscore
            self.exit_zscore = exit_zscore
            self.requiredbars = lookback_period

        def generate_signals(self, symbol, data):
            pass  # Implementation goes here
        
        def calculateFeatures(self, data):
            pass  # Implementation goes here
       
class BreakoutStrategy(Strategies):
        def __init__(self, breakout_period=20):
            super().__init__("Breakout Strategy")
            self.breakout_period = breakout_period
            self.requiredbars = breakout_period

        def generate_signals(self, symbol, data):
            pass  # Implementation goes here

        def calculateFeatures(self, data):
            pass  # Implementation goes here
       
class MovingAverageCrossoverStrategy(Strategies):
        def __init__(self, short_window=50, long_window=200):
            super().__init__("Moving Average Crossover Strategy")
            self.short_window = short_window
            self.long_window = long_window
            self.requiredbars = long_window

        def generate_signals(self, symbol, data):
            pass  # Implementation goes here

        def calculateFeatures(self, data):
            pass  # Implementation goes here
        

class RSIStrategy(Strategies):
        def __init__(self, period=14, overbought=70, oversold=30):
            super().__init__("RSI Strategy")
            self.period = period
            self.overbought = overbought
            self.oversold = oversold
            self.requiredbars = period

        def generate_signals(self, symbol, data):
            pass  # Implementation goes here

        def calculateFeatures(self, data):
            pass  # Implementation goes here
        
class NewsSentimentStrategy(Strategies):
        def __init__(self, sentiment_threshold=0.5):
            super().__init__("News Sentiment Strategy")
            self.sentiment_threshold = sentiment_threshold
            self.requiredbars = 0  # Depends on news data availability

        def generate_signals(self, symbol, data):
            pass  # Implementation goes here

        def calculateFeatures(self, data):
            pass  # Implementation goes here
        