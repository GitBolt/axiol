import time


class Chronometer:

    def __init__(self) -> None:
        self.start_time = time.perf_counter()

    def __call__(self) -> float:
        return time.perf_counter() - self.start_time
