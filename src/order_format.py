
import struct

# Order side mapping: BUY = 0, SELL = 1
BUY = 0
SELL = 1

# Order format: Order ID, Side, Price, Quantity
ORDER_FORMAT = struct.Struct("=IBdI")


def encode_order(order_id, side, price, quantity):
    """Convert an order into bytes."""
    if side not in ("BUY", "SELL"):
        raise ValueError("Side must be BUY or SELL")

    side_code = BUY if side == "BUY" else SELL

    return ORDER_FORMAT.pack(
        order_id, side_code, price, quantity
    )


def decode_order(order_data):
    """Convert stored bytes back into an order."""
    order_id, side_code, price, quantity = (
        ORDER_FORMAT.unpack(order_data)
    )

    if side_code not in (BUY, SELL):
        raise ValueError("Invalid order side code")

    side = "BUY" if side_code == BUY else "SELL"

    return order_id, side, price, quantity


if __name__ == "__main__":
    order_id = 101
    side = "BUY"
    price = 250.50
    quantity = 10

    order_data = encode_order(
        order_id, side, price, quantity
    )

    print("Original order:")
    print("Order ID:", order_id)
    print("Side:", side)
    print("Price:", price)
    print("Quantity:", quantity)

    print("\nOrder size:", ORDER_FORMAT.size, "bytes")
    print("Stored data:", order_data)
    print("Decoded order:", decode_order(order_data))
