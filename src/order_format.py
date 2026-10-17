
import struct

# Order ka format define karna
ORDER_FORMAT = struct.Struct("IdI")

# Ek sample trading order
order_id = 101
price = 250.50
quantity = 10

# Order ko bytes mein convert karna
order_data = ORDER_FORMAT.pack(order_id, price, quantity)

print("Original order:")
print("Order ID:", order_id)
print("Price:", price)
print("Quantity:", quantity)

print("\nOrder ka size:", ORDER_FORMAT.size, "bytes")
print("Stored data:", order_data)

# Bytes ko wapas values mein convert karna
decoded_order = ORDER_FORMAT.unpack(order_data)

print("\nDecoded order:", decoded_order)
