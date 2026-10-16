
import asyncio
import random
import time

from src.ipc.ring_buffer import RingBuffer


async def main():
    total_orders = 100
    buffer = RingBuffer(capacity=total_orders)

    start = time.perf_counter()

    try:
        # Orders generate karke buffer mein write karna
        for order_id in range(1, total_orders + 1):
            price = round(random.uniform(100, 500), 2)
            quantity = random.randint(1, 100)

            accepted = buffer.write(order_id, price, quantity)

            if not accepted:
                print("Buffer full!")
                break

            if order_id % 1000 == 0:
                await asyncio.sleep(0)

        # Buffer se orders read karna
        received = 0

        while True:
            order = buffer.read()

            if order is None:
                break

            received += 1

        elapsed = time.perf_counter() - start

        print("Orders generated:", total_orders)
        print("Orders read:", received)
        print("Time taken:", round(elapsed, 6), "seconds")

        if elapsed > 0:
            print("Orders per second:", int(received / elapsed))

    finally:
        buffer.close()


if __name__ == "__main__":
    asyncio.run(main())
