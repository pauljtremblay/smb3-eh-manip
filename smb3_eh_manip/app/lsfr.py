class LSFR:
    def __init__(self, data=None):
        self.data = (
            [0x88, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00] if not data else data
        )

    def clone(self):
        return LSFR(list(self.data))

    def get(self, byte):
        return self.data[byte]

    def next_n(self, iterations):
        for _x in range(iterations):
            self.next()

    def next(self):
        temp = self.data[0] & 0x2
        carry = not not ((self.data[1] & 0x2) ^ temp)
        for i, rng_byte in enumerate(self.data):
            b = rng_byte & 1
            self.data[i] = (carry << 7) | (rng_byte >> 1)
            carry = b
        return self.data
