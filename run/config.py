"""Where a run lives. Every script here works on one run, named by BENCH_RUN (e.g. BENCH_RUN=run_002)."""
import os, sys

RUN_ID = os.environ.get('BENCH_RUN') or sys.exit('set BENCH_RUN, e.g. BENCH_RUN=run_002')
DATASET_ID = 'benchmark_001'
DATA = os.path.expanduser('~/Desktop/benchmark/benchmark-data')
RUN = os.path.expanduser(f'~/Desktop/benchmark/runs/{RUN_ID}')
SKILLS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'skills')
