
import mmap
import struct

# fixed format for order data: order_id (int), price (double), quantity (int)
order_format = struct.Struct("IdI")

# to demonstrate memory-mapped file usage, we will create a memory-mapped object and write/read order data to/from it
with mmap.mmap(-1, order_format.size) as memory:

    # Order values
    order_id = 101
    price = 250.50
    quantity = 10

    # convert order values to bytes using the defined format
    order_data = order_format.pack(
        order_id, price, quantity
    )

    # write the order data to the memory-mapped object
    memory.write(order_data)

    # reset the file pointer to the beginning of the memory-mapped object
    memory.seek(0)

    # read the data back from the memory-mapped object
    saved_data = memory.read(order_format.size)

    # unpack the saved data back into order values
    saved_order = order_format.unpack(saved_data)

    print("Order read from memory:", saved_order)
