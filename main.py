class MAIN: 
    def __init__(self):
        self.value = "Hello, This is a \n === Agentic Trading System === \n Welcome! Let's set up your trading environment."

    def greet(self):
        return self.value
    
    def askinput(self, prompt):
        return input(prompt)
    
    def askQuestions(self):
        print(self.greet())
        capital = self.askinput("How much capital do you want to trade with? ")
        riskTolerance = self.askinput("2. What's your risk tolerance? \n"
        "   (1) Conservative - Max 10% per position, 50% total exposure\n"
        "   (2) Moderate - Max 15% per position, 70% total exposure\n"
        "   (3) Aggressive - Max 25% per position, 90% total exposure\n")
        stock = self.askinput("3. What markets are you interested in? \n"
        "(1) Single stock (AAPL)\n"
        "(2) Multiple stocks (20 bascket)\n"
        "(3) Tech basket (5 stocks)\n"
        "(4) Custom list\n")
        return {
            "capital": capital,
            "riskTolerance": riskTolerance,
            "stock": stock
        }
    def processAnswers(self, answers):
        print("Setting up your trading environment with the following parameters:")
        print(f"Capital: {answers['capital']}")
        print(f"Risk Tolerance: {answers['riskTolerance']}")
        print(f"Stock Selection: {answers['stock']}")
        # Further processing can be done here
        # Validate capital
        try:
            capital = float(answers['capital'])
            if capital <= 0:
                raise ValueError("Capital must be positive")
        except ValueError:
            print("Error: Capital must be a valid number")
            return False

        # Validate risk tolerance
        if answers['riskTolerance'] not in ['1', '2', '3']:
            print("Error: Invalid risk tolerance selection")
            return False

        # Validate stock selection
        if answers['stock'] not in ['1', '2', '3', '4']:
            print("Error: Invalid stock selection")
            return False

        return True
    
    def createAccount(self, answers):
        from data.account import Account
        universe = []
        if answers['stock'] == '1':
            universe = ['AAPL']
        elif answers['stock'] == '2':
            universe = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'FB', 'TSLA', 'BRK.B', 'JPM', 'JNJ', 'V', 
                        'WMT', 'PG', 'UNH', 'DIS', 'NVDA', 'HD', 'MA', 'PYPL', 'BAC', 'VZ']
        elif answers['stock'] == '3':
            universe = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'FB']
        elif answers['stock'] == '4':
            custom_stocks = self.askinput("Enter your custom stock symbols separated by commas: ")
            universe = [stock.strip().upper() for stock in custom_stocks.split(',')]

        account = Account(
            cash=float(answers['capital']),
            riskProfile=answers['riskTolerance'],
            universe=universe,
            mode="paper"
        )
        print("Account created successfully!")
        return account


if __name__ == "__main__":
    app = MAIN()
    answers = app.askQuestions()
    if app.processAnswers(answers):
        account = app.createAccount(answers)