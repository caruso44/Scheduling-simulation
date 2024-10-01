import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Função para calcular estatísticas e plotar os dados
def analyze_algorithms(csv_file):
    # Lendo o CSV
    data = pd.read_csv(csv_file)

    # Lista para armazenar os resultados
    results = {}

    # Iterando sobre cada coluna (exceto a primeira)
    for column in data.columns[1:]:
        times = data[column]
        
        # Calculando média, desvio padrão e intervalo de confiança
        mean = np.mean(times)
        std_dev = np.std(times)
        conf_interval = stats.t.interval(0.95, len(times)-1, loc=mean, scale=std_dev/np.sqrt(len(times)))

        # Armazenando os resultados
        results[column] = {
            'Mean': mean,
            'Standard Deviation': std_dev,
            '95% Confidence Interval': conf_interval
        }

        # Plotando os dados
        plt.figure(figsize=(10, 6))
        plt.hist(times, bins=10, alpha=0.7, label=column)
        plt.axvline(mean, color='red', linestyle='dashed', linewidth=2, label='Mean')
        plt.axvline(conf_interval[0], color='green', linestyle='dashed', linewidth=2, label='95% CI Lower')
        plt.axvline(conf_interval[1], color='green', linestyle='dashed', linewidth=2, label='95% CI Upper')
        plt.title(f'Histogram of {column}')
        plt.xlabel('Time')
        plt.ylabel('Frequency')
        plt.legend()
        plt.grid()
        
        # Salvando a imagem
        plt.savefig(f'histogram_{column}_high_4.png')  # Salva a imagem como PNG
        plt.close()  # Fecha a figura para liberar memória

    return results

# Chame a função com o nome do seu arquivo CSV
results = analyze_algorithms('average_ready_times_4_high.csv')

# Exibindo os resultados
for algorithm, stats in results.items():
    print(f"{algorithm}:")
    print(f"  Mean: {stats['Mean']:.2f}")
    print(f"  Standard Deviation: {stats['Standard Deviation']:.2f}")
    print(f"  95% Confidence Interval: {stats['95% Confidence Interval']}\n")
