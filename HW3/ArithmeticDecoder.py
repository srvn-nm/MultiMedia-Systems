class ArithmeticDecoder:
    def __init__(self, encoded_data, model):
        self.encoded_data = encoded_data
        self.model = model
        self.code = 0
        self.range_interval = 1

        # Initialize code
        for _ in range(32):  # Assume 32-bit precision
            self.code <<= 1
            self.code += self.read_bit()

    def read_bit(self):
        # Here you would read a bit from your encoded data stream
        # For the sake of this example, let's assume you have encoded data stored in a string
        bit = int(self.encoded_data[0])
        self.encoded_data = self.encoded_data[1:]
        return bit

    def decode(self):
        high = 1
        low = 0
        decoded_symbol = None

        while True:
            range_interval = high - low
            scaled_code = (self.code - low) / range_interval

            for symbol, probability in zip(self.model.symbols, self.model.probabilities):
                symbol_high = low + range_interval * probability
                if low <= scaled_code < symbol_high:
                    decoded_symbol = symbol
                    high = symbol_high
                    low = low + range_interval * self.model.get_low(symbol)
                    self.normalize_interval(high, low)
                    break

            if decoded_symbol is not None:
                break

        return decoded_symbol

    def normalize_interval(self, high, low):
        while True:
            if high < 0.5:
                pass
            elif low >= 0.5:
                self.code -= 0.5
                low -= 0.5
                high -= 0.5
            elif 0.25 <= low < 0.75 and 0.25 <= high < 0.75:
                self.code -= 0.25
                low -= 0.25
                high -= 0.25
            else:
                break

            high *= 2
            low *= 2
            self.code *= 2
            self.code += self.read_bit()
