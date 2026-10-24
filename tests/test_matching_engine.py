
import unittest
from src.matching_engine import MatchingEngine


class TestMatchingEngine(unittest.TestCase):

    def setUp(self):
        self.engine = MatchingEngine()

    def test_orders_do_not_match_when_prices_do_not_cross(self):
        self.engine.add_order(1, "BUY", 99, 5)
        trades = self.engine.add_order(2, "SELL", 100, 5)

        self.assertEqual(trades, [])
        self.assertEqual(len(self.engine.buy_orders), 1)
        self.assertEqual(len(self.engine.sell_orders), 1)

    def test_matching_orders_create_trade(self):
        self.engine.add_order(1, "SELL", 100, 5)
        trades = self.engine.add_order(2, "BUY", 101, 3)

        self.assertEqual(len(trades), 1)
        self.assertEqual(trades[0].price, 100)
        self.assertEqual(trades[0].quantity, 3)
        self.assertEqual(trades[0].buy_order_id, 2)
        self.assertEqual(trades[0].sell_order_id, 1)
        self.assertEqual(self.engine.sell_orders[0].quantity, 2)

    def test_partial_fill_leaves_remaining_buy_quantity(self):
        self.engine.add_order(1, "SELL", 100, 2)
        trades = self.engine.add_order(2, "BUY", 105, 5)

        self.assertEqual(trades[0].quantity, 2)
        self.assertEqual(len(self.engine.sell_orders), 0)
        self.assertEqual(len(self.engine.buy_orders), 1)
        self.assertEqual(self.engine.buy_orders[0].quantity, 3)

    def test_same_price_uses_first_in_first_out(self):
        self.engine.add_order(1, "SELL", 100, 2)
        self.engine.add_order(2, "SELL", 100, 2)

        trades = self.engine.add_order(3, "BUY", 100, 3)

        self.assertEqual(len(trades), 2)
        self.assertEqual(trades[0].sell_order_id, 1)
        self.assertEqual(trades[0].quantity, 2)
        self.assertEqual(trades[1].sell_order_id, 2)
        self.assertEqual(trades[1].quantity, 1)

    def test_best_prices_and_spread(self):
        self.engine.add_order(1, "BUY", 98, 5)
        self.engine.add_order(2, "BUY", 99, 3)
        self.engine.add_order(3, "SELL", 102, 4)
        self.engine.add_order(4, "SELL", 101, 2)

        self.assertEqual(self.engine.get_best_bid(), 99)
        self.assertEqual(self.engine.get_best_ask(), 101)
        self.assertEqual(self.engine.get_spread(), 2)


if __name__ == "__main__":
    unittest.main()
def test_duplicate_order_id_is_rejected(self):
    self.engine.add_order(1, "BUY", 99, 5)

    with self.assertRaisesRegex(
        ValueError, "Order ID already exists"
    ):
        self.engine.add_order(1, "SELL", 100, 3)
def test_non_string_side_is_rejected(self):
    with self.assertRaisesRegex(
        ValueError, "Side must be BUY or SELL"
    ):
        self.engine.add_order(1, 123, 100, 5)  

def test_non_string_side_is_rejected(self):
        with self.assertRaises(ValueError):
            self.engine.add_order(1, 123, 100, 5)

def test_non_positive_price_is_rejected(self):
        with self.assertRaises(ValueError):
            self.engine.add_order(1, "BUY", 0, 5)

def test_non_integer_quantity_is_rejected(self):
        with self.assertRaises(ValueError):
            self.engine.add_order(1, "BUY", 100, 2.5)

def test_duplicate_order_id_is_rejected(self):
        self.engine.add_order(1, "BUY", 99, 5)

        with self.assertRaisesRegex(
            ValueError, "Order ID already exists"
        ):
            self.engine.add_order(1, "SELL", 100, 3)

def test_trade_history_records_executed_trades(self):
        self.engine.add_order(1, "SELL", 100, 5)
        self.engine.add_order(2, "BUY", 100, 3)

        self.assertEqual(len(self.engine.trade_history), 1)
        self.assertEqual(
            self.engine.trade_history[0].quantity, 3
        )
        self.assertEqual(
            self.engine.trade_history[0].sell_order_id, 1
        )
