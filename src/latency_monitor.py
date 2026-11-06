
import time


class LatencyMonitor:
    """
    Monitors the time taken by functions to execute.

    This class measures order processing latency in milliseconds
    using Python's high-resolution performance counter. It stores
    individual latency values for future analysis.

    It also provides methods to calculate average, minimum,
    maximum latency and total number of processed orders.
    """

    def __init__(self):
        self.latencies = []

    def measure_latency(self, function, *args, **kwargs):
        start_time = time.perf_counter()
        result = function(*args, **kwargs)
        end_time = time.perf_counter()

        latency = (end_time - start_time) * 1000
        self.latencies.append(latency)

        return result, latency

    def get_average_latency(self):
        if not self.latencies:
            return 0
        return sum(self.latencies) / len(self.latencies)

    def get_min_latency(self):
        if not self.latencies:
            return 0
        return min(self.latencies)

    def get_max_latency(self):
        if not self.latencies:
            return 0
        return max(self.latencies)

    def get_total_orders(self):
        return len(self.latencies)
