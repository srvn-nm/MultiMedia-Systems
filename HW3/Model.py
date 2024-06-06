class Model:
    def __init__(self, symbols, probabilities):
        self.symbols = symbols
        self.probabilities = probabilities

    def get_low(self, symbol):
        low = 0
        for sym, prob in zip(self.symbols, self.probabilities):
            if sym == symbol:
                return low
            low += prob
        raise ValueError("Symbol not found in model.")

    def get_high(self, symbol):
        high = 0
        for sym, prob in zip(self.symbols, self.probabilities):
            if sym == symbol:
                return high + prob
            high += prob
        raise ValueError("Symbol not found in model.")
