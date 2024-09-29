from typing import List, Optional
import heapq

from Processor import Processor
from Process import Process


class Scheduler:
    def __init__(self, processors: List[Processor], scheduling_algorithm: str) -> None:
        self.processors: List[Processor] = processors  # Lista de processadores
        self.scheduling_algorithm: str = scheduling_algorithm  # Algoritmo de escalonamento
        self.queue: List[tuple[float, int, Process]] = []  # Fila de processos
        self.counter: int = 0  # Contador para desempate

    def add_process(self, process: Process) -> None:
        # Usamos um contador para desempate, garantindo que o heapq funcione corretamente
        heapq.heappush(self.queue, (process.arrival_time, self.counter, process))
        self.counter += 1

    def schedule(self, current_time: float) -> None:
        if self.scheduling_algorithm == 'fifo':
            self.schedule_fifo(current_time)
        elif self.scheduling_algorithm == 'sjf':
            self.schedule_sjf(current_time)

    def schedule_fifo(self, current_time: float) -> None:
        # First-In-First-Out (FIFO) - escalona com base no tempo de chegada
        for processor in self.processors:
            if processor.is_idle(current_time) and self.queue:
                _, _, process = heapq.heappop(self.queue)
                processor.assign_process(process, current_time)

    def schedule_sjf(self, current_time: float) -> None:
        # Shortest Job First (SJF) - escolhe o processo com menor duração restante
        for processor in self.processors:
            if processor.is_idle(current_time) and self.queue:
                self.queue.sort(key=lambda x: x[2].duration)  # Ordena pelo tempo de duração do processo
                _, _, process = self.queue.pop(0)
                processor.assign_process(process, current_time)