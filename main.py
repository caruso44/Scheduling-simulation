import json
from tqdm import tqdm

import matplotlib.pyplot as plt

from Simulation import Simulation


def load_config(filename: str) -> dict:
    """Carrega as variáveis de configuração de um arquivo JSON."""
    with open(filename, 'r') as file:
        return json.load(file)


def run_simulations_and_plot(num_simulations: int, config: dict) -> None:
    idle_times = []

    # Executa a simulação o número de vezes especificado
    with tqdm(total=(num_simulations)) as pbar:
        for i in range(num_simulations):
            sim = Simulation(
                config["num_processors"],
                config["scheduling_algorithm"],
                config["arrival_rate"],
                config["alfa"],
                config["beta"]
            )
            sim.simulate(config["total_simulation_time"])
            idle_times.append(sim.get_average_idle_time())
            pbar.update(1)

    plt.figure(figsize=(10, 6))
    plt.hist(idle_times, bins=20, color='skyblue', edgecolor='black')  # 'bins' define o número de intervalos no histograma
    plt.xlabel("Tempo Ocioso Médio")
    plt.ylabel("Frequência")
    plt.title(f"Frequência dos Tempos Ociosos Médios ({num_simulations} simulações)")
    plt.show()

if __name__ == '__main__':
    # Carregar configurações do arquivo JSON
    config = load_config('config.json')

    # Definir o número de simulações
    num_simulations = 1000

    # Rodar as simulações e gerar o gráfico
    run_simulations_and_plot(num_simulations, config)
