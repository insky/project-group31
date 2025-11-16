"""Benchmark suite for measuring suggest_command performance."""

from time import perf_counter

from src.intelligent_command import suggest_command

def benchmark_suggest_command(iterations: int = 1000) -> float:
    """Measure the average execution time per suggest_command invocation."""
    inputs = ("hlep", "addbirthday", "exlt", "phon")
    start = perf_counter()
    for index in range(iterations):
        misspelled = inputs[index % len(inputs)]
        suggest_command(misspelled)
    total_duration = perf_counter() - start
    return total_duration / iterations


def run_benchmark(iterations: int = 1000) -> None:
    """Run the benchmark suite and print aggregated timing data."""
    suggest_command("smth")  # Warm-up call

    average_duration = benchmark_suggest_command(iterations)
    print(
        "suggest_command average: "
        f"{average_duration * 1_000_000:.2f} microseconds"
    )


if __name__ == "__main__":
    run_benchmark()
