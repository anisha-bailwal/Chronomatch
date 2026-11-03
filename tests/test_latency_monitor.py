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


if __name__ == "__main__":
    unittest.main()
    