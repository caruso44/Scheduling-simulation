from typing import List, Optional

class Process:
    def __init__(self, pid: int, arrival_time: float, duration: int, priority: int):
        self.pid = pid
        self.arrival_time = arrival_time
        self.duration = duration
        self.remaining_time = duration
        self.priority = priority  
        self.start_time = None
        self.finish_time = None

    def is_finished(self) -> bool:
        return self.remaining_time <= 0