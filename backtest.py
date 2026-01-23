from data.dataLodaer import getMarketData

class BackTester:
    def __init__(self,initial_captial, risk_profile):
        self.initial_captial = initial_captial #constant original cash
        self.cash = initial_captial #variable cash
        self.positions = {} #tracks all stocks {symbol:{number of shares, entry price,}}
        self.portfolio_history = [] #Track portfolio history 
        self.trades = [] #log all trades
        self.risk_profile = risk_profile # from account class

    

    def runBacktest(self,strategy, symbol, historical_data, risk_params):

        for i in range(len(historical_data)):
            data_window = historical_data[0:i+1]
            if len(data_window) < strategy.requiredbars:
                continue
            signal = strategy.generate_signals(symbol, data_window)
            
            if signal.action == "BUY":
                if symbol not in self.positions:
                    position_value = self.cash * signal.suggested_position_size
                    max_position_value = self.cash * risk_params.max_position_pct
                    position_value = min(position_value, max_position_value)
                    current_price = data_window['close'].iloc[-1]
                    shares = position_value / current_price
                    if self.cash >= position_value:
                        self.positions[symbol] = {
                            'shares': shares,
                            'entry_price': current_price,
                            'stop_loss_price': signal.stop_loss,
                            'take_profit_price': signal.take_profit

                        }
                        self.cash -= position_value
                        self.trades.append({
                            'symbol': symbol,
                            'action': signal.action,
                            'date': data_window['ts'].iloc[-1],
                            'price': current_price,
                            'shares': shares,
                            'value': position_value,
                            'reason': signal.reason, 
                            'type': 'SIGNAL',
                            'pnl': None,
                                                
                        })
            elif signal.action == "SELL":
                if symbol in self.positions:
                    current_price = data_window['close'].iloc[-1]
                    entry_price = self.positions[symbol]['entry_price']
                    shares = self.positions[symbol]['shares']
                    sell_value = shares * current_price

                    cost_basis = shares * entry_price
                    profit_loss = sell_value - cost_basis
                    self.cash += sell_value

                    self.trades.append({
                        'symbol': symbol,
                        'action': signal.action,
                        'date': data_window['ts'].iloc[-1],
                        'price': current_price,
                        'shares': shares,
                        'value': sell_value,
                        'reason': signal.reason, 
                        'type': 'SIGNAL',
                        'pnl': profit_loss,
                                            
                    })
                    del self.positions[symbol]
            for sym in list(self.positions.keys()):
                    if sym in self.positions:
                        current_price = data_window['close'].iloc[-1]
                        position = self.positions[sym]

                        if current_price <= position['stop_loss_price']:
                            entry_price = position['entry_price']
                            shares = position['shares']
                            sell_value = shares* current_price
                            cost_basis = shares * entry_price
                            profit_loss = sell_value - cost_basis
                            self.cash += sell_value
                            self.trades.append({
                            'symbol': sym,
                            'action': 'SELL',
                            'date': data_window['ts'].iloc[-1],
                            'price': current_price,
                            'shares': shares,
                            'value': sell_value,
                            'reason': "stop-loss triggered", 
                            'type': 'STOP_LOSS',
                            'pnl': profit_loss,
                                
                            })
                            del self.positions[sym
                                               ]
                            continue
                    if current_price >= position['take_profit_price']:
                        # Sell at take-profit
                        shares = position['shares']
                        entry_price = position['entry_price']
                        sell_value = shares * current_price
                        cost_basis = shares * entry_price
                        profit_loss = sell_value - cost_basis
                        
                        self.cash += sell_value
                        self.trades.append({
                            'symbol': sym,
                            'action': 'SELL',
                            'date': data_window['ts'].iloc[-1],
                            'price': current_price,
                            'shares': shares,
                            'value': sell_value,
                            'reason': f"Take-profit triggered at ${current_price:.2f} (target: ${position['take_profit_price']:.2f})",
                            'type': 'TAKE_PROFIT',
                            'pnl': profit_loss
                        })
                        del self.positions[sym] 
            total_value = self.cash
            position_value = 0
            for sym, position in self.positions.items():
                current_price = data_window['close'].iloc[-1] 
                position_value += position['shares'] * current_price
            total_value += position_value
            self.portfolio_history.append({
                            'date': data_window['ts'].iloc[-1],
                            'cash': float(self.cash),
                            'position_value': float(position_value),
                            'total_value': float(total_value)
                        })


            
            
            

        
