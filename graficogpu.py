import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Carregar os dados
df = pd.read_csv('database.csv')

# Filtrar apenas dados de GPU e pegar o último mês (Abril 2025)
gpu_data = df[df.iloc[:, 1] == 'Video Card Description'].copy()
gpu_data = gpu_data.iloc[:, [0, 2, 4]]  # Data, Modelo, Percentual
gpu_data.columns = ['Date', 'GPU', 'Percentage']
gpu_data['Date'] = pd.to_datetime(gpu_data['Date'])
last_month = gpu_data['Date'].max()
gpu_last = gpu_data[gpu_data['Date'] == last_month]

# Selecionar as top 10 GPUs
top_gpus = gpu_last.sort_values('Percentage', ascending=False).head(10)

# Configurações do gráfico
plt.figure(figsize=(12, 7))
colors = plt.cm.tab20.colors  # Paleta de cores mais acessível

# Gráfico de barras horizontais (mais legível para muitos textos)
bars = plt.barh(top_gpus['GPU'], top_gpus['Percentage'], 
                color=colors, edgecolor='black')

# Adicionar valores e porcentagens
for bar in bars:
    width = bar.get_width()
    plt.text(width + 0.005, bar.get_y() + bar.get_height()/2,
             f'{width:.2%}',
             va='center', ha='left', fontsize=10)

# Estilização
plt.title('Top 10 GPUs Mais Utilizadas (Abril 2025)', fontsize=16, pad=20)
plt.xlabel('Percentual de Usuários', fontsize=12)
plt.ylabel('Modelo de GPU', fontsize=12)
plt.gca().xaxis.set_major_formatter(ticker.PercentFormatter(xmax=1.0))
plt.grid(axis='x', linestyle='--', alpha=0.6)
plt.gca().invert_yaxis()  # Ordenar do maior para o menor

# Ajustar margens e layout
plt.tight_layout()
plt.show()