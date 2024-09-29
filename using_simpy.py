import simpy
import random
import numpy as np
from abc import ABC, abstractmethod

# Constants
NUM_PROCESSORS = 1        # Fixed number of processors
QUANTUM = 1               # Quantum for Round Robin (updated to 1 unit)
MEAN_DURATION = 5         # Mean process duration (updated)
STD_DURATION = 1          # Standard deviation of process duration (updated)
ARRIVAL_RATE = 0.5        # Arrival rate (processes per unit time, updated)
SIM_TIME = 200            # Simulation time (updated)


# Process class representing a process in the system
class Process:
    def __init__(self, env, pid, duration):
        self.env = env
        self.pid = pid
        self.duration = duration
        self.start_time = None
        self.end_time = None
        self.ready_time = 0  # Total time spent in ready state
        self.added_to_ready_queue = None  # Time when the process was added to the ready queue


# CPU class representing a processor
class CPU:
    def __init__(self, env):
        self.env = env
        self.processor = simpy.Resource(env, capacity=NUM_PROCESSORS)


# Abstract base class for scheduling algorithms
class Scheduler(ABC):
    def __init__(self, env, cpu):
        self.env = env
        self.cpu = cpu
        self.ready_queue = []

    @abstractmethod
    def schedule(self):
        pass

    def add_process(self, process):
        process.added_to_ready_queue = self.env.now  # Track when process enters the ready queue
        self.ready_queue.append(process)
        self.schedule()


# First Come, First Served (FCFS) Scheduler
class FCFSScheduler(Scheduler):
    def schedule(self):
        if self.ready_queue and self.cpu.processor.count < NUM_PROCESSORS:
            process = self.ready_queue.pop(0)
            self.env.process(self.execute_process(process))

    def execute_process(self, process):
        with self.cpu.processor.request() as req:
            yield req
            process.start_time = self.env.now
            # Calculate how long the process was in the ready queue
            process.ready_time += self.env.now - process.added_to_ready_queue
            yield self.env.timeout(process.duration)
            process.end_time = self.env.now
            print(f"Process {process.pid} finished at {self.env.now}")
            self.schedule()


# Shortest Job First (SJF) Scheduler
class SJFScheduler(Scheduler):
    def schedule(self):
        if self.ready_queue and self.cpu.processor.count < NUM_PROCESSORS:
            # Sort by shortest duration first
            self.ready_queue.sort(key=lambda p: p.duration)
            process = self.ready_queue.pop(0)
            self.env.process(self.execute_process(process))

    def execute_process(self, process):
        with self.cpu.processor.request() as req:
            yield req
            process.start_time = self.env.now
            # Calculate how long the process was in the ready queue
            process.ready_time += self.env.now - process.added_to_ready_queue
            yield self.env.timeout(process.duration)
            process.end_time = self.env.now
            print(f"Process {process.pid} finished at {self.env.now}")
            self.schedule()


# Shortest Job First with Preemption (SJF-P) Scheduler
class SJFPreemptiveScheduler(Scheduler):
    def __init__(self, env, cpu):
        super().__init__(env, cpu)
        self.current_processes = [None] * NUM_PROCESSORS  # Track current process on each CPU

    def schedule(self):
        if self.ready_queue:
            # Sort by shortest duration first
            self.ready_queue.sort(key=lambda p: p.duration)
            for i in range(NUM_PROCESSORS):
                if self.current_processes[i] is None:
                    process = self.ready_queue.pop(0)
                    self.current_processes[i] = process
                    self.env.process(self.execute_process(process, i))
                    return

                # Preemption logic
                next_process = self.ready_queue[0]
                current_process = self.current_processes[i]
                if next_process.duration < current_process.duration:
                    self.current_processes[i] = next_process
                    self.ready_queue.append(current_process)
                    self.env.process(self.execute_process(next_process, i))
                    return

    def execute_process(self, process, cpu_id):
        with self.cpu.processor.request() as req:
            try:
                yield req
                process.start_time = self.env.now
                # Calculate how long the process was in the ready queue
                process.ready_time += self.env.now - process.added_to_ready_queue
                yield self.env.timeout(process.duration)
                process.end_time = self.env.now
                print(f"Process {process.pid} finished at {self.env.now}")
                self.current_processes[cpu_id] = None
                self.schedule()
            except simpy.Interrupt as interrupt:
                self.ready_queue.append(process)
                self.current_processes[cpu_id] = None
                self.schedule()


# Round Robin (RR) Scheduler
class RRScheduler(Scheduler):
    def schedule(self):
        if self.ready_queue and self.cpu.processor.count < NUM_PROCESSORS:
            process = self.ready_queue.pop(0)
            self.env.process(self.execute_process(process))

    def execute_process(self, process):
        with self.cpu.processor.request() as req:
            yield req
            process.start_time = self.env.now
            # Calculate how long the process was in the ready queue
            process.ready_time += self.env.now - process.added_to_ready_queue
            execution_time = min(QUANTUM, process.duration)
            yield self.env.timeout(execution_time)
            process.duration -= execution_time

            if process.duration > 0:
                # Process not finished, re-enter ready queue
                process.added_to_ready_queue = self.env.now  # Update when it goes back to the queue
                self.ready_queue.append(process)
            else:
                process.end_time = self.env.now
                print(f"Process {process.pid} finished at {self.env.now}")
            self.schedule()



# List to store completed processes
completed_processes = []


# Process Generator
def process_generator(env, scheduler, arrival_rate):
    pid = 0
    while True:
        duration = max(0, np.random.normal(MEAN_DURATION, STD_DURATION))  # Process execution time
        process = Process(env, pid, duration)
        scheduler.add_process(process)
        completed_processes.append(process)  # Track completed processes
        pid += 1
        yield env.timeout(random.expovariate(1 / arrival_rate))


# Simulation Setup
def simulate(scheduler_class, arrival_rate=ARRIVAL_RATE, sim_time=SIM_TIME):
    global completed_processes
    completed_processes = []  # Reset for each simulation
    env = simpy.Environment()
    cpu = CPU(env)
    scheduler = scheduler_class(env, cpu)
    env.process(process_generator(env, scheduler, arrival_rate))
    env.run(until=sim_time)

    # Calculate average ready time
    total_ready_time = sum(p.ready_time for p in completed_processes if p.end_time)
    average_ready_time = total_ready_time / len(completed_processes)
    print(f"Average Ready Time: {average_ready_time:.2f} units")


# Run the simulations with different schedulers
print("First Come, First Served (FCFS) Simulation:")
simulate(FCFSScheduler)

print("\nShortest Job First (SJF) Simulation:")
simulate(SJFScheduler)

print("\nShortest Job First with Preemption (SJF-P) Simulation:")
simulate(SJFPreemptiveScheduler)

print("\nRound Robin (RR) Simulation:")
simulate(RRScheduler)
