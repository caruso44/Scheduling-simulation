import random
import heapq
import numpy as np
from typing import List, Optional

from Processor import Processor
from Process import Process
from Scheduler import Scheduler

class Simulation:
    def __init__(self, num_processors: int, scheduling_algorithm: str, arrival_rate: float, quantum: int) -> None:
        self.current_time: float = 0
        self.processes: List[Process] = []
        self.processors: List[Processor] = [Processor(i) for i in range(num_processors)]
        self.scheduler: Scheduler = Scheduler(self.processors, scheduling_algorithm, quantum)
        self.arrival_rate: float = arrival_rate  # Taxa de chegada dos processos

    def create_process(self, pid: int):
        arrival_time = self.current_time
        duration = random.randint(1, 10) 
        priority = random.randint(1, 5) 
        process = Process(pid, arrival_time, duration, priority)
        self.processes.append(process)
        self.scheduler.add_process(process)

    def simulate(self, total_time: int) -> None:
        process_id = 0
        while self.current_time < total_time:
            # Gerar novos processos baseados na distribuição de Poisson
            if np.random.binomial(n=1, p=self.arrival_rate):
                n_process = random.randint(1, 5) 
                for i in range(n_process):
                    self.create_process(process_id)
                    process_id += 1
            
            # Escalonamento de processos
            self.scheduler.schedule(self.current_time)

            # Atualização do tempo dos processadores e processos
            for processor in self.processors:
                processor.update_idle_time(self.current_time)
                if processor.current_process:
                    processor.current_process.remaining_time -= 1
                    if processor.current_process.is_finished():
                        processor.release_process(self.current_time)
            
            self.current_time += 1

    def get_average_idle_time(self) -> float:
        total_idle_time = sum(processor.idle_time for processor in self.processors)
        return total_idle_time / len(self.processors)
