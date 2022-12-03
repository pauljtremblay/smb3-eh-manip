class LSFR:
    def __init__(self):
        self.data = [0x88, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

    def next(self):
        temp = self.data[0] & 0x2
        carry = not not ((self.data[1] & 0x2) ^ temp)
        for i, rng_byte in enumerate(self.data):
            b = rng_byte & 1
            self.data[i] = (carry << 7) | (rng_byte >> 1)
            carry = b
        return self.data
