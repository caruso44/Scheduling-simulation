import json
from tqdm import tqdm
import statistics

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

from Simulation import Simulation


def load_config(filename: str) -> dict:
    """Carrega as variáveis de configuração de um arquivo JSON."""
    with open(filename, 'r') as file:
        return json.load(file)

def calcular_intervalo_confianca(media: float, desvio_padrao: float, tamanho_amostra: int, confianca: float = 0.95) -> tuple:
    # Calcular o erro padrão
    erro_padrao = desvio_padrao / np.sqrt(tamanho_amostra)
    
    # Obter o valor Z para o nível de confiança desejado
    z = stats.norm.ppf((1 + confianca) / 2)
    
    # Calcular o intervalo de confiança
    limite_inferior = media - z * erro_padrao
    limite_superior = media + z * erro_padrao
    
    return limite_inferior, limite_superior

def run_simulations_and_plot(num_simulations: int, config: dict) -> None:
    idle_times = []
    quantum = config.get('quantum', None)  # Quantum para Round Robin
    # Executa a simulação o número de vezes especificado
    with tqdm(total=(num_simulations)) as pbar:
        for i in range(num_simulations):
            sim = Simulation(
                config["num_processors"],
                config["scheduling_algorithm"],
                config["arrival_rate"],
                quantum
            )
            sim.simulate(config["total_simulation_time"])
            idle_times.append(sim.get_average_idle_time())
            pbar.update(1)
    print(statistics.mean(idle_times))
    print(statistics.stdev(idle_times))
    intervalo_confianca = calcular_intervalo_confianca(statistics.mean(idle_times), statistics.stdev(idle_times), num_simulations)
    print(intervalo_confianca)
    plt.figure(figsize=(10, 6))
    plt.hist(idle_times, bins=20, color='skyblue', edgecolor='black')  # 'bins' define o número de intervalos no histograma
    plt.xlabel("Tempo Ocioso Médio")
    plt.ylabel("Frequência")
    plt.title("Frequência dos Tempos Ociosos Médios (1000 simulações)")

    # Salvar a imagem
    plt.savefig(f"idle_times_"+ config["scheduling_algorithm"] + ".png")  # Salva a imagem como "idle_times_histogram.png" no diretório atual

    plt.show()  # Mostra o gráfico na tela (opcional)

if __name__ == '__main__':
    # Carregar configurações do arquivo JSON
    config = load_config('config.json')

    # Definir o número de simulações
    num_simulations = 5000

    # Rodar as simulações e gerar o gráfico
    run_simulations_and_plot(num_simulations, config)
