import unittest
import time

from src.latency_monitor import LatencyMonitor


class TestLatencyMonitor(unittest.TestCase):

    def setUp(self):
        self.monitor = LatencyMonitor()

    def test_measure_latency(self):
        def sample_function():
            time.sleep(0.01)
            return "Completed"

        result, latency = self.monitor.measure_latency(sample_function)

        self.assertEqual(result, "Completed")
        self.assertGreater(latency, 0)

    def test_latency_is_stored(self):
        self.monitor.measure_latency(lambda: "Done")

        self.assertEqual(len(self.monitor.latencies), 1)

    def test_average_latency(self):
        self.monitor.latencies = [10, 20, 30]

        self.assertEqual(self.monitor.get_average_latency(), 20)

    def test_min_latency(self):
        self.monitor.latencies = [10, 20, 30]

        self.assertEqual(self.monitor.get_min_latency(), 10)

    def test_max_latency(self):
        self.monitor.latencies = [10, 20, 30]

        self.assertEqual(self.monitor.get_max_latency(), 30)

    def test_empty_latency_metrics(self):
        self.assertEqual(self.monitor.get_average_latency(), 0)
        self.assertEqual(self.monitor.get_min_latency(), 0)
        self.assertEqual(self.monitor.get_max_latency(), 0)

        def test_total_orders(self):
            self.monitor.measure_latency(lambda: "Done")
            self.monitor.measure_latency(lambda: "Done")

            self.assertEqual(self.monitor.get_total_orders(), 2)

if __name__ == "__main__":
    unittest.main()