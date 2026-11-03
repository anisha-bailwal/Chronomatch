from src.latency_monitor import LatencyMonitor
from src.matching_engine import MatchingEngine

engine = MatchingEngine()
monitor = LatencyMonitor()

# Add sell orders
print("Adding sell orders...")
engine.add_order(1, "SELL", 100, 5)
engine.add_order(2, "SELL", 102, 3)

# Add a buy order that matches
print("\nAdding buy order...")
trades, latency = monitor.measure_latency(
    engine.add_order, 3, "BUY", 101, 2
)

print(f"Order Processing Latency: {latency:.4f} ms")

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
