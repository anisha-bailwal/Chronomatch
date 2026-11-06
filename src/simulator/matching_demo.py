
from src.latency_monitor import LatencyMonitor
from src.matching_engine import MatchingEngine

engine = MatchingEngine()
monitor = LatencyMonitor()

# Add sell orders
print("Adding sell orders...")

_, latency1 = monitor.measure_latency(
    engine.add_order, 1, "SELL", 100, 5
)

_, latency2 = monitor.measure_latency(
    engine.add_order, 2, "SELL", 102, 3
)

# Add a buy order that matches
print("\nAdding buy order...")

trades, latency3 = monitor.measure_latency(
    engine.add_order, 3, "BUY", 101, 2
)

print("\nIndividual Order Latencies:")
print(f"Sell Order 1: {latency1:.4f} ms")
print(f"Sell Order 2: {latency2:.4f} ms")
print(f"Buy Order 3: {latency3:.4f} ms")

# Display latency statistics
print("\nLatency Statistics:")
print(f"Average Latency: {monitor.get_average_latency():.4f} ms")
print(f"Minimum Latency: {monitor.get_min_latency():.4f} ms")
print(f"Maximum Latency: {monitor.get_max_latency():.4f} ms")
print(f"Total Orders Processed: {monitor.get_total_orders()}")

# Display completed trades
print("\nCompleted Trades:")
for trade in trades:
    print(
        f"Buy Order: {trade.buy_order_id}, "
        f"Sell Order: {trade.sell_order_id}, "
        f"Price: {trade.price}, "
        f"Quantity: {trade.quantity}"
    )

# Display remaining orders
engine.display_order_book()
