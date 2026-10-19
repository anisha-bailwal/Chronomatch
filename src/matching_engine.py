
from dataclasses import dataclass, field


@dataclass
class Order:
    order_id: int
    side: str
    price: float
    quantity: int


@dataclass
class Trade:
    buy_order_id: int
    sell_order_id: int
    price: float
    quantity: int


@dataclass
class MatchingEngine:
    buy_orders: list = field(default_factory=list)
    sell_orders: list = field(default_factory=list)

    def add_order(self, order_id, side, price, quantity):
        side = side.upper()

        if side not in ("BUY", "SELL"):
            raise ValueError("Side must be BUY or SELL")

        if price <= 0 or quantity <= 0:
            raise ValueError("Price and quantity must be positive")

        incoming = Order(order_id, side, price, quantity)
        trades = []

        while incoming.quantity > 0:
            book = self.sell_orders if side == "BUY" else self.buy_orders

            if not book:
                break

            # Best price: lowest sell or highest buy
            best = book[0]

            # Check whether the orders can match
            crosses = (
                incoming.price >= best.price
                if side == "BUY"
                else incoming.price <= best.price
            )

            if not crosses:
                break

            traded_quantity = min(incoming.quantity, best.quantity)

            # Trade executes at the resting order's price
            trade_price = best.price

            if side == "BUY":
                trades.append(
                    Trade(order_id, best.order_id,
                          trade_price, traded_quantity)
                )
            else:
                trades.append(
                    Trade(best.order_id, order_id,
                          trade_price, traded_quantity)
                )

            incoming.quantity -= traded_quantity
            best.quantity -= traded_quantity

            if best.quantity == 0:
                book.pop(0)

        # Add any unfilled quantity to the correct book
        if incoming.quantity > 0:
            book = self.buy_orders if side == "BUY" else self.sell_orders
            book.append(incoming)

            # Sort by best price. Stable sorting preserves FIFO
            # order when prices are equal.
            if side == "BUY":
                book.sort(key=lambda order: -order.price)
            else:
                book.sort(key=lambda order: order.price)

        return trades
    
    def get_best_bid(self):
        if not self.buy_orders:
            return None
        return self.buy_orders[0].price

    def get_best_ask(self):
        if not self.sell_orders:
            return None
        return self.sell_orders[0].price

    def get_spread(self):
        bid = self.get_best_bid()
        ask = self.get_best_ask()

        if bid is None or ask is None:
            return None

        return ask - bid

    def display_order_book(self):
        print("\n========== CHRONOSMATCH ==========")
        print("BUY ORDERS")
        print(f"{'Order ID':<12}{'Price':<12}{'Quantity':<10}")

        for order in self.buy_orders:
            print(
                f"{order.order_id:<12}"
                f"{order.price:<12.2f}"
                f"{order.quantity:<10}"
            )

        print("\nSELL ORDERS")
        print(f"{'Order ID':<12}{'Price':<12}{'Quantity':<10}")

        for order in self.sell_orders:
            print(
                f"{order.order_id:<12}"
                f"{order.price:<12.2f}"
                f"{order.quantity:<10}"
            )

        print("\nBest Bid:", self.get_best_bid())
        print("Best Ask:", self.get_best_ask())
        print("Spread:", self.get_spread())
        print("==================================")
