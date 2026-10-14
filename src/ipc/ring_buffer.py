
import mmap
import struct


class RingBuffer:
    def __init__(self, capacity):
        self.order_format = struct.Struct("=IdI")
        self.capacity = capacity

        # Saare slots ke liye fixed memory
        self.memory = mmap.mmap(
            -1, capacity * self.order_format.size
        )

        self.write_pos = 0
        self.read_pos = 0
        self.count = 0

    def write(self, order_id, price, quantity):
        # Buffer full hai toh order reject karo
        if self.count == self.capacity:
            return False

        data = self.order_format.pack(
            order_id, price, quantity
        )

        position = self.write_pos * self.order_format.size
        self.memory.seek(position)
        self.memory.write(data)

        self.write_pos = (self.write_pos + 1) % self.capacity
        self.count += 1
        return True

    def read(self):
        # Buffer empty hai
        if self.count == 0:
            return None

        position = self.read_pos * self.order_format.size
        self.memory.seek(position)
        data = self.memory.read(self.order_format.size)

        order = self.order_format.unpack(data)

        self.read_pos = (self.read_pos + 1) % self.capacity
        self.count -= 1
        return order

    def close(self):
        self.memory.close()


# Chhota test
if __name__ == "__main__":
    buffer = RingBuffer(capacity=3)

    buffer.write(101, 250.50, 10)
    buffer.write(102, 251.00, 5)
    buffer.write(103, 249.75, 8)

    # Buffer full hai, isliye ye order reject hoga
    print("Fourth order accepted?", buffer.write(104, 252.00, 2))

    print("Read:", buffer.read())
    print("Read:", buffer.read())

    # Ab ek slot free hai
    print("Fourth order accepted now?", buffer.write(104, 252.00, 2))

    print("Read:", buffer.read())
    print("Read:", buffer.read())

    buffer.close()
