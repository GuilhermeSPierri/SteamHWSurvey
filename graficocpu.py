import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Carregar os dados do CSV
df = pd.read_csv('database.csv')

# Filtrar apenas os dados de "Physical CPUs" e fazer uma cópia explícita
cpus_df = df[df.iloc[:, 1] == 'Physical CPUs'].copy()

# Extrair as colunas relevantes
cpus_data = cpus_df.iloc[:, [0, 2, 4]]  # Data, Tipo de CPU, Percentual
cpus_data.columns = ['Date', 'CPU_Type', 'Percentage']

# Converter a coluna de data para datetime
cpus_data['Date'] = pd.to_datetime(cpus_data['Date'])

# Obter o último valor disponível para cada tipo de CPU (em vez da média)
last_cpus = cpus_data.sort_values('Date').groupby('CPU_Type').last().reset_index()

# Ordenar as CPUs pelo número (convertendo strings para números)
def cpu_sort_key(col):
    try:
        return int(col.split()[0])
    except:
        return float('inf')  # Coloca valores não numéricos no final

last_cpus['Sort_Key'] = last_cpus['CPU_Type'].apply(cpu_sort_key)
last_cpus = last_cpus.sort_values('Sort_Key')

# Filtrar apenas CPUs com percentual > 0
last_cpus = last_cpus[last_cpus['Percentage'] > 0]

# Plotar o gráfico de barras
plt.figure(figsize=(14, 8))

bars = plt.bar(last_cpus['CPU_Type'], last_cpus['Percentage'], 
               color='skyblue', edgecolor='black')

# Adicionar valores nas barras
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:.2%}',
             ha='center', va='bottom')

plt.title('Distribuição de núcleos por CPU (Abril 2025)', fontsize=16)
plt.xlabel('Tipo de CPU', fontsize=12)
plt.ylabel('Percentual de Usuários', fontsize=12)

# Formatando o eixo Y para mostrar porcentagens
plt.gca().yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1.0))

# Rotacionar labels do eixo X para melhor visualização
plt.xticks(rotation=45, ha='right')

plt.grid(True, axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

plt.show()