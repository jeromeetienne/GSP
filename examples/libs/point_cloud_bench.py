# Experiment to handle intellisense in VSCode
import matplotlib.figure
import numpy as np

import matplotlib
import matplotlib.pyplot as plt

import time

"""
Library to display point clouds using GSP.
"""

def display_benchmark_pure_matplotlib(figure=matplotlib.figure.Figure, log_enabled=False, max_bench_delay_seconds=10) -> float:
    """
    Benchmark the performance of pure Matplotlib rendering.

    Args:
        figure (matplotlib.figure.Figure): The Matplotlib figure to use for rendering.
        log_enabled (bool): Whether to log the benchmark results. default is False.
        max_bench_delay_seconds (int): Maximum time to wait for the benchmark in seconds. default is 10.

    Returns:
        float: The average time taken for one rendering in seconds.
    """
    plt.show(block=False)
    start_time = time.perf_counter()
    bench_count = 0
    for _ in range(100):
        figure.canvas.draw()
        figure.canvas.flush_events()
        # count the number of drawings
        bench_count += 1
        # break of the loop after 10 seconds maximum
        if time.perf_counter() - start_time > max_bench_delay_seconds:
            break
    # measure the elapsed time for {bench_count} drawings
    elapsed_time = time.perf_counter() - start_time
    # print the elapsed time and the FPS
    print(f"{bench_count} drawings took {elapsed_time:.2f}s; {bench_count / (elapsed_time):.2f} FPS")

    drawing_time = elapsed_time / bench_count
    return drawing_time

