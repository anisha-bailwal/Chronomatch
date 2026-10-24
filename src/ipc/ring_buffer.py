import math
import mmap
import struct
from src.order_format import ORDER_FORMAT, encode_order, decode_order


class RingBuffer:
    def __init__(self, capacity):
        # Validate buffer capacity
        if (
            not isinstance(capacity, int)
            or isinstance(capacity, bool)
            or capacity <= 0
        ):
            raise ValueError(
                "Capacity must be a positive integer"
            )

        self.order_format = ORDER_FORMAT
        self.capacity = capacity

        # Fixed memory for all buffer slots
        self.memory = mmap.mmap(
            -1, capacity * self.order_format.size
        )

        self.write_pos = 0
        self.read_pos = 0
        self.count = 0

     
  
    def write(self, order_id, side, price, quantity):
    # Validate order ID
      if (
        not isinstance(order_id, int)
        or isinstance(order_id, bool)
        or order_id < 0
      ):
        raise ValueError("Order ID must be a non-negative integer")

    # Validate side and encode order
      if not isinstance(side, str) or side.upper() not in ("BUY", "SELL"):
        raise ValueError("Side must be BUY or SELL")

      side = side.upper()

    # Validate price
      if (
        isinstance(price, bool)
        or not isinstance(price, (int, float))
        or not math.isfinite(price)
        or price <= 0
    ):
        raise ValueError("Price must be a finite positive number")

    # Validate quantity
      if (
        not isinstance(quantity, int)
        or isinstance(quantity, bool)
        or quantity <= 0
    ):
        raise ValueError("Quantity must be a positive integer")

    # Reject order if buffer is full
      if self.count == self.capacity:
        return False

      data = encode_order(order_id, side, price, quantity)

      position = self.write_pos * self.order_format.size
      self.memory.seek(position)
      self.memory.write(data)

      self.write_pos = (self.write_pos + 1) % self.capacity
      self.count += 1

      return True

   

    
    def read(self):
    # Return None if buffer is empty
      if self.count == 0:
        return None

      position = self.read_pos * self.order_format.size
      self.memory.seek(position)
      data = self.memory.read(self.order_format.size)

      order = decode_order(data)

      self.read_pos = (self.read_pos + 1) % self.capacity
      self.count -= 1

      return order


    def size(self):
        """Return the number of orders currently stored."""
        return self.count

    def is_empty(self):
        """Check whether the buffer is empty."""
        return self.count == 0

    def is_full(self):
        """Check whether the buffer is full."""
        return self.count == self.capacity

    def available_space(self):
        """Return the number of free slots in the buffer."""
        return self.capacity - self.count

    def close(self):
        """Release the allocated memory."""
        self.memory.close()


# Small manual test
if __name__ == "__main__":
    buffer = RingBuffer(capacity=3)

    try:
        buffer.write(101, 250.50, 10)
        buffer.write(102, 251.00, 5)
        buffer.write(103, 249.75, 8)

        print("Buffer size:", buffer.size())
        print("Is buffer full?", buffer.is_full())
        print("Available space:", buffer.available_space())

        print(
            "Fourth order accepted?",
            buffer.write(104, 252.00, 2)
        )

        print("Read:", buffer.read())
        print("Read:", buffer.read())

        print(
            "Fourth order accepted now?",
            buffer.write(104, 252.00, 2)
        )

        print("Buffer size:", buffer.size())
        print("Available space:", buffer.available_space())

        print("Read:", buffer.read())
        print("Read:", buffer.read())

        print("Is buffer empty?", buffer.is_empty())

    finally:
        buffer.close()
