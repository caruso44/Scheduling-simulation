from typing import List, Optional
import heapq
from collections import deque

from Processor import Processor
from Process import Process


class Scheduler:
    def __init__(self, processors: list, scheduling_algorithm: str, quantum: int = 3):
        self.processors : list[Processor] = processors  # Lista de processadores
        self.scheduling_algorithm = scheduling_algorithm  # Algoritmo de escalonamento
        self.queue = deque()  # Fila de processos para RR e FIFO
        self.quantum = quantum  # Quantum para o Round Robin

    def add_process(self, process: Process):
        self.queue.append(process)

    def schedule(self, current_time: int):
        if self.scheduling_algorithm == 'fifo':
            self.schedule_fifo(current_time)
        elif self.scheduling_algorithm == 'sjf':
            self.schedule_sjf(current_time)
        elif self.scheduling_algorithm == 'round_robin':
            self.schedule_round_robin(current_time)
        elif self.scheduling_algorithm == 'priority':
            self.schedule_priority(current_time)
            
    def schedule_fifo(self, current_time: int):
        for processor in self.processors:
            if processor.is_idle(current_time) and self.queue:
                process = self.queue.popleft()
                processor.assign_process(process, current_time)

    def schedule_sjf(self, current_time: int):
        # Shortest Job First (SJF) - escolhe o processo com menor duração restante
        if self.queue:
            self.queue = deque(sorted(self.queue, key=lambda p: p.remaining_time))
        for processor in self.processors:
            if processor.is_idle(current_time) and self.queue:
                process = self.queue.popleft()
                processor.assign_process(process, current_time)

    def schedule_round_robin(self, current_time: int):
        for processor in self.processors:
            if processor.is_idle(current_time) and self.queue:
                process = self.queue.popleft()
                processor.assign_process(process, current_time)
            elif processor.current_process:
                processor.current_process.remaining_time -= self.quantum
                if processor.current_process.remaining_time > 0:
                    self.queue.append(processor.current_process)  # Preempção e volta à fila
                processor.release_process(current_time)

    def schedule_priority(self, current_time: int):
        if self.queue:
            self.queue = deque(sorted(self.queue, key=lambda p: p.priority))
        for processor in self.processors:
            if processor.is_idle(current_time) and self.queue:
                process = self.queue.popleft()
                processor.assign_process(process, current_time)