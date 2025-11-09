


class Signals:
    def __init__(self):
        self.symbol = ""  # Ticker symbol
        self.action = ""  # List to hold generated signals
        self.confidence = 0.0 # Confidence level of the signal
        self.reason = "" # Reason for the signal
        self.suggested_position_size = 0.0  # Suggested position size as a fraction of total capital
        self.stop_loss = 0.0  # Suggested stop loss 
        self.take_profit = 0.0  # Suggested take profit


    