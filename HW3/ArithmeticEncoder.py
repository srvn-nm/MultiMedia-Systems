class ArithmeticEncoder:
    def __init__(self, model):
        self.model = model
        self.low = 0
        self.high = 1
        self.pending_bits = 0
        self.pending_bits_count = 0

    def encode(self, symbol):
        range_interval = self.high - self.low
        high_interval = self.low + range_interval * self.model.get_high(symbol)
        low_interval = self.low + range_interval * self.model.get_low(symbol)

        self.low = low_interval
        self.high = high_interval

        while True:
            if self.high < 0.5:
                self.output_bit(0)
            elif self.low >= 0.5:
                self.output_bit(1)
            elif 0.25 <= self.low < 0.75 and 0.25 <= self.high < 0.75:
                self.pending_bits += 1
                self.pending_bits_count += 1
            else:
                break
            self.low *= 2
            self.high *= 2
            self.low %= 1
            self.high %= 1

        while self.pending_bits_count > 0:
            self.output_bit(1)
            self.pending_bits_count -= 1

    def output_bit(self, bit):
        print(bit, end='')
        # Here you would append the bit to your encoded image or stream

    def finish(self):
        self.output_bit(0)  # If needed, output additional bits to ensure termination
        return ''
