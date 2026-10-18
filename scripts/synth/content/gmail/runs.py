"""david.barron.runs@gmail.com — the second personal Gmail (created 2025-12-03). Hand-written threads, split by period:
runs_a.py (2025-12-03 .. 2026-05-31) and runs_b.py (2026-06-01 .. 2026-10-17)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _dsl import *
from runs_a import THREADS as A_THREADS
from runs_b import THREADS as B_THREADS

THREADS = A_THREADS + B_THREADS
