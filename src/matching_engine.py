import math
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
@dataclass
class MatchingEngine:
    buy_orders: list = field(default_factory=list)
    sell_orders: list = field(default_factory=list)
    trade_history: list = field(default_factory=list)

    def add_order(self, order_id, side, price, quantity):
        # Validate order side
        if not isinstance(side, str):
            raise ValueError("Side must be BUY or SELL")

        side = side.upper()

        if side not in ("BUY", "SELL"):
            raise ValueError("Side must be BUY or SELL")

        # Validate price and quantity
        if (
            isinstance(price, bool)
            or not isinstance(price, (int, float))
            or not math.isfinite(price)
            or price <= 0
        ):
            raise ValueError("Price must be a finite positive number")

        if (
            isinstance(quantity, bool)
            or not isinstance(quantity, int)
            or quantity <= 0
        ):
            raise ValueError("Quantity must be a positive integer")

        # Prevent duplicate IDs among active orders
        existing_ids = {
            order.order_id
            for order in self.buy_orders + self.sell_orders
        }

        if order_id in existing_ids:
            raise ValueError("Order ID already exists")

        incoming = Order(order_id, side, price, quantity)
        trades = []

        # Match incoming order against the opposite order book
        while incoming.quantity > 0:
            book = (
                self.sell_orders
                if side == "BUY"
                else self.buy_orders
            )

            if not book:
                break

            # Best sell = lowest price; best buy = highest price
            best = book[0]

            crosses = (
                incoming.price >= best.price
                if side == "BUY"
                else incoming.price <= best.price
            )

            if not crosses:
                break

            traded_quantity = min(
                incoming.quantity,
                best.quantity
            )

            # Trade executes at the resting order's price
            trade_price = best.price

            if side == "BUY":
                trades.append(
                    Trade(
                        buy_order_id=order_id,
                        sell_order_id=best.order_id,
                        price=trade_price,
                        quantity=traded_quantity
                    )
                )
            else:
                trades.append(
                    Trade(
                        buy_order_id=best.order_id,
                        sell_order_id=order_id,
                        price=trade_price,
                        quantity=traded_quantity
                    )
                )

            incoming.quantity -= traded_quantity
            best.quantity -= traded_quantity

            # Remove fully filled resting order
            if best.quantity == 0:
                book.pop(0)

        # Store any remaining quantity in the order book
        if incoming.quantity > 0:
            book = (
                self.buy_orders
                if side == "BUY"
                else self.sell_orders
            )

            book.append(incoming)

            # Sort by best price; stable sort preserves FIFO
            if side == "BUY":
                book.sort(key=lambda order: -order.price)
            else:
                book.sort(key=lambda order: order.price)

        self.trade_history.extend(trades)
        return trades
    
    def display_trade_history(self):
        print("\n========== TRADE HISTORY ==========")

        if not self.trade_history:
            print("No trades executed yet.")
            print("===================================")
            return

        print(
            f"{'Buy Order':<12}"
            f"{'Sell Order':<12}"
            f"{'Price':<12}"
            f"{'Quantity':<10}"
        )

        for trade in self.trade_history:
            print(
                f"{trade.buy_order_id:<12}"
                f"{trade.sell_order_id:<12}"
                f"{trade.price:<12.2f}"
                f"{trade.quantity:<10}"
            )

        print("===================================")


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
