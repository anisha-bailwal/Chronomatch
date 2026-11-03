import time


class LatencyMonitor:

    def measure_latency(self, function, *args, **kwargs):
        start_time = time.perf_counter()

        result = function(*args, **kwargs)

        end_time = time.perf_counter()

        latency = (end_time - start_time) * 1000

        return result, latency