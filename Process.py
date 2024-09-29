from typing import List, Optional

class Process:
    def __init__(self, pid: int, arrival_time: float, duration: int) -> None:
        self.pid: int = pid  # ID do processo
        self.arrival_time: float = arrival_time  # Tempo de chegada
        self.duration: int = duration  # Duração total do processo
        self.remaining_time: int = duration  # Tempo restante para completar
        self.start_time: Optional[float] = None  # Tempo de início
        self.finish_time: Optional[float] = None  # Tempo de término

    def is_finished(self) -> bool:
        return self.remaining_time <= 0