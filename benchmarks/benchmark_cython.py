import timeit
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from matching_engine import MatchingEngine as CythonEngine
from src.matching_engine import MatchingEngine as PythonEngine


def run_python_engine():
    engine = PythonEngine()
    engine.add_order(1, "SELL", 100, 10)
    engine.add_order(2, "BUY", 100, 5)


def run_cython_engine():
    engine = CythonEngine()
    engine.add_order(1, "SELL", 100, 10)
    engine.add_order(2, "BUY", 100, 5)


runs = 10000

python_time = timeit.timeit(run_python_engine, number=runs)
cython_time = timeit.timeit(run_cython_engine, number=runs)

print(f"Runs per engine: {runs}")
print(f"Python time: {python_time:.4f} seconds")
print(f"Cython time: {cython_time:.4f} seconds")

if cython_time > 0:
    print(f"Speed ratio (Python/Cython): {python_time / cython_time:.2f}x")