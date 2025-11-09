class Account:
    """ Trading Account with position management and risk controls. """

    def __init__(self, cash: float, riskProfile: str, universe:list, mode:str="paper"):
        self.cash = cash
        self.risk_profile = riskProfile
        self.universe = universe
        self.positions = {}
        self.mode = mode  # "paper" or "live" paper by default

        self._setRiskParameters()
    def _setRiskParameters(self):
        """ Set risk parameters based on risk profile. """
        if self.risk_profile == '1':  # Conservative
            self.max_position_size = 0.10
            self.max_total_exposure = 0.50
            self.stop_loss_pct = 0.02
            self.max_daily_loss = 0.03
        elif self.risk_profile == '2':  # Moderate
            self.max_position_size = 0.15
            self.max_total_exposure = 0.70
            self.stop_loss_pct = 0.03
            self.max_daily_loss = 0.05
        elif self.risk_profile == '3':  # Aggressive
            self.max_position_size = 0.25
            self.max_total_exposure = 0.90
            self.stop_loss_pct = 0.05
            self.max_daily_loss = 0.10
        else:
            raise ValueError("Invalid risk profile")