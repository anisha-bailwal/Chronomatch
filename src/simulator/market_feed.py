
import asyncio
import random
import time


async def generate_orders(total_orders):
    start = time.perf_counter()

    for order_id in range(1, total_orders + 1):
        price = round(random.uniform(100, 500), 2)
        quantity = random.randint(1, 100)

        print(
            f"Order ID: {order_id}, "
            f"Price: {price}, Quantity: {quantity}"
        )

        # Doosre async tasks ko mauka dena
        if order_id % 1000 == 0:
            await asyncio.sleep(0)

    elapsed = time.perf_counter() - start

    print("\nTotal orders:", total_orders)
    print("Time taken:", round(elapsed, 4), "seconds")

    if elapsed > 0:
        print("Orders per second:", int(total_orders / elapsed))


async def main():
    await generate_orders(100)


if __name__ == "__main__":
    asyncio.run(main())
