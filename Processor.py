from typing import List, Optional

from Process import Process


class Processor:
    def __init__(self, id: int) -> None:
        self.id: int = id  # ID do processador
        self.current_process: Optional[Process] = None  # Processo atualmente sendo executado
        self.idle_time: float = 0  # Tempo ocioso do processador
        self.last_idle_time_update: float = 0  # Última atualização de tempo ocioso

    def is_idle(self, current_time: float) -> bool:
        return self.current_process is None

    def update_idle_time(self, current_time: float) -> None:
        if self.is_idle(current_time):
            self.idle_time += (current_time - self.last_idle_time_update)
        self.last_idle_time_update = current_time

    def assign_process(self, process: Process, current_time: float) -> None:
        self.update_idle_time(current_time)
        self.current_process = process
        process.start_time = current_time

    def release_process(self, current_time: float) -> None:
        if self.current_process:
            self.current_process.finish_time = current_time
            self.current_process = None
        self.last_idle_time_update = current_time
